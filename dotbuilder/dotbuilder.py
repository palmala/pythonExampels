from pydot import Dot, Node, Edge
from collections import defaultdict

import logging

logger = logging.getLogger(__name__)


def dot_builder(nodes: dict, name: str, ranksep: int = "2"):
    if not nodes:
        raise AttributeError("Nodes can't be empty!")

    added = set()

    graph = Dot("my_graph", graph_type="digraph", bgcolor="white")
    graph.set_name(name)
    graph.set('ranksep', ranksep)
    _fill_graph_from_dict(graph, nodes, added)
    generate_statistics(graph)

    return graph


def generate_statistics(graph: Dot):
    logging.info(f"[Graph:{graph.get_name()}] Number of projects: {len(graph.get_node_list())}")
    logging.info(f"[Graph:{graph.get_name()}] Number of dependencies: {len(graph.get_edge_list())}")

    in_edges, out_edges = _extract_edges(graph)
    node_names = [node.get_name() for node in graph.get_node_list()]
    orphan_nodes = [node for node in node_names if in_edges[node] == 0 and out_edges[node] == 0]
    logging.info(
        f"[Graph:{graph.get_name()}] Projects with no visible dependencies: {len(orphan_nodes)}")
    logging.info(
        f"[Graph:{graph.get_name()}] Projects with dependency connection: {len(node_names) - len(orphan_nodes)}")

    node_with_in_edges_only = [node for node in node_names if in_edges[node] and not out_edges[node]]
    logging.info(f"[Graph:{graph.get_name()}] Projects with dependants only: {len(node_with_in_edges_only)}")

    node_with_out_edges_only = [node for node in node_names if out_edges[node] and not in_edges[node]]
    logging.info(f"[Graph:{graph.get_name()}] Projects with dependencies only: {len(node_with_out_edges_only)}")

    num_dependants = list(reversed(sorted(in_edges.items(), key=lambda item: item[1])))
    logging.info(
        f"[Graph:{graph.get_name()}] Projects with most direct dependants: {num_dependants[:min(5, len(num_dependants))]}")

    num_dependencies = list(reversed(sorted(out_edges.items(), key=lambda item: item[1])))
    logging.info(
        f"[Graph:{graph.get_name()}] Projects with most direct dependencies: {num_dependencies[:min(5, len(num_dependencies))]}")


def _fill_graph_from_dict(graph, nodes, added):
    for source in nodes:
        _add_node_to_graph(graph, added, source)
        for target in nodes[source]:
            _add_node_to_graph(graph, added, target)
            edge = Edge(source, target)
            graph.add_edge(edge)


def _add_node_to_graph(graph, added, source):
    if source not in added:
        graph.add_node(Node(source, label=source))
        added.add(source)


def calculate_instability(mygraph: Dot):
    logger.debug(f"[Graph:{mygraph.get_name()}] Instability calculations start")
    instability = {}

    in_edges, out_edges = _extract_edges(mygraph)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        instability[node_name] = _evaluate_node(node_name, in_edges, out_edges)
        node.set("label", f"{node.get('label')}\nI: {instability[node_name]}".replace("\"", ""))

    logger.debug(f"[Graph:{mygraph.get_name()}] Instability calculations end")
    average_i = float(sum(list(instability.values()))) / len(mygraph.get_edges())
    logger.info(f"[Graph:{mygraph.get_name()}]: average instability {average_i}")
    logger.info(
        f"[Graph:{mygraph.get_name()}]: average instability times edges {str(sum(list(instability.values())) * len(mygraph.get_edges()))}")
    return instability


def _evaluate_node(node_name, in_edges, out_edges):
    if in_edges[node_name] + out_edges[node_name] == 0:
        instability = 1
    else:
        instability = round(
            float(out_edges[node_name]) /
            float(in_edges[node_name] + out_edges[node_name])
            , 3)
    return instability


def _extract_edges(mygraph):
    in_edges = defaultdict(int)
    out_edges = defaultdict(int)

    for edge in mygraph.get_edge_list():
        in_edges[edge.get_destination()] += 1
        out_edges[edge.get_source()] += 1

    return in_edges, out_edges


