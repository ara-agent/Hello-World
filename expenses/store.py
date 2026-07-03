"""JSON-file-backed expense store."""

from __future__ import annotations

import json
import os
import tempfile
from collections import defaultdict
from datetime import date
from pathlib import Path
from typing import Any, Iterable

from .models import Expense


class ExpenseStore:
    """Persist expenses in a local JSON file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

    def add(self, expense: Expense) -> Expense:
        expenses = self._load()
        if any(existing.id == expense.id for existing in expenses):
            raise ValueError(f"expense id already exists: {expense.id}")
        expenses.append(expense)
        self._save(expenses)
        return expense

    def remove(self, expense_id: str) -> Expense:
        if not isinstance(expense_id, str) or not expense_id.strip():
            raise ValueError("expense id must not be empty")
        expenses = self._load()
        for index, expense in enumerate(expenses):
            if expense.id == expense_id.strip():
                removed = expenses.pop(index)
                self._save(expenses)
                return removed
        raise KeyError(f"expense not found: {expense_id}")

    def list(
        self,
        *,
        category: str | None = None,
        start_date: str | None = None,
        end_date: str | None = None,
    ) -> list[Expense]:
        start = _parse_optional_date(start_date, "start_date")
        end = _parse_optional_date(end_date, "end_date")
        if start and end and start > end:
            raise ValueError("start_date must be on or before end_date")

        wanted_category = _parse_optional_category(category)
        results = []
        for expense in self._load():
            expense_date = date.fromisoformat(expense.date)
            if wanted_category and expense.category != wanted_category:
                continue
            if start and expense_date < start:
                continue
            if end and expense_date > end:
                continue
            results.append(expense)
        return sorted(results, key=lambda expense: (expense.date, expense.category, expense.id))

    def monthly_totals_by_category(self, month: str) -> dict[str, int]:
        _validate_month(month)
        totals: dict[str, int] = defaultdict(int)
        for expense in self.list(start_date=f"{month}-01", end_date=_month_end(month)):
            totals[expense.category] += expense.amount_cents
        return dict(sorted(totals.items()))

    def _load(self) -> list[Expense]:
        if not self.path.exists():
            return []
        try:
            with self.path.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
        except json.JSONDecodeError:
            self._recover_corrupt_store()
            return []

        try:
            raw_expenses = _extract_expenses(data)
            return [Expense.from_dict(item) for item in raw_expenses]
        except ValueError:
            self._recover_corrupt_store()
            return []

    def _save(self, expenses: Iterable[Expense]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        payload = {"expenses": [expense.to_dict() for expense in expenses]}
        fd, tmp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            dir=str(self.path.parent),
            text=True,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as handle:
                json.dump(payload, handle, indent=2, sort_keys=True)
                handle.write("\n")
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(tmp_name, self.path)
        except Exception:
            try:
                os.unlink(tmp_name)
            except FileNotFoundError:
                pass
            raise

    def _recover_corrupt_store(self) -> None:
        if not self.path.exists():
            return
        backup = self.path.with_suffix(f"{self.path.suffix}.corrupt")
        counter = 1
        while backup.exists():
            backup = self.path.with_suffix(f"{self.path.suffix}.corrupt{counter}")
            counter += 1
        os.replace(self.path, backup)


def _extract_expenses(data: Any) -> list[Any]:
    if isinstance(data, list):
        return data
    if isinstance(data, dict) and isinstance(data.get("expenses"), list):
        return data["expenses"]
    raise ValueError("store must contain an expenses list")


def _parse_optional_date(value: str | None, field: str) -> date | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string in YYYY-MM-DD format")
    try:
        return date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"{field} must be a valid ISO date in YYYY-MM-DD format") from exc


def _parse_optional_category(value: str | None) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError("category filter must be a string")
    cleaned = value.strip()
    if not cleaned:
        raise ValueError("category filter must not be empty")
    return cleaned


def _validate_month(month: str) -> None:
    if not isinstance(month, str) or len(month) != 7:
        raise ValueError("month must be in YYYY-MM format")
    try:
        date.fromisoformat(f"{month}-01")
    except ValueError as exc:
        raise ValueError("month must be a valid month in YYYY-MM format") from exc


def _month_end(month: str) -> str:
    year, month_number = [int(part) for part in month.split("-")]
    if month_number == 12:
        next_month = date(year + 1, 1, 1)
    else:
        next_month = date(year, month_number + 1, 1)
    return date.fromordinal(next_month.toordinal() - 1).isoformat()
