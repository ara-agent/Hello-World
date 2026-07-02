"""Provide a tiny JSON-backed key-value store."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any


class KeyValueStore:
    """Store key-value pairs in memory and persist them to a JSON file."""

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)
        self._data: dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def delete(self, key: str) -> bool:
        if key not in self._data:
            return False
        del self._data[key]
        return True

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("w", encoding="utf-8") as file:
            json.dump(self._data, file)

    def load(self) -> None:
        if not self.path.exists():
            self._data = {}
            return

        with self.path.open("r", encoding="utf-8") as file:
            data = json.load(file)

        if not isinstance(data, dict):
            raise ValueError("key-value store JSON must contain an object")

        self._data = data
