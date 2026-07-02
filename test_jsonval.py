import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

from jsonval import validate
from jsonval.types import SchemaNode


class ValidateTests(unittest.TestCase):
    def test_object_type_valid_and_invalid(self):
        self.assertEqual(validate({"name": "Ada"}, {"type": "object"}), [])
        self.assertEqual(validate([], {"type": "object"}), ["/: expected object"])

    def test_array_type_valid_and_invalid(self):
        self.assertEqual(validate([1, 2], {"type": "array"}), [])
        self.assertEqual(validate({}, {"type": "array"}), ["/: expected array"])

    def test_string_type_valid_and_invalid(self):
        self.assertEqual(validate("ok", {"type": "string"}), [])
        self.assertEqual(validate(12, {"type": "string"}), ["/: expected string"])

    def test_number_type_valid_and_invalid(self):
        self.assertEqual(validate(1.5, {"type": "number"}), [])
        self.assertEqual(validate(True, {"type": "number"}), ["/: expected number"])

    def test_integer_type_valid_and_invalid(self):
        self.assertEqual(validate(2, {"type": "integer"}), [])
        self.assertEqual(validate(2.0, {"type": "integer"}), [])
        self.assertEqual(validate(2.5, {"type": "integer"}), ["/: expected integer"])

    def test_boolean_type_valid_and_invalid(self):
        self.assertEqual(validate(False, {"type": "boolean"}), [])
        self.assertEqual(validate(0, {"type": "boolean"}), ["/: expected boolean"])

    def test_null_type_valid_and_invalid(self):
        self.assertEqual(validate(None, {"type": "null"}), [])
        self.assertEqual(validate("null", {"type": "null"}), ["/: expected null"])

    def test_properties_valid_and_invalid(self):
        schema = {"type": "object", "properties": {"name": {"type": "string"}}}
        self.assertEqual(validate({"name": "Ada"}, schema), [])
        self.assertEqual(validate({"name": 7}, schema), ["/name: expected string"])

    def test_required_valid_and_invalid(self):
        schema = {"type": "object", "required": ["name", "age"]}
        self.assertEqual(validate({"name": "Ada", "age": 36}, schema), [])
        self.assertEqual(
            validate({"name": "Ada"}, schema),
            ["/age: required property missing"],
        )

    def test_items_valid_and_invalid(self):
        schema = {"type": "array", "items": {"type": "integer"}}
        self.assertEqual(validate([1, 2, 3], schema), [])
        self.assertEqual(validate([1, "2", 3.5], schema), ["/1: expected integer", "/2: expected integer"])

    def test_enum_valid_and_invalid_with_type_sensitive_values(self):
        schema = {"enum": [1.0, "1", None]}
        self.assertEqual(validate("1", schema), [])
        self.assertEqual(validate(1, schema), [])
        self.assertEqual(validate(True, {"enum": [1]}), ["/: value not in enum"])
        self.assertEqual(validate("x", schema), ["/: value not in enum"])

    def test_enum_compares_nested_json_values(self):
        schema = {"enum": [{"a": [1, False, None]}]}
        self.assertEqual(validate({"a": [1.0, False, None]}, schema), [])
        self.assertEqual(validate({"a": [1, 0, None]}, schema), ["/: value not in enum"])

    def test_schema_node_empty_enum_rejects_top_level_values(self):
        self.assertEqual(validate("x", SchemaNode(enum=[])), ["/: value not in enum"])

    def test_schema_node_empty_enum_rejects_nested_values(self):
        schema = SchemaNode(type="object", properties={"name": SchemaNode(enum=[])})
        self.assertEqual(validate({"name": "Ada"}, schema), ["/name: value not in enum"])

    def test_minimum_valid_and_invalid(self):
        schema = {"type": "number", "minimum": 10}
        self.assertEqual(validate(10, schema), [])
        self.assertEqual(validate(9.99, schema), ["/: value less than minimum 10"])

    def test_maximum_valid_and_invalid(self):
        schema = {"type": "number", "maximum": 10}
        self.assertEqual(validate(10, schema), [])
        self.assertEqual(validate(11, schema), ["/: value greater than maximum 10"])

    def test_min_length_valid_and_invalid(self):
        schema = {"type": "string", "minLength": 3}
        self.assertEqual(validate("abc", schema), [])
        self.assertEqual(validate("ab", schema), ["/: length less than minLength 3"])

    def test_max_length_valid_and_invalid(self):
        schema = {"type": "string", "maxLength": 3}
        self.assertEqual(validate("abc", schema), [])
        self.assertEqual(validate("abcd", schema), ["/: length greater than maxLength 3"])

    def test_pattern_valid_and_invalid(self):
        schema = {"type": "string", "pattern": r"^[A-Z]{2}-\d{3}$"}
        self.assertEqual(validate("AB-123", schema), [])
        self.assertEqual(validate("ab-123", schema), ["/: does not match pattern '^[A-Z]{2}-\\\\d{3}$'"])

    def test_pattern_search_semantics_and_anchors(self):
        self.assertEqual(validate("xxabcxx", {"type": "string", "pattern": "abc"}), [])
        self.assertEqual(
            validate("xxabcxx", {"type": "string", "pattern": "^abc$"}),
            ["/: does not match pattern '^abc$'"],
        )

    def test_invalid_pattern_reports_error(self):
        self.assertEqual(
            validate("abc", {"type": "string", "pattern": "["}),
            ["/: invalid pattern '[': unterminated character set at position 0"],
        )

    def test_deep_nested_objects_and_arrays(self):
        schema = {
            "type": "object",
            "properties": {
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["name"],
                        "properties": {"name": {"type": "string", "minLength": 2}},
                    },
                }
            },
        }
        self.assertEqual(validate({"items": [{"name": "Ada"}, {"name": "Bo"}]}, schema), [])
        self.assertEqual(
            validate({"items": [{"name": "A"}, {}, {"name": 3}]}, schema),
            [
                "/items/0/name: length less than minLength 2",
                "/items/1/name: required property missing",
                "/items/2/name: expected string",
            ],
        )

    def test_multiple_simultaneous_errors(self):
        schema = {
            "type": "object",
            "required": ["id", "name"],
            "properties": {
                "id": {"type": "integer", "minimum": 1},
                "name": {"type": "string", "minLength": 3, "pattern": r"^[A-Z]"},
                "tags": {"type": "array", "items": {"type": "string", "maxLength": 4}},
            },
        }
        self.assertEqual(
            validate({"id": 0, "name": "al", "tags": ["good", "toolong", 2]}, schema),
            [
                "/id: value less than minimum 1",
                "/name: length less than minLength 3",
                "/name: does not match pattern '^[A-Z]'",
                "/tags/1: length greater than maxLength 4",
                "/tags/2: expected string",
            ],
        )

    def test_json_pointer_escaping(self):
        schema = {
            "type": "object",
            "required": ["a/b"],
            "properties": {"x~y": {"type": "number"}, "a/b": {"type": "string"}},
        }
        self.assertEqual(
            validate({"x~y": "no"}, schema),
            ["/a~1b: required property missing", "/x~0y: expected number"],
        )

    def test_schema_node_dataclass_is_supported(self):
        schema = SchemaNode(type="object", properties={"ok": SchemaNode(type="boolean")})
        self.assertEqual(validate({"ok": True}, schema), [])
        self.assertEqual(validate({"ok": "true"}, schema), ["/ok: expected boolean"])

    def test_unsupported_schema_type_reports_error(self):
        self.assertEqual(validate("x", {"type": "date"}), ["/: unsupported schema type 'date'"])


