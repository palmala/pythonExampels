import pandas as pd
from abc import ABC, abstractmethod
from collections import defaultdict

CATS_DATAFRAME = pd.read_csv('data.csv')

class Checker2(ABC):
	
	@abstractmethod
	def __init__(self):
		pass
		
		
	@abstractmethod
	def check(self, row: dict) -> dict:
		pass
	
	
	@staticmethod
	def merge_issues(list_of_issues_dataframes: list):
		all_issues = {}
		df_all_rows = pd.concat(list_of_issues_dataframes)
		for owner, issue_df in df_all_rows.groupby('owner', dropna=False):
			cat_and_issues_pairs = defaultdict(list)
			for cat, issue in zip(issue_df.cat, issue_df.issue):
				cat_and_issues_pairs[cat].append(issue)
			all_issues[owner] = cat_and_issues_pairs
		return all_issues
			
		
class AttributeMissingChecker2(Checker2):
	
	def __init__(self, csv_dataframe, checking_attribute):
		self.csv_dataframe = csv_dataframe
		self.checking_attribute = checking_attribute
		self.issues = None
		
		
	def check(self):
		rows_with_missing_attribues = self.csv_dataframe[self.csv_dataframe[self.checking_attribute].isna()]
		rows_with_missing_attribues = rows_with_missing_attribues[['cat', 'owner']]
		rows_with_missing_attribues['issue'] = f"Missing {self.checking_attribute} info"
		rows_with_missing_attribues['owner'] = rows_with_missing_attribues['owner'].fillna("Missing Owner")
		self.issues = rows_with_missing_attribues
		
		
