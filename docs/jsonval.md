# jsonval

`jsonval` is a small JSON-schema validator package. It supports a focused subset
of JSON Schema and returns all discovered validation errors as strings with
JSON-pointer-style paths.

## Supported Keywords

| Keyword | Applies to | Behavior |
| --- | --- | --- |
| `type` | any value | Supports `object`, `array`, `string`, `number`, `integer`, `boolean`, and `null`. |
| `properties` | objects | Validates schemas for present named properties. Extra properties are allowed. |
| `required` | objects | Reports each missing required property. |
| `items` | arrays | Validates every array item against one schema. |
| `enum` | any value | Requires the value to exactly match one listed value, including Python/JSON type. |
| `minimum` | numbers, integers | Requires a numeric value greater than or equal to the limit. |
| `maximum` | numbers, integers | Requires a numeric value less than or equal to the limit. |
| `minLength` | strings | Requires string length greater than or equal to the limit. |
| `maxLength` | strings | Requires string length less than or equal to the limit. |
| `pattern` | strings | Uses Python regular expression search semantics. Anchor with `^` and `$` for full-string checks. |

Unsupported keywords are ignored. Unknown `type` values are reported as schema
errors.

## Python Example

```python
from jsonval import validate

schema = {
    "type": "object",
    "required": ["items"],
    "properties": {
        "items": {
            "type": "array",
            "items": {
                "type": "object",
                "required": ["name"],
                "properties": {
                    "name": {"type": "string", "minLength": 2},
                    "price": {"type": "number", "minimum": 0},
                },
            },
        }
    },
}

errors = validate({"items": [{"name": "A", "price": -1}]}, schema)
assert errors == [
    "/items/0/name: length less than minLength 2",
    "/items/0/price: value less than minimum 0",
]
```

## CLI Example

```sh
python -m jsonval.cli schema.json instance.json
```

The CLI exits with status `0` when the instance is valid. It prints validation
errors to stdout and exits with status `1` when invalid. File loading or JSON
parse failures are printed to stderr and exit with status `2`.
