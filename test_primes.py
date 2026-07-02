import unittest

from primes import is_prime


class IsPrimeTests(unittest.TestCase):
    def test_rejects_numbers_less_than_two(self):
        for value in (-10, -1, 0, 1):
            with self.subTest(value=value):
                self.assertFalse(is_prime(value))

    def test_identifies_prime_numbers(self):
        for value in (2, 3, 5, 17, 97):
            with self.subTest(value=value):
                self.assertTrue(is_prime(value))

    def test_rejects_composite_numbers(self):
        for value in (4, 6, 9, 25, 49, 100):
            with self.subTest(value=value):
                self.assertFalse(is_prime(value))


if __name__ == "__main__":
    unittest.main()