class CliTests(unittest.TestCase):
    def test_cli_exits_zero_for_valid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            schema = Path(tmp) / "schema.json"
            instance = Path(tmp) / "instance.json"
            schema.write_text(json.dumps({"type": "object", "required": ["ok"]}), encoding="utf-8")
            instance.write_text(json.dumps({"ok": True}), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-m", "jsonval.cli", str(schema), str(instance)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_cli_accepts_whole_float_for_integer_schema(self):
        with tempfile.TemporaryDirectory() as tmp:
            schema = Path(tmp) / "schema.json"
            instance = Path(tmp) / "instance.json"
            schema.write_text(json.dumps({"type": "integer"}), encoding="utf-8")
            instance.write_text("2.0", encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-m", "jsonval.cli", str(schema), str(instance)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 0)
        self.assertEqual(result.stdout, "")

    def test_cli_exits_one_and_prints_errors_for_invalid_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            schema = Path(tmp) / "schema.json"
            instance = Path(tmp) / "instance.json"
            schema.write_text(json.dumps({"type": "array", "items": {"type": "string"}}), encoding="utf-8")
            instance.write_text(json.dumps(["ok", 3]), encoding="utf-8")

            result = subprocess.run(
                [sys.executable, "-m", "jsonval.cli", str(schema), str(instance)],
                check=False,
                capture_output=True,
                text=True,
            )

        self.assertEqual(result.returncode, 1)
        self.assertEqual(result.stdout, "/1: expected string\n")


if __name__ == "__main__":
    unittest.main()
