from abc import ABC, abstractmethod
import csv
from collections import defaultdict


class Checker(ABC):

    @abstractmethod
    def __init__(self):
        pass


    @abstractmethod
    def check(self, row: dict) -> dict:
        pass
    
    
    @staticmethod
    def merge_issues_dicts(list_of_issues_dicts: list):
        merged_issues = defaultdict(lambda: defaultdict(list))
        for issues_dict in list_of_issues_dicts:
            for key, value in issues_dict.items():
                for project, issue in value.items():
                    merged_issues[key][project].append(issue)
        
        return merged_issues


class AttributeMissingChecker(Checker):
    
    def __init__(self, checking_column, handling_issue_value):
        self.checking_attribute = checking_column
        self.issues = defaultdict(dict)
        self.handling_issue_value = handling_issue_value
        
    
    def check(self, row: dict):
        if row[self.checking_attribute] == self.handling_issue_value:
            issue = {row['cat']: f"Missing {self.checking_attribute} info"}
            self.issues[row['owner']].update(issue)



class AttributeIsNotProperChecker(Checker):
    
    def __init__(self, checking_column, ehcck_if_value_is_proper_function):
        self.checking_attribute = checking_column
        self.issues = defaultdict(dict)
        self.ehcck_if_value_is_proper_function = ehcck_if_value_is_proper_function
        
    
    
    def check(self, row: dict):
        if self.ehcck_if_value_is_proper_function(row[self.checking_attribute]):
            issue = {row['cat']: f"Not proper {self.checking_attribute} value ({row[self.checking_attribute]})"}
            self.issues[row['owner']].update(issue)


if __name__ == '__main__':
    with open('data.csv', 'r') as data_csv:
        checkers = [AttributeMissingChecker('owner', ''), AttributeMissingChecker('sex', ''), AttributeIsNotProperChecker('sconar_findings', lambda x: int(x) > 5)]
        cats = csv.DictReader(data_csv)
        
        for cat in cats:
            for checker in checkers:
                checker.check(cat)
                
        issues = Checker.merge_issues_dicts([checker.issues for checker in checkers])
        for k, v in issues.items():
            print(f"OWNER={k}: {v}")
        
        