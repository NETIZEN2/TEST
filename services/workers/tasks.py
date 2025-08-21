"""Celery workers stub."""

from celery import Celery

app = Celery("workers")


@app.task
def example() -> bool:
    """Example task."""
    return True
