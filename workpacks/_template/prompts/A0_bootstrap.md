# Bootstrap Agent Prompt

> Prompt for the bootstrap agent to set up branches, prerequisites, and shared infrastructure.

---

## READ FIRST

Read these files before starting:

1. `./README.md` — Project overview
2. `./AGENTS.md` — Agent guidelines
3. `./workpacks/<workpack>/00_request.md` — Original request
4. `./workpacks/<workpack>/01_plan.md` — Full plan with branch strategy
5. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary: typically "Set up feature branches and prerequisites" -->

---

## Delivery Mode

- **Direct push**: Bootstrap creates branches directly; no PR needed for branch creation.

---

## Objective

<!--
Describe what branches need to be created, in which repos, and any prerequisites.
Focus on unblocking other agents to work in parallel.
-->

---

## Reference Points

<!--
Reference existing branch naming patterns or setup procedures.

Example:
- **Branch naming**: Follow existing pattern `feature/<workpack-slug>`
- **Git workflow**: See README.md for branch conventions
-->

- **Pattern reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT must be set up, not HOW (the agent knows git commands).

Example:
- Create feature root branch from main
- Ensure branch is pushed to origin
- Verify clean git status
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Scope

### In Scope

- Creating feature branches
- Pushing branches to origin
- Verifying clean git status

### Out of Scope

- Code implementation (handled by A1–A4 agents)

---

## Acceptance Criteria

- [ ] Feature branch exists in repository
- [ ] Branch is pushed to origin
- [ ] `git status` shows clean state

---

## Constraints

- **CRITICAL**: Never push to `main` without a PR (unless direct push delivery mode)
- Branch names must follow project convention: `feature/<workpack-slug>`

---

## Verification

### Commands

```bash
# Verify branch exists
git branch -a | grep feature/<slug>

# Verify clean git status
git status
```

### Verification Checklist

- [ ] Feature branch created and pushed
- [ ] Git status is clean

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A0_bootstrap.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A0_bootstrap",
  "component": "bootstrap",
  "delivery_mode": "direct_push",
  "branch": {
    "base": "main",
    "work": "feature/<slug>",
    "merge_target": "main"
  },
  "repos": ["FurlanG2P"],
  "artifacts": {
    "pr_url": "",
    "commit_shas": []
  },
  "changes": {
    "files_modified": [],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "change_details": [],
  "verification": {
    "commands": [],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": {
    "model": "",
    "tokens_in": 0,
    "tokens_out": 0,
    "duration_ms": 0
  },
  "handoff": {
    "summary": "",
    "next_steps": ["A1, A2, A3 can now proceed on their respective branches"],
    "known_issues": []
  },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- Branch already exists with conflicting content
- Permission issues prevent pushing to origin

---

## Deliverables

- [ ] All required branches created
- [ ] All branches pushed to origin
- [ ] Output JSON created in `outputs/A0_bootstrap.json`
- [ ] Other agents unblocked to proceed
