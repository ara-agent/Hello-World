#!/usr/bin/env python3
"""Print selected columns from a CSV file."""

import argparse
import csv
import sys


def parse_columns(value):
    columns = [column.strip() for column in value.split(",") if column.strip()]
    if not columns:
        raise argparse.ArgumentTypeError("at least one column is required")
    return columns


def pick_columns(path, columns, output):
    try:
        csv_file = open(path, newline="")
    except OSError as error:
        raise SystemExit(f"error: cannot open '{path}': {error.strerror}") from error

    with csv_file:
        reader = csv.DictReader(csv_file)
        if reader.fieldnames is None:
            raise SystemExit(f"error: '{path}' has no header row")

        unknown = [column for column in columns if column not in reader.fieldnames]
        if unknown:
            names = ", ".join(unknown)
            raise SystemExit(f"error: unknown column(s): {names}")

        writer = csv.DictWriter(output, fieldnames=columns, extrasaction="ignore")
        writer.writeheader()
        for row in reader:
            writer.writerow(row)


def main(argv=None):
    parser = argparse.ArgumentParser(
        description="Print selected columns from a CSV file."
    )
    parser.add_argument("csvfile", help="CSV file to read")
    parser.add_argument(
        "columns",
        type=parse_columns,
        help="comma-separated column names to print",
    )
    args = parser.parse_args(argv)

    pick_columns(args.csvfile, args.columns, sys.stdout)


if __name__ == "__main__":
    main()
