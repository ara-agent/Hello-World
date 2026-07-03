"""Expense domain model and validation helpers."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from typing import Any
from uuid import uuid4


@dataclass(frozen=True, slots=True)
class Expense:
    """A single expense stored in integer cents."""

    amount_cents: int
    category: str
    date: str
    note: str = ""
    id: str | None = None

    def __post_init__(self) -> None:
        if not isinstance(self.amount_cents, int) or isinstance(self.amount_cents, bool):
            raise ValueError("amount_cents must be an integer number of cents")
        if self.amount_cents <= 0:
            raise ValueError("amount_cents must be greater than zero")

        category = _clean_text(self.category, "category", required=True)
        expense_date = _validate_iso_date(self.date)
        note = _clean_text(self.note, "note", required=False)

        expense_id = self.id
        if expense_id is None:
            expense_id = uuid4().hex
        expense_id = _clean_text(expense_id, "id", required=True)

        object.__setattr__(self, "category", category)
        object.__setattr__(self, "date", expense_date)
        object.__setattr__(self, "note", note)
        object.__setattr__(self, "id", expense_id)

    @property
    def month(self) -> str:
        return self.date[:7]

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "amount_cents": self.amount_cents,
            "category": self.category,
            "date": self.date,
            "note": self.note,
        }

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Expense":
        if not isinstance(data, dict):
            raise ValueError("expense must be an object")
        try:
            return cls(
                id=data["id"],
                amount_cents=data["amount_cents"],
                category=data["category"],
                date=data["date"],
                note=data.get("note", ""),
            )
        except KeyError as exc:
            raise ValueError(f"expense is missing required field: {exc.args[0]}") from exc


def _clean_text(value: Any, field: str, *, required: bool) -> str:
    if not isinstance(value, str):
        raise ValueError(f"{field} must be a string")
    cleaned = value.strip()
    if required and not cleaned:
        raise ValueError(f"{field} must not be empty")
    return cleaned


def _validate_iso_date(value: Any) -> str:
    if not isinstance(value, str):
        raise ValueError("date must be a string in YYYY-MM-DD format")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError("date must be a valid ISO date in YYYY-MM-DD format") from exc
    return parsed.isoformat()
