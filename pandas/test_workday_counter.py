#!/usr/bin/env python3

import unittest
from workday_counter import _get_country_name_for_region, _get_num_of_workdays_of_a_country, get_min_num_of_workdays_of_month, get_min_num_of_workdays_of_time_period
from pandas import Timestamp


class TestWorkdayCounter(unittest.TestCase):

    def test_get_country_name_for_region(self):
        # GIVEN
        ln_region = 'ln'
        hk_region = 'hk'
        ny_region = 'newyork'
        tk_region = 'tokio'
        invalid_region = 'invalid_region'

        # WHEN
        actual_ln = _get_country_name_for_region(ln_region)
        actual_hk = _get_country_name_for_region(hk_region)
        actual_ny = _get_country_name_for_region(ny_region)
        actual_tk = _get_country_name_for_region(tk_region)

        # THEN
        self.assertEqual(actual_ln, 'UnitedKingdom')
        self.assertEqual(actual_hk, 'HongKong')
        self.assertEqual(actual_ny, 'UnitedStates')
        self.assertEqual(actual_tk, 'Japan')
        self.assertRaises(ValueError, _get_country_name_for_region, invalid_region)

    def test_get_num_of_workdays_of_a_country(self):
        # GIVEN / WHEN
        actual_ln_workdays_2022_04 = _get_num_of_workdays_of_a_country('ln', year=2022, month=4)
        actual_hk_workdays_2022_02 = _get_num_of_workdays_of_a_country('hk', year=2022, month=2)
        actual_tk_workdays_2021_04 = _get_num_of_workdays_of_a_country('tk', year=2021, month=4)
        actual_ny_workdays_2020_07 = _get_num_of_workdays_of_a_country('ny', year=2020, month=7)

        # THEN
        self.assertEqual(actual_ln_workdays_2022_04, 19)
        self.assertEqual(actual_hk_workdays_2022_02, 17)
        self.assertEqual(actual_tk_workdays_2021_04, 21)
        self.assertEqual(actual_ny_workdays_2020_07, 22)

    def test_get_min_num_of_workdays_of_month(self):
        # GIVEN / WHEN
        actual_hk_workdays_2022_04 = get_min_num_of_workdays_of_month(regions=['hk'], year=2022, month=4)
        actual_ny_workdays_2022_04 = get_min_num_of_workdays_of_month(regions=['ny'], year=2022, month=4)
        actual_ln_workdays_2022_04 = get_min_num_of_workdays_of_month(regions=['ln'], year=2022, month=4)
        actual_tk_workdays_2022_04 = get_min_num_of_workdays_of_month(regions=['tk'], year=2022, month=4)
        the_min_num_of_workdays_amongst_regions = get_min_num_of_workdays_of_month(year=2022, month=4)

        actual_hk_workdays_2022_04_tp = get_min_num_of_workdays_of_time_period(regions=['hk'], start='2022-04-01', end='2022-05-01')
        actual_ny_workdays_2022_04_tp = get_min_num_of_workdays_of_time_period(regions=['ny'], start='2022-04-01', end='2022-05-01')
        actual_ln_workdays_2022_04_tp = get_min_num_of_workdays_of_time_period(regions=['ln'], start='2022-04-01', end='2022-05-01')
        actual_tk_workdays_2022_04_tp = get_min_num_of_workdays_of_time_period(regions=['tk'], start='2022-04-01', end='2022-05-01')
        the_min_num_of_workdays_amongst_regions_tp = get_min_num_of_workdays_of_time_period(start='2022-04-01', end='2022-05-01')
        
        # THEN
        self.assertEqual({actual_hk_workdays_2022_04, actual_hk_workdays_2022_04_tp}, {18})
        self.assertEqual({actual_ln_workdays_2022_04, actual_ln_workdays_2022_04_tp}, {19})
        self.assertEqual({actual_tk_workdays_2022_04, actual_tk_workdays_2022_04_tp}, {20})
        self.assertEqual({actual_ny_workdays_2022_04, actual_ny_workdays_2022_04_tp}, {21})
        self.assertEqual({the_min_num_of_workdays_amongst_regions, the_min_num_of_workdays_amongst_regions_tp}, {18})


    def test_get_workday_hours_in_time_range(self):
        # GIVEN
        ranges = [
            {'from': Timestamp(), 'to': Timestamp(), 'expected': 0},
            {'from': Timestamp(), 'to': Timestamp(), 'expected': 0},
            {'from': Timestamp(), 'to': Timestamp(), 'expected': 0},
            {'from': Timestamp(), 'to': Timestamp(), 'expected': 0}
        ]

        # WHEN
        results = [get_workday_hours_in_time_range(trange['from'], trange['to']) for trange in ranges]

        # THEN
        for result in results:
            self.assertEqual(results['expected'], result)


if __name__ == "__main__":
    unittest.main()
    