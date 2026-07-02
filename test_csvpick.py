import argparse
import io
import os
import tempfile
import unittest

import csvpick


class CsvpickTests(unittest.TestCase):
    def write_temp_csv(self, content):
        temp = tempfile.NamedTemporaryFile("w", delete=False, newline="")
        try:
            temp.write(content)
            return temp.name
        finally:
            temp.close()

    def test_prints_requested_columns(self):
        path = self.write_temp_csv("name,age,city\nAda,36,London\nLinus,54,Helsinki\n")
        self.addCleanup(os.unlink, path)
        output = io.StringIO()

        csvpick.pick_columns(path, ["city", "name"], output)

        self.assertEqual(
            output.getvalue(),
            "city,name\r\nLondon,Ada\r\nHelsinki,Linus\r\n",
        )

    def test_missing_file_has_clear_error(self):
        missing = os.path.join(tempfile.gettempdir(), "csvpick-missing-file.csv")

        with self.assertRaises(SystemExit) as caught:
            csvpick.pick_columns(missing, ["name"], io.StringIO())

        self.assertIn("cannot open", str(caught.exception))
        self.assertIn(missing, str(caught.exception))

    def test_unknown_column_has_clear_error(self):
        path = self.write_temp_csv("name,age\nAda,36\n")
        self.addCleanup(os.unlink, path)

        with self.assertRaises(SystemExit) as caught:
            csvpick.pick_columns(path, ["name", "city"], io.StringIO())

        self.assertEqual("error: unknown column(s): city", str(caught.exception))

    def test_parse_columns_rejects_empty_list(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            csvpick.parse_columns(" , ")


if __name__ == "__main__":
    unittest.main()
