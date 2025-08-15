"""Simple backup and restore helpers for docs."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Iterable, Dict, Any, List


def backup_docs(docs: Iterable[Dict[str, Any]], path: Path) -> None:
    """Serialise *docs* to *path* as JSON."""
    path.write_text(json.dumps(list(docs)))


def restore_docs(path: Path) -> List[Dict[str, Any]]:
    """Load documents from *path*."""
    if not path.exists():
        return []
    return json.loads(path.read_text())
