"""Schema node type definitions supported by jsonval."""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

JSONTypeName = Literal[
    "object",
    "array",
    "string",
    "number",
    "integer",
    "boolean",
    "null",
]


@dataclass(frozen=True)
class SchemaNode:
    """Typed representation of the schema keywords jsonval understands."""

    type: JSONTypeName | None = None
    properties: dict[str, "Schema"] = field(default_factory=dict)
    required: list[str] = field(default_factory=list)
    items: "Schema | None" = None
    enum: list[Any] | None = None
    minimum: int | float | None = None
    maximum: int | float | None = None
    minLength: int | None = None
    maxLength: int | None = None
    pattern: str | None = None


Schema = dict[str, Any] | SchemaNode
