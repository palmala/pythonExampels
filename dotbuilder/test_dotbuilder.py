import unittest
from dotbuilder import *
from dummy_commit_provider import DummyCommitProvider

example = {
    'componentA': ['componentB'],
    'componentC': ['componentB', 'componentA'],
    'componentB': ['componentC']
}


class TestDotBuild(unittest.TestCase):
    def test_parsing(self):
        subject = dot_builder(example)
        with open("test_original.dot", "w") as resultdot:
            resultdot.write(str(subject))
        instability = calculate_instability(subject)
        with open("test_instability.dot", "w") as resultdot:
            resultdot.write(str(subject))
        violations = calculate_violations(subject, instability)
        with open("test_violations.dot", "w") as resultdot:
            resultdot.write(str(subject))

        self.assertEqual(len(violations), 1, "Number of violations is incorrect!")
        self.assertTrue("componentB->componentC" in violations)
        self.assertAlmostEqual(instability['componentC'], 0.667, places=3)
        self.assertAlmostEqual(instability['componentA'], 0.5, places=3)

        commits = update_with_commits(subject, DummyCommitProvider())
        with open("test_commits.dot", "w") as resultdot:
            resultdot.write(str(subject))

        color_changed_nodes(mygraph=subject, commits=commits)
        with open("test_commits_colored_changed.dot", "w") as resultdot:
            resultdot.write(str(subject))

        color_changed_nodes_per_instability(mygraph=subject, instability=instability, commits=commits)
        with open("test_commits_colored_instability.dot", "w") as resultdot:
            resultdot.write(str(subject))


if __name__ == "__main__":
    unittest.main()
