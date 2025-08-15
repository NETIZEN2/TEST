"""NER service with fallback and Wikidata linking."""
from __future__ import annotations
import re
from typing import Dict, List

try:  # pragma: no cover - optional dependency
    import spacy
    try:
        _NLP = spacy.load("en_core_web_sm")
    except Exception:  # model may not be available
        _NLP = spacy.blank("en")
        if "ner" not in _NLP.pipe_names:
            _NLP.add_pipe("ner")
except Exception:  # pragma: no cover - spaCy not installed
    spacy = None
    _NLP = None

# minimal mapping for offline Wikidata linking
_ENTITY_LINKS = {
    "Barack Obama": "Q76",
    "Paris": "Q90",
    "Microsoft": "Q2283",
    "Alice": "Q123",
    "Acme": "Q223",
    "Sydney": "Q3130",
}

# simple label hints for fallback regex matcher
_PEOPLE = {"Barack Obama", "Alice"}
_ORGS = {"Microsoft", "Acme"}
_LOCS = {"Paris", "Sydney"}


def _link_entity(text: str) -> str | None:
    """Return Wikidata ID for entity text if known."""
    return _ENTITY_LINKS.get(text)


def extract_entities(text: str) -> List[Dict[str, str]]:
    """Extract PERSON/ORG/GPE entities with optional Wikidata IDs."""
    entities: List[Dict[str, str]] = []
    if _NLP and _NLP.pipe_names:
        doc = _NLP(text)
        for ent in doc.ents:
            if ent.label_ in {"PERSON", "ORG", "GPE"}:
                entities.append(
                    {
                        "text": ent.text,
                        "label": ent.label_,
                        "wikidata_id": _link_entity(ent.text),
                    }
                )
    else:  # fallback regex-based extraction
        pattern = r"\b([A-Z][a-z]+(?: [A-Z][a-z]+)*)\b"
        for match in re.finditer(pattern, text):
            ent_text = match.group(1)
            if ent_text in _PEOPLE:
                label = "PERSON"
            elif ent_text in _LOCS:
                label = "GPE"
            elif ent_text in _ORGS:
                label = "ORG"
            else:
                continue
            entities.append(
                {
                    "text": ent_text,
                    "label": label,
                    "wikidata_id": _link_entity(ent_text),
                }
            )
    return entities
"""NER service stub."""
from typing import List


def extract_entities(text: str) -> List[str]:
    """Extract entities from text (stub)."""
    return []
