import unittest
import pandas
from pandas import Timestamp
from pandas.testing import assert_frame_equal

import timestamp_lib
import numpy


class BasicTests(unittest.TestCase):

    def test_month_overflow(self):
        # GIVEN a time window in the dataset which overflows to another month
        data = [
            {'month': '2022-01', 'from': Timestamp('2022-01-30 23:00:00'), 'to': Timestamp('2022-02-02 01:00:00')},
            {'month': '2022-01', 'from': Timestamp('2022-01-01 23:00:00'), 'to': Timestamp('2022-01-02 01:00:00')}
        ]
        subject = pandas.DataFrame.from_dict(data)

        # WHEN we detect the overflows in the dataset
        overflows = timestamp_lib.detect_month_overflows(subject)

        # THEN that time window is part of the returned collection as (from, to)
        self.assertTrue(overflows)
        self.assertTrue(tuple([Timestamp('2022-01-30 23:00:00'), Timestamp('2022-02-02 01:00:00')]) in overflows)

    def test_merge_overlaps(self):
        # GIVEN
        data = [
            {'month': '2022-01', 'from': Timestamp('2022-01-01 04:00:00'), 'to': Timestamp('2022-01-01 14:00:00')},
            {'month': '2022-01', 'from': Timestamp('2022-01-01 04:00:00'), 'to': Timestamp('2022-01-01 08:00:00')},
            {'month': '2022-01', 'from': Timestamp('2022-01-01 08:00:00'), 'to': Timestamp('2022-01-01 16:00:00')},
            {'month': '2022-01', 'from': Timestamp('2022-01-02 01:00:00'), 'to': Timestamp('2022-01-02 11:00:00')},
            {'month': '2022-02', 'from': Timestamp('2022-02-01 04:00:00'), 'to': Timestamp('2022-02-01 08:00:00')},
            {'month': '2022-02', 'from': Timestamp('2022-02-01 08:00:00'), 'to': Timestamp('2022-02-01 12:00:00')},
            {'month': '2022-02', 'from': Timestamp('2022-02-02 08:00:00'), 'to': Timestamp('2022-02-02 16:00:00')}

        ]
        subject = pandas.DataFrame.from_dict(data)

        # WHEN
        merged_overlaps = timestamp_lib.merge_overlaps(dataframe=subject, group_by="month")

        # THEN
        self.assertFalse(merged_overlaps.empty)
        expected = pandas.DataFrame.from_dict([
            {'month': '2022-01', 'from': Timestamp('2022-01-01 04:00:00'), 'to': Timestamp('2022-01-01 16:00:00')},
            {'month': '2022-01', 'from': Timestamp('2022-01-02 01:00:00'), 'to': Timestamp('2022-01-02 11:00:00')},
            {'month': '2022-02', 'from': Timestamp('2022-02-01 04:00:00'), 'to': Timestamp('2022-02-01 12:00:00')},
            {'month': '2022-02', 'from': Timestamp('2022-02-02 08:00:00'), 'to': Timestamp('2022-02-02 16:00:00')}
        ])
        diff = expected.compare(merged_overlaps)
        self.assertTrue(diff.empty)

    def test_split_month_overflow(self):
        # GIVEN
        data = [
            {'from': Timestamp('2022-01-31 20:00:00'), 'to': Timestamp('2022-02-01 04:00:00')},
            {'from': Timestamp('2022-01-11 20:00:00'), 'to': Timestamp('2022-01-11 23:00:00')}
        ]
        subject = pandas.DataFrame.from_dict(data)

        # WHEN
        split_overflows = timestamp_lib.split_overflows(dataframe=subject)

        # THEN
        self.assertFalse(split_overflows.empty)
        expected = pandas.DataFrame.from_dict([
            {'from': Timestamp('2022-01-11 20:00:00'), 'to': Timestamp('2022-01-11 23:00:00')},
            {'from': Timestamp('2022-01-31 20:00:00'), 'to': Timestamp('2022-02-01 00:00:00')},
            {'from': Timestamp('2022-02-01 00:00:00'), 'to': Timestamp('2022-02-01 04:00:00')}
        ])
        assert_frame_equal(expected, split_overflows, check_index_type=False)
