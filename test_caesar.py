import unittest

from caesar import decrypt, encrypt


class CaesarTest(unittest.TestCase):
    def test_encrypt_preserves_case_and_non_letters(self):
        self.assertEqual(encrypt("Hello, World! 123", 3), "Khoor, Zruog! 123")

    def test_decrypt_reverses_encrypt(self):
        self.assertEqual(decrypt("Khoor, Zruog! 123", 3), "Hello, World! 123")

    def test_wraps_alphabet(self):
        self.assertEqual(encrypt("xyz XYZ", 4), "bcd BCD")

    def test_negative_shift(self):
        self.assertEqual(encrypt("abc ABC", -1), "zab ZAB")

    def test_large_shift(self):
        self.assertEqual(encrypt("abc ABC", 29), "def DEF")

    def test_round_trips(self):
        samples = [
            "",
            "Attack at Dawn!",
            "Zebra-493",
            "Mixed CASE with punctuation.",
        ]

        for sample in samples:
            for shift in range(-52, 53):
                with self.subTest(sample=sample, shift=shift):
                    self.assertEqual(decrypt(encrypt(sample, shift), shift), sample)


if __name__ == "__main__":
    unittest.main()
