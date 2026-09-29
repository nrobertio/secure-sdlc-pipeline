# Secure SDLC Pipeline (DevSecOps)

A reference **shift-left security pipeline** that integrates SAST, SCA (dependency scanning), secret scanning, container image scanning, IaC scanning, SBOM generation and DAST into CI/CD. The same pipeline is provided for **GitLab CI/CD** and **Jenkins**, running against a small sample service, with a **STRIDE threat model** and guidance for feeding results into a vulnerability-management dashboard.

> Maintained by [nrobertio](https://github.com/nrobertio). A generic, public reference for the application-security and DevSecOps work described in modern product-security roles: securing the SDLC, threat modelling, and vulnerability lifecycle management.

## What this demonstrates

- **SAST**: SonarQube plus Semgrep on the application source.
- **SCA / dependency scanning**: Trivy and OWASP Dependency-Check on third-party libraries.
- **Secret scanning**: Gitleaks across the repo and history.
- **Container scanning**: Trivy on the built image.
- **IaC scanning**: Checkov / tfsec on any infrastructure code.
- **SBOM**: Syft generates a CycloneDX software bill of materials.
- **DAST**: OWASP ZAP baseline scan against the running app.
- **Two pipelines**: `.gitlab-ci.yml` and `Jenkinsfile`, functionally equivalent.
- **Threat model**: STRIDE analysis of the sample service in `docs/THREAT-MODEL.md`.

## Pipeline stages (shift-left order)

```
build -> secrets -> sast -> sca -> container-scan -> sbom -> dast -> report
```

Each stage fails the build on findings above a set severity, so issues are caught before merge, not in production.

## Layout

```
app/                 sample FastAPI service, Dockerfile and tests
.gitlab-ci.yml       GitLab CI/CD DevSecOps pipeline
Jenkinsfile          Jenkins declarative equivalent
ci/                  tool configs (Gitleaks, ZAP rules, Semgrep)
sonar-project.properties  SonarQube configuration
docs/                PROJECT.md and THREAT-MODEL.md
```

## Feeding a dashboard

Every scanner emits a report artifact (SARIF, JSON or CycloneDX). In a real setup these are imported into a vulnerability-management platform such as DefectDojo or GitLab's own Security Dashboard for triage, tracking and reporting. See docs/PROJECT.md.

## License

MIT. See [LICENSE](LICENSE).
