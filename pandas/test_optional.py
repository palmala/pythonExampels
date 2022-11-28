import unittest
from typing import Optional


def func1(num1: int = 1, num2: int = 2) -> int:
    return num1 + num2


def func2(num1: Optional[int] = 1, num2: Optional[int] = 2) -> int:
    return num1 + num2


class OptionalTests(unittest.TestCase):

    def test_func(self):
        self.assertEqual(func1(), 3)
        self.assertEqual(func1(1), 3)
        self.assertEqual(func1(1, 2), 3)
        self.assertEqual(func1(None), 3)
