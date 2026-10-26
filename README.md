# Pro AI Agent Skills

Reusable, portable agent skills for coding, design, QA, security, and AI automation. The repository also retains the existing ELORA AI landing-page artifact in `index.html`; the skill workflow does not overwrite or repurpose that page.

## Skill catalog

| Skill | Purpose | Path |
| --- | --- | --- |
| Release Quality Gate | Repository-aware pre-merge and pre-release checks, security review, honest evidence reporting, and task-ledger discipline | [skills/release-quality-gate/SKILL.md](skills/release-quality-gate/SKILL.md) |
| Third-Party Skill Audit | Review external agent skills for provenance, prompt injection, risky code, license, permissions, and safe sandbox trials before adoption | [skills/third-party-skill-audit/SKILL.md](skills/third-party-skill-audit/SKILL.md) |

## Validate skills locally

Requires Python 3.10+ and no third-party packages:

    python -m unittest discover -s scripts -p "test_*.py"
    python scripts/validate_agent_skills.py

The validator checks required frontmatter fields, naming conventions, directory-name agreement, description limits, a non-empty Markdown body, and a title. It is a lightweight repository check—not a full YAML parser or a replacement for the official Agent Skills validator.

## Research notes

- [docs/NVIDIA_SKILLS.md](docs/NVIDIA_SKILLS.md) — curated NVIDIA skill shortlist and installation cautions for ELORA AI. Listing a skill is not the same as installing it or shipping a runtime feature.
- [docs/DAILY_BUILD_LOG.md](docs/DAILY_BUILD_LOG.md) — concise task history and blockers used to avoid repeating portfolio work.
- [Agent Skills specification](https://agentskills.io/specification) — format reference for portable skill files.
- [GitHub secure-use guidance](https://docs.github.com/en/actions/reference/security/secure-use) — supply-chain and third-party execution guidance.

## Safety baseline

- Inspect repository instructions and current files before editing.
- Do not commit secrets or private user data.
- Do not install or execute third-party skills without reviewing source, license, dependencies, and permissions.
- Treat static checks as bounded evidence; they do not prove a skill is safe at runtime.
- Report what was implemented, what was tested, what remains unverified, and the exact blocker.
