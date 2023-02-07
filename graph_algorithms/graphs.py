from collections import defaultdict


def reverse_edges(graph: dict[str: list]):
    result = defaultdict(list)
    for node in graph:
        if node not in result:
            result[node] = []
        for child in graph[node]:
            result[child].append(node)

    return result


def extract_edge_numbers(graph: dict[str: list]):
    in_edges = defaultdict(int)
    out_edges = defaultdict(int)

    for source in graph:
        for target in graph[source]:
            in_edges[target] += 1
            out_edges[source] += 1

    return in_edges, out_edges


def generate_statistics(graph: dict[str: list]):
    statistics = dict()
    statistics["number_of_nodes"] = len(graph)
    statistics["number_of_edges"] = sum([1 for node in graph for edge in graph[node]])

    in_edge_numbers, out_edge_numbers = extract_edge_numbers(graph)
    node_names = graph.keys()
    orphan_nodes = [node for node in node_names if out_edge_numbers[node] == 0 and in_edge_numbers[node] == 0]
    statistics["nodes_without_edges"] = len(orphan_nodes)
    statistics["nodes_with_edges"] = len(node_names) - len(orphan_nodes)

    node_with_reversed_graph_only = [node for node in node_names if
                                     in_edge_numbers[node] and not out_edge_numbers[node]]
    statistics["nodes_with_in_edges_only"] = len(node_with_reversed_graph_only)

    node_with_graph_only = [node for node in node_names if out_edge_numbers[node] and not in_edge_numbers[node]]
    statistics["nodes_with_out_edges_only"] = len(node_with_graph_only)

    num_dependants = list(reversed(sorted(in_edge_numbers.items(), key=lambda item: item[1])))
    statistics["nodes_with_most_in_edges"] = num_dependants[:min(5, len(num_dependants))]

    num_dependencies = list(reversed(sorted(out_edge_numbers.items(), key=lambda item: item[1])))
    statistics["nodes_with_most_out_edges"] = num_dependencies[:min(5, len(num_dependencies))]
    return statistics


def get_leveling(graph: dict[str: list]):
    result = dict()

    for node in graph:
        if not graph[node]:
            result[node] = 0
        else:
            result[node] = -1

    while any([result[x] == -1 for x in result]):
        for node in graph:
            if result[node] > -1:
                continue
            else:
                if all([result[x] > -1 for x in graph[node]]):
                    result[node] = max([result[x] for x in graph[node]]) + 1

    return result


def calculate_instability(graph: dict[str: list]):
    instability = defaultdict(int)

    in_edge_numbers, out_edge_numbers = extract_edge_numbers(graph)

    for node in graph.keys():
        instability[node] = _evaluate_node(node, in_edge_numbers, out_edge_numbers)

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


def calculate_violations(graph: dict[str: list], instability: dict[str: int]):
    violations = set()

    if not instability:
        instability = calculate_instability(graph)

    for source in graph:
        for target in graph[source]:
            if instability[source] < instability[target]:
                violations.add((source, target))

    return violations


def detect_all_cycles(graph: dict[str: list]):
    cycles_raw = [[node] + path[:-1] for node in graph for path in _generate_paths(graph, node, node)]
    cycles = set()
    for c in cycles_raw:
        while c[0] != min(c):
            c.append(c.pop(0))
        c.append(c[0])
        cycles.add(tuple(c))
    return cycles


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


def get_all_dependants(graph: dict[str: list], node: str):
    edges_to_node = defaultdict(list)

    for source in graph:
        if source not in edges_to_node:
            edges_to_node[source] = list()
        for target in graph[source]:
            edges_to_node[target].append(source)

    to_process = [node]
    all_dependants_nodes = set(to_process)
    visited = set()

    while to_process:
        current = to_process.pop()
        if current in visited:
            continue
        visited.add(current)

        dependants = [dep for dep in edges_to_node[current]]
        for dependant in dependants:
            all_dependants_nodes.add(dependant)
            to_process.append(dependant)

    result = _restrict_graph_to_nodes(graph, all_dependants_nodes)

    return result


def _restrict_graph_to_nodes(graph: dict[str: list], nodes: set):
    result = defaultdict(list)
    for source in graph:
        for target in graph[source]:
            if source in nodes and target in nodes:
                if source not in result:
                    result[source] = list()
                if target not in result:
                    result[target] = list()
                result[source].append(target)

    return result
