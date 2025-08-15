"""Simple event extraction producing timeline tuples."""
from __future__ import annotations
import re
from datetime import datetime
from typing import List, Dict

_EVENT_RE = re.compile(
    r"On (?P<date>\d{1,2} \w+ \d{4}), (?P<who>[A-Z][a-z]+(?: [A-Z][a-z]+)*) "
    r"(?P<verb>founded|acquired|visited) (?P<target>[A-Z][a-z]+(?: [A-Z][a-z]+)*) "
    r"in (?P<where>[A-Z][a-z]+(?: [A-Z][a-z]+)*)"
)

def extract_events(text: str, source: str) -> List[Dict[str, object]]:
    """Extract events with who/what/when/where and citations."""
    events: List[Dict[str, object]] = []
    for match in _EVENT_RE.finditer(text):
        date = datetime.strptime(match.group("date"), "%d %b %Y").date().isoformat()
        events.append(
            {
                "who": match.group("who"),
                "what": match.group("verb"),
                "when": date,
                "where": match.group("where"),
                "source": source,
                "confidence": 0.9,
                "citations": [{"url": source}],
            }
        )
    return events
