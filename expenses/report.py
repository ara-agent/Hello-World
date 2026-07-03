"""Plain-text report rendering."""

from __future__ import annotations


def render_monthly_report(month: str, totals_by_category: dict[str, int]) -> str:
    """Render an aligned monthly category total table."""

    rows = [(category, amount) for category, amount in sorted(totals_by_category.items())]
    total = sum(amount for _, amount in rows)

    category_width = max([len("Category"), *(len(category) for category, _ in rows), len("Total")])
    amount_width = max([len("Amount"), *(len(_format_cents(amount)) for _, amount in rows), len(_format_cents(total))])

    lines = [
        f"Expense report for {month}",
        f"{'Category':<{category_width}}  {'Amount':>{amount_width}}",
        f"{'-' * category_width}  {'-' * amount_width}",
    ]
    lines.extend(
        f"{category:<{category_width}}  {_format_cents(amount):>{amount_width}}"
        for category, amount in rows
    )
    lines.append(f"{'-' * category_width}  {'-' * amount_width}")
    lines.append(f"{'Total':<{category_width}}  {_format_cents(total):>{amount_width}}")
    return "\n".join(lines)


def _format_cents(cents: int) -> str:
    sign = "-" if cents < 0 else ""
    cents = abs(cents)
    return f"{sign}${cents // 100}.{cents % 100:02d}"
