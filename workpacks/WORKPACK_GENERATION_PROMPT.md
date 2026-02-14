# Workpack Generation Prompt — Protocol v5

> **Purpose**: Meta-prompt for AI agents (GitHub Copilot, Claude, etc.) to generate high-quality, agent-centric workpacks following Protocol v5.

---

## Quick Start

1. **Attach this prompt** as context
2. **Append your request** at the end
3. **Submit to the AI agent**
4. **Review the output** and commit to `workpacks/`

---

## System Instructions

You are an expert software architect generating **workpacks** for parallel AI agent execution. Your task is to create a complete workpack following **Protocol v5** conventions.

### Protocol v5 Core Principles

1. **Agent-Centric**: Prompts describe WHAT to implement, not HOW. Agents are implementers, not copy-pasters.
2. **Semantic References**: Point to existing patterns by class/method name, NEVER by line numbers.
3. **80/20 Rule**: Maximum 20% of a prompt can be code (signatures only). 80%+ must be prose.
4. **Integration as Reviewer**: A5 agent validates all work, runs tests, and authorizes merge.
5. **Mandatory Verification Gate**: Every workpack MUST include at least one verification prompt (`A5_integration_meta.md` or `V#_verify.md`). The linter will error if absent.
6. **V-Loop for Bug Fixes**: When B-series prompts exist, a `V2_bugfix_verify.md` prompt is created and executed iteratively until all bugs are confirmed resolved.
7. **B-Series Severity**: Every B-series prompt MUST declare a severity (`blocker`, `major`, `minor`).
8. **Subagent Parallelization**: Agents SHOULD spawn subagents (e.g., Copilot, Codex) to parallelize independent subtasks within a single prompt.
9. **Task Tracking**: Agents SHOULD maintain a structured todo list (e.g., `manage_todo_list`) to track multi-step work, provided the tool/model supports it.

---

## Your Output Must Include

1. `00_request.md` — Formatted request with acceptance criteria (Protocol Version: 5)
2. `01_plan.md` — Work Breakdown Structure with parallelization map, DAG, and cross-workpack refs
3. `prompts/*.md` — One prompt file per agent (following v5 structure with YAML front-matter)
4. `prompts/A5_integration_meta.md` — **MANDATORY** verification/merge reviewer prompt
5. `prompts/V2_bugfix_verify.md` — Created automatically when B-series prompts exist
6. `outputs/.gitkeep` — Placeholder for handoff JSONs
7. `99_status.md` — Status tracking template (with V-series, R-series sections)

---

## ⚠️ ANTI-PATTERNS — NEVER DO THIS

### ❌ Complete Code Implementations

```markdown
<!-- WRONG: This defeats the purpose of agent parallelization -->
## Step 3: Create the Service

\`\`\`csharp
public class ExerciseService : IExerciseService
{
    private readonly IRepository<Exercise> _repository;
    // ... 50 lines of code ...
}
\`\`\`
```

### ❌ Line Number References

```markdown
<!-- WRONG: Line numbers become stale immediately -->
See lines 45-89 of UserService.cs for the pattern.
```

### ❌ Vague Pattern References

```markdown
<!-- WRONG: Too vague, agent can't find the pattern -->
Implement it like we usually do.
```

---

## ✅ CORRECT PATTERNS

### ✅ Semantic References

```markdown
## Reference Points

- **Service pattern**: Follow the structure of `UserService` class in `src/Services/`
- **Repository pattern**: Implement like `ExerciseRepository.GetByIdAsync` method
- **Error handling**: Apply the try-catch-log pattern from `ApiControllerBase.HandleRequest`
```

### ✅ Behavioral Requirements

```markdown
## Implementation Requirements

- The service must validate input before processing
- Failed lookups should return null, not throw exceptions
- All async methods must accept CancellationToken
- Logging should occur at Information level for successful operations
```

### ✅ Contract Signatures Only (when new)

```markdown
## Contracts

### IExerciseService (new interface)

| Method | Returns | Notes |
|--------|---------|-------|
| GetByIdAsync(Guid, CancellationToken) | Task<Exercise?> | Returns null if not found |
| CreateAsync(CreateExerciseDto, CancellationToken) | Task<Exercise> | Validates before creation |
```

