import unittest

from statistics_utils import mean, median


class StatisticsUtilsTest(unittest.TestCase):
    def test_mean_returns_average(self):
        self.assertEqual(mean([1, 2, 3, 4]), 2.5)

    def test_mean_rejects_empty_values(self):
        with self.assertRaises(ValueError):
            mean([])

    def test_median_returns_middle_value_for_odd_count(self):
        self.assertEqual(median([3, 1, 2]), 2)

    def test_median_returns_average_for_even_count(self):
        self.assertEqual(median([4, 1, 2, 3]), 2.5)

    def test_median_rejects_empty_values(self):
        with self.assertRaises(ValueError):
            median([])


if __name__ == "__main__":
    unittest.main()
