import unittest
from graphs import *
from graphs import extract_edge_numbers

EXAMPLE = {
    'A': ['B', 'D'],
    'B': ['A'],
    'C': ['A'],
    'D': ['B', 'E'],
    'E': []
}


class TestGraphs(unittest.TestCase):

    def test_statistics(self):
        stats = generate_statistics(EXAMPLE)
        self.assertEqual(stats["number_of_nodes"], 5)
        self.assertEqual(stats["number_of_edges"], 6)
        self.assertEqual(stats["nodes_without_edges"], 0)
        self.assertEqual(stats["nodes_with_in_edges_only"], 1)
        self.assertEqual(stats["nodes_with_out_edges_only"], 1)
        self.assertEqual(stats["nodes_with_most_in_edges"][0][1], 2)

    def test_reverse_edges(self):
        subject = reverse_edges(EXAMPLE)
        self.assertSetEqual(set(subject['A']), {'C', 'B'})

    def test_extract_edge_numbers(self):
        in_edges, out_edges = extract_edge_numbers(EXAMPLE)
        self.assertEqual(in_edges['A'], 2)
        self.assertEqual(out_edges['D'], 2)

    def test_instability(self):
        subject = calculate_instability(EXAMPLE)
        self.assertEqual(subject['E'], 0)
        self.assertEqual(subject['C'], 1)
        self.assertEqual(subject['A'], 0.5)

    def test_violations(self):
        instability = calculate_instability(EXAMPLE)
        subject = calculate_violations(EXAMPLE, instability)
        self.assertSetEqual(subject, {('A', 'D'), ('B', 'A')})

    def test_detect_cycles(self):
        cycles = detect_all_cycles(EXAMPLE)
        self.assertEqual(len(cycles), 2)
        self.assertTrue(('A', 'B', 'A') in cycles)
        self.assertTrue(('A', 'D', 'B', 'A') in cycles)

    def test_get_all_dependants(self):
        subject = get_all_dependants(EXAMPLE, 'E')
        expected = {'A', 'B', 'C', 'D', 'E'}
        self.assertSetEqual(set(subject.keys()), expected)

        subject = get_all_dependants(EXAMPLE, 'D')
        expected = {'A', 'B', 'C', 'D'}
        self.assertSetEqual(set(subject.keys()), expected)
