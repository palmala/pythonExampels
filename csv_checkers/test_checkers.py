import unittest
import csv
from checkers import AttributeMissingChecker, Checker
from collections import defaultdict


class CheckerTests(unittest.TestCase):

    def test_checkers(self):
        # GIVEN
        subject = AttributeMissingChecker('owner')

        # WHEN / THEN
        self.assertTrue(isinstance(subject, Checker))


    def test_single_attribute(self):
        # GIVEN
        with open('data.csv', 'r') as data_csv:
            checkers = [AttributeMissingChecker("owner"), AttributeMissingChecker("sex")]
            cats = csv.DictReader(data_csv)

            # WHEN
            for cat in cats:
                for checker in checkers:
                    checker.check(cat)
            
            issues = Checker.merge_issues_dicts([checker.issues for checker in checkers])
            

        # THEN
        self.assertDictEqual(issues['Owner1'], {'Cat3': ['Missing sex info'], 'Cat4': ['Missing sex info']})
        self.assertDictEqual(issues[""], {'Cat2': ["Missing owner info"], 'Cat5': ["Missing owner info"], "Cat6": ["Missing owner info", "Missing sex info"]})
