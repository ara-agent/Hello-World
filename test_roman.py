import unittest

from roman import int_to_roman


class IntToRomanTest(unittest.TestCase):
    def test_edge_values(self):
        self.assertEqual(int_to_roman(1), "I")
        self.assertEqual(int_to_roman(3999), "MMMCMXCIX")

    def test_subtractive_notation(self):
        cases = {
            4: "IV",
            9: "IX",
            40: "XL",
            90: "XC",
            400: "CD",
            900: "CM",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(int_to_roman(value), expected)

    def test_representative_values(self):
        cases = {
            3: "III",
            58: "LVIII",
            1994: "MCMXCIV",
            2026: "MMXXVI",
            3888: "MMMDCCCLXXXVIII",
        }
        for value, expected in cases.items():
            with self.subTest(value=value):
                self.assertEqual(int_to_roman(value), expected)

    def test_out_of_range_values_raise_value_error(self):
        for value in (0, -1, 4000, 10000):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    int_to_roman(value)

    def test_non_integer_values_raise_value_error(self):
        for value in (True, 1.5, "10", None):
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    int_to_roman(value)


if __name__ == "__main__":
    unittest.main()
