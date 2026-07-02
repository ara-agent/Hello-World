import unittest

from rle import decode, encode


class RunLengthEncodingTests(unittest.TestCase):
    def test_empty_string(self):
        self.assertEqual(encode(""), "")
        self.assertEqual(decode(""), "")

    def test_known_encoding_escapes_digits(self):
        self.assertEqual(encode("111aa"), "3:31;2:61;")
        self.assertEqual(decode("3:31;2:61;"), "111aa")

    def test_round_trip_edge_cases(self):
        samples = [
            "a",
            "aaabccccaa",
            "012233344445",
            ":::;;;;",
            "a1b22c333",
            "hello\nhello",
            "😀😀xx😀",
        ]

        for sample in samples:
            with self.subTest(sample=sample):
                self.assertEqual(decode(encode(sample)), sample)

    def test_decode_rejects_malformed_data(self):
        for encoded in ["1", "x:61;", "1:;", "1:zz;", "1:61"]:
            with self.subTest(encoded=encoded):
                with self.assertRaises(ValueError):
                    decode(encoded)


if __name__ == "__main__":
    unittest.main()
