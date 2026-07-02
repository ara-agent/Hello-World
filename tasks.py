"""Small JSON-backed task list library."""

from __future__ import annotations

import json
import os
import tempfile
from pathlib import Path
from typing import Any


class TaskList:
    """Manage tasks persisted to a JSON file."""

    def __init__(self, path: str | os.PathLike[str]) -> None:
        self.path = Path(path)
        self._tasks = self._load()

    def add(self, title: str) -> dict[str, Any]:
        title = title.strip()
        if not title:
            raise ValueError("task title cannot be empty")

        task = {"id": self._next_id(), "title": title, "done": False}
        self._tasks.append(task)
        self._save()
        return dict(task)

    def complete(self, task_id: int) -> dict[str, Any]:
        task = self._find(task_id)
        task["done"] = True
        self._save()
        return dict(task)

    def remove(self, task_id: int) -> dict[str, Any]:
        for index, task in enumerate(self._tasks):
            if task["id"] == task_id:
                removed = self._tasks.pop(index)
                self._save()
                return dict(removed)
        raise KeyError(f"task id {task_id} not found")

    def list_pending(self) -> list[dict[str, Any]]:
        return [dict(task) for task in self._tasks if not task["done"]]

    def list_done(self) -> list[dict[str, Any]]:
        return [dict(task) for task in self._tasks if task["done"]]

    def _load(self) -> list[dict[str, Any]]:
        try:
            raw = json.loads(self.path.read_text(encoding="utf-8"))
        except FileNotFoundError:
            return []
        except (json.JSONDecodeError, OSError):
            return []

        if not isinstance(raw, list):
            return []

        tasks: list[dict[str, Any]] = []
        for item in raw:
            if not isinstance(item, dict):
                continue
            task_id = item.get("id")
            title = item.get("title")
            done = item.get("done")
            if isinstance(task_id, int) and isinstance(title, str) and isinstance(done, bool):
                tasks.append({"id": task_id, "title": title, "done": done})
        return tasks

    def _save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        fd, temp_name = tempfile.mkstemp(
            prefix=f".{self.path.name}.",
            suffix=".tmp",
            dir=self.path.parent,
            text=True,
        )
        try:
            with os.fdopen(fd, "w", encoding="utf-8") as temp_file:
                json.dump(self._tasks, temp_file, indent=2)
                temp_file.write("\n")
                temp_file.flush()
                os.fsync(temp_file.fileno())
            os.replace(temp_name, self.path)
        except Exception:
            try:
                os.unlink(temp_name)
            except FileNotFoundError:
                pass
            raise

    def _find(self, task_id: int) -> dict[str, Any]:
        for task in self._tasks:
            if task["id"] == task_id:
                return task
        raise KeyError(f"task id {task_id} not found")

    def _next_id(self) -> int:
        if not self._tasks:
            return 1
        return max(task["id"] for task in self._tasks) + 1
