#!/usr/bin/env python3

import numpy as np
from datetime import datetime, timedelta
from typing import Optional
import datetime as dt
from datetime import date
import holidays


REGIONS = ['ln', 'ny', 'tk', 'hk']

def _transform_region_to_country(region: str):
	region = region.lower()
	
	if region in ['tk', 'tokio']:
		return 'Japan'
	elif region in ['hk', 'hongkong', 'hong_kong']:		
		return 'HongKong'
	elif region in ['ny', 'newyork', 'new_york']:		
		return 'UnitedStates'
	elif region in ['ln', 'london']:		
		return 'UnitedKingdom'
	else:
		raise ValueError(f"Region \"{region}\" is not valid. Please choose from these: {REGIONS}")
		

def _get_num_of_workdays(country: str, month: int, year: int):
	holidays_res = holidays.country_holidays(country=country, years=year).keys()
	holidays_of_month = [holiday for holiday in holidays_res if holiday.month == month]
	
	start = dt.date( year, month, 1)
	end = (dt.date( year, month, 1) + timedelta(days=32)).replace(day=1)
	
	num_of_workdays = np.busday_count(start, end, holidays=holidays_of_month)
	return num_of_workdays
	
	
def get_num_of_workdays(region: Optional[str] = 'global', month: Optional[int] = datetime.now().month, year: Optional[int] = dt.datetime.now().year):
	if region == 'global':
		workdays_of_all_regions = [_get_num_of_workdays(_transform_region_to_country(reg), month, year) for reg in REGIONS]
		return min(workdays_of_all_regions)
	else:
		country = _transform_region_to_country(region)
		return _get_num_of_workdays(country, month, year)
		
		
if __name__ == '__main__':
	print(f"global: {get_num_of_workdays()}")
	print(f"LN : {get_num_of_workdays('ln')}")
	print(f"HK Feb 2022: {get_num_of_workdays('hk', 2, 2022)}")
	