import json
from pathlib import Path

SCHEMA_DIR = Path("packages/schemas")
SCHEMAS = [
    "doc.schema.json",
    "signal.schema.json",
    "entity_profile.schema.json",
    "audit_event.schema.json",
    "pivot_edge.schema.json",
]


def test_json_schemas_load():
    for name in SCHEMAS:
        with open(SCHEMA_DIR / name) as f:
            schema = json.load(f)
        assert schema["$schema"].startswith("https://json-schema.org"), name
        assert schema["type"] == "object"


def test_openapi_spec_load():
    with open("services/api/openapi.json") as f:
    with open("services/api/openapi.yaml") as f:
        spec = json.load(f)
    assert spec["openapi"].startswith("3"), "openapi version"
    for path in ["/health", "/search", "/profile", "/entities", "/entities/{id}", "/export"]:
        assert path in spec["paths"], path
    assert "Doc" in spec["components"]["schemas"]
