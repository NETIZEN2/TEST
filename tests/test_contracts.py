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
        schema = json.loads((SCHEMA_DIR / name).read_text())
        assert schema["$schema"].startswith("https://json-schema.org"), name
        assert schema["type"] == "object"


def test_openapi_spec_load():
    spec = json.loads(Path("services/api/openapi.json").read_text())
    assert spec["openapi"].startswith("3"), "openapi version"
    for path in [
        "/health",
        "/search",
        "/profile",
        "/entities",
        "/entities/{id}",
        "/export",
    ]:
        assert path in spec["paths"], path
    assert "Doc" in spec["components"]["schemas"]
