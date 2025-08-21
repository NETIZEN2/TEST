"""Simple append-only audit log with Merkle root calculation."""

from __future__ import annotations

import hashlib
import json
from collections import defaultdict
from datetime import date
from typing import Dict, List


class AuditLog:
    """Stores immutable audit events and computes daily Merkle roots."""

    def __init__(self) -> None:
        self._events: Dict[date, List[str]] = defaultdict(list)

    def append(self, event: dict) -> None:
        """Append an *event* to the log."""

        raw = json.dumps(event, sort_keys=True)
        self._events[date.today()].append(raw)

    def merkle_root(self, day: date) -> str:
        """Return the Merkle root for *day* or an empty string."""

        leaves = [
            hashlib.sha256(e.encode()).digest() for e in self._events.get(day, [])
        ]
        if not leaves:
            return ""
        while len(leaves) > 1:
            it = iter(leaves)
            leaves = [hashlib.sha256(a + next(it, a)).digest() for a in it]
        return leaves[0].hex()
