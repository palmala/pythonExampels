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
    
    def __init__(self, checking_column: str):
        self.checking_attribute = checking_column
        self.issues = defaultdict(dict)
    
    
    def check(self, row: dict) -> dict:
        if not row[self.checking_attribute]:
            issue = {row['cat']: f"Missing {self.checking_attribute} info"}
            self.issues[row['owner']].update(issue)
