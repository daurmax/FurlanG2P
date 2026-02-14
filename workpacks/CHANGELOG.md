# Workpack Protocol Changelog

> **Note**: This protocol was originally developed for the Beorcje-Meta project and has been adapted for FurlanG2P.

All notable changes to the Workpack Protocol are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for protocol versions.

---

## [5.0] - 2026-02-11

### ⚠️ Breaking Changes

This is a **hard-break** release. The folder layout has changed: workpack instances now live under `workpacks/instances/` instead of directly under `workpacks/`. Existing v4 workpacks should be migrated using `MIGRATION_PROMPT.md`.

### Added

- **Instances Subfolder**: Workpack instances are now stored under `workpacks/instances/` to separate protocol files from instance data. The linter scans both `instances/` and the legacy top-level layout.
- **DAG Dependency Graph**: Prompts may declare `depends_on` in YAML front-matter. The linter validates no circular dependencies exist (`ERR_DAG_CYCLE`) and warns on unknown references (`WARN_DAG_UNKNOWN_DEP`).
- **Prompt Scaffolding Tool**: `workpack_scaffold.py` reads `01_plan.md` and auto-generates skeleton prompt files with correct YAML front-matter, reducing manual boilerplate.
- **Execution Cost Tracking**: Output JSON gains an `execution` block with `model`, `tokens_in`, `tokens_out`, `duration_ms` fields. The linter warns when completed outputs lack it (`WARN_MISSING_EXECUTION`).
- **Multi-Repo Awareness**: Prompts declare `repos` in YAML front-matter specifying which repositories they touch. The linter warns on empty `repos` for A/B-series prompts (`WARN_MISSING_REPOS`).
- **Structured Change Details**: Output JSON gains `change_details` array with per-file `repo`, `file`, `action`, `lines_added`, `lines_removed`.
- **R-Series Retrospective**: New `R_retrospective.md` template for post-merge lessons learned, cost analysis, and prompt quality assessment.
- **Cross-Workpack References**: `01_plan.md` template gains `requires_workpack` field for declaring dependencies between workpacks.
- **Machine-Verifiable Acceptance Criteria**: `00_request.md` template gains structured `## Acceptance Criteria (machine-verifiable)` section with `type: test_pass | file_exists | lint_clean` entries.
- **New Linter Checks (v5)**:
  - `ERR_DAG_CYCLE`: Circular dependency in `depends_on` graph → ERROR
  - `WARN_DAG_UNKNOWN_DEP`: `depends_on` references non-existent prompt → WARNING
  - `WARN_MISSING_REPOS`: A/B-series prompt with empty `repos: []` → WARNING
  - `WARN_MISSING_EXECUTION`: Completed output JSON without `execution` block → WARNING

### Changed

- **Folder Layout**: `workpacks/YYYY-MM-DD_*` moved to `workpacks/instances/YYYY-MM-DD_*`.
- **Linter Scan Path**: Linter now scans `workpacks/instances/` first, then falls back to top-level for legacy workpacks.
- **WORKPACK_OUTPUT_SCHEMA.json**: Added `repos`, `execution`, and `change_details` fields.
- **00_request.md Template**: Added machine-verifiable acceptance criteria section and protocol version bumped to 5.
- **01_plan.md Template**: Added `requires_workpack` and DAG sections.
- **99_status.md Template**: Added R-series tracking section and execution cost summary.
- **All Prompt Templates**: Added YAML front-matter with `depends_on` and `repos` fields.
- **MIGRATION_PROMPT.md**: Updated for v4→v5 migration path.
- **README.md**: Updated folder structure, v5 documentation, scaffold tool docs.

### Lifecycle (v5)

```
A0 → A1–A4 (parallel, DAG-ordered) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE → R1 (retrospective)
```

### Migration

Use `MIGRATION_PROMPT.md` to convert existing workpacks. Key changes: move instances to `instances/` subfolder, add YAML front-matter to prompts, add `execution` block to output JSONs, bump protocol version to 5.

---

## [4.0] - 2026-02-09

### ⚠️ Breaking Changes

This is a **hard-break** release. Existing v3 workpacks are considered legacy and should be migrated using `MIGRATION_PROMPT.md`.

### Added

