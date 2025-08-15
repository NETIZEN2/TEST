"""Confidence model based on tunable weights."""
from __future__ import annotations
from pathlib import Path


def _load_weights(path: Path) -> dict:
    weights = {}
    for line in path.read_text().splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if line.startswith("weights"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            weights[key.strip()] = float(val.strip())
    return weights

WEIGHTS = _load_weights(Path(__file__).with_name("confidence.yaml"))


def compute_confidence(
    source_weight: float,
    corroboration_count: int,
    recency_days: int,
    media_verification_score: float,
) -> float:
    """Compute confidence in range [0,1]."""
    recency_score = max(0.0, 1 - recency_days / 365)
    corr_score = min(1.0, corroboration_count / 5)
    confidence = (
        WEIGHTS.get("source_weight", 0) * source_weight
        + WEIGHTS.get("corroboration_count", 0) * corr_score
        + WEIGHTS.get("recency", 0) * recency_score
        + WEIGHTS.get("media_verification_score", 0) * media_verification_score
    )
    return round(min(confidence, 1.0), 3)
