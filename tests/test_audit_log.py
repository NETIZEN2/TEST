"""Tests for the append-only audit log."""

import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api.audit_log import AuditLog


def test_merkle_root_changes():
    log = AuditLog()
    day = date.today()
    assert log.merkle_root(day) == ""
    log.append({"a": 1})
    first = log.merkle_root(day)
    log.append({"a": 2})
    second = log.merkle_root(day)
    assert first != "" and second != ""
    assert first != second
