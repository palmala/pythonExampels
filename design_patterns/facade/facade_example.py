#!/usr/bin/env python3
import get_owner
import get_color
import get_num_of_rooms
from house import House


class PropertyLoader:
	
	def __init__(self):
		self.owner_data = self._get_owner_data()
		self.color_data = self._get_color_data()
		
	
	def _get_owner_data(self):
		return {'house1':'owner1', 'house2': 'owner2', 'house3':'owner3'}
	
	
	def _get_color_data(self):
		return {'house1':'white', 'house2': 'yellow', 'house3':'green'}
	
	
	def load_house_properties(self, house):
		house.owner = get_owner.get_owner(house, self.owner_data)
		house.color = get_color.get_color(house, self.color_data)
		house.num_of_rooms = get_num_of_rooms.get_num_of_rooms(house)
	
	
if __name__ == '__main__':
	house_list = [House('house1'), House('house2'), House('house3')]	
	loader = PropertyLoader()
	for house in house_list:
		loader.load_house_properties(house)
	print(f"facade: {[(house.id, house.owner) for house in house_list]}")
	