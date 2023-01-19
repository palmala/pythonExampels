import unittest
import csv
from checkers import AttributeMissingChecker3, Checker
from collections import defaultdict
from checkers2 import AttributeMissingChecker2, Checker2
import pandas as pd

class CheckerTests(unittest.TestCase):

    def test_checkers(self):
        # GIVEN
        subject = AttributeMissingChecker('owner', '')

        # WHEN / THEN
        self.assertTrue(isinstance(subject, Checker))


    def test_single_attribute(self):
        # GIVEN
        with open('data.csv', 'r') as data_csv:
            checkers = [AttributeMissingChecker('owner', ''), AttributeMissingChecker('sex', '')]
            cats = csv.DictReader(data_csv)

            # WHEN
            for cat in cats:
                for checker in checkers:
                    checker.check(cat)
            
            issues = Checker.merge_issues_dicts([checker.issues for checker in checkers])
            

        # THEN
        self.assertDictEqual(issues['Owner1'], {'Cat3': ['Missing sex info'], 'Cat4': ['Missing sex info']})
        self.assertDictEqual(issues[""], {'Cat2': ["Missing owner info"], 'Cat5': ["Missing owner info"], "Cat6": ["Missing owner info", "Missing sex info"]})


    def test_checkers2(self):
        # GIVEN
        subject = AttributeMissingChecker2(None, 'owner')
        
        # WHEN / THEN
        self.assertTrue(isinstance(subject, Checker2))
        
        
    def test_single_attribute2(self):
        # GIVEN
        cats_dataframe = pd.read_csv('data.csv')
        checkers = [AttributeMissingChecker2(cats_dataframe, 'owner'), AttributeMissingChecker2(cats_dataframe, 'sex')]
        
        # WHEN
        for checker in checkers:
            checker.check()
                    
        issues = Checker2.merge_issues([checker.issues for checker in checkers])
            
            
        # THEN
        self.assertDictEqual(issues['Owner1'], {'Cat3': ['Missing sex info'], 'Cat4': ['Missing sex info']})
        self.assertDictEqual(issues['Missing Owner'], {'Cat2': ["Missing owner info"], 'Cat5': ["Missing owner info"], "Cat6": ["Missing owner info", "Missing sex info"]})
        
        
if __name__ == '__main__':
    unittest.main()