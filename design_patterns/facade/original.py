#!/usr/bin/env python3

import get_owner
import get_color
import get_num_of_rooms
from house import House

def get_owner_data():
	return {'house1':'owner1', 'house2': 'owner2', 'house3':'owner3'}


def get_color_data():
	return {'house1':'white', 'house2': 'yellow', 'house3':'green'}


def load_house_properties(house, owner_data, color_data):
	house.owner = get_owner.get_owner(house, owner_data)
	house.color = get_color.get_color(house, color_data)
	house.num_of_rooms = get_num_of_rooms.get_num_of_rooms(house)
	
	
if __name__ == '__main__':
	house_list = [House('house1'), House('house2'), House('house3')]
	owner_data = get_owner_data()
	color_data = get_color_data()
	
	for house in house_list:
		load_house_properties(house, owner_data, color_data)
	print(f"original: {[(house.id, house.owner) for house in house_list]}")
	