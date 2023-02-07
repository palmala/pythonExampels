import unittest
from graph import reverse_edges
from graph import get_leveling

GRAPH = {
    'node1': ['node2'],
    'node2': ['node3', 'node5'],
    'node3': ['node4'],
    'node0': ['node3']
}


class TestLeveling(unittest.TestCase):

    def test_basic(self):
        reversed_graph = reverse_edges(GRAPH)
        self.assertEqual(['node3'], reversed_graph['node4'])

        levels = get_leveling(reversed_graph)
        print(levels)
        self.assertEqual(levels['node1'], 0)
        self.assertEqual(levels['node0'], 0)
        self.assertEqual(levels['node2'], 1)
