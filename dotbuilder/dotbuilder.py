import pydot
from collections import defaultdict
from commit_provider import CommitProvider

import logging

logger = logging.getLogger(__name__)


def dot_builder(nodes, name):
    if not nodes:
        raise AttributeError("Nodes can't be empty!")
    graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")
    graph.set_name(name)

    for source in nodes:
        for target in nodes[source]:
            graph.add_node(pydot.Node(source, label=source))
            graph.add_node(pydot.Node(target, label=target))
            edge = pydot.Edge(source, target)
            graph.add_edge(edge)

    return graph


def calculate_instability(mygraph: pydot.Dot):
    logger.info(f"[{mygraph.get_name()}] Instability calculations start")
    instability = {}
    in_edges = defaultdict(int)
    out_edges = defaultdict(int)

    for edge in mygraph.get_edge_list():
        in_edges[edge.get_source()] += 1
        out_edges[edge.get_destination()] += 1

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if in_edges[node_name] + out_edges[node_name] == 0:
            instability[node_name] = 0
        else:
            instability[node_name] = round(float(in_edges[node_name]) / float(
                in_edges[node_name] + out_edges[node_name]), 3)
        node.set("label", f"{node.get('label')}\nI: {instability[node_name]}".replace("\"", ""))

    logger.debug(f"[{mygraph.get_name()}] Instability calculations end")
    return instability


def calculate_violations(mygraph: pydot.Dot, instability=None):
    instability = _check_instability(instability, mygraph)

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


def update_with_commits(mygraph, commit_provider):
    if not isinstance(commit_provider, CommitProvider):
        raise AttributeError("commit_provider is not an instance of CommitProvider!")

    commits = {}
    for node in mygraph.get_node_list():
        node_name = node.get_name()
        commits[node_name] = commit_provider.get_number_of_commits(node.get_name())
        node.set('label', f"{node.get('label')}\nC: {commits[node_name]}".replace("\"", ""))
    return commits


def color_changed_nodes_per_instability(*, mygraph, instability=None, commits=None, commit_provider=None):
    instability = _check_instability(instability, mygraph)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if commits[node_name] > 0:
            if instability[node_name] <= 0.5:
                fill_node(node, 'red')
            elif instability[node_name] < 1.0:
                fill_node(node, 'orange')
            else:
                fill_node(node, 'green')


def _check_instability(instability, mygraph: pydot.Dot):
    if not instability:
        logger.debug(f"[{mygraph.get_name()}] No instability values provided.")
        instability = calculate_instability(mygraph)
    return instability


def color_changed_nodes(*, mygraph, commits=None, commit_provider=None):
    commits = _check_commits(commit_provider, commits)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if commits[node_name] > 0:
            fill_node(node, 'orange')


def _check_commits(commit_provider, commits):
    if not commits:
        if not commit_provider:
            raise AttributeError("Need commits or CommitProvider!")
        commits = update_with_commits(commit_provider)
    return commits


def reset_colors(*, mygraph: pydot.Dot):
    logger.info(f"[{mygraph.get_name()}] Resetting colors.")
    for edge in mygraph.get_edge_list():
        edge.set('color', 'black')

    for node in mygraph.get_node_list():
        fill_node(node=node, color="white")


def fill_node(node: pydot.Node, color="white"):
    node.set('style', 'filled')
    node.set('fillcolor', color)


def get_all_dependants(*, mygraph: pydot.Dot, node_name: str):
    logger.info(f"[{mygraph.get_name()}] Getting all dependants sub-graph for node: {node_name}")
    candidates = [node for node in mygraph.get_node_list() if node.get_name().strip() == node_name]
    if candidates:
        edges_to_node = defaultdict(list)
        for edge in mygraph.get_edge_list():
            edges_to_node[edge.get_destination()].append(edge.get_source())
        to_process = [node_name]
        all_dependants_nodes = set(to_process)

        while to_process:
            current = to_process.pop()
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


def classify_nodes_per_instability(graph: pydot.Dot, instability: list):
    logger.info(f"[{graph.get_name()}] Classifying nodes per instability.")
    _check_instability(instability=instability, mygraph=graph)
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
                classified[c[2]].append(node_name)
                visited.append(node_name)
                break
    for c in classification:
        logger.info(f"[{graph.get_name()}] Number of {c[3]} class nodes: {len(classified[c[3]])}")
    return classified
