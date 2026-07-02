import unittest

from expenses.report import render_monthly_report


class ExpenseReportTests(unittest.TestCase):
    def test_renders_aligned_monthly_report_with_total(self):
        report = render_monthly_report("2026-07", {"food": 1250, "transport": 345})

        self.assertEqual(
            report,
            "\n".join(
                [
                    "Expense report for 2026-07",
                    "Category   Amount",
                    "---------  ------",
                    "food       $12.50",
                    "transport   $3.45",
                    "---------  ------",
                    "Total      $15.95",
                ]
            ),
        )

    def test_renders_empty_month_with_zero_total(self):
        report = render_monthly_report("2026-07", {})

        self.assertEqual(
            report,
            "\n".join(
                [
                    "Expense report for 2026-07",
                    "Category  Amount",
                    "--------  ------",
                    "--------  ------",
                    "Total      $0.00",
                ]
            ),
        )


if __name__ == "__main__":
    unittest.main()
