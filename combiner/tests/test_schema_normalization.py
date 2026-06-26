from __future__ import annotations

import mcp_combiner.server as server_mod


def test_normalize_schema_hoists_parent_type_into_anyof() -> None:
    schema = {
        "type": "array",
        "items": {"type": "string"},
        "anyOf": [
            {},
            {"type": "null"},
        ],
    }

    normalized = server_mod._normalize_schema(schema)

    assert normalized == {
        "anyOf": [
            {"type": "array", "items": {"type": "string"}},
            {"type": "null"},
        ]
    }


def test_normalize_schema_closes_object_subschemas_inside_unions() -> None:
    schema = {
        "type": "object",
        "properties": {
            "import_options": {
                "anyOf": [
                    {
                        "properties": {
                            "mode": {"type": "string"},
                        },
                    },
                    {"type": "null"},
                ],
            },
        },
    }

    normalized = server_mod._normalize_schema(schema)
    import_options = normalized["properties"]["import_options"]
    object_branch = import_options["anyOf"][0]

    assert normalized["type"] == "object"
    assert normalized["additionalProperties"] is False
    assert object_branch["type"] == "object"
    assert object_branch["properties"] == {"mode": {"type": "string"}}
    assert object_branch["additionalProperties"] is False
