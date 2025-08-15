# Records and FOI Notes

Guidance on record keeping and Freedom of Information (FOI) discovery.

## Audit Log Discoverability
- Append-only audit log with daily Merkle roots stored in WORM storage.
- Logs indexed by correlation ID and timestamp to enable targeted searches.
- Access restricted to authorised officers; queries logged for oversight.

## Protecting Secrets
- Log entries exclude plaintext secrets; only references to KMS keys or redacted identifiers are stored.
- Sensitive connector errors are summarised without payload details.

## FOI Process
- FOI officer queries audit log using correlation IDs linked to case files.
- Redactions applied to privileged or security-sensitive material before release.

## Review Checklist
| Item | Responsible | Frequency |
| --- | --- | --- |
| Audit log integrity verified | Security Lead | Monthly |
| FOI procedure tested | Records Officer | Annually |
| Redaction process reviewed | Legal Counsel | Annually |

