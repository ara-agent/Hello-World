"""Command-line interface for jsonval."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .validate import validate


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Validate a JSON instance against a small schema.")
    parser.add_argument("schema_file", help="Path to the JSON schema file")
    parser.add_argument("instance_file", help="Path to the JSON instance file")
    args = parser.parse_args(argv)

    try:
        schema = _load_json(args.schema_file)
        instance = _load_json(args.instance_file)
    except (OSError, json.JSONDecodeError) as exc:
        print(f"jsonval: {exc}", file=sys.stderr)
        return 2

    errors = validate(instance, schema)
    if errors:
        for error in errors:
            print(error)
        return 1

    return 0


def _load_json(path: str) -> object:
    with Path(path).open(encoding="utf-8") as handle:
        return json.load(handle)


if __name__ == "__main__":
    raise SystemExit(main())
