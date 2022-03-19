import os
import sys
import unittest
import json

from click.testing import CliRunner

current_directory = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current_directory)
sys.path.append(parent)
from app.validator import get_untagged
from app.validator import get_tags
from app.validator import get_tests_for_tag
from app.validator import get_random_tests_per_tag
from app.validator import get_tests_per_tags

TEST_CASES_DIR = "test_cases"


class CliTests(unittest.TestCase):

    def setUp(self):
        runner = CliRunner()
        results = runner.invoke(get_tests_per_tags, [f"{TEST_CASES_DIR}", "--js"])
        self.all_tests = json.loads(results.output)

    @staticmethod
    def test_get_untagged():
        runner = CliRunner()
        result = runner.invoke(get_untagged, f"{TEST_CASES_DIR}")
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

    def test_get_random_tests(self):
        runner = CliRunner()
        NUM_TESTS = 2
        result = runner.invoke(get_random_tests_per_tag, [TEST_CASES_DIR, str(NUM_TESTS), "--js"])
        result_json = json.loads(result.output)
        assert (result.exit_code == 0)
        all_tags = set([tag for tag in self.all_tests if tag != "UNTAGGED"])
        result_tags = set([tag for tag in result_json])
        assert (all_tags == result_tags)
        for tag in result_tags:
            if len(self.all_tests[tag]) <= NUM_TESTS:
                assert (len(result_json[tag]) == len(self.all_tests[tag]))
                assert (set(result_json[tag]) == set(self.all_tests[tag]))
            else:
                assert (len(result_json[tag]) < len(self.all_tests[tag]))
                assert (set(result_json[tag]).issubset(set(self.all_tests[tag])))


if __name__ == '__main__':
    unittest.main()
