"""Command line interface for the task tracker."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path
from typing import Sequence

from tasks import TaskList


DEFAULT_PATH = Path(os.environ.get("TASKS_FILE", "~/.tasks.json")).expanduser()


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Track small tasks in a JSON file.")
    parser.add_argument(
        "--file",
        default=str(DEFAULT_PATH),
        help=f"task JSON file (default: {DEFAULT_PATH})",
    )
    subparsers = parser.add_subparsers(dest="command", required=True)

    add_parser = subparsers.add_parser("add", help="add a pending task")
    add_parser.add_argument("title", nargs="+", help="task title")

    done_parser = subparsers.add_parser("done", help="mark a task complete")
    done_parser.add_argument("id", type=int, help="task id")

    rm_parser = subparsers.add_parser("rm", help="remove a task")
    rm_parser.add_argument("id", type=int, help="task id")

    ls_parser = subparsers.add_parser("ls", help="list tasks")
    ls_parser.add_argument(
        "--done",
        action="store_true",
        help="list completed tasks instead of pending tasks",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    task_list = TaskList(args.file)

    try:
        if args.command == "add":
            task = task_list.add(" ".join(args.title))
            print(f"Added task {task['id']}: {task['title']}")
            return 0
        if args.command == "done":
            task = task_list.complete(args.id)
            print(f"Completed task {task['id']}: {task['title']}")
            return 0
        if args.command == "rm":
            task = task_list.remove(args.id)
            print(f"Removed task {task['id']}: {task['title']}")
            return 0
        if args.command == "ls":
            tasks = task_list.list_done() if args.done else task_list.list_pending()
            for task in tasks:
                status = "done" if task["done"] else "pending"
                print(f"{task['id']}\t{status}\t{task['title']}")
            return 0
    except (KeyError, ValueError) as exc:
        message = exc.args[0] if exc.args else str(exc)
        print(f"error: {message}", file=sys.stderr)
        return 1

    parser.error(f"unknown command: {args.command}")
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
