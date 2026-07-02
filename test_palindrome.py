import unittest

from palindrome import is_palindrome


class TestIsPalindrome(unittest.TestCase):
    def test_simple_palindrome(self):
        self.assertTrue(is_palindrome("racecar"))

    def test_ignores_case(self):
        self.assertTrue(is_palindrome("RaceCar"))

    def test_ignores_non_alphanumerics(self):
        self.assertTrue(is_palindrome("A man, a plan, a canal: Panama!"))

    def test_digits_are_included(self):
        self.assertTrue(is_palindrome("No. 1, 2, 1 on"))

    def test_not_palindrome(self):
        self.assertFalse(is_palindrome("hello"))

    def test_empty_string(self):
        self.assertTrue(is_palindrome(""))


if __name__ == "__main__":
    unittest.main()
