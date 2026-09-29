# Threat Model: sample service (STRIDE)

A lightweight STRIDE threat model of the sample FastAPI service, to show design-level security thinking alongside the automated scanning. STRIDE finds flaws that scanners cannot.

## System and trust boundary

```
Client (untrusted)  --HTTPS-->  API (FastAPI)  -->  (future) datastore
```

The trust boundary is the API edge: everything from the client is untrusted input.

## STRIDE analysis

| Threat | Category | Example against this service | Mitigation |
|--------|----------|------------------------------|------------|
| Spoofing | Authentication | Caller pretends to be another user | Add authentication (OIDC/JWT) at the API edge; no anonymous write paths |
| Tampering | Integrity | Modified request body or path parameter | Validate and type-constrain inputs (FastAPI/Pydantic); TLS in transit |
| Repudiation | Non-repudiation | User denies making a request | Structured request logging with request IDs, shipped off-host |
| Information disclosure | Confidentiality | Verbose errors leak stack traces or data | Generic error responses; no secrets in logs; least-privilege data access |
| Denial of service | Availability | Flood of requests exhausts the service | Rate limiting at the gateway; autoscaling; request size limits |
| Elevation of privilege | Authorization | User reaches an admin action | Authorization checks per route; deny by default |

## How the pipeline supports this model

- Input tampering: SAST (Semgrep, SonarQube) flags unsafe input handling.
- Information disclosure: secret scanning (Gitleaks) stops credential leaks; DAST (ZAP) flags verbose headers and error leakage.
- Vulnerable dependencies enabling any of the above: SCA (Trivy, Dependency-Check).
- Insecure runtime configuration: DAST and container scanning.

## Residual risks and next steps

Authentication, authorization and rate limiting are not implemented in this sample and are the top priorities before any real use. The pipeline reduces known-vulnerability risk but does not replace design review; run threat modelling at design time for every new feature.