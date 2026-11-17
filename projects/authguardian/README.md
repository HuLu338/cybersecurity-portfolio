# AuthGuardianPro: identity and API permissions

**Type:** existing identity-security prototype

**Stack:** Go, Gin, SQLite, React, TypeScript, JWT, bcrypt and TOTP

**Repository:** [AuthGuardianPro](https://github.com/HuLu338/AuthGuardianPro)

## Objective

Explore how authentication, role checks, API-key permissions and audit events fit into one identity-security application. The project also includes risk, alert and response demonstrations for a local environment.

## Environment and tools

The prototype has a Go/Gin backend, SQLite storage and a React dashboard. The repository provides Docker Compose setup, API documentation and local smoke-test instructions. Seeded users and simulation features are demonstration facilities, not production identity controls.

## Method

1. Read the repository's local-demo instructions and use an isolated, disposable environment.
2. Trace the authentication module and the documented login/MFA flow. Keep demonstration secrets out of shared screenshots and deployment configuration.
3. Inspect the RBAC helper and its table-driven tests for accepted roles, missing roles, empty roles and whitespace handling.
4. Inspect API-key permission tests for exact, wildcard, denied and empty-permission behavior. Read those assertions alongside the protected route implementations.
5. Follow the repository's backend checks and smoke-test procedure when reproducing the application locally. Use audit events to connect an action with its outcome.

For this portfolio refresh, the source and test assertions were reviewed. The application and its automated checks were not rerun.

## Results and evidence

The repository includes a login/MFA implementation, role matching and separate API-key permission tests. The README describes the broader audit-to-risk-to-alert workflow. That broader feature list is a description of the prototype's scope, not independent validation of every path.

| Evidence | What it supports |
|---|---|
| [Authentication module](https://github.com/HuLu338/AuthGuardianPro/blob/fee84beeb17285ccb89f754ed9f78c483f8cfca0/backend/internal/auth/auth.go) | Login and MFA implementation to inspect |
| [RBAC helper](https://github.com/HuLu338/AuthGuardianPro/blob/fee84beeb17285ccb89f754ed9f78c483f8cfca0/backend/internal/rbac/rbac.go) | Server-side role matching |
| [RBAC tests](https://github.com/HuLu338/AuthGuardianPro/blob/fee84beeb17285ccb89f754ed9f78c483f8cfca0/backend/internal/rbac/rbac_test.go) | Five table-driven role scenarios |
| [API-key permission tests](https://github.com/HuLu338/AuthGuardianPro/blob/fee84beeb17285ccb89f754ed9f78c483f8cfca0/backend/internal/apikey/apikey_test.go) | Permission matching, wildcard handling and denial cases |
| [Project README](https://github.com/HuLu338/AuthGuardianPro/blob/fee84beeb17285ccb89f754ed9f78c483f8cfca0/README.md) | Architecture, setup and known limitations |

## Reflection and next improvements

Authentication identifies a caller; authorization decides whether that caller can act. The project provides a useful place to keep those decisions separate and inspect their audit records.

The README identifies further hardening work, including secret management, TLS, rate limiting and broader testing. Before claiming stronger assurance, I would add route-level tests proving that every sensitive endpoint applies the intended policy. SQLite, seeded users and local MFA demonstrations also need a clear boundary from real accounts. This remains a portfolio prototype.

## Source and scope

This case study summarizes the existing public repository at commit `fee84beeb17285ccb89f754ed9f78c483f8cfca0`, reviewed on 17 November 2026. Pinned links let a reader inspect the evidence behind each statement. No production deployment, new passing test run or measured detection effectiveness is claimed.

[Return to the portfolio](../../index.html#projects)
