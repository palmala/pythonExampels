#!/usr/bin/env python3

import numpy as np
from datetime import datetime, timedelta
from typing import Optional
import datetime as dt
from datetime import date
import holidays


REGIONS = {('ln', 'london'): 'UnitedKingdom', ('ny', 'new_york', 'newyork'): 'UnitedStates', ('tk', 'tokio'): "Japan", ('hk', 'hong_kong', 'hongkong'): 'HongKong'}


def _get_country_name_for_region(region: str):
	region = region.lower()
	for reg in REGIONS:
		if region in reg:
			return REGIONS[reg]
	raise ValueError(f"Region \"{region}\" is not valid. Please choose from these: {list(('/').join(region) for region in REGIONS)}")
	

def _get_num_of_workdays_of_a_country(country: str, month: int, year: int):
	holidays_res = holidays.country_holidays(country=country, years=year).keys()
	holidays_of_month = [holiday for holiday in holidays_res if holiday.month == month]
	start = dt.date( year, month, 1)
	end = (dt.date( year, month, 1) + timedelta(days=32)).replace(day=1)
	num_of_workdays = np.busday_count(start, end, holidays=holidays_of_month)
	return num_of_workdays
	
	
def get_num_of_workdays(region: Optional[str] = 'global', month: Optional[int] = datetime.now().month, year: Optional[int] = dt.datetime.now().year):
	if region == 'global':
		workdays_of_all_regions = [_get_num_of_workdays_of_a_country(country, month, year) for reg, country in REGIONS.items()]
		return min(workdays_of_all_regions)
	else:
		country = _get_country_name_for_region(region)
		return _get_num_of_workdays_of_a_country(country, month, year)
