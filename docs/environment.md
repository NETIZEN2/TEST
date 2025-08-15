# Environment variable catalogue

| Variable | Default | Purpose |
|----------|---------|---------|
| `ADVANCED_FACTS` | `false` | Enable advanced fact extraction modules |
| `PHASE1_CONNECTORS` | `false` | Activate phase one connectors |
| `CONNECTOR_LIMIT` | `5` | Default maximum docs per connector |
| `CONNECTOR_TIMEOUT_MS` | `10000` | Connector call timeout in milliseconds |
| `FETCHER_TIMEOUT` | `5` | HTTP fetcher timeout in seconds |
| `FETCHER_MAX_BYTES` | `1000000` | Maximum response size in bytes |
| `RETENTION_DAYS` | `180` | Data retention period |
| `FETCHER_ALLOWED_HOSTS` | `` | Comma separated egress allowlist |
| `FETCHER_ALLOWED_MIME_PREFIXES` | `text/,application/json` | Allowed response MIME prefixes |
| `SECRET_DB_URL` | none | Database connection string |
