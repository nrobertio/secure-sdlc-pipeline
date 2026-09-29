# Project Writeup: Secure SDLC Pipeline (DevSecOps)

Why this exists, how it was built, why each tool, the benefits, and the interview talking-track. This project maps directly to product-security and application-security roles that ask for security tooling integrated into CI/CD.

## 1. The problem it solves

Security bolted on at the end is slow and expensive: a vulnerability found in production costs far more to fix than one caught at the pull request. "Shift left" means moving security checks into the pipeline so developers get findings within minutes of committing, in the tools they already use. This project wires the full set of checks, secrets, SAST, dependency scanning, container scanning, SBOM and DAST, into both GitLab CI and Jenkins, against a sample service.

## 2. How it was built

A small FastAPI service is the scan target. Two functionally equivalent pipelines run the same stages in shift-left order:

```
build -> secrets -> sast -> sca -> container -> sbom -> dast
```

- GitLab: `.gitlab-ci.yml` with one job per tool, each publishing a report artifact.
- Jenkins: `Jenkinsfile` (declarative) running the same tools via their containers, archiving the reports.
- A GitHub Actions workflow is included as a third option.

## 3. Why each tool

- Gitleaks (secrets): catches committed credentials before they ever reach a registry or prod. Secrets in git history are one of the most common breach causes.
- Semgrep and SonarQube (SAST): analyse source for insecure patterns. Semgrep is fast and open for the pipeline; SonarQube adds quality gates and a review UI. Using both shows the open and enterprise sides.
- Trivy and OWASP Dependency-Check (SCA): most application risk is in third-party libraries, not your own code. These flag known-vulnerable dependencies with a severity gate.
- Trivy (container image): scans the built image for OS and library CVEs, because a clean app on a vulnerable base image is still vulnerable.
- Syft (SBOM): produces a CycloneDX software bill of materials, increasingly required for supply-chain transparency and incident response.
- OWASP ZAP (DAST): runs against the actually-running app to find issues static analysis cannot see, such as missing security headers and runtime behaviour.
- Checkov / tfsec (IaC): scans any infrastructure code so misconfigurations are caught as code, not in the cloud.

## 4. Why fail the build

Each stage fails on findings above a chosen severity (HIGH and CRITICAL here). A scan that only warns gets ignored; a gate that blocks the merge is what actually changes behaviour. DAST is set to report rather than block by default, because dynamic scans can be noisy and are better triaged than hard-gated at first.

## 5. Feeding a dashboard (vulnerability lifecycle)

Every tool emits a machine-readable report (SARIF, JSON or CycloneDX). In a real setup these are imported into a vulnerability-management platform such as DefectDojo, or GitLab's built-in Security Dashboard, where findings are deduplicated, triaged, assigned, tracked to closure, and reported to leadership. That closes the loop from detection to remediation, which is the core of a product-security role.

## 6. Benefits

- Findings arrive at pull-request time, when they are cheapest to fix.
- Coverage across the whole surface: secrets, code, dependencies, image, runtime and IaC.
- Portable: the same checks run in GitLab, Jenkins or GitHub, so the approach transfers between employers.
- Auditable and reportable: SARIF and SBOM artifacts feed a dashboard for tracking and compliance.

## 7. Interview talking points

- SAST vs DAST vs SCA: SAST reads source for insecure patterns, DAST tests the running app from the outside, SCA checks third-party dependencies for known CVEs. You want all three because each finds what the others miss.
- Why fail the build vs warn: a blocking gate changes behaviour; a warning is noise. Tune severity so gates are credible, not annoying.
- Handling false positives: allowlists (Gitleaks), rule tuning (ZAP rules file, Semgrep configs), and triage in the dashboard rather than disabling scans.
- Shift-left plus threat modelling: scanning finds known issues; STRIDE threat modelling (see THREAT-MODEL.md) finds design flaws a scanner never will.
- What to add next: signed commits and provenance (SLSA), image signing (cosign), and DefectDojo for full lifecycle tracking.

## 8. How to run it

- GitLab: push to a GitLab project; the pipeline runs automatically. Set SONAR_HOST_URL and SONAR_TOKEN to enable the SonarQube job.
- Jenkins: point a pipeline job at the Jenkinsfile on a Docker-enabled agent.
- Locally: you can run any single tool, for example `docker run --rm -v %CD%:/src aquasec/trivy fs /src/app`.