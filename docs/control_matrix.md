# Control Matrix

Mapping Australian controls to implemented measures.

| Control | APP Reference | PSPF/ISM Reference | Implementation |
| --- | --- | --- | --- |
| Transparent management of personal information | APP 1 | PSPF GovSec 1, ISM INFOSEC-1 | Source registry, DPIA and published policies |
| Limits on collection of personal information | APP 3 | PSPF GovSec 3, ISM PRIVSEC-1 | Connectors collect only public data, feature flags guard optional modules |
| Notification and consent | APP 5 | PSPF GovSec 4 | Provenance recorded and classification banners on exports |
| Data security | APP 11 | PSPF INFOSEC 4, ISM CRYPTO-3 | SSRF-safe fetcher, mTLS, KMS-wrapped secrets, audit log |
| Access and correction | APP 12/13 | PSPF GovSec 5 | API supports authorised access, audit events enable traceability |
| Retention and disposal | APP 4 | PSPF GovSec 7 | Configurable 180-day retention, purge tasks |

Review cadence: matrix reviewed quarterly by compliance team.

