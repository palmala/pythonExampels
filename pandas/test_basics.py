import unittest
import pandas
from pandas import Timestamp
import timestamp_lib


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

        # THEN that time window is part of the returned set as (from, to)
        self.assertTrue(overflows)
        self.assertSetEqual(overflows, {tuple([Timestamp('2022-01-30 23:00:00'), Timestamp('2022-02-02 01:00:00')])})
