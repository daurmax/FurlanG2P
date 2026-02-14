# Workpacks — Versioned Prompt History

A **workpack** is a durable, git-tracked record of work requested from AI agents. It preserves the full lifecycle of a request: the original ask, the breakdown plan, prompts dispatched to downstream agents, and final status.

> **Purpose**: Ensure every non-trivial request leaves a traceable artifact in version control—enabling replay, auditing, and learning from past decisions.

> **📁 Template Location**: All templates live under `./workpacks/_template/`. Copy from there when creating a new workpack.

---

## Workpack Meta Prompt (Copilot) — Recommended Entry Point

**For GitHub Copilot workflows**, the recommended way to create and manage workpacks is to use the **Workpack Meta Prompt**:

📄 **Location**: `./workpacks/WORKPACK_META_PROMPT.txt`

This is a single, paste-ready "router" prompt that drives the complete workpack workflow end-to-end in Copilot agentic mode.

### How to Use (Step-by-Step)

1. **Copy** the entire contents of `WORKPACK_META_PROMPT.txt`
2. **Edit ONLY** the "USER REQUEST (EDIT ONLY THIS SECTION)" block:
   - Set `Request Type` (NEW_FEATURE, BUGFIX, REFACTOR, etc.)
   - Provide a kebab-case slug (2–5 words)
   - Paste your request summary
   - Add any constraints or notes
   - Set delivery mode (PR or DIRECT_PUSH)
   - Set target base branch
3. **Paste** the entire edited file into GitHub Copilot Chat or agentic mode
4. **Copilot will route** your request:
   - NEW_FEATURE/REFACTOR/DOCS/PERF/SECURITY/DEBUG → `WORKPACK_GENERATION_PROMPT.md`
   - BUGFIX → `WORKPACK_BUG_REPORT_PROMPT.md`
5. **Copilot enforces** Workpack Protocol v2 (outputs + status) automatically

### Non-Negotiables (Always Enforced)

- ✅ Always read and follow `workpacks/README.md` (this file)
- ✅ Workpack Protocol Version must be **5** for v5 behavior
- ✅ `outputs/` folder and `99_status.md` must be maintained
- ✅ Never mark a prompt completed unless `outputs/<PROMPT>.json` exists and is updated
- ✅ Never include secrets, API keys, or credentials in prompts or outputs
- ✅ All B-series prompts must include `## Severity` (v4+)
- ✅ V-series verification gates are mandatory (v4+)
- ✅ YAML front-matter (`depends_on`, `repos`) in all prompts (v5)
- ✅ `execution` block in all output JSONs (v5)
- ✅ R-series retrospective after merge (v5)

### Why Use the Meta Prompt?

- **Single source of truth**: One file to copy, one place to edit your request
- **Automatic routing**: Copilot picks the right workflow (feature vs bugfix)
- **Protocol v2 compliance**: Built-in enforcement of outputs + status rules
- **No clarifying questions**: Copilot makes reasonable assumptions and proceeds
- **Consistent structure**: All workpacks follow the same conventions

> **Note**: For manual/ChatGPT-based workflows, you can still use `WORKPACK_GENERATION_PROMPT.md` or `WORKPACK_BUG_REPORT_PROMPT.md` directly. See sections below.

---

## What Is a Workpack?

A workpack captures:

| Artifact | Description |
|----------|-------------|
| **Request** | The original user request, acceptance criteria, and constraints |
| **Plan** | Work Breakdown Structure (WBS), sequencing, parallelization map, risks |
| **Prompts** | One prompt file per downstream agent (library, CLI, tests, ML, docs, integration) |
| **Status** | Checklist of completion, links to PRs, merge order (optional) |

Workpacks are **always committed to git**. They are never placed in `temp/` or ignored.

---

## Naming Convention

Each workpack lives in its own folder under `./workpacks/instances/`.

**Folder name format:**

```
YYYY-MM-DD_<category>_<short-slug>
```

