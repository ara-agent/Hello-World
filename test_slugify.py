import unittest

from slugify import slugify


class SlugifyTests(unittest.TestCase):
    def test_lowercases_words(self):
        self.assertEqual(slugify("Hello World"), "hello-world")

    def test_collapses_spaces_and_punctuation(self):
        self.assertEqual(slugify("  Hello,   world!!!  "), "hello-world")

    def test_trims_hyphens(self):
        self.assertEqual(slugify("---Hello---World---"), "hello-world")

    def test_normalizes_unicode_to_ascii_where_possible(self):
        self.assertEqual(slugify("Café déjà vu"), "cafe-deja-vu")

    def test_converts_unicode_punctuation_to_hyphens(self):
        self.assertEqual(slugify("Hello—world"), "hello-world")

    def test_drops_unconvertible_unicode(self):
        self.assertEqual(slugify("Hello ☃ World"), "hello-world")

    def test_empty_after_cleanup(self):
        self.assertEqual(slugify("!@#$"), "")


if __name__ == "__main__":
    unittest.main()
