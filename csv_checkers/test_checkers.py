import unittest
import csv
from checkers import AttributeMissingChecker, Checker
from collections import defaultdict


class CheckerTests(unittest.TestCase):

    def test_checkers(self):
        # GIVEN
        subject = AttributeMissingChecker()

        # WHEN / THEN
        self.assertTrue(isinstance(subject, Checker))

    def test_single_attribute(self):
        # GIVEN
        with open('data.csv', 'r') as data_csv:
            checkers = [AttributeMissingChecker("owner"), AttributeMissingChecker("sex")]
            cats = csv.DictReader(data_csv)
            issues = defaultdict(dict)

            # WHEN
            for cat in cats:
                issues.update(checkers.check(cat))

        # THEN
        self.assertDictEqual(issues['Owner1'], [{'Cat3': ["Missing sex info"]}])
        self.assertDictEqual(issues[None], [{'Cat2': ["Missing owner info"]}])
