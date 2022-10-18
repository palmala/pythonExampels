import pydot
from collections import defaultdict


class DotBuilder:

    def __init__(self, nodes):
        if not nodes:
            raise AttributeError("Nodes can't be empty!")
        self._graph = pydot.Dot("my_graph", graph_type="digraph", bgcolor="white")
        self._instability = {}
        self._fill_from_dict(nodes)
        self._violations = []

    def _fill_from_dict(self, nodes):
        self._fill_nodes(nodes)
        self._fill_edges(nodes)

    def _fill_edges(self, nodes):
        for source in nodes:
            for target in nodes[source]:
                edge = pydot.Edge(source, target)
                self._graph.add_edge(edge)

    def _fill_nodes(self, nodes):
        for source in nodes:
            node = pydot.Node(source, label=source)
            self._graph.add_node(node)

    def calculate_instability(self):
        self._instability = {}
        in_edges = defaultdict(int)
        out_edges = defaultdict(int)
        for edge in self._graph.get_edge_list():
            in_edges[edge.get_source()] += 1
            out_edges[edge.get_destination()] += 1

        for node in self._graph.get_node_list():
            node_name = node.get_name()
            if in_edges[node_name] + out_edges[node_name] == 0:
                self._instability[node_name] = 0
            else:
                self._instability[node_name] = float(in_edges[node_name]) / float(
                    in_edges[node_name] + out_edges[node_name])
            node.set("label", f"{node_name}\n{self._instability[node_name]}".replace("\"", ""))

    def get_instability(self):
        return self._instability

    def calculate_violations(self):
        self._violations = []
        for edge in self._graph.get_edge_list():
            source = edge.get_source()
            destination = edge.get_destination()
            if self._instability[source] < self._instability[destination]:
                edge.set('color', 'red')
                self._violations.append(f"{source}->{destination}")
        return self._violations

    def get_violations(self):
        return self._violations

    def get_edges(self):
        return self._graph.get_edge_list()

    def get_stats(self):
        stats = ""
        stats += f"Number of edges: {len(self.get_edges())}\n"
        stats += f"Number of violations: {len(self._violations)}\n"
        stats += f"Violation ratio: {str(float(len(self._violations)) / float(len(self.get_edges())))}\n"
        stats += f"Violations: {self._violations}\n"
        return stats

    def __str__(self):
        return self._graph.to_string()