---

## Workpack Structure Specification

### Folder Naming Convention

```
YYYY-MM-DD_<category>_<short-slug>/
```

| Component | Format | Examples |
|-----------|--------|----------|
| Date | `YYYY-MM-DD` (ISO 8601) | `2026-01-31` |
| Category | `feature`, `refactor`, `hotfix`, `bugfix`, `debug`, `docs`, `perf`, `security` | `feature` |
| Slug | Kebab-case, 2-5 words | `user-authentication` |

### Required Files

```
workpacks/instances/YYYY-MM-DD_<category>_<short-slug>/
├── 00_request.md
├── 01_plan.md
├── prompts/
│   ├── A0_bootstrap.md          (optional)
│   ├── A1_library.md            (if library work needed)
│   ├── A2_cli.md                (if CLI work needed)
│   ├── A3_tests.md              (if test infrastructure needed)
│   ├── A4_ml.md                 (if ML model work needed)
│   ├── A5_integration_meta.md   (ALWAYS required — Merge Reviewer / V1 gate)
│   ├── B#_<comp>_<desc>.md      (post-implementation bug fixes, with ## Severity)
│   ├── V2_bugfix_verify.md      (created when B-series exist — V-loop gate)
│   └── R1_retrospective.md      (post-merge retrospective — v5)
├── outputs/
│   └── .gitkeep
└── 99_status.md
```

---

## File Specifications

### 00_request.md Structure

```markdown
# Request

## Workpack Protocol Version

Workpack Protocol Version: 5

## Original Request

<Verbatim copy of the user's request>

## Acceptance Criteria

- [ ] AC1: Specific, testable criterion
- [ ] AC2: Specific, testable criterion

## Constraints

- Constraint 1
- Constraint 2

## Acceptance Criteria → Verification Mapping

| AC ID | Criterion | How to Verify |
|-------|-----------|---------------|
| AC1 | Description | Command or test |
| AC2 | Description | Command or test |

## Delivery Mode

- [x] **PR-based** (default)
- [ ] **Direct push**

## Scope

### In Scope
- Item 1

### Out of Scope
- Item 1
```

### 01_plan.md Structure

```markdown
# Plan

## Summary

<One paragraph summarizing all work>

## Work Breakdown Structure (WBS)

| # | Task | Agent | Depends On | Effort |
|---|------|-------|------------|--------|
| 1 | Task | A1_library | - | S |
| 2 | Task | A2_cli | 1 | M |

**Effort**: XS <30min, S 30min-2h, M 2h-4h, L 4h-8h

## DAG Dependencies (v5)

Prompts declare dependencies in YAML front-matter (`depends_on`). The plan MUST document the DAG:

| Prompt | depends_on | repos |
|--------|-----------|-------|
| A0_bootstrap | [] | [] |
| A1_library | [A0_bootstrap] | [FurlanG2P] |
| A2_cli | [A0_bootstrap] | [FurlanG2P] |
| A5_integration_meta | [A1_library, A2_cli] | [FurlanG2P] |

## Cross-Workpack References (v5)

If this workpack depends on another workpack being completed first, declare it:

```yaml
requires_workpack:
  - 2026-01-24_feature_exercise-content-backend-signalr-transport
