import unittest

from statistics_utils import mean, median, mode, stdev


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

    def test_mode_returns_most_common_value(self):
        self.assertEqual(mode([1, 2, 2, 3]), 2)

    def test_mode_returns_smallest_value_when_tied(self):
        self.assertEqual(mode([3, 1, 3, 1]), 1)

    def test_mode_rejects_empty_values(self):
        with self.assertRaises(ValueError):
            mode([])

    def test_stdev_returns_sample_standard_deviation(self):
        self.assertAlmostEqual(stdev([2, 4, 4, 4, 5, 5, 7, 9]), 2.138089935)

    def test_stdev_rejects_fewer_than_two_values(self):
        with self.assertRaises(ValueError):
            stdev([1])


if __name__ == "__main__":
    unittest.main()
