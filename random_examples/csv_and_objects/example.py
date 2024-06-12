# !/usr/bin/env python3
import csv

class PersonModel():
	def __init__(self):
		self.name = None
		self.age = None
		self.gender = None
#		self.new_field = None
		
		
	def convert_data(self, field, value):
		if field == 'name':
			value = value.upper()
		elif field == 'age':
			value = int(value)
		
		return value
	
	
class Person(PersonModel):
	def __init__(self, **kwargs):
		super().__init__()
		unexppected_properties = self.get_unexpected_passed_properties(kwargs)
		missing_properties = self.check_missing_passed_properties_and_set_a_default_value(kwargs, "Missing")
		correct_properties_for_set = {field: value for field, value in kwargs.items() if ((field not in unexppected_properties) and (field not in missing_properties))}
		for field, value in correct_properties_for_set.items():	
			setattr(self, field, self.convert_data(field, value))


	def get_unexpected_passed_properties(self, properties_for_set: dict):		
		unexpected_properties = (set(properties_for_set)) - (set(self.__dict__))
		if unexpected_properties:
			print(f"These properties are not set, because they are not in the model: {unexpected_properties}")
		return unexpected_properties
	
	
	def check_missing_passed_properties_and_set_a_default_value(self, properties_for_set: dict, default_value):		
		missing_properties = (set(self.__dict__)) - (set(properties_for_set))
		if missing_properties:
			print(f"These properties are missing: {missing_properties}")
		for field in missing_properties:
			setattr(self, field, default_value)
		return missing_properties
		
		
if __name__ == '__main__':
	with open('example.csv') as f:
		reader = csv.DictReader(f)
		rows = [row for row in reader]
	persons = [Person(**row) for row in rows]
	for person in persons:
		print(f"{person.__dict__}")
	
		