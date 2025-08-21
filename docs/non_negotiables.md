# Non-negotiable engineering principles

This platform is built for lawful, explainable open-source intelligence in line with Australian guidance.

## Global constraints
- **Lawful by design:** Respect Terms of Service and `robots.txt`; store personal data only when required and purge after 180 days by default. Every fact must carry provenance (URL, timestamp and content hash).
- **Security:** Enforce OIDC/SSO, role- or attribute-based access controls and TLS. Secrets live in a KMS or vault. Network calls go through SSRF-safe fetchers. All actions emit append-only audit logs.
- **Observability:** Structured JSON logs include correlation IDs. Collect metrics per connector and trace requests end-to-end.
- **Accessibility:** UI follows WCAG 2.1 AA with keyboard navigation and screen‑reader landmarks.

## Deliverables
- Repository scaffold with backend services, web app, infrastructure stubs and documentation.
- OpenAPI specification and JSON Schemas that match implemented services.
- CI/CD enforcing lint, tests, security scans and licence checks.

## Definition of done
- Unit and contract tests pass.
- OpenAPI validates.
- Connectors obey rate limits and return provenance.
- UI pages are accessible.
- CI passes including security and licence checks.