```

## Parallelization Map

\`\`\`
Phase 0 (sequential):
  └── A0_bootstrap.md

Phase 1 (parallel):
  ├── A1_library.md  ─┐
  ├── A2_cli.md      ─┼──► Phase 2
  └── A3_tests.md    ─┘

Phase 2 (sequential — verification gate V1):
  └── A5_integration_meta.md (Merge Reviewer)
        ├── PASS ──► MERGE ✅
        └── FAIL ──► Phase 3

Phase 3 (parallel — bug fixes, if any):
  ├── B1_xxx.md ─┐
  ├── B2_xxx.md ─┼──► Phase 4
  └── B3_xxx.md ─┘

Phase 4 (sequential — V-loop):
  └── V2_bugfix_verify.md
        ├── PASS ──► MERGE ✅
        └── FAIL ──► New B-series → re-run V2

Phase 5 (post-merge — retrospective, v5):
  └── R1_retrospective.md
\`\`\`

## Branch Strategy

| Component | Branch | Base | PR Target |
|-----------|--------|------|-----------|
| Feature | feature/<slug> | main | main |

## Risks and Mitigations

| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| Risk 1 | Med | High | Strategy |

## Security & Tool Safety

- No secrets in prompts or outputs
- Limit writes to repository workspace only

## Handoff Outputs Plan (Protocol v5)

- Each prompt produces `outputs/<PROMPT>.json` on completion
- Schema: `workpacks/WORKPACK_OUTPUT_SCHEMA.json`
- Output JSON MUST include `repos` (repos touched) and `execution` (model, tokens, duration)
- Output JSON SHOULD include `change_details` (per-file action/lines summary)
- A5 validates all outputs before merge

## Integration Agent Role

A5_integration_meta acts as **Merge Reviewer** (V1 verification gate):
1. Validates all agent output JSONs
2. Runs tests: `python -m pytest tests/ -v`
3. Runs type/lint checks: `mypy src/ tests/` + `ruff check src/ tests/`
4. Cross-checks all acceptance criteria
5. Authorizes or blocks merge
6. If blocked: generates B-series prompts with mandatory `## Severity`

> **Note (v5)**: `A5` is a **fixed role name** — always `A5_integration_meta.md`, even if A3/A4 are absent. Do NOT renumber to A3.

## V-Loop (Post-Bugfix Verification)

When B-series prompts exist:
1. After all B-series prompts are resolved, execute `V2_bugfix_verify.md`
2. V2 re-runs all tests, verifies each bug is fixed, checks AC
3. If V2 finds **new** issues → generate new B-series prompts → re-run V2
4. The loop terminates when V2 passes clean
5. Output JSON tracks `"iteration"` count

## R-Series Retrospective (v5)

After the workpack is **merged**, execute `R1_retrospective.md`:
1. Summarise what went well, what didn't, and root causes
2. Record execution cost (model, tokens, duration) from all output JSONs
3. Rate estimation accuracy (planned effort vs actual)
4. Capture lessons learned and style-guide update proposals
5. Note cross-workpack observations for future planning

## Subagent Parallelization

Agents SHOULD leverage subagent capabilities when available:
- Spawn subagents for independent subtasks within a prompt (e.g., creating multiple files simultaneously)
- Use subagents for parallel research/investigation tasks
- Document subagent usage in the output JSON `handoff.summary`

## CHANGELOG Enforcement

When introducing a new protocol version, update `workpacks/CHANGELOG.md` with the new version entry.
```

---

## Agent Prompt Structure (v5)

Every prompt MUST follow this structure:

```markdown
---
depends_on: []   # YAML front-matter: list of prompt stems this depends on
repos: []        # YAML front-matter: list of repos this prompt touches
---
# <Agent> Agent Prompt

> One-line objective summary.

---

## READ FIRST

- List of files to read

## Context

Workpack name and one-line objective.

## Delivery Mode

PR-based or direct push.

## Objective

Detailed description of WHAT to accomplish (1-3 paragraphs).
Focus on end goal, NOT implementation.

## Reference Points

Semantic references to existing patterns.
Use class/method names, NOT line numbers.

## Implementation Requirements

Behavioral specifications.
Describe WHAT, NOT HOW.

## Contracts

New interfaces/DTOs (signatures only) or references to existing.

## Subagent Strategy

Identify subtasks that can be delegated to subagents for parallel execution.

## Task Tracking

Remind the agent to use a structured todo list for multi-step work (if supported by the tool/model).

## Scope

In/out of scope.

## Acceptance Criteria

Testable criteria from 00_request.md.

## Constraints

Hard rules.

## Verification

Commands and checklist.

## Handoff Output (JSON)

Output JSON skeleton.

## Stop Conditions

When to escalate.

## Deliverables

