import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import wordcount


class WordCountTests(unittest.TestCase):
    def test_top_words_counts_case_insensitively(self):
        text = "Hello hello HELLO world, world test."

        self.assertEqual(
            wordcount.top_words(text, 3),
            [("hello", 3), ("world", 2), ("test", 1)],
        )

    def test_top_words_breaks_ties_alphabetically(self):
        text = "banana apple carrot banana carrot apple"

        self.assertEqual(
            wordcount.top_words(text, 3),
            [("apple", 2), ("banana", 2), ("carrot", 2)],
        )

    def test_main_prints_top_words(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "input.txt"
            path.write_text("Beta beta alpha gamma gamma gamma", encoding="utf-8")
            stdout = StringIO()

            with redirect_stdout(stdout):
                exit_code = wordcount.main([str(path), "--top", "2"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stdout.getvalue(), "gamma 3\nbeta 2\n")

    def test_main_reports_missing_file(self):
        stderr = StringIO()

        with redirect_stderr(stderr):
            exit_code = wordcount.main(["does-not-exist.txt"])

        self.assertEqual(exit_code, 1)
        self.assertIn("error: file not found: does-not-exist.txt", stderr.getvalue())

    def test_main_reports_empty_input(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            path = Path(temp_dir) / "empty.txt"
            path.write_text(" \n\t", encoding="utf-8")
            stderr = StringIO()

            with redirect_stderr(stderr):
                exit_code = wordcount.main([str(path)])

        self.assertEqual(exit_code, 1)
        self.assertIn("error: no words found in", stderr.getvalue())

    def test_top_must_be_positive(self):
        stderr = StringIO()

        with self.assertRaises(SystemExit) as raised, redirect_stderr(stderr):
            wordcount.main(["input.txt", "--top", "0"])

        self.assertEqual(raised.exception.code, 2)
        self.assertIn("--top must be a positive integer", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
