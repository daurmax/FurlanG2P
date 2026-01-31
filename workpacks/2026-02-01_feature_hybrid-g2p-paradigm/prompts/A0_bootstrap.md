# Bootstrap Agent Prompt

> Create feature branch for hybrid G2P paradigm workpack.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Request details
4. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Create and push the feature branch that all agents will work on.

---

## Delivery Mode

- **Direct push**: Create branch and push to origin

---

## Objective

Create the feature branch `feature/hybrid-g2p-paradigm` from `main` to serve as the working branch for this workpack. All subsequent agents will create sub-branches from this branch or commit directly to it.

---

## Implementation Requirements

- Ensure working directory is clean (no uncommitted changes)
- Create branch from latest `main`
- Push branch to origin
- Verify branch exists on remote

---

## Scope

### In Scope

- Branch creation
- Push to origin

### Out of Scope

- Any code changes
- File modifications

---

## Acceptance Criteria

- [ ] Branch `feature/hybrid-g2p-paradigm` exists locally
- [ ] Branch is pushed to origin
- [ ] Branch is based on latest `main`

---

## Verification

### Commands

```bash
# Ensure on main and up to date
git checkout main
git pull origin main

# Create feature branch
git checkout -b feature/hybrid-g2p-paradigm

# Push to origin
git push -u origin feature/hybrid-g2p-paradigm

# Verify branch exists
git branch -a | grep hybrid-g2p-paradigm
```

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A0_bootstrap.json`

```json
{
  "schema_version": "1.0",
  "workpack": "2026-02-01_feature_hybrid-g2p-paradigm",
  "prompt": "A0_bootstrap",
  "component": "bootstrap",
  "delivery_mode": "direct_push",
  "branch": {
    "base": "main",
    "work": "feature/hybrid-g2p-paradigm",
    "merge_target": "main"
  },
  "summary": "Created feature branch for hybrid G2P paradigm workpack",
  "handoff": {
    "files_modified": [],
    "files_created": [],
    "verification": {
      "commands_run": ["git branch -a"],
      "all_passed": true
    },
    "next_steps": [
      "A1_library can begin implementation",
      "A4_docs can begin architecture documentation"
    ],
    "known_issues": []
  },
  "artifacts": {
    "commits": ["<commit-sha>"]
  }
}
```

---

## Stop Conditions

- **STOP** if `main` branch has uncommitted changes
- **STOP** if branch already exists (check with team first)
- **CONTINUE** otherwise

---

## Deliverables

- [ ] Feature branch created and pushed
- [ ] Handoff output JSON created
