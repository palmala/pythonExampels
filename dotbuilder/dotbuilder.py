import pydot
from collections import defaultdict
from commit_provider import CommitProvider


def dot_builder(nodes):
    if not nodes:
        raise AttributeError("Nodes can't be empty!")
    graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")

    for source in nodes:
        for target in nodes[source]:
            graph.add_node(pydot.Node(source, label=source))
            graph.add_node(pydot.Node(target, label=target))
            edge = pydot.Edge(source, target)
            graph.add_edge(edge)

    return graph


def calculate_instability(mygraph):
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
    return instability


def calculate_violations(mygraph, instability=None):
    if not instability:
        instability = calculate_instability(mygraph)
    violations = []
    for edge in mygraph.get_edge_list():
        source = edge.get_source()
        destination = edge.get_destination()
        if instability[source] < instability[destination]:
            edge.set('color', 'red')
            violations.append(f"{source}->{destination}")
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
                node.set('style', 'filled')
                node.set('fillcolor', 'red')
            elif instability[node_name] < 1.0:
                node.set('style', 'filled')
                node.set('fillcolor', 'orange')
            else:
                node.set('style', 'filled')
                node.set('fillcolor', 'green')


def _check_instability(instability, mygraph):
    if not instability:
        instability = calculate_instability(mygraph)
    return instability


def color_changed_nodes(*, mygraph, commits=None, commit_provider=None):
    commits = _check_commits(commit_provider, commits)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if commits[node_name] > 0:
            node.set('style', 'filled')
            node.set('fillcolor', 'orange')


def _check_commits(commit_provider, commits):
    if not commits:
        if not commit_provider:
            raise AttributeError("Need commits or CommitProvider!")
        commits = update_with_commits(commit_provider)
    return commits


def reset_colors(*, mygraph):
    for edge in mygraph.get_edge_list():
        edge.set('color', 'black')

    for node in mygraph.get_node_list():
        node.set('style', 'filled')
        node.set('fillcolor', 'white')


# def color_critical_paths(*, mygraph, commits=None, commit_provider=None):
#     _check_commits(commits=commits, commit_provider=commit_provider)
#     edges = set(mygraph.get_edge_list())
#     edges_by_source = defaultdict(list)
#
#     for edge in edges:
#         edges_by_source[edge.get_source()].append(edge)
#
#     colored_prev = set()
#     colored = set()
#
#     while colored != colored_prev:
#         colored_prev = colored.copy()

def get_all_dependants(*, mygraph: pydot.Dot, node_name: str):
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

        return dot_builder(result)
    else:
        raise AttributeError(f"No node found with name {node_name}!")
