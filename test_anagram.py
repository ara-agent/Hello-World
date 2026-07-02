import unittest

from anagram import are_anagrams


class AreAnagramsTest(unittest.TestCase):
    def test_matches_simple_anagrams(self):
        self.assertTrue(are_anagrams("listen", "silent"))

    def test_ignores_case(self):
        self.assertTrue(are_anagrams("Dormitory", "Dirtyroom"))

    def test_ignores_whitespace(self):
        self.assertTrue(are_anagrams("conversation", "voices rant on"))

    def test_rejects_non_anagrams(self):
        self.assertFalse(are_anagrams("hello", "world"))


if __name__ == "__main__":
    unittest.main()
