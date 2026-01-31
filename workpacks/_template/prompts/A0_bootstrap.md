# Bootstrap Agent Prompt

> Prompt for the bootstrap agent to set up branches and prerequisites.

---

## READ FIRST

Read these files before starting:

1. `./README.md` — Project overview
2. `./AGENTS.md` — Agent guidelines
3. `./workpacks/<workpack>/00_request.md` — Original request
4. `./workpacks/<workpack>/01_plan.md` — Full plan with branch strategy
5. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v3)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary: typically "Set up feature branch and prerequisites" -->

---

## Delivery Mode

- **Direct push**: Bootstrap creates branches directly; no PR needed for branch creation.

---

## Objective

<!--
Describe what branches need to be created and any prerequisites.
Focus on unblocking other agents to work in parallel.
-->

---

## Reference Points

<!--
Reference existing branch naming patterns or setup procedures.

Example:
- **Branch naming**: Follow existing pattern `feature/<workpack-slug>`
-->

- **Pattern reference 1**: <!-- Description -->

---

## Implementation Requirements

<!--
Describe WHAT must be set up, not HOW (the agent knows git commands).

Example:
- Create feature branch from main
- Ensure branch is pushed to origin
- Verify clean git status
-->

- Requirement 1
- Requirement 2
- Requirement 3

---

## Scope

### In Scope

- Creating feature branch
- Pushing branch to origin
- Verifying clean git status

### Out of Scope

- Code implementation (handled by A1-A4 agents)

---

## Acceptance Criteria

- [ ] Feature branch exists
- [ ] Branch is pushed to origin
- [ ] `git status` shows clean state

---

## Constraints

- **CRITICAL**: Never force push to main
- Branch name must follow `feature/<slug>` pattern

---

## Verification

### Commands

```bash
# Verify branch exists
git branch -a | grep feature/<slug>

# Verify clean status
git status
```

### Checklist

- [ ] Branch created
- [ ] Branch pushed to origin
- [ ] Clean git status

---

## Handoff Output (JSON) — REQUIRED

After completing the work, create/update:

**Path**: `./workpacks/<workpack>/outputs/A0_bootstrap.json`

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
  "artifacts": {
    "commit_shas": ["<sha>"]
  },
  "changes": {
    "files_modified": [],
    "files_created": [],
    "contracts_changed": [],
    "breaking_change": false
  },
  "verification": {
    "commands": [
      { "cmd": "git branch -a", "result": "pass" }
    ]
  },
  "handoff": {
    "summary": "Created feature branch feature/<slug>",
    "known_issues": [],
    "next_steps": ["Proceed with A1-A4 implementation"]
  }
}
```

---

## Stop Conditions

### Continue if:
- Git commands succeed

### Escalate if:
- Branch already exists with conflicting changes
- Permission issues with remote

---

## Deliverables

- [ ] Feature branch created and pushed
- [ ] `outputs/A0_bootstrap.json` created
- [ ] `99_status.md` updated with A0 status