def calculate_violations(mygraph: Dot, instability: dict):
    logger.debug(f"[Graph:{mygraph.get_name()}]: SDP violations calculations start.")
    violations = []

    for edge in mygraph.get_edge_list():
        source = edge.get_source()
        destination = edge.get_destination()

        if instability[source] < instability[destination]:
            edge.set('color', 'red')
            violations.append(f"{source}->{destination}")

    logger.info(f"[Graph:{mygraph.get_name()}]: {len(violations)} SDP violation(s) found.")
    for violation in violations:
        logger.info(f"[Graph:{mygraph.get_name()}]: SDP violation found: {violation}")
    return violations


def fill_node(node: Node, color="white"):
    node.set('style', 'filled')
    node.set('fillcolor', color)


def get_all_dependants(*, mygraph: Dot, node_name: str):
    logger.info(f"[Graph:{mygraph.get_name()}] Getting all dependants sub-graph for node: {node_name}")

    candidates = [node for node in mygraph.get_node_list() if node.get_name().strip() == node_name]
    if candidates:
        edges_to_node = defaultdict(list)

        edges_to_node = _get_edges_to_node(mygraph)

        to_process = [node_name]
        all_dependants_nodes = set(to_process)
        visited = set()

        while to_process:
            current = to_process.pop()
            if current in visited:
                continue
            visited.add(current)

            dependants = [desc for desc in edges_to_node[current]]
            for dependant in dependants:
                all_dependants_nodes.add(dependant)
                to_process.append(dependant)

        result = _restrict_graph_to_nodes(all_dependants_nodes, mygraph)

        logger.info(
            f"[Graph:{mygraph.get_name()}] generating dependants of {node_name} sub-graph")
        return dot_builder(nodes=result, name=f"{node_name}_dependants")
    else:
        raise AttributeError(f"No node found with name {node_name}!")


def _restrict_graph_to_nodes(all_dependants_nodes, mygraph: Dot):
    result = defaultdict(list)
    for edge in mygraph.get_edge_list():
        source = edge.get_source()
        target = edge.get_destination()
        if source in all_dependants_nodes and target in all_dependants_nodes:
            result[source].append(target)
    return result


def _get_edges_to_node(mygraph: Dot):
    edges_to_node = defaultdict(list)
    for edge in mygraph.get_edge_list():
        edges_to_node[edge.get_destination()].append(edge.get_source())
    return edges_to_node


def _generate_paths(graph, start, end):
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


def detect_all_cycles(graph: Dot):
    logger.debug(f"[Graph:{graph.get_name()}] Converting graph to dict")

    graph_dict = _convert_dot_to_dict(graph)

    logger.info(f"[Graph:{graph.get_name()}] Detecting cycles")
    cycles_raw = [[node] + path[:-1] for node in graph_dict for path in _generate_paths(graph_dict, node, node)]
    cycles = set()
    for c in cycles_raw:
        while c[0] != min(c):
            c.append(c.pop(0))
        c.append(c[0])
        cycles.add(tuple(c))
    logger.info(f"[Graph:{graph.get_name()}] Number of cycles detected: {len(cycles)}.")
    if cycles:
        for cycle in cycles:
            logger.info(f"[Graph:{graph.get_name()}] Cycle: {cycle}.")
    return cycles


def _convert_dot_to_dict(graph):
    graph_dict = dict()
    for node in graph.get_node_list():
        graph_dict[node.get_name()] = list()
    for edge in graph.get_edge_list():
        graph_dict[edge.get_source()].append(edge.get_destination())
    return graph_dict


def classify_nodes_per_instability(graph: Dot, instability: dict):
    logger.info(f"[Graph:{graph.get_name()}] Classifying nodes per instability.")
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
        logger.info(f"[Graph:{graph.get_name()}] Number of {c[3]} class nodes: {len(classified[c[3]])}")
    return classified


def write_to_file(what: Dot, filename: str):
    with open(filename, "w") as outfile:
        outfile.write(str(what))
