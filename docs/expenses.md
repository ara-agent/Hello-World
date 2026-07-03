# Expense tracker

This repository includes a small standard-library expense tracker.

## Add an expense

```sh
python3 expensecli.py --store expenses.json add 12.50 food 2026-07-02 "lunch"
```

The command prints the generated expense id.

## List expenses

```sh
python3 expensecli.py --store expenses.json ls
python3 expensecli.py --store expenses.json ls --category food
python3 expensecli.py --store expenses.json ls --start-date 2026-07-01 --end-date 2026-07-31
```

## Remove an expense

```sh
python3 expensecli.py --store expenses.json rm 4f516bc597314571837958ed4a3ad442
```

## Monthly report

```sh
python3 expensecli.py --store expenses.json report 2026-07
```

Example output:

```text
Expense report for 2026-07
Category  Amount
--------  ------
food      $12.50
travel    $33.00
--------  ------
Total     $45.50
```

The store is written atomically. If a corrupt JSON store is encountered, it is moved aside with a `.corrupt` suffix and the tracker starts from an empty store.
