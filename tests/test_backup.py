"""Test backup and restore helpers."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from services.api.backup import backup_docs, restore_docs


def test_backup_and_restore(tmp_path):
    docs = [{"id": "1", "title": "A"}]
    path = tmp_path / "backup.json"
    backup_docs(docs, path)
    restored = restore_docs(path)
    assert restored == docs