| Component | Description | Examples |
|-----------|-------------|----------|
| `YYYY-MM-DD` | Creation date (ISO 8601) | `2026-01-22` |
| `<category>` | Work type: `feature`, `refactor`, `hotfix`, `bugfix`, `debug`, `docs`, `perf`, `security` | `feature`, `bugfix` |
| `<short-slug>` | Kebab-case slug (2–5 words) describing the work | `new-exercise`, `login-crash` |

**Examples:**

- `2026-01-22_feature_new-exercise`
- `2026-01-22_refactor_backend-di-cleanup`
- `2026-01-22_bugfix_login-crash`
- `2026-01-22_hotfix_urgent-security-patch`
- `2026-01-22_debug_session-timeout`

> **v5**: Instances live under `workpacks/instances/`, not directly under `workpacks/`.

**Category Clarification:**
- `bugfix` = standard fix for discovered issues
- `hotfix` = urgent fix requiring immediate deployment (if used)

---

## Required Contents

Every workpack folder MUST contain:

```
workpacks/
└── instances/
    └── YYYY-MM-DD_<category>_<short-slug>/
        ├── 00_request.md          # Original request, acceptance criteria, constraints
        ├── 01_plan.md             # WBS, parallelization map, sequencing, risks
        ├── prompts/               # Prompts for downstream agents
        │   ├── A0_bootstrap.md    # (optional) Shared branch creation, unblocking steps
        │   ├── A1_library.md      # Library agent prompt
        │   ├── A2_cli.md          # CLI agent prompt
        │   ├── A3_tests.md        # Tests agent prompt
        │   ├── A4_ml.md           # ML agent prompt
        │   ├── A5_integration_meta.md  # Integration agent prompt (V1 gate)
        │   ├── V_bugfix_verify.md     # (v4+) Post-bugfix verification V-loop prompt
        │   ├── R1_retrospective.md    # (v5) Post-merge retrospective
        │   ├── B1_<component>_<fix-name>.md  # (optional) Post-implementation bug fix
        │   ├── B2_<component>_<fix-name>.md  # (optional) Additional bug fix
        │   └── ...                # Additional bug fixes as needed
        ├── outputs/               # (Protocol v2+) Structured handoff JSON outputs
        │   ├── A1_library.json    # Output for A1 prompt (created when complete)
        │   ├── A2_cli.json        # Output for A2 prompt (created when complete)
        │   └── ...                # One JSON per completed prompt
        └── 99_status.md           # (optional) Checklist, PR links, merge order
```

> **Note (Protocol v2)**: The `outputs/` folder contains structured handoff JSON files. Each output file is named exactly like its corresponding prompt (same basename, `.json` extension).

