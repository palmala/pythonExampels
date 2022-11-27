#!/usr/bin/env python3

import unittest
from workday_counter import _get_country_name_for_region, _get_num_of_workdays_of_a_country, get_min_num_of_workdays

class TestWorkdayCounter(unittest.TestCase):
	
	def test_get_country_name_for_region(self):
		#GIVEN
		ln_region = 'ln'
		hk_region = 'hk'
		ny_region = 'newyork'
		tk_region = 'tokio'
		invalid_region = 'invalid_region'
		
		#WHEN
		actual_ln = _get_country_name_for_region(ln_region)
		actual_hk = _get_country_name_for_region(hk_region)
		actual_ny= _get_country_name_for_region(ny_region)
		actual_tk = _get_country_name_for_region(tk_region)

		#THEN
		self.assertEqual(actual_ln, 'UnitedKingdom')
		self.assertEqual(actual_hk, 'HongKong')
		self.assertEqual(actual_ny, 'UnitedStates')
		self.assertEqual(actual_tk, 'Japan')
		self.assertRaises(ValueError, _get_country_name_for_region, invalid_region)
			
		
	def test_get_num_of_workdays_of_a_country(self):
		#GIVEN
		#WHEN
		actual_ln_workdays_2022_04 = _get_num_of_workdays_of_a_country('ln', 4, 2022)
		actual_hk_workdays_2022_02 = _get_num_of_workdays_of_a_country('hk', 2, 2022)
		actual_tk_workdays_2021_04 = _get_num_of_workdays_of_a_country('tk', 4, 2021)
		actual_ny_workdays_2020_07 = _get_num_of_workdays_of_a_country('ny', 7, 2020)
		
		#THEN
		self.assertEqual(actual_ln_workdays_2022_04, 19)
		self.assertEqual(actual_hk_workdays_2022_02, 17)
		self.assertEqual(actual_tk_workdays_2021_04, 21)
		self.assertEqual(actual_ny_workdays_2020_07, 22)


	def testget_min_num_of_workdays(self):
		#GIVEN
		#WHEN
		actual_hk_workdays_2022_04 = get_min_num_of_workdays(['hk'], month=4, year=2022)
		actual_ny_workdays_2022_04 = get_min_num_of_workdays(['ny'], month=4, year=2022)
		actual_ln_workdays_2022_04 = get_min_num_of_workdays(['ln'], month=4, year=2022)
		actual_tk_workdays_2022_04 = get_min_num_of_workdays(['tk'], month=4, year=2022)
		the_smallest_num_of_workdays_amongst_regions = get_min_num_of_workdays(month=4, year=2022)
		
		
		#THEN
		self.assertEqual(actual_hk_workdays_2022_04, 18)
		self.assertEqual(actual_ln_workdays_2022_04, 19)
		self.assertEqual(actual_tk_workdays_2022_04, 20)
		self.assertEqual(actual_ny_workdays_2022_04, 21)
		self.assertEqual(the_smallest_num_of_workdays_amongst_regions, 18)

	
if __name__ == "__main__":
	unittest.main()