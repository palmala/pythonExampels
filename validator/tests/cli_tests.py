import os
import sys
import unittest

from click.testing import CliRunner

current_directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current_directory)
sys.path.append(parent)
from app.validator import get_untagged
from app.validator import get_tags
from app.validator import get_tests_for_tag

TEST_CASES_DIR = "test_cases"


class CliTests(unittest.TestCase):

    @staticmethod
    def test_get_untagged():
        runner = CliRunner()
        result = runner.invoke(get_untagged, f"{TEST_CASES_DIR}/untagged")
        print(f"Output is {result.output}")
        assert (result.exit_code != 0)
        assert ("test1.md" in result.output)

    @staticmethod
    def test_get_tags():
        runner = CliRunner()
        result = runner.invoke(get_tags, TEST_CASES_DIR)
        print(f"Output is {result.output}")
        assert (result.exit_code == 0)
        assert (all([tag in result.output for tag in ["tag1", "tag2"]]))

    @staticmethod
    def test_get_tests_for_tag():
        runner = CliRunner()
        result = runner.invoke(get_tests_for_tag, [TEST_CASES_DIR, "tag1"])
        print(f"Output is {result.output}")
        assert (result.exit_code == 0)
        assert (all([test in result.output for test in ["test2.md", "test3.md", "test4.md"]]))


if __name__ == '__main__':
    unittest.main()
