# Disaster recovery and resilience

- **RTO**: 1 hour for core services
- **RPO**: 15 minutes via S3 snapshotting

## Backup and restore

Backups of persisted entities and audit logs are written to S3 with versioning. Restore procedures are exercised quarterly using the test in `tests/test_backup.py`.

## Chaos experiments

Connector outages are simulated in tests (`tests/test_resilience.py`). The system must continue serving results from healthy connectors without error.
