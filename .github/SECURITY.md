# Security Policy

## Supported Versions

Only the `main` branch is actively supported with security updates. Generated
projects should pin to a released template version and follow the update
guidance in `docs/MAINTENANCE_SECURITY.md`.

## Reporting a Vulnerability

**Do not open a public issue for security vulnerabilities.**

- Email the maintainer via the address listed in the GitHub profile, or
- Use GitHub's private vulnerability reporting:
  `https://github.com/Create-Python-App/cpa-templates/security/advisories/new`

Include:

- Affected template or extension slug (e.g. `fastapi-starter`, `fastapi-auth-jwt`)
- Steps to reproduce and impact assessment
- Suggested fix or mitigation, if available

You will receive an initial response within 72 hours. If the issue is
confirmed, a fix will be coordinated and a CVE/advisory published as needed.

## Triage and Remediation

See `docs/MAINTENANCE_SECURITY.md` for the full triage matrix, fix patterns for
`create-python-app` vs `cpa-templates`, and audit commands (`pip-audit`,
`osv-scanner`, `CodeQL`).

## Disclosure

Coordinated disclosure is preferred. Please allow up to 90 days before public
disclosure unless a shorter timeline is mutually agreed.
