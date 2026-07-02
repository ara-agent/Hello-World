"""Validation logic for jsonval."""

from __future__ import annotations

import re
from typing import Any

from .types import SchemaNode

VALID_TYPES = {"object", "array", "string", "number", "integer", "boolean", "null"}


def validate(instance: Any, schema: dict[str, Any] | SchemaNode) -> list[str]:
    """Return a list of validation error strings for instance against schema."""

    return _validate(instance, _schema_dict(schema), "")


def _validate(instance: Any, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []

    if "enum" in schema and not _in_enum(instance, schema["enum"]):
        errors.append(f"{_display_path(path)}: value not in enum")

    expected_type = schema.get("type")
    if expected_type is not None:
        if expected_type not in VALID_TYPES:
            errors.append(f"{_display_path(path)}: unsupported schema type {expected_type!r}")
        elif not _matches_type(instance, expected_type):
            errors.append(f"{_display_path(path)}: expected {expected_type}")
            return errors

    if isinstance(instance, dict):
        errors.extend(_validate_object(instance, schema, path))

    if isinstance(instance, list):
        errors.extend(_validate_array(instance, schema, path))

    if isinstance(instance, str):
        errors.extend(_validate_string(instance, schema, path))

    if _is_number(instance):
        errors.extend(_validate_number(instance, schema, path))

    return errors


def _validate_object(instance: dict[str, Any], schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []

    required = schema.get("required", [])
    for prop in required:
        if prop not in instance:
            errors.append(f"{_display_path(_join_path(path, str(prop)))}: required property missing")

    properties = schema.get("properties", {})
    for prop, prop_schema in properties.items():
        if prop in instance:
            errors.extend(_validate(instance[prop], _schema_dict(prop_schema), _join_path(path, prop)))

    return errors


def _validate_array(instance: list[Any], schema: dict[str, Any], path: str) -> list[str]:
    item_schema = schema.get("items")
    if item_schema is None:
        return []

    errors: list[str] = []
    schema_dict = _schema_dict(item_schema)
    for index, item in enumerate(instance):
        errors.extend(_validate(item, schema_dict, _join_path(path, str(index))))
    return errors


def _validate_string(instance: str, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []

    min_length = schema.get("minLength")
    if min_length is not None and len(instance) < min_length:
        errors.append(f"{_display_path(path)}: length less than minLength {min_length}")

    max_length = schema.get("maxLength")
    if max_length is not None and len(instance) > max_length:
        errors.append(f"{_display_path(path)}: length greater than maxLength {max_length}")

    pattern = schema.get("pattern")
    if pattern is not None:
        try:
            matches = re.search(pattern, instance) is not None
        except re.error as exc:
            errors.append(f"{_display_path(path)}: invalid pattern {pattern!r}: {exc}")
        else:
            if not matches:
                errors.append(f"{_display_path(path)}: does not match pattern {pattern!r}")

    return errors


def _validate_number(instance: int | float, schema: dict[str, Any], path: str) -> list[str]:
    errors: list[str] = []

    minimum = schema.get("minimum")
    if minimum is not None and instance < minimum:
        errors.append(f"{_display_path(path)}: value less than minimum {minimum}")

    maximum = schema.get("maximum")
    if maximum is not None and instance > maximum:
        errors.append(f"{_display_path(path)}: value greater than maximum {maximum}")

    return errors


def _schema_dict(schema: dict[str, Any] | SchemaNode) -> dict[str, Any]:
    if isinstance(schema, dict):
        return schema
    if isinstance(schema, SchemaNode):
        result: dict[str, Any] = {}
        for key, value in schema.__dict__.items():
            if value in (None, [], {}):
                continue
            if key == "properties":
                result[key] = {name: _schema_dict(child) for name, child in value.items()}
            elif key == "items":
                result[key] = _schema_dict(value)
            else:
                result[key] = value
        return result
    raise TypeError("schema must be a dict or SchemaNode")


def _matches_type(instance: Any, expected_type: str) -> bool:
    if expected_type == "object":
        return isinstance(instance, dict)
    if expected_type == "array":
        return isinstance(instance, list)
    if expected_type == "string":
        return isinstance(instance, str)
    if expected_type == "number":
        return _is_number(instance)
    if expected_type == "integer":
        return isinstance(instance, int) and not isinstance(instance, bool)
    if expected_type == "boolean":
        return isinstance(instance, bool)
    if expected_type == "null":
        return instance is None
    return False


def _is_number(instance: Any) -> bool:
    return isinstance(instance, (int, float)) and not isinstance(instance, bool)


def _in_enum(instance: Any, enum_values: Any) -> bool:
    if not isinstance(enum_values, list):
        return False
    return any(_json_equal(instance, value) for value in enum_values)


def _json_equal(left: Any, right: Any) -> bool:
    if isinstance(left, bool) or isinstance(right, bool):
        return isinstance(left, bool) and isinstance(right, bool) and left == right
    if _is_number(left) and _is_number(right):
        return left == right
    if type(left) is not type(right):
        return False
    if isinstance(left, list):
        return len(left) == len(right) and all(_json_equal(a, b) for a, b in zip(left, right))
    if isinstance(left, dict):
        return left.keys() == right.keys() and all(_json_equal(left[key], right[key]) for key in left)
    return left == right


def _join_path(path: str, token: str) -> str:
    escaped = token.replace("~", "~0").replace("/", "~1")
    return f"{path}/{escaped}" if path else f"/{escaped}"


def _display_path(path: str) -> str:
    return path or "/"
