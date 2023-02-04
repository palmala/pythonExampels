import networkx as nx

EXAMPLE = {
    'A': ['B', 'D'],
    'B': ['A'],
    'C': ['A'],
    'D': ['B', 'E'],
    'E': []
}


def dict_to_nx(graph: dict[str: list]):
    nx_graph = nx.DiGraph(graph)
    nx_graph.nodes(data=True)
    return nx_graph


def update_nx_with_instability(nx_graph: nx.DiGraph, instability: dict[str: int], in_edges: dict[int]):
    for node, data in nx_graph.nodes(data=True):
        data['fontsize'] = 10
        data['label'] = f"{node} {instability[node]}"
        data['instability'] = instability[node]
        data['size'] = data['fontsize'] * len(data['label']) + 5 * in_edges[node]


def update_nx_with_violations(nx_graph, violations):
    for s, t, data in nx_graph.edges(data=True):
        for violation in violations:
            if s == violation[0] and t == violation[1]:
                data['classes'] = 'violation'


def update_nx_with_cycles(nx_graph, cycles):
    for s, t, data in nx_graph.edges(data=True):
        for cycle in cycles:
            for i in range(len(cycle) - 1):
                if s == cycle[i] and t == cycle[i + 1]:
                    data['classes'] = 'cycle'


def get_nodes_details(nx_graph: nx.DiGraph):
    for node, data in nx_graph.nodes(data=True):
        print(f"node: {node}, data: {data}")


def get_edges_details(nx_graph: nx.DiGraph):
    for s, t, data in nx_graph.edges(data=True):
        print(f"edge source: {s}, target: {t}, data: {data}")


def main():
    graph = EXAMPLE
    subject = dict_to_nx(graph)

    import graphs

    instability = graphs.calculate_instability(graph)
    update_nx_with_instability(subject, instability)
    get_nodes_details(subject)
    # nx.draw(subject, with_labels=True)
    # plt.show()


if __name__ == "__main__":
    main()
