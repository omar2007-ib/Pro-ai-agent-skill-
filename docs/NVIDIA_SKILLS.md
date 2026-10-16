# NVIDIA Agent Skills for ELORA AI

This document records NVIDIA's official agent skills that are relevant to ELORA AI's future AI workspace. These are instructions for a compatible coding agent (such as Codex); they are **not runtime AI features installed into the website** merely by listing them here.

Official catalog: https://github.com/NVIDIA/skills
NVIDIA skills hub: https://build.nvidia.com/skills

## Recommended skills

### 1. `aiq-research`
- **Use for:** research workflows and multi-step information gathering that could support ELORA AI's research assistant.
- **Install into Codex:** `npx skills add nvidia/skills --skill aiq-research --agent codex`
- **First task after installation:** "Review the ELORA AI repository and propose a safe, testable research-assistant workflow; do not add paid services or secrets without approval."

### 2. `rag-blueprint`
- **Use for:** learning and evaluating NVIDIA's RAG Blueprint for document retrieval and question-answering, potentially relevant to an ELORA AI document assistant.
- **Install into Codex:** `npx skills add nvidia/skills --skill rag-blueprint --agent codex`
- **First task after installation:** "Assess whether the RAG Blueprint fits ELORA AI's document assistant. List infrastructure, GPU, model, security, and cost requirements before proposing integration. Do not deploy anything yet."

### 3. `nemo-relay-get-started`
- **Use for:** exploring NeMo Relay as an agent-instrumentation/orchestration option for future multi-agent workflows.
- **Install into Codex:** `npx skills add nvidia/skills --skill nemo-relay-get-started --agent codex`
- **First task after installation:** "Evaluate whether NeMo Relay is appropriate for ELORA AI's multi-agent architecture. Provide a minimal proof-of-concept plan and dependencies; do not replace the current architecture without approval."

## Safe installation workflow

Run these commands from the ELORA AI project environment where Codex can access the repository. Review the skill names in the current catalog first, then install one at a time:

```bash
npx skills add nvidia/skills --list
npx skills add nvidia/skills --skill aiq-research --agent codex
npx skills add nvidia/skills --skill rag-blueprint --agent codex
npx skills add nvidia/skills --skill nemo-relay-get-started --agent codex
```

After installing, reload/restart the coding agent if the new skills are not detected. Check installed skills with the skills CLI before beginning implementation.

## Important limitations

- The skill instructions and the service/runtime they describe are different things. Installing a skill does not automatically add a working AI model, API, database, or website feature.
- NVIDIA GPU infrastructure, hosted inference, or other external services may require compatible hardware, account access, setup, or payment. Verify actual requirements and costs before adopting a workflow.
- Never commit API keys, access tokens, `.env` files, or private credentials.
- Do not claim a capability is live in ELORA AI until it is integrated, tested, and documented.

## Current status

- [x] Curated initial NVIDIA skill shortlist for ELORA AI.
- [x] Added installation and evaluation instructions to the repository.
- [ ] Install the skills in the actual Codex project environment.
- [ ] Evaluate dependencies and costs.
- [ ] Implement and test any approved website integrations.

The current ChatGPT-connected Codex environment list was empty during this task, so the skills could not be installed directly into a project runtime from this session. The commands above are ready to run in the connected ELORA AI development environment.