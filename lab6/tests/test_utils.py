import unittest
from lab6.src.utils import StringUtils, ListUtils


class TestStringUtils(unittest.TestCase):
    def setUp(self):
        self.string_utils = StringUtils()

    def test_reverse_string(self):
        self.assertEqual(self.string_utils.reverse_string("hello"), "olleh")
        self.assertEqual(self.string_utils.reverse_string(""), "")
        self.assertEqual(self.string_utils.reverse_string("a"), "a")

    def test_count_vowels(self):
        self.assertEqual(self.string_utils.count_vowels("hello"), 2)
        self.assertEqual(self.string_utils.count_vowels("AEIOU"), 5)
        self.assertEqual(self.string_utils.count_vowels("xyz"), 0)

    def test_is_palindrome(self):
        result = self.string_utils.is_palindrome("164461")
        self.assertTrue(result)

class TestListUtils(unittest.TestCase):
    def setUp(self):
        self.list_utils = ListUtils()

    def test_find_max(self):
        self.assertEqual(self.list_utils.find_max([1, 2, 3, 4, 5]), 5)
        self.assertEqual(self.list_utils.find_max([-5, -2, -10]), -2)
        self.assertIsNone(self.list_utils.find_max([]))

    def test_find_min(self):
        self.assertEqual(self.list_utils.find_min([1, 2, 3, 4, 5]), 1)
        self.assertEqual(self.list_utils.find_min([-5, -2, -10]), -10)
        self.assertIsNone(self.list_utils.find_min([]))

    def test_calculate_average(self):
        self.assertEqual(self.list_utils.calculate_average([]),None)
        self.assertEqual(self.list_utils.calculate_average([1,3,2]),2)