"""Command-line interface for the expense tracker."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from expenses.models import Expense
from expenses.report import render_monthly_report
from expenses.store import ExpenseStore

DEFAULT_STORE = Path.home() / ".expenses.json"


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track expenses in a JSON file.")
    parser.add_argument("--store", default=str(DEFAULT_STORE), help="path to the JSON expense store")
    subparsers = parser.add_subparsers(dest="command", required=True)

    add = subparsers.add_parser("add", help="add an expense")
    add.add_argument("amount", help="amount in dollars, for example 12.34")
    add.add_argument("category", help="expense category")
    add.add_argument("date", help="expense date in YYYY-MM-DD format")
    add.add_argument("note", nargs="?", default="", help="optional note")
    add.set_defaults(func=_cmd_add)

    rm = subparsers.add_parser("rm", help="remove an expense by id")
    rm.add_argument("id", help="expense id")
    rm.set_defaults(func=_cmd_rm)

    ls = subparsers.add_parser("ls", help="list expenses")
    ls.add_argument("--category", help="filter by category")
    ls.add_argument("--start-date", help="inclusive start date in YYYY-MM-DD format")
    ls.add_argument("--end-date", help="inclusive end date in YYYY-MM-DD format")
    ls.set_defaults(func=_cmd_ls)

    report = subparsers.add_parser("report", help="show monthly totals by category")
    report.add_argument("month", help="month in YYYY-MM format")
    report.set_defaults(func=_cmd_report)
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    store = ExpenseStore(args.store)
    try:
        args.func(args, store)
    except KeyError as exc:
        parser.exit(1, f"error: {exc.args[0]}\n")
    except (ValueError, OSError) as exc:
        parser.exit(1, f"error: {exc}\n")
    return 0


def _cmd_add(args: argparse.Namespace, store: ExpenseStore) -> None:
    expense = store.add(
        Expense(
            amount_cents=_parse_amount(args.amount),
            category=args.category,
            date=args.date,
            note=args.note,
        )
    )
    print(f"added {expense.id}")


def _cmd_rm(args: argparse.Namespace, store: ExpenseStore) -> None:
    removed = store.remove(args.id)
    print(f"removed {removed.id}")


def _cmd_ls(args: argparse.Namespace, store: ExpenseStore) -> None:
    for expense in store.list(
        category=args.category,
        start_date=args.start_date,
        end_date=args.end_date,
    ):
        print(
            f"{expense.id}  {expense.date}  {expense.category}  "
            f"{_format_cents(expense.amount_cents)}  {expense.note}"
        )


def _cmd_report(args: argparse.Namespace, store: ExpenseStore) -> None:
    print(render_monthly_report(args.month, store.monthly_totals_by_category(args.month)))


def _parse_amount(value: str) -> int:
    if not isinstance(value, str) or not value.strip():
        raise ValueError("amount must not be empty")
    raw = value.strip()
    if raw.startswith("$"):
        raw = raw[1:]
    if raw.startswith("-"):
        raise ValueError("amount must be greater than zero")
    whole, dot, fraction = raw.partition(".")
    if not whole.isdigit() or (dot and (not fraction.isdigit() or len(fraction) > 2)):
        raise ValueError("amount must be dollars with up to two decimal places")
    if not dot:
        fraction = "0"
    cents = int(whole) * 100 + int(fraction.ljust(2, "0"))
    if cents <= 0:
        raise ValueError("amount must be greater than zero")
    return cents


def _format_cents(cents: int) -> str:
    return f"${cents // 100}.{cents % 100:02d}"


if __name__ == "__main__":
    sys.exit(main())
