# Observability

The platform emits structured JSON logs with basic PII redaction and a
correlation identifier propagated via the `X-Request-ID` header.

In-process metrics track connector call counts, error codes, latency and the
search pipeline deduplication ratio. Metrics are exposed at `/metrics` and are
intended for demo/testing purposes.

Tracing uses OpenTelemetry when available, falling back to no-ops otherwise.