- **V-Series (Verification Prompts)**: New prompt series dedicated to verification gates.
  - Every workpack **MUST** include at least one verification prompt (`A5_integration_meta.md` or `V#_verify.md`). The linter emits `ERR_NO_VERIFICATION` if none is found.
  - `V_bugfix_verify.md` template: lightweight, iterative post-bugfix verification gate (V-loop).
- **V-Loop Paradigm**: After B-series fixes are applied, a single `V2_bugfix_verify.md` prompt is executed iteratively until all bugs are confirmed resolved. Output JSON tracks `"iteration"` count and `"b_series_resolved"` / `"b_series_remaining"` arrays.
- **B-Series Severity Field**: `## Severity` section is now **mandatory** in all B-series prompts. Values: `blocker`, `major`, `minor`. Output JSON gains `"severity"` field.
- **B-Series Budget Warning**: The linter emits `WARN_B_SERIES_BUDGET` when a workpack has >5 B-series prompts, and `WARN_B_SERIES_RESCOPE` when >8. V-loop output must include `"b_series_budget_warning"` flag.
- **Protocol Version Consistency Check**: Linter verifies that `00_request.md`, `01_plan.md`, and `99_status.md` all reference the same protocol version. Emits `WARN_VERSION_MISMATCH` on inconsistency.
- **Subagent Parallelization Guidance**: All A-series and V-series templates now include a `## Subagent Strategy` section encouraging agents to spawn subagents (e.g., Copilot/Codex) for parallelizable subtasks within a single prompt.
- **Task Tracking Guidance**: All prompt templates now include a `## Task Tracking` section encouraging agents to maintain a structured todo list (e.g., `manage_todo_list`) for multi-step work, provided the tool/model supports it.
- **Linter Virtual Environment**: `workpack_lint.py` now auto-creates and re-runs inside a Python virtual environment (`tools/.venv/`) when invoked outside one, ensuring isolation and reproducibility.
- **CHANGELOG Enforcement**: `WORKPACK_GENERATION_PROMPT.md` and `MIGRATION_PROMPT.md` now instruct agents to update `workpacks/CHANGELOG.md` when introducing protocol version changes.
- **New Linter Checks**:
  - `ERR_NO_VERIFICATION`: No `A5_*` or `V#_*` prompt present → ERROR
  - `WARN_BUGFIX_NO_VERIFY`: B-series prompts present but no `V#_*` prompt → WARNING
  - `WARN_B_SERIES_BUDGET`: >5 B-series prompts → WARNING
  - `WARN_B_SERIES_RESCOPE`: >8 B-series prompts → WARNING (suggests re-scoping)
  - `ERR_SEVERITY_MISSING`: B-series prompt without `## Severity` section → ERROR
  - `WARN_VERSION_MISMATCH`: Protocol version inconsistency across workpack files → WARNING
  - v4 workpack validation: code blocks in prompts now emit ERROR (was WARNING in v3)

### Changed

- **A5 as Fixed Role**: `A5_integration_meta.md` is now a **fixed role name** regardless of how many A-series prompts exist. Even if A3/A4 are absent, the integration agent is always `A5`. This simplifies linter rules and naming consistency.
- **01_plan.md Template**: Now includes V-loop phase in parallelization map and B-series severity table.
- **99_status.md Template**: Now includes V-Series tracking section alongside A-Series and B-Series.
- **B_template.md**: Added mandatory `## Severity` section and severity guidance.
- **PROMPT_STYLE_GUIDE.md**: Added V-series documentation and subagent parallelization section.
- **WORKPACK_OUTPUT_SCHEMA.json**: Added optional `severity`, `iteration`, `b_series_resolved`, `b_series_remaining`, `b_series_budget_warning` fields.
- **MIGRATION_PROMPT.md**: Updated for v3→v4 migration path.
- **README.md**: Updated with V-series documentation, V-loop lifecycle diagram, and subagent guidance.

### Lifecycle (v4)

```
A0 → A1–A4 (parallel) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE
```

### Migration

Use `MIGRATION_PROMPT.md` to convert existing workpacks. Key changes: add `## Severity` to B-series prompts, add V2_bugfix_verify if B-series exist, update protocol version to 4.

---

## [3.0] - 2026-01-31

