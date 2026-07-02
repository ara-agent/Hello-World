#!/usr/bin/env python3
"""Count the most common words in a text file."""

from __future__ import annotations

import argparse
import re
import sys
from collections import Counter
from pathlib import Path


WORD_RE = re.compile(r"[A-Za-z0-9']+")


def extract_words(text: str) -> list[str]:
    """Return normalized words from text."""
    return [match.group(0).lower() for match in WORD_RE.finditer(text)]


def top_words(text: str, limit: int) -> list[tuple[str, int]]:
    counts = Counter(extract_words(text))
    return sorted(counts.items(), key=lambda item: (-item[1], item[0]))[:limit]


def read_input(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError as exc:
        raise ValueError(f"error: file not found: {path}") from exc
    except IsADirectoryError as exc:
        raise ValueError(f"error: expected a file, got directory: {path}") from exc
    except OSError as exc:
        raise ValueError(f"error: could not read {path}: {exc.strerror}") from exc


def positive_int(value: str) -> int:
    try:
        parsed = int(value)
    except ValueError as exc:
        raise argparse.ArgumentTypeError("--top must be a positive integer") from exc
    if parsed < 1:
        raise argparse.ArgumentTypeError("--top must be a positive integer")
    return parsed


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Print the most common words in a file.")
    parser.add_argument("path", help="file to count words from")
    parser.add_argument(
        "--top",
        metavar="N",
        type=positive_int,
        default=10,
        help="number of words to print (default: 10)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        text = read_input(Path(args.path))
    except ValueError as exc:
        print(exc, file=sys.stderr)
        return 1

    results = top_words(text, args.top)
    if not results:
        print(f"error: no words found in {args.path}", file=sys.stderr)
        return 1

    for word, count in results:
        print(f"{word} {count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
