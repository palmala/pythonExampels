import unittest
from dotbuilder import *
from dummy_commit_provider import DummyCommitProvider
from dummy_projects_provider import DummyProjectsProvider
from projects_filter import restrict_projects
import os
import shutil

shutil.rmtree("build", ignore_errors=True)
os.makedirs("build")


class TestDotBuild(unittest.TestCase):
    def test_parsing(self):
        projects_provider = DummyProjectsProvider()
        subject = dot_builder(projects_provider.get_projects())
        with open("build/1_test_original.dot", "w") as resultdot:
            resultdot.write(str(subject))
        instability = calculate_instability(subject)
        with open("build/2_test_instability.dot", "w") as resultdot:
            resultdot.write(str(subject))
        violations = calculate_violations(subject, instability)
        with open("build/3_test_violations.dot", "w") as resultdot:
            resultdot.write(str(subject))

        self.assertEqual(len(violations), 1, "Number of violations is incorrect!")
        self.assertTrue("componentB->componentC" in violations)
        self.assertAlmostEqual(instability['componentC'], 0.667, places=3)
        self.assertAlmostEqual(instability['componentA'], 0.5, places=3)

        commits = update_with_commits(subject, DummyCommitProvider())
        with open("build/4_test_commits.dot", "w") as resultdot:
            resultdot.write(str(subject))

        color_changed_nodes(mygraph=subject, commits=commits)
        with open("build/5_test_commits_colored_changed.dot", "w") as resultdot:
            resultdot.write(str(subject))

        color_changed_nodes_per_instability(mygraph=subject, instability=instability, commits=commits)
        with open("build/6_test_commits_colored_instability.dot", "w") as resultdot:
            resultdot.write(str(subject))

        reset_colors(mygraph=subject)
        with open("test_reset.dot", "w") as resultdot:
            resultdot.write(str(subject))

        # color_critical_paths(mygraph=subject, commits=commits)
        # with open("build/7_test_critical_path.dot", "w") as resultdot:
        #     resultdot.write(str(subject))

    def test_projects_filter(self):
        projects_provider = DummyProjectsProvider()
        projects = projects_provider.get_projects()
        filtered = restrict_projects(projects, ["componentA", "componentC"])
        print(filtered)

    def test_get_subtree(self):
        projects = {
            'B': ['A'],
            'C': ['A'],
            'D': ['B'],
            'E': ['B'],
            'F': ['C'],
            'G': ['C']
        }
        subject = dot_builder(projects)
        with open("build/test_subtree_1.dot", "w") as resultdot:
            resultdot.write(str(subject))
        result = get_all_dependants(mygraph=subject, node_name="A")
        with open("build/test_subtree_2.dot", "w") as resultdot:
            resultdot.write(str(result))


if __name__ == "__main__":
    unittest.main()
