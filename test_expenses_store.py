import json
import os
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from expenses.models import Expense
from expenses.store import ExpenseStore


class ExpenseStoreTests(unittest.TestCase):
    def setUp(self):
        self.tempdir = tempfile.TemporaryDirectory()
        self.path = Path(self.tempdir.name) / "expenses.json"
        self.store = ExpenseStore(self.path)

    def tearDown(self):
        self.tempdir.cleanup()

    def test_add_list_and_remove(self):
        expense = self.store.add(Expense(1200, "food", "2026-07-02", "lunch", id="e1"))

        self.assertEqual(self.store.list(), [expense])
        removed = self.store.remove("e1")

        self.assertEqual(removed, expense)
        self.assertEqual(self.store.list(), [])

    def test_remove_unknown_id_raises_key_error(self):
        with self.assertRaises(KeyError):
            self.store.remove("missing")

    def test_filters_by_category_and_inclusive_date_range(self):
        self.store.add(Expense(100, "food", "2026-07-01", id="a"))
        self.store.add(Expense(200, "food", "2026-07-31", id="b"))
        self.store.add(Expense(300, "travel", "2026-07-15", id="c"))
        self.store.add(Expense(400, "food", "2026-08-01", id="d"))

        found = self.store.list(category="food", start_date="2026-07-01", end_date="2026-07-31")

        self.assertEqual([expense.id for expense in found], ["a", "b"])

    def test_rejects_blank_category_filters(self):
        for category in ("", "   "):
            with self.subTest(category=category):
                with self.assertRaisesRegex(ValueError, "category filter must not be empty"):
                    self.store.list(category=category)

    def test_rejects_non_string_category_filter(self):
        with self.assertRaisesRegex(ValueError, "category filter must be a string"):
            self.store.list(category=123)

    def test_rejects_inverted_date_range(self):
        with self.assertRaises(ValueError):
            self.store.list(start_date="2026-08-01", end_date="2026-07-01")

    def test_monthly_totals_by_category(self):
        self.store.add(Expense(100, "food", "2026-07-01", id="a"))
        self.store.add(Expense(250, "food", "2026-07-31", id="b"))
        self.store.add(Expense(400, "travel", "2026-07-15", id="c"))
        self.store.add(Expense(999, "food", "2026-08-01", id="d"))

        self.assertEqual(
            self.store.monthly_totals_by_category("2026-07"),
            {"food": 350, "travel": 400},
        )

    def test_empty_month_returns_empty_totals(self):
        self.store.add(Expense(100, "food", "2026-06-30", id="a"))

        self.assertEqual(self.store.monthly_totals_by_category("2026-07"), {})

    def test_corrupt_store_is_moved_aside_and_recovers_empty(self):
        self.path.write_text("{not json", encoding="utf-8")

        self.assertEqual(self.store.list(), [])
        self.assertFalse(self.path.exists())
        self.assertEqual(self.path.with_suffix(".json.corrupt").read_text(encoding="utf-8"), "{not json")

        self.store.add(Expense(100, "food", "2026-07-02", id="new"))
        self.assertEqual([expense.id for expense in self.store.list()], ["new"])

    def test_invalid_store_shape_is_moved_aside(self):
        self.path.write_text(json.dumps({"expenses": [{"id": "bad"}]}), encoding="utf-8")

        self.assertEqual(self.store.list(), [])
        self.assertTrue(self.path.with_suffix(".json.corrupt").exists())

    def test_atomic_write_removes_temp_file_on_failure(self):
        with mock.patch("expenses.store.os.replace", side_effect=OSError("boom")):
            with self.assertRaises(OSError):
                self.store.add(Expense(100, "food", "2026-07-02", id="x"))

        leftovers = [name for name in os.listdir(self.tempdir.name) if name.endswith(".tmp")]
        self.assertEqual(leftovers, [])


if __name__ == "__main__":
    unittest.main()
