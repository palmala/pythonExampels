#!/usr/bin/env python3

import numpy as np
from datetime import datetime, timedelta
from typing import Optional
import datetime as dt
from datetime import date
import holidays

REGIONS = {('ln', 'london'): 'UnitedKingdom', ('ny', 'new_york', 'newyork'): 'UnitedStates', ('tk', 'tokio'): "Japan",
           ('hk', 'hong_kong', 'hongkong'): 'HongKong'}


def _get_country_name_for_region(region: str) -> str:
    region = region.lower()
    for reg in REGIONS:
        if region in reg:
            return REGIONS[reg]
    raise ValueError(
        f"Region \"{region}\" is not valid. Please choose from these: {list('/'.join(region) for region in REGIONS)}")


def _create_start_and_end_date(**kwargs) -> tuple:
    if 'year' in kwargs.keys() and 'month' in kwargs.keys():
        year = kwargs['year']
        month = kwargs['month']
        start = dt.date(year, month, 1)
        end = (dt.date(year, month, 1) + timedelta(days=32)).replace(day=1)
        return start, end
    elif 'start' in kwargs.keys() and 'end' in kwargs.keys():
        start = dt.datetime.strptime(kwargs['start'], '%Y-%m-%d').date()
        end = dt.datetime.strptime(kwargs['end'], '%Y-%m-%d').date()
        return start, end
    else:
        ValueError(f'Missing year, month / start, end keyword arguments.')
    
    
def _get_num_of_workdays_of_a_country(region: str, **kwargs) -> int:
    country = _get_country_name_for_region(region)
    start, end = _create_start_and_end_date(**kwargs)
    holidays_res = holidays.country_holidays(country=country, years=[start.year, end.year]).keys()
    holiday_dates = [holiday for holiday in holidays_res if holiday >= start and holiday < end]
    num_of_workdays = np.busday_count(start, end, holidays=holiday_dates)
    return num_of_workdays


def get_min_num_of_workdays_of_month(year: int = dt.datetime.now().year, month: int = datetime.now().month, regions: list = [reg[0] for reg in REGIONS]) -> int:
    return min([_get_num_of_workdays_of_a_country(reg, year=year, month=month) for reg in regions])


def get_min_num_of_workdays_of_time_period(start: str, end: str, regions: list = [reg[0] for reg in REGIONS]) -> int:
    return min([_get_num_of_workdays_of_a_country(reg, start=start, end=end) for reg in regions])


