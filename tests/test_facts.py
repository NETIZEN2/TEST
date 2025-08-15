import json
import os

from services.facts import extract_facts


def test_extract_facts_keys():
    data = extract_facts("sample text")
    assert set(data.keys()) == {"tech", "geo", "legal", "media"}


def test_fact_schemas_exist():
    base = os.path.join("packages", "schemas")
    schemas = [
        "tech_facts.schema.json",
        "geo_facts.schema.json",
        "legal_facts.schema.json",
        "media_facts.schema.json",
    ]
    for name in schemas:
        path = os.path.join(base, name)
        assert os.path.exists(path), f"{name} missing"
        with open(path) as fh:
            data = json.load(fh)
        assert data.get("title"), f"{name} missing title"
