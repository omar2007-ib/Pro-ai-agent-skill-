---
name: release-quality-gate
description: Run a repository-aware quality, security, and evidence check before committing code, opening a pull request, changing authentication or data access, or describing a project as release-ready.
---

# Release Quality Gate

## Purpose

Use this skill to make small, verifiable changes without confusing implementation with proof. It applies across web apps, APIs, static sites, serverless functions, AI integrations, and shared tooling.

## Workflow

1. **Read the project contract first.** Inspect AGENTS.md, README.md, package manifests, architecture/launch notes, recent commits, and the relevant source files. Preserve named product boundaries, approved design decisions, and existing security assumptions.
2. **Confirm the target.** Verify the repository owner, default branch, current working tree, and write permission. Never write to a similarly named or third-party repository just because the intended one is blocked.
3. **Choose one bounded change.** Trace the affected user flow and nearby implementation before editing. Avoid unrelated cleanup and avoid adding a dependency when the existing toolchain can solve the task.
4. **Review security on reachable paths.** Check authentication and authorization separately; validate untrusted inputs and imported files; inspect secrets, logging, webhook signatures/replay handling, rate limits, upload restrictions, access-control policies, injection risks, and unsafe external requests as applicable. Do not change live databases or production permissions without a verified target and an explicit need.
5. **Run the strongest available checks.** Use project-defined tests first, then lint/type checks and a production build where available. For UI work, check keyboard access, accessible names, Arabic/RTL where relevant, reduced motion, and the supported viewport sizes. Prefer a reproducible regression test for each fixed defect.
6. **Verify the diff.** Inspect every changed path and the full diff. Remove unrelated edits, debug output, generated artifacts, credentials, .env files, and private data. Confirm tests cover the new behavior rather than only checking that source text contains a token.
7. **Report evidence honestly.** Separate implemented, tested, not tested, and blocked items. State exact commands and results. A static check is not an end-to-end test; a successful build is not proof of working authentication, external APIs, storage, or production deployment.
8. **Publish safely.** Commit only to a confirmed user-owned or user-authorized repository. Prefer a focused branch and pull request when available. Do not deploy merely because a commit exists; verify the deployment and critical routes before calling a service live.
9. **Maintain the task ledger.** Before choosing the next task, read the project's existing build log or issue list. Record the task, changed paths, verification evidence, blockers, and the next distinct task so work is not repeated.

## Rules

- Never invent repositories, files, credentials, test results, service status, or deployment URLs.
- Never expose secrets in source, logs, issue text, screenshots, or reports. If a secret may have been committed, stop and report rotation/removal steps rather than copying it.
- Never treat UI-only role checks as a security boundary; verify server-side authorization and database/storage policies.
- Never silently swallow errors on a user-critical path. Preserve actionable error states without leaking sensitive details.
- Do not bypass a failing test by weakening its assertion unless the intended contract has changed and the new contract is tested.
- When a required environment, service, permission, or credit limit blocks work, switch to a safe task in an accessible authorized repository and state the blocker precisely.

## Evidence report template

- **Project/repository:** exact name and branch.
- **Change:** behavior or defect addressed and changed paths.
- **Tests run:** exact commands and pass/fail outcomes.
- **Verified manually:** only actions actually exercised.
- **Not verified:** end-to-end flows, integrations, or deployment checks that were not run.
- **Blockers:** missing access, credentials, environment, or service availability.
- **Commit/PR:** link and current state.
- **Next distinct task:** one bounded follow-up, checked against the task ledger.

## Edge cases

- If tests require a paid service, unavailable database, production account, or secret, do not fabricate a successful result. Use mocks only for isolated unit behavior and label them as mocks.
- If repository identity is ambiguous or the only writable target is unrelated, do not write. Report the exact repository/permission blocker.
- If a change touches authentication, authorization, billing, uploads, private files, or AI-generated educational answers, raise the verification bar and include negative-path tests where feasible.
- If a fix cannot be executed in the current environment, prepare a reviewable patch or PR only when the source and target are confirmed; otherwise stop at a precise diagnostic.

## References

- Agent Skills format: https://agentskills.io/specification
- OWASP Top 10: https://owasp.org/www-project-top-ten/
- GitHub Actions security hardening: https://docs.github.com/en/actions/security-for-github-actions/security-guides/security-hardening-for-github-actions
