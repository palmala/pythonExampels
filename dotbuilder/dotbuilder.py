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
    if not instability:
        instability = calculate_instability(mygraph)
    if not commits:
        if not commit_provider:
            raise AttributeError("Need commits or CommitProvider!")
        commits = update_with_commits(commit_provider)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if commits[node_name] > 0:
            if instability[node_name] <= 0.5:
                node.set('color', 'red')
            elif instability[node_name] < 1.0:
                node.set('color', 'orange')
            else:
                node.set('color', 'green')


def color_changed_nodes(*, mygraph, commits=None, commit_provider=None):
    if not commits:
        if not commit_provider:
            raise AttributeError("Need commits or CommitProvider!")
        commits = update_with_commits(commit_provider)

    for node in mygraph.get_node_list():
        node_name = node.get_name()
        if commits[node_name] > 0:
            node.set('color', 'yellow')
