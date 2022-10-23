import unittest
from dotbuilder import *
from dummy_commit_provider import DummyCommitProvider
from dummy_projects_provider import DummyProjectsProvider
import os
import shutil

shutil.rmtree("build", ignore_errors=True)
os.makedirs("build")
OUTPUT = "build"


class TestDotBuild(unittest.TestCase):
    def test_parsing(self):
        projects_provider = DummyProjectsProvider()
        subject = dot_builder(projects_provider.get_projects())
        self._write_to_file(str(subject), "main_1_original.dot")

        instability = calculate_instability(subject)
        self._write_to_file(str(subject), "main_2_instability.dot")

        violations = calculate_violations(subject, instability)
        self._write_to_file(str(subject), "main_3_violations.dot")

        commits = update_with_commits(subject, DummyCommitProvider())
        self._write_to_file(str(subject), "main_4_commits.dot")

        color_changed_nodes(mygraph=subject, commits=commits)
        self._write_to_file(str(subject), "main_5_color_changed.dot")

        color_changed_nodes_per_instability(mygraph=subject, instability=instability, commits=commits)
        self._write_to_file(str(subject), "main_6_color_changed_per_instability.dot")

        reset_colors(mygraph=subject)
        self._write_to_file(subject, "main_7_reset.dot")

    def test_get_all_dependants(self):
        subject = dot_builder(DummyProjectsProvider().get_projects())
        self._write_to_file(str(subject), "dependants1_orig.dot")
        result = get_all_dependants(mygraph=subject, node_name="B")
        self._write_to_file(str(result), "dependants2.dot")

    @classmethod
    def _write_to_file(cls, what: str, where: str):
        with open(f"{OUTPUT}/test_{where}", "w") as resultdot:
            resultdot.write(str(what))


if __name__ == "__main__":
    unittest.main()
