import list_examples
import unittest


class TestCollections(unittest.TestCase):

    def test_list_splitting(self):
        # split empty list to 2 chunks
        self.assertListEqual([list()], list_examples.split_list_equal_chunks(list(), 2))
        # split empty list to 0 chunks
        self.assertListEqual([list()], list_examples.split_list_equal_chunks(list(), 0))

        example = list(range(6))
        # split list to 1 chunk
        self.assertListEqual([[0, 1, 2, 3, 4, 5]], list_examples.split_list_equal_chunks(example, 1))
        # split list to 2 chunks
        self.assertListEqual([[0, 1, 2], [3, 4, 5]], list_examples.split_list_equal_chunks(example, 2))