> **Note**: Copy from `workpacks/_template/` when creating a new workpack. See [Template](#template) section.

### File Descriptions

| File | Required | Purpose |
|------|----------|---------|
| `00_request.md` | ✅ | Captures the original request verbatim, plus acceptance criteria and hard constraints |
| `01_plan.md` | ✅ | Contains the Work Breakdown Structure, task sequencing, parallelization notes, and risks |
| `prompts/` | ✅ | Folder containing one prompt file per downstream agent |
| `prompts/A0_bootstrap.md` | ❌ | Optional: steps to create shared branches or unblock prerequisites |
| `prompts/A1_library.md` | ❌ | Prompt for library agent (if library work is needed) |
| `prompts/A2_cli.md` | ❌ | Prompt for CLI agent (if CLI work is needed) |
| `prompts/A3_tests.md` | ❌ | Prompt for tests agent (if test infrastructure needed) |
| `prompts/A4_ml.md` | ❌ | Prompt for ML agent (if ML model work is needed) |
| `prompts/A5_integration_meta.md` | ❌ | Prompt for meta-repo integration (V1 verification gate in v4) |
| `prompts/V_bugfix_verify.md` | ❌ | (v4+) Post-bugfix V-loop verification prompt |
| `prompts/R1_retrospective.md` | ❌ | (v5) Post-merge retrospective |
| `prompts/B#_*.md` | ❌ | Post-implementation bug fix prompts (added after initial implementation) |
| `99_status.md` | ❌ | Optional: tracks completion status, PR links, merge order |

> **Tip**: Only include prompt files for agents that will actually be invoked. Delete unused templates.

---

## Prompt Naming Convention

### A-Series: Feature Implementation Prompts

These prompts are created during initial workpack planning and cover the main implementation work.

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `A0_` | Bootstrap/setup (branch creation, prerequisites) | `A0_bootstrap.md` |
| `A1_` | Library implementation | `A1_library.md` |
| `A2_` | CLI implementation | `A2_cli.md` |
| `A3_` | Tests / test infrastructure | `A3_tests.md` |
| `A4_` | ML model interface | `A4_ml.md` |
| `A5_` | Integration and merge (V1 verification gate) | `A5_integration_meta.md` |

> **A5 is a fixed role name** (v4+): Never renumber A5. The integration/verification role always uses the A5 prefix.

### R-Series: Retrospective Prompts (Protocol v5)

These prompts are executed **after merge** for continuous improvement.

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `R1` | Post-merge retrospective | `R1_retrospective.md` |

> **R-series**: Captures lessons learned, execution cost, estimation accuracy. Uses `_template/prompts/R_retrospective.md`.

### V-Series: Verification Prompts (Protocol v4+)

These prompts are mandatory verification gates introduced in Protocol v4.

| Prefix | Purpose | Examples |
|--------|---------|----------|
| `V1` | Integration verification (built into A5) | A5 acts as V1 gate |
| `V2` | Post-bugfix V-loop verification | `V_bugfix_verify.md` |

> **V-Loop**: V2 is a single prompt that runs iteratively. Do NOT create V3, V4, etc. Re-run V2 with updated context.

### B-Series: Post-Implementation Bug Fix Prompts

These prompts are added **after initial implementation** when bugs or issues are discovered during testing or integration. They are numbered sequentially and include a descriptive name.

| Prefix | Purpose | Naming Pattern |
|--------|---------|----------------|
| `B1_` | First bug fix | `B1_<component>_<fix-description>.md` |
| `B2_` | Second bug fix | `B2_<component>_<fix-description>.md` |
| `B3_` | Third bug fix | `B3_<component>_<fix-description>.md` |
| ... | Additional bug fixes | Continue numbering sequentially |

**Examples:**
- `B1_library_oov_handling.md` — Fix OOV words not falling through to rules
- `B2_cli_batch_error.md` — Fix batch processing error on empty input
- `B3_tests_golden_set_mismatch.md` — Fix golden set test expected values

**When to create B-series prompts:**
1. Initial implementation (A-series) is complete and merged
2. Integration testing reveals bugs or issues
3. User feedback identifies problems
4. New requirements emerge that fit within the workpack scope

**B-series prompt structure:**
- Same structure as A-series prompts
- Must reference the original workpack context
- Should specify working on the feature root branch (not a new sub-branch)
- Must update `01_plan.md` and `99_status.md` to reflect new work
- Must include `## Severity` section with blocker/major/minor classification (v4)
- Must include `"severity"` field in output JSON (v4)

---

## Workpack Protocol v2 — Structured Handoffs (outputs/)

Workpack Protocol v2 introduces **structured handoffs** for reliable agent-to-agent communication and audit/replay capabilities.

### Key Rules

- **Declaration**: Workpacks v2 declare `Workpack Protocol Version: 2` in `00_request.md`.
- **Mapping rule**: `prompts/<PROMPT>.md` → `outputs/<PROMPT>.json` (same basename).
- **Schema conformance**: Every JSON must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`.
- **Purpose**: Reliable agent-to-agent handoff + audit/replay + automated validation.
- **Prohibition**: Do NOT include secrets/keys/tokens in outputs.

### When to Create Output Files

- Agents create/update output JSON files **after completing** their assigned prompt.
- The `outputs/` folder should exist in the workpack; individual JSON files are created on completion.
- **Output files are required** only for prompts marked as completed in `99_status.md`.
- Prompts not marked as completed do not require output files.

### Completion Markers Recognized by Tooling

The workpack linter recognizes the following completion markers in `99_status.md`:

**A-series prompts** (feature implementation):
- 🟢 Complete
- 🟢 Done
- ✅ Applied
- ✅ Done
- ✅ Completed

**B-series prompts** (bug fixes):
- ✅ Fixed
- ✅ Resolved
- ✅ Done

When any of these markers appears on the same line as a prompt basename, the linter considers that prompt completed and expects a corresponding output JSON file.

### Schema Location

The formal JSON schema is at: `workpacks/WORKPACK_OUTPUT_SCHEMA.json`

### outputs/ + status enforcement (Protocol v2)

**Critical completion rules:**

1. **Output JSON is REQUIRED only when a prompt is marked completed** in `99_status.md`
   - Prompts not marked completed do NOT require output JSON yet
   - This allows incremental work without requiring immediate outputs

2. **Completion is INVALID unless BOTH conditions are met:**
   - ✅ `99_status.md` contains a completion marker (✅ Done, 🟢 Complete, etc.)
   - ✅ `outputs/<PROMPT>.json` exists and is properly updated

3. **Never include secrets in outputs:**
   - ❌ No API keys, tokens, passwords, or credentials
   - ✅ Use references to secure storage (e.g., "stored in Azure Key Vault")
   - ✅ Use placeholder values in examples

**When agents must create output files:**
- After completing all work described in a prompt
- Before marking that prompt as completed in `99_status.md`
- Using the schema at `workpacks/WORKPACK_OUTPUT_SCHEMA.json`

**Validation:**
- Use `workpacks/tools/workpack_lint.py` to validate outputs match status
- The linter auto-creates a virtual environment in `tools/.venv/` and re-runs inside it
- The linter will flag completed prompts missing output JSON
- The linter will validate JSON against the schema

---

## Workpack Protocol v3 — Agent-Centric Prompts

Protocol v3 introduces an **agent-centric paradigm** where prompts describe *what* to implement, not *how*. This ensures agents are true implementers, not copy-pasters.

### Key Principles

1. **NO_CODE_BLOCKS**: Prompts must not contain complete code implementations
   - Maximum 20% of a prompt can be code (signatures/interfaces only)
   - 80%+ must be prose: objectives, requirements, reference points

2. **SEMANTIC_REFERENCES**: Point to patterns by class/method name, never line numbers
   - ✅ `"Follow the pattern of UserService.CreateAsync method"`
   - ❌ `"See lines 45-89 of UserService.cs"`

3. **INTEGRATION_AS_REVIEWER**: A5 agent is the Merge Reviewer
   - Validates all agent output JSONs
   - Runs test suites (`pytest`, `mypy`, `ruff`)
   - Cross-checks acceptance criteria
   - Can block merge if verification fails

### Style Guide

See `_template/prompts/PROMPT_STYLE_GUIDE.md` for comprehensive guidance on writing agent-centric prompts.

---

## Workpack Protocol v4 — Verification Gates, Severity & Subagent Parallelization

Protocol v4 builds on v3 and introduces **mandatory verification gates**, **B-series severity**, **iterative V-loop**, **subagent parallelization guidance**, and **budget-aware bug tracking**.

### Key Principles (v4 additions)

1. **MANDATORY_VERIFICATION**: Every workpack must have at least one verification gate (A5/V1)
2. **V_LOOP**: Post-bugfix verification runs iteratively until convergence
3. **B_SERIES_SEVERITY**: Every bug report must be classified as blocker/major/minor
4. **SUBAGENT_PARALLELIZATION**: Prompts document parallelizable sub-tasks for spawning subagents
5. **A5_FIXED_ROLE**: A5 is a permanent role name — never renumber it
6. **BUDGET_WARNINGS**: >5 B-series emits warning; >8 suggests re-scoping
7. **CHANGELOG_ENFORCEMENT**: Every workpack must update CHANGELOG.md in affected repos

### v4 Lifecycle

```
A0 → A1–A4 (parallel) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE
```

### V-Series Verification Prompts

| Gate | When | Purpose |
|------|------|---------|
| **V1 (A5 gate)** | After all A-series complete | Integration verification: tests, AC cross-check, merge decision |
| **V2 (V-loop)** | After B-series fixes applied | Post-bugfix verification; iterates until all pass |

**V-Loop rules**:
- V2 is a **single prompt** re-run iteratively (never create V3, V4, etc.)
- Track iterations via `"iteration"` field in output JSON
- V2 can generate new B-series if new issues found
- V-loop terminates when: all tests pass + all B-series resolved + all AC satisfied

### B-Series Severity

Every B-series prompt must include a `## Severity` section:

| Level | Definition |
|-------|------------|
| **blocker** | Prevents merge; must fix before V-loop can pass |
| **major** | Significant defect; should fix in this workpack |
| **minor** | Low-impact; can defer to follow-up workpack |

### B-Series Budget

| Threshold | Action |
|-----------|--------|
| ≤5 | Normal workflow |
| 6–8 | Emit `"b_series_budget_warning": true` in V2 output |
| >8 | Suggest re-scoping; workpack may be too large |

### Subagent Parallelization

Prompts may include a `## Subagent Strategy` section documenting tasks that can be delegated to parallel subagents:

```markdown
## Subagent Strategy

This agent may spawn subagents for parallelizable tasks:

- **Subagent 1**: Run `pytest` test suite
- **Subagent 2**: Run `mypy` and `ruff` checks

> Document subagent usage in the output JSON `handoff.summary`.
```

Guidelines:
- Sub-tasks must be independent (no shared mutable state)
- Parent agent integrates results
- Document usage in handoff output

### Task Tracking

Prompts encourage agents to maintain a **structured todo list** (e.g., `manage_todo_list`) to track multi-step work.

- Agents SHOULD create a todo list before starting complex work
- Mark each step in-progress before starting, completed immediately after
- Especially important for A5 (verification), V2 (V-loop iterations), and multi-file implementations
- Task tracking is a recommendation — not all tools/models support it

### Migration from v3

Use `MIGRATION_PROMPT.md` to convert v3 workpacks to v4. Key changes:
1. Add `## Severity` to all B-series prompts
2. Add V2_bugfix_verify.md if B-series exist
3. Update protocol version to 4 in `00_request.md`
4. Ensure A5 naming is correct (fixed role, not renumbered)
5. Update protocol version references in all prompt files

---

## Workpack Protocol v5 — Instances Subfolder, DAG, Multi-Repo, Execution Cost, R-Series

Protocol v5 builds on v4 and introduces **structural** and **observability** improvements.

### Key Principles (v5 additions)

1. **INSTANCES_SUBFOLDER**: Workpack instances live under `workpacks/instances/` (not directly under `workpacks/`)
2. **DAG_DEPENDENCIES**: Prompts declare `depends_on` in YAML front-matter; linter validates for cycles
3. **MULTI_REPO_AWARENESS**: Prompts declare `repos` in YAML front-matter and output JSON
4. **EXECUTION_COST**: Output JSON includes `execution` block (model, tokens, duration) and `change_details`
5. **R_SERIES_RETROSPECTIVE**: Post-merge `R1_retrospective.md` captures lessons and cost analysis
6. **MACHINE_VERIFIABLE_AC**: Acceptance criteria should be testable via commands where possible
7. **CROSS_WORKPACK_REFS**: Plans can declare `requires_workpack` for inter-workpack dependencies
8. **SCAFFOLD_TOOL**: `workpack_scaffold.py` generates prompt skeletons from `01_plan.md`

### v5 Lifecycle

```
A0 → A1–A4 (parallel, DAG-ordered) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE → R1
```

### YAML Front-Matter (v5)

Every prompt (except A0_bootstrap) MUST include:

```yaml
---
depends_on: [A0_bootstrap]   # prompt stems this depends on
repos: [FurlanG2P]           # repos this prompt touches
---
```

### Scaffold Tool (v5)

Generate prompt skeletons from `01_plan.md`:

```bash
python workpacks/tools/workpack_scaffold.py workpacks/instances/<workpack>
```

### Linter v5 Checks

| Check | Level | Description |
|-------|-------|-------------|
| `ERR_DAG_CYCLE` | ERROR | Cycle detected in `depends_on` graph |
| `WARN_DAG_UNKNOWN_DEP` | WARNING | `depends_on` references non-existent prompt |
| `WARN_MISSING_REPOS` | WARNING | A/B-series (except A0) with empty `repos` |
| `WARN_MISSING_EXECUTION` | WARNING | Completed output without `execution` block |

### Migration from v4

Use `MIGRATION_PROMPT.md` to convert v4 workpacks to v5. Key changes:
1. Move instance folder from `workpacks/` to `workpacks/instances/`
2. Add YAML front-matter (`depends_on`, `repos`) to all prompts
3. Add `execution` block to output JSONs
4. Add `R1_retrospective.md` from template
5. Update protocol version to 5 in `00_request.md`

---

## Parallelization Guidelines

To minimize merge conflicts and maximize throughput:

### Safe to Parallelize

| Agent A | Agent B | Why Safe |
|---------|---------|----------|
| Library | CLI | Different modules; no shared files |
| Library | Docs | Different folders; no shared files |
| CLI | Docs | Different folders; minimal overlap |
| Tests | Docs | Different folders; minimal overlap |
| ML | Docs | Different folders; no shared files |

### Must Be Sequential

| First | Then | Why Sequential |
|-------|------|----------------|
| A0_bootstrap | All others | Shared branch must exist before parallel work |
| All component work | A5_integration_meta | Integration depends on all components being done |
| Library core changes | CLI (if interface changes) | CLI depends on library public API |

### Best Practices

1. **Modules vs. Tests**: Work in `src/furlan_g2p/` modules can run in parallel if touching different modules.
2. **Docs vs. Code**: Documentation agents can work in parallel with code agents if they operate in separate folders.
3. **Branch Strategy**: Each agent should work on a feature branch; integration agent merges.
4. **Conflict Zones**: Avoid parallel edits to `README.md` files at repo root—assign one owner.

---

## Git Policy

### MUST

- ✅ Workpacks MUST be committed to git (tracked in version control)
- ✅ Workpacks MUST be created in `./workpacks/instances/`, never in `./temp/`
- ✅ Commit workpack creation as part of the first commit in a feature branch
- ✅ Keep prompts actionable and deterministic (no ambiguous instructions)

### MUST NOT

- ❌ Never store secrets, API keys, or credentials in workpacks
- ❌ Never add workpacks to `.gitignore`
- ❌ Never place workpacks under `./temp/`
- ❌ Never include user-specific paths or machine-specific configuration

### Delivery Mode Policy

| Mode | When to Use | Notes |
|------|-------------|-------|
| **PR-based** (default) | All standard work | Recommended for review and traceability |
| **Direct push** | Only when explicitly requested by the user | Push directly to `main`; record commits in `99_status.md` |

- **PR-based is the default.** Always create a PR unless the user explicitly requests direct push.
- **Direct push is allowed only when explicitly requested.** This bypasses review; use extra caution.
- **Workpacks must state the selected delivery mode** in `00_request.md`.

### Outputs JSON Policy (Protocol v2)

- **MUST be committed**: Output JSON files are part of the workpack record; never treat them as temporary.
- **MUST NOT include secrets**: No API keys, tokens, passwords, or credentials in output files.
- **MUST link artifacts**: Include PR URLs in `artifacts.pr_url` and/or commit SHAs in `artifacts.commit_shas`.

### Branch Policy

| Rule | Description |
|------|-------------|
| **Base branch** | All feature branches MUST be created from `main` |
| **PR target** | All PRs MUST target `main` |
| **Applies to** | FurlanG2P repository |

### Commit Message Convention

When creating a new workpack, use this commit message format:

```
workpack: create <category>/<short-slug>

Creates workpack for: <one-line summary of the request>
```

Example:

```
workpack: create feature/new-exercise

Creates workpack for: Add new exercise type with audio prompts
```

---

## Template

A ready-to-copy template scaffold is available at:

```
./workpacks/_template/
```

To start a new workpack:

1. Copy `workpacks/_template/` to a new folder with the correct naming convention
2. Fill in `00_request.md` with the original request
3. Fill in `01_plan.md` with the breakdown and sequencing
4. Create prompt files under `prompts/` for each required agent
5. Delete any unused prompt templates
6. Commit the workpack immediately

---

## Generating Workpacks with ChatGPT (optional)

> **For GitHub Copilot workflows**, prefer `WORKPACK_META_PROMPT.txt` (see [Workpack Meta Prompt](#workpack-meta-prompt-copilot--recommended-entry-point) section above). Use this section only if you are using ChatGPT directly or working outside of Copilot.

For complex workpacks, you can use ChatGPT (or similar LLMs) to generate the complete workpack structure. A comprehensive meta-prompt is available at:

```
./workpacks/WORKPACK_GENERATION_PROMPT.md
```

### How to use:

1. Copy the entire contents of `WORKPACK_GENERATION_PROMPT.md`
2. Paste your feature request, bug report, or task at the end
3. Submit to ChatGPT
4. Review the generated files and paste them into your workpack folder
5. Adjust as needed and commit

This meta-prompt ensures that ChatGPT generates workpacks that follow all conventions defined in this document.

---

## Adding Bug Fix Prompts with ChatGPT (optional)

> **For GitHub Copilot workflows**, prefer `WORKPACK_META_PROMPT.txt` which routes to `WORKPACK_BUG_REPORT_PROMPT.md` automatically when Request Type is BUGFIX. Use this section only if you are using ChatGPT directly or working outside of Copilot.

When bugs are discovered after initial implementation, you can use ChatGPT to add B-series bug fix prompts to an existing workpack. A dedicated meta-prompt is available at:

```
./workpacks/WORKPACK_BUG_REPORT_PROMPT.md
```

### How to use:

1. Copy the entire contents of `WORKPACK_BUG_REPORT_PROMPT.md`
2. Provide the workpack name (e.g., `2026-01-24_feature_exercise-content-backend-signalr-transport`)
3. Describe the bug(s) you've discovered
4. ChatGPT will generate:
   - New `BX_<component>_<description>.md` prompt file(s)
   - Updates to `01_plan.md` with new bug fix tasks
   - Updates to `99_status.md` with pending status
5. Apply the changes to your workpack folder and commit

This ensures consistent B-series prompt structure and proper tracking of post-implementation fixes.

---

## Common Mistakes

| Mistake | Correction |
|---------|------------|
| Creating template files at repo root | Templates live under `./workpacks/_template/`. Copy from there. |
| Placing workpacks in `./temp/` | Workpacks MUST be created under `./workpacks/instances/`, never in `./temp/`. |
| Forgetting to specify delivery mode | Always set delivery mode in `00_request.md`. PR-based is default. |
| Using relative paths like `_template/` without context | Always use full paths: `workpacks/_template/00_request.md`. |
| Pushing to `main` without review | Prefer PR-based delivery. Direct push only when explicitly requested. |
| Not creating B-series prompts for post-implementation fixes | When bugs are found after integration, create B-series prompts and update plan/status files. |
| Workpack v2+ missing `outputs/` folder | Protocol v2+ workpacks MUST have an `outputs/` folder. Create it when setting up the workpack. |
| Prompt completed but output JSON missing/not updated | When a prompt is marked complete in `99_status.md`, the corresponding `outputs/<PROMPT>.json` MUST exist. |
| B-series without `## Severity` (v4+) | Every B-series prompt in v4+ must have a `## Severity` section classifying the bug as blocker/major/minor. |
| Creating V3, V4, V5... prompts | V-loop uses a single V2 prompt re-run iteratively. Never create V3+. Track iterations via output JSON. |
| Renumbering A5 | A5 is a fixed role name (integration/verification gate). Never renumber it, even if other A-series are skipped. |
| Ignoring B-series budget warnings | >5 B-series warrants attention; >8 should trigger re-scoping discussion. |
| Running linter outside venv | The linter auto-creates `tools/.venv/` and re-runs inside it. No manual venv setup needed. |

---

## Quick Reference

### Copilot Entrypoint (Recommended)

**For GitHub Copilot users** (fastest method):

1. Copy `workpacks/WORKPACK_META_PROMPT.txt`
2. Edit only the "USER REQUEST (EDIT ONLY THIS SECTION)" block
3. Paste into GitHub Copilot Chat (agentic mode)
4. Copilot creates the workpack and executes the workflow

See [Workpack Meta Prompt](#workpack-meta-prompt-copilot--recommended-entry-point) section for details.

### Creating a New Workpack (Manual)

> **Note**: The `date` command differs across platforms. See examples below.

#### Bash / macOS / Linux

```bash
# 1. Determine the date, category, and slug
DATE=$(date +%Y-%m-%d)
CATEGORY="feature"  # or: refactor, hotfix, debug, docs, perf, security
SLUG="my-feature-name"

# 2. Copy the template
cp -r workpacks/_template "workpacks/instances/${DATE}_${CATEGORY}_${SLUG}"

# 3. Edit the files
# - 00_request.md: paste the original request
# - 01_plan.md: write the breakdown
# - prompts/*.md: create agent prompts

# 4. Commit
git add "workpacks/instances/${DATE}_${CATEGORY}_${SLUG}"
git commit -m "workpack: create ${CATEGORY}/${SLUG}"
```

#### PowerShell (Windows)

```powershell
# 1. Determine the date, category, and slug
$DATE = Get-Date -Format "yyyy-MM-dd"
$CATEGORY = "feature"  # or: refactor, hotfix, debug, docs, perf, security
$SLUG = "my-feature-name"

# 2. Copy the template
Copy-Item -Recurse workpacks/_template "workpacks/instances/${DATE}_${CATEGORY}_${SLUG}"

# 3. Edit the files
# - 00_request.md: paste the original request
# - 01_plan.md: write the breakdown
# - prompts/*.md: create agent prompts

# 4. Commit
git add "workpacks/instances/${DATE}_${CATEGORY}_${SLUG}"
git commit -m "workpack: create ${CATEGORY}/${SLUG}"
```

### Router Agent Workflow

When a router agent receives a new request:

1. Read `playbooks/README.md` to classify the request
2. Create a new workpack folder under `./workpacks/instances/`
3. Write `00_request.md` and `01_plan.md`
4. Generate prompts for downstream agents in `prompts/`
5. Commit the workpack
6. Execute the selected playbook (or delegate via prompts)

---

## See Also

- **[Workpack Meta Prompt (Copilot)](./WORKPACK_META_PROMPT.txt)** — **Recommended entrypoint** for GitHub Copilot agentic workflows (routes to generation or bug report prompts)
- [Playbooks README](../playbooks/README.md) — Router and playbook selection
- [Auto-Router Prompt](../playbooks/auto-router-prompt.md) — Canonical prompt for AI agent routing
- [Workpack Generation Prompt](./WORKPACK_GENERATION_PROMPT.md) — Meta-prompt for generating complete workpacks via ChatGPT (routed to by meta prompt for NEW_FEATURE)
- [Bug Report Prompt](./WORKPACK_BUG_REPORT_PROMPT.md) — Meta-prompt for adding B-series bug fix prompts to existing workpacks (routed to by meta prompt for BUGFIX)
