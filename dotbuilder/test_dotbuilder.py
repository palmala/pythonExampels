import unittest

from dotbuilder import *
from dummy_projects_provider import DummyProjectsProvider
import os
import shutil

OUTPUT = "build"

PROJECTS = {
    'A': ['B', 'D'],
    'B': ['A'],
    'C': ['A'],
    'D': ['B', 'E'],
    'E': []
}


class TestDotBuild(unittest.TestCase):

    def setUp(self) -> None:
        shutil.rmtree(OUTPUT, ignore_errors=True)
        os.makedirs(OUTPUT)

    def test_parsing_empty_graph(self):
        # GIVEN
        projects = dict()

        # WHEN / THEN
        with self.assertRaises(AttributeError):
            subject = dot_builder(projects, "test_main")

    def test_parsing(self):
        # GIVEN
        projects_provider = DummyProjectsProvider()

        # WHEN
        subject = dot_builder(projects_provider.get_projects(), "test_main")

        # THEN
        self.assertIsInstance(subject, Dot)

    def test_instability(self):
        # GIVEN
        projects = PROJECTS.copy()
        projects['F'] = []
        subject = dot_builder(projects, "test_instability")

        # WHEN
        instability = calculate_instability(subject)

        # THEN
        self.assertEqual(instability['A'], 0.5)
        self.assertAlmostEqual(instability['B'], 0.333, places=3)
        self.assertEqual(instability['C'], 1)
        self.assertAlmostEqual(instability['D'], 0.667, places=3)
        self.assertEqual(instability['E'], 0)
        self.assertEqual(instability['F'], 1)

    def test_violations(self):
        # GIVEN
        subject = dot_builder(PROJECTS, "test_violations")
        instability = calculate_instability(subject)

        # WHEN
        violations = calculate_violations(subject, instability)

        # THEN
        self.assertEqual(len(violations), 2)
        self.assertIn("B->A", violations)
        self.assertIn("A->D", violations)
        write_to_file(subject, f"{OUTPUT}/test.dot")

    def test_classifications(self):
        # GIVEN
        subject = dot_builder(PROJECTS, "test_classifications")
        instability = calculate_instability(subject)

        # WHEN
        classifications = classify_nodes_per_instability(subject, instability)

        # THEN
        self.assertEqual(len(classifications), 5)
        self.assertEqual(classifications['CRITICAL'], ['E'])
        self.assertEqual(classifications['NONE'], ['C'])
        self.assertEqual(classifications['LOW'], list())
        self.assertListEqual(classifications['MEDIUM'], ['A', 'D'])
        self.assertEqual(classifications['HIGH'], ['B'])

    def test_cycles(self):
        # GIVEN
        subject = dot_builder(PROJECTS, "cycles")

        # WHEN
        cycles = detect_all_cycles(subject)

        # THEN
        self.assertEqual(len(cycles), 2)
        self.assertIn(('A', 'B', 'A'), cycles)
        self.assertIn(('A', 'D', 'B', 'A'), cycles)

    def test_no_cycles(self):
        # GIVEN
        projects = {
            'B': [],
            'A': ['B']
        }
        subject = dot_builder(projects, "no_cycles")

        # WHEN
        cycles = detect_all_cycles(subject)

        # THEN
        self.assertEqual(len(cycles), 0)

    def test_dependants(self):
        # GIVEN
        subject = dot_builder(PROJECTS, "test_dependants")

        # WHEN
        dependants = get_all_dependants(mygraph=subject, node_name="A")

        # THEN
        self.assertEqual(len(list(dependants.get_edge_list())), 5)
        self.assertTrue(self._graph_has_edge(dependants, source_name='A', target_name='B'))
        self.assertTrue(self._graph_has_edge(dependants, source_name='A', target_name='D'))
        self.assertTrue(self._graph_has_edge(dependants, source_name='B', target_name='A'))
        self.assertTrue(self._graph_has_edge(dependants, source_name='D', target_name='B'))
        self.assertTrue(self._graph_has_edge(dependants, source_name='C', target_name='A'))

    def test_dependants_of_nonexistent(self):
        # GIVEN
        subject = dot_builder(PROJECTS, "test_dependants")

        # WHEN / THEN
        with self.assertRaises(AttributeError):
            dependants = get_all_dependants(mygraph=subject, node_name="NO_SUCH_NODE")

    @staticmethod
    def _graph_has_edge(graph: Dot, source_name: str, target_name: str):
        for edge in graph.get_edge_list():
            if edge.get_source() == source_name and edge.get_destination() == target_name:
                return True
        return False


if __name__ == "__main__":
    unittest.main()
