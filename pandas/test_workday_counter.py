#!/usr/bin/env python3

import unittest
from workday_counter import _get_country_name_for_region, _get_num_of_workdays_of_a_country, get_min_num_of_workdays
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
        # GIVEN
        # WHEN
        actual_ln_workdays_2022_04 = _get_num_of_workdays_of_a_country('ln', 2022, 4)
        actual_hk_workdays_2022_02 = _get_num_of_workdays_of_a_country('hk', 2022, 2)
        actual_tk_workdays_2021_04 = _get_num_of_workdays_of_a_country('tk', 2021, 4)
        actual_ny_workdays_2020_07 = _get_num_of_workdays_of_a_country('ny', 2020, 7)

        # THEN
        self.assertEqual(actual_ln_workdays_2022_04, 19)
        self.assertEqual(actual_hk_workdays_2022_02, 17)
        self.assertEqual(actual_tk_workdays_2021_04, 21)
        self.assertEqual(actual_ny_workdays_2020_07, 22)

    def test_get_min_num_of_workdays(self):
        # GIVEN
        # WHEN
        actual_hk_workdays_2022_04 = get_min_num_of_workdays(['hk'], year=2022, month=4)
        actual_ny_workdays_2022_04 = get_min_num_of_workdays(['ny'], year=2022, month=4)
        actual_ln_workdays_2022_04 = get_min_num_of_workdays(['ln'], year=2022, month=4)
        actual_tk_workdays_2022_04 = get_min_num_of_workdays(['tk'], year=2022, month=4)
        the_smallest_num_of_workdays_amongst_regions = get_min_num_of_workdays(year=2022, month=4)

        # THEN
        self.assertEqual(actual_hk_workdays_2022_04, 18)
        self.assertEqual(actual_ln_workdays_2022_04, 19)
        self.assertEqual(actual_tk_workdays_2022_04, 20)
        self.assertEqual(actual_ny_workdays_2022_04, 21)
        self.assertEqual(the_smallest_num_of_workdays_amongst_regions, 18)

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
