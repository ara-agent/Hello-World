import contextlib
import io
import tempfile
import unittest
from pathlib import Path

import expensecli


class ExpenseCliTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.store = Path(self.tempdir.name) / "expenses.json"

    def tearDown(self):
        self.tempdir.cleanup()

    def run_cli(self, *args):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            code = expensecli.main(["--store", str(self.store), *args])
        return code, stdout.getvalue(), stderr.getvalue()

    def test_add_ls_report_and_remove_flow(self):
        code, out, err = self.run_cli("add", "12.50", "food", "2026-07-02", "lunch")
        self.assertEqual((code, err), (0, ""))
        expense_id = out.strip().removeprefix("added ")
        self.assertTrue(expense_id)

        code, out, err = self.run_cli("ls", "--category", "food", "--start-date", "2026-07-01", "--end-date", "2026-07-31")
        self.assertEqual(code, 0)
        self.assertIn(expense_id, out)
        self.assertIn("$12.50", out)
        self.assertEqual(err, "")

        code, out, err = self.run_cli("report", "2026-07")
        self.assertEqual(code, 0)
        self.assertIn("food      $12.50", out)
        self.assertIn("Total     $12.50", out)
        self.assertEqual(err, "")

        code, out, err = self.run_cli("rm", expense_id)
        self.assertEqual((code, out.strip(), err), (0, f"removed {expense_id}", ""))

    def test_ls_filter_edge_returns_no_rows(self):
        self.run_cli("add", "1.00", "food", "2026-07-02")

        code, out, err = self.run_cli("ls", "--category", "travel")

        self.assertEqual((code, out, err), (0, "", ""))

    def test_invalid_amount_has_clear_error(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as caught:
                expensecli.main(["--store", str(self.store), "add", "1.234", "food", "2026-07-02"])

        self.assertEqual(caught.exception.code, 1)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn("error: amount must be dollars with up to two decimal places", stderr.getvalue())

    def test_remove_missing_has_clear_error(self):
        stdout = io.StringIO()
        stderr = io.StringIO()
        with contextlib.redirect_stdout(stdout), contextlib.redirect_stderr(stderr):
            with self.assertRaises(SystemExit) as caught:
                expensecli.main(["--store", str(self.store), "rm", "missing"])

        self.assertEqual(caught.exception.code, 1)
        self.assertIn("error: expense not found: missing", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