Final checklist.
```

---

## B-Series Prompts (Bug Fixes)

B-series prompts are created after initial implementation when bugs are discovered.

### Naming Convention

```
B#_<component>_<description>.md
```

Examples: `B1_library_oov_handling.md`, `B2_cli_batch_error.md`

### Key Differences from A-series

- Work on feature branch directly, no sub-branch
- Must describe problem (expected vs actual behavior)
- Reference Points to help find fix pattern
- Regression test strongly encouraged
- **Mandatory `## Severity` section** with value: `blocker`, `major`, or `minor`

### V-Series: Verification Prompts

V-series prompts are verification gates. They do NOT implement code — they validate work done by others.

| Prompt | Purpose |
|--------|---------|
| `A5_integration_meta.md` | Primary verification gate (V1) — always required |
| `V2_bugfix_verify.md` | Post-bugfix verification gate (V-loop) — required when B-series exist |

**V-loop iteration**: V2 is a single prompt that runs iteratively. Each iteration:
1. Re-runs tests and verifies each B-series fix
2. If new bugs found → generates new B-series → re-runs V2
3. Terminates when all checks pass

---

## 99_status.md Structure

```markdown
# Status

## Overall Status

🔴 Not Started | 🟡 In Progress | 🟢 Complete

## Artifacts

- [ ] `00_request.md` created
- [ ] `01_plan.md` created
- [ ] All prompts created
- [ ] `outputs/` folder exists

## Agent Progress

### A-Series

| Prompt | Status | Output JSON | Notes |
|--------|--------|-------------|-------|
| A0_bootstrap | ⏳ Pending | ❌ | |
| A1_library | ⏳ Pending | ❌ | |

### B-Series

| Prompt | Severity | Status | Output JSON | Notes |
|--------|----------|--------|-------------|-------|
| (none yet) | | | | |

### V-Series

| Prompt | Iteration | Status | Notes |
|--------|-----------|--------|-------|
| V2_bugfix_verify | 0 | ⏳ Pending | |

### R-Series (v5)

| Prompt | Status | Notes |
|--------|--------|-------|
| R1_retrospective | ⏳ Pending | Post-merge |

## Pull Requests

- [ ] Library PR: (link)
- [ ] CLI PR: (link)

## Merge Order

1. A1_library
2. A2_cli
3. A5_integration_meta (Merge Reviewer)
```

---

## Quality Checklist

Before finalizing output, verify:

### 00_request.md
- [ ] Protocol Version is 5
- [ ] Acceptance criteria are specific and testable
- [ ] AC → Verification mapping complete

### 01_plan.md
- [ ] WBS covers all work
- [ ] Parallelization maximized
- [ ] A5 described as Merge Reviewer
- [ ] DAG dependencies documented

### Prompts
- [ ] NO complete code implementations
- [ ] 80/20 rule followed (max 20% code)
- [ ] Reference Points use semantic names
- [ ] Implementation Requirements are behavioral
- [ ] Verification commands are runnable
- [ ] YAML front-matter with `depends_on` and `repos`

### A5_integration_meta.md (MANDATORY)
- [ ] Includes standard test suite execution
- [ ] Includes acceptance criteria cross-check
- [ ] Includes output validation steps
- [ ] Named exactly `A5_integration_meta.md` (fixed role, never renumbered)

### B-series
- [ ] Every B-series prompt has `## Severity` section
- [ ] Severity is one of: `blocker`, `major`, `minor`

### V2_bugfix_verify.md (if B-series exist)
- [ ] Created when B-series prompts exist
- [ ] Includes V-loop iteration tracking
- [ ] Includes B-series resolution checklist

### Task Tracking
- [ ] Prompts remind agents to use a todo list for multi-step work
- [ ] Complex prompts (A5, V2) explicitly include a `## Task Tracking` section

### R-Series Retrospective (v5)
- [ ] `R1_retrospective.md` created from template
- [ ] Plan mentions R-series as post-merge step

---

## Your Task

Generate a complete workpack for the request below. Follow Protocol v5 exactly.

**Output each file in a separate code block with the filename as a header.**

---

**User Request:**

<PASTE YOUR REQUEST BELOW THIS LINE>