### ⚠️ Breaking Changes

This is a **hard-break** release. Existing v2 workpacks are considered legacy and should be migrated using `MIGRATION_PROMPT.md`.

### Added

- **Agent-Centric Prompt Philosophy**: Prompts now describe *what* to implement using semantic references, not *how* by embedding code. Agents are implementers, not copy-pasters.
- **PROMPT_STYLE_GUIDE.md**: Comprehensive guide for writing agent-centric prompts with valid/invalid examples.
- **Integration Agent as Merge Reviewer**: A5 now executes mandatory test suites and validates that all agents followed directives before allowing merge.
- **Linter Code-Block Detection**: `workpack_lint.py` now detects code blocks in v3 prompts and emits warnings (errors in v3.1+).
- **MIGRATION_PROMPT.md**: General-purpose migration prompt to convert any workpack version to latest.
- **Standard Verification Checklist**: A5 has a standard checklist (backend tests, Unity EditMode tests) plus custom workpack-specific checks.

### Changed

- **Template Prompt Structure**: New architecture with sections:
  - `## Objective` — High-level goal description
  - `## Reference Points` — Semantic references to existing code patterns (method names, class patterns, NOT line numbers)
  - `## Implementation Requirements` — Behavioral specifications, NOT code
  - `## Contracts` — Interface/DTO signatures or references to existing files
  - `## Verification` — Commands and criteria, NOT implementation
- **WORKPACK_GENERATION_PROMPT.md**: Now agent-centric (no ChatGPT workflow), includes anti-patterns section, 80/20 rule for code snippets.
- **WORKPACK_BUG_REPORT_PROMPT.md**: Now agent-centric, describes expected vs observed behavior without proposing fix code.
- **WORKPACK_META_PROMPT.txt**: Added `NO_CODE_BLOCKS` constraint and semantic reference instructions.

### Removed

- **Inline Code Blocks in Prompts**: Prompts should NOT contain complete code implementations. Max 20% of prompt can be signatures/interfaces.
- **Line Number References**: Use semantic references (`HandleExerciseRequest method in ExerciseService`) instead of fragile line numbers (`L15-45`).
- **ChatGPT Workflow References**: All prompts now assume agent execution (Copilot/Claude), not ChatGPT copy-paste workflow.

### Migration

Use `MIGRATION_PROMPT.md` to convert existing workpacks. Migration uncertainties are collected in a `MIGRATION_NOTES.md` file within the workpack.

---

## [2.0] - 2026-01-24

### Added

- **Structured Handoff Outputs**: Every completed prompt must produce `outputs/<PROMPT>.json` conforming to `WORKPACK_OUTPUT_SCHEMA.json`.
- **Linter Validation**: `tools/workpack_lint.py` validates v2 workpacks for:
  - Required `outputs/` directory
  - JSON output for each completed prompt
  - Schema conformance
  - Field value consistency
- **Output JSON Schema**: `WORKPACK_OUTPUT_SCHEMA.json` with required fields for traceability.
- **B-Series Prompts**: Post-implementation bug fix prompts with naming convention `B#_<component>_<description>.md`.
- **99_status.md**: Formalized status tracking with completion markers.
- **Protocol Version Declaration**: `Workpack Protocol Version: 2` in `00_request.md`.

### Changed

- **Completion Rules**: A prompt is only complete when BOTH status marker exists AND output JSON is created.
- **Acceptance Criteria Mapping**: `00_request.md` now includes AC → Verification mapping table.

---

## [1.0] - 2026-01-22

### Added

- **Initial Workpack Structure**: Folder-based organization with `00_request.md`, `01_plan.md`, `prompts/`, `99_status.md`.
- **Naming Convention**: `YYYY-MM-DD_<category>_<short-slug>` folder naming.
- **A-Series Prompts**: A0 (bootstrap), A1 (backend), A2 (Unity), A3 (tools), A4 (docs), A5 (integration).
- **Template Directory**: `_template/` with reusable scaffolds.
- **WORKPACK_GENERATION_PROMPT.md**: Meta-prompt for generating workpacks.
- **WORKPACK_META_PROMPT.txt**: Single-file router for Copilot workflows.

### Notes

- v1 workpacks do not require structured outputs.
- No linter validation for v1.
