# Infrastructure

IaC templates for deployment.

- **mTLS** – services authenticate using mutual TLS certificates issued by an
  internal CA. Service identities are bound to these certificates.
- **OPA/Gatekeeper** – Kubernetes admission policies ensure only compliant
  deployments proceed.
- **Secrets** – all secrets are wrapped by a cloud KMS and rotated regularly;
  emergency break-glass access triggers alerting and detailed audit logs.
