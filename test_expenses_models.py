import unittest

from expenses.models import Expense


class ExpenseModelTests(unittest.TestCase):
    def test_valid_expense_normalizes_text_and_generates_id(self):
        expense = Expense(1250, " food ", "2026-07-02", " lunch ")

        self.assertEqual(expense.amount_cents, 1250)
        self.assertEqual(expense.category, "food")
        self.assertEqual(expense.date, "2026-07-02")
        self.assertEqual(expense.note, "lunch")
        self.assertTrue(expense.id)
        self.assertEqual(expense.month, "2026-07")

    def test_rejects_invalid_amounts(self):
        for amount in (0, -1, 1.2, True):
            with self.subTest(amount=amount):
                with self.assertRaises(ValueError):
                    Expense(amount, "food", "2026-07-02")

    def test_rejects_blank_category_and_bad_date(self):
        with self.assertRaises(ValueError):
            Expense(100, " ", "2026-07-02")
        with self.assertRaises(ValueError):
            Expense(100, "food", "2026-02-30")

    def test_round_trips_dict(self):
        expense = Expense.from_dict(
            {
                "id": "abc",
                "amount_cents": 999,
                "category": "books",
                "date": "2026-01-31",
                "note": "paperback",
            }
        )

        self.assertEqual(
            expense.to_dict(),
            {
                "id": "abc",
                "amount_cents": 999,
                "category": "books",
                "date": "2026-01-31",
                "note": "paperback",
            },
        )

    def test_from_dict_requires_required_fields(self):
        with self.assertRaisesRegex(ValueError, "missing required field"):
            Expense.from_dict({"id": "abc"})


if __name__ == "__main__":
    unittest.main()
