# Fetcher Service

Sandboxed HTTP fetch service.

The fetcher runs in a locked-down container with an egress allowlist and
performs DNS pinning to prevent SSRF. Responses are limited in size and
validated for acceptable MIME types.
