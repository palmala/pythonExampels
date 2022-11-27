import graphs
import unittest
import pydot

WRITE_FILES = True


def build_dot(graph: dict):
    dot = pydot.Dot()
    for source in graph:
        for target in graph[source]:
            edge = pydot.Edge(source, target)
            dot.add_edge(edge)
    return dot


def color_edges(graph: pydot.Dot, edges: dict, labels: dict = None):
    for edge in graph.get_edges():
        source = edge.get_source()
        target = edge.get_destination()
        if source in edges and target in edges[source]:
            edge.set('color', 'red')
            edge.set('style', 'dashed')
            if labels and source in labels:
                edge.set('label', labels[source])


def write_dots(subject: pydot.Dot, name: str):
    if WRITE_FILES:
        subject.write(f"{name}.svg", format="svg")


class GraphTests(unittest.TestCase):

    def test_basic(self):
        graph = {
            1: [2, 3],
            2: [3],
            3: []
        }

        dot = build_dot(graph)
        write_dots(dot, "test1")

        tree, parent, distances = graphs.bfs(graph, 1)
        dot2 = build_dot(tree)
        write_dots(dot2, "test2")

    def test_generate(self):
        graph = graphs.generate_graph(15, 30)
        dot = build_dot(graph)
        write_dots(dot, "generate1")

        tree, parent, distances = graphs.bfs(graph, 0)
        dot2 = build_dot(tree)
        write_dots(dot2, "generate2")

        color_edges(dot, tree, distances)
        write_dots(dot, "generate3")


if __name__ == "__main__":
    unittest.main()
