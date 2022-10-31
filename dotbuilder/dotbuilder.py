from pydot import Dot, Node, Edge
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)


def dot_builder(nodes, name):
    if not nodes:
        raise AttributeError("Nodes can't be empty!")
    graph = Dot("my_graph", graph_type="digraph", bgcolor="white")
    graph.set_name(name)
    added = set()

    for source in nodes:
        if source not in added:
            graph.add_node(Node(source, label=source))
            added.add(source)
        for target in nodes[source]:
            if target not in added:
                graph.add_node(Node(target, label=target))
                added.add(target)
            edge = Edge(source, target)
            graph.add_edge(edge)

    return graph


def calculate_instability(mygraph: Dot):
    logger.info(f"[{mygraph.get_name()}] Instability calculations start")
    instability = {}
    in_edges = defaultdict(int)
    out_edges = defaultdict(int)

    for edge in mygraph.get_edge_list():
        in_edges[edge.get_destination()] += 1
        out_edges[edge.get_source()] += 1

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if in_edges[node_name] + out_edges[node_name] == 0:
            instability[node_name] = 1
        else:
            instability[node_name] = round(float(out_edges[node_name]) / float(
                in_edges[node_name] + out_edges[node_name]), 3)
        node.set("label", f"{node.get('label')}\nI: {instability[node_name]}".replace("\"", ""))

    logger.debug(f"[{mygraph.get_name()}] Instability calculations end")
    return instability


def calculate_violations(mygraph: Dot, instability: dict):
    logger.info(f"[Graph:{mygraph.get_name()}]: SDP violations calculations start.")
    violations = []
    for edge in mygraph.get_edge_list():
        source = edge.get_source()
        destination = edge.get_destination()
        if instability[source] < instability[destination]:
            edge.set('color', 'red')
            logger.info(f"[Graph:{mygraph.get_name()}]: SDP violation found: {source} -> {destination}.")
            violations.append(f"{source}->{destination}")

    logger.info(f"[Graph:{mygraph.get_name()}]: {len(violations)} SDP violation(s) found.")
    return violations


def fill_node(node: Node, color="white"):
    node.set('style', 'filled')
    node.set('fillcolor', color)


def get_all_dependants(*, mygraph: Dot, node_name: str):
    logger.info(f"[{mygraph.get_name()}] Getting all dependants sub-graph for node: {node_name}")
    candidates = [node for node in mygraph.get_node_list() if node.get_name().strip() == node_name]
    if candidates:
        edges_to_node = defaultdict(list)
        for edge in mygraph.get_edge_list():
            edges_to_node[edge.get_destination()].append(edge.get_source())
        to_process = [node_name]
        all_dependants_nodes = set(to_process)
        visited = set()

        while to_process:
            current = to_process.pop()
            if current in visited:
                continue
            visited.add(current)
            descendants = [desc for desc in edges_to_node[current]]
            for descendant in descendants:
                all_dependants_nodes.add(descendant)
                to_process.append(descendant)

        result = defaultdict(list)
        for edge in mygraph.get_edge_list():
            source = edge.get_source()
            target = edge.get_destination()
            if source in all_dependants_nodes and target in all_dependants_nodes:
                result[source].append(target)

        logger.info(f"[{mygraph.get_name()}] dependants of {node_name} sub-graph generated, size is {len(result)}")
        return dot_builder(nodes=result, name=f"{node_name}_dependant")
    else:
        raise AttributeError(f"No node found with name {node_name}!")


def _detect_cycles(graph, start, end):
    fringe = [(start, [])]
    while fringe:
        node, path = fringe.pop()
        if path and node == end:
            yield path
            continue
        for child in graph[node]:
            if child in path:
                continue
            fringe.append((child, path + [child]))


def detect_all_cycles(graph):
    logger.info(f"Detecting cycles for graph with {len(graph)} nodes.")
    cycles_raw = [[node] + path[:-1] for node in graph for path in _detect_cycles(graph, node, node)]
    cycles = set()
    for c in cycles_raw:
        while c[0] != min(c):
            c.append(c.pop(0))
        c.append(c[0])
        cycles.add(tuple(c))
    logger.info(f"Number of cycles detected: {len(cycles)}.")
    if cycles:
        for cycle in cycles:
            logging.info(f"Cycle: {cycle}.")
    return cycles


def classify_nodes_per_instability(graph: Dot, instability: dict):
    logger.info(f"[{graph.get_name()}] Classifying nodes per instability.")
    classification = [
        (1, 1.1, 'green', 'NONE'),
        (0.75, 1, 'yellow', 'LOW'),
        (0.5, 0.75, 'orange', 'MEDIUM'),
        (0.25, 0.5, 'red', 'HIGH'),
        (0, 0.25, 'purple', 'CRITICAL')
    ]
    classified = defaultdict(list)
    visited = []
    for node in graph.get_node_list():
        node_name = node.get_name()
        for c in classification:
            if c[0] <= instability[node_name] < c[1] and node_name not in visited:
                fill_node(node, c[2])
                classified[c[3]].append(node_name)
                visited.append(node_name)
                break
    for c in classification:
        logger.info(f"[{graph.get_name()}] Number of {c[3]} class nodes: {len(classified[c[3]])}")
    return classified


def write_to_file(what: Dot, filename: str):
    with open(filename, "w") as outfile:
        outfile.write(str(what))
