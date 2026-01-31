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
5. **Copilot enforces** Workpack Protocol v3 (outputs + status) automatically

### Non-Negotiables (Always Enforced)

- ✅ Always read and follow `workpacks/README.md` (this file)
- ✅ Workpack Protocol Version must be **3** for v3 behavior
- ✅ `outputs/` folder and `99_status.md` must be maintained
- ✅ Never mark a prompt completed unless `outputs/<PROMPT>.json` exists and is updated
- ✅ Never include secrets, API keys, or credentials in prompts or outputs

### Why Use the Meta Prompt?

- **Single source of truth**: One file to copy, one place to edit your request
- **Automatic routing**: Copilot picks the right workflow (feature vs bugfix)
- **Protocol v3 compliance**: Built-in enforcement of outputs + status rules
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
| **Prompts** | One prompt file per downstream agent (library, CLI, tests, docs, integration) |
| **Status** | Checklist of completion, links to PRs, merge order (optional) |

Workpacks are **always committed to git**. They are never placed in `temp/` or ignored.

---

## Naming Convention

Each workpack lives in its own folder under `./workpacks/`.

**Folder name format:**

```
YYYY-MM-DD_<category>_<short-slug>
```

| Component | Description | Examples |
|-----------|-------------|----------|
| `YYYY-MM-DD` | Creation date (ISO 8601) | `2026-01-22` |
| `<category>` | Work type: `feature`, `refactor`, `hotfix`, `bugfix`, `debug`, `docs`, `perf`, `security` | `feature`, `bugfix` |
| `<short-slug>` | Kebab-case slug (2–5 words) describing the work | `lexicon-expansion`, `cli-batch-mode` |

**Examples:**

- `2026-01-22_feature_lexicon-expansion`
- `2026-01-22_refactor_normalizer-cleanup`
- `2026-01-22_bugfix_stress-assignment`
- `2026-01-22_hotfix_urgent-phoneme-fix`
- `2026-01-22_debug_tokenizer-edge-cases`

**Category Clarification:**
- `bugfix` = standard fix for discovered issues
- `hotfix` = urgent fix requiring immediate deployment (if used)

---

## Required Contents

Every workpack folder MUST contain:

```
workpacks/
└── YYYY-MM-DD_<category>_<short-slug>/
    ├── 00_request.md          # Original request, acceptance criteria, constraints
    ├── 01_plan.md             # WBS, parallelization map, sequencing, risks
    ├── prompts/               # Prompts for downstream agents
    │   ├── A0_bootstrap.md    # (optional) Shared branch creation, unblocking steps
    │   ├── A1_library.md      # Library/core implementation agent prompt
    │   ├── A2_cli.md          # CLI implementation agent prompt
    │   ├── A3_tests.md        # Tests agent prompt
    │   ├── A4_docs.md         # Documentation agent prompt
    │   ├── A5_integration.md  # Integration agent prompt
    │   ├── B1_<component>_<fix-name>.md  # (optional) Post-implementation bug fix
    │   ├── B2_<component>_<fix-name>.md  # (optional) Additional bug fix
    │   └── ...                # Additional bug fixes as needed
    ├── outputs/               # (Protocol v3) Structured handoff JSON outputs
    │   ├── A1_library.json    # Output for A1 prompt (created when complete)
    │   ├── A2_cli.json        # Output for A2 prompt (created when complete)
    │   └── ...                # One JSON per completed prompt
    └── 99_status.md           # (optional) Checklist, PR links, merge order
```

> **Note (Protocol v3)**: The `outputs/` folder contains structured handoff JSON files. Each output file is named exactly like its corresponding prompt (same basename, `.json` extension).

> **Note**: Copy from `workpacks/_template/` when creating a new workpack. See [Template](#template) section.

### File Descriptions

| File | Required | Purpose |
|------|----------|---------|
| `00_request.md` | ✅ | Captures the original request verbatim, plus acceptance criteria and hard constraints |
| `01_plan.md` | ✅ | Contains the Work Breakdown Structure, task sequencing, parallelization notes, and risks |
| `prompts/` | ✅ | Folder containing one prompt file per downstream agent |
| `prompts/A0_bootstrap.md` | ❌ | Optional: steps to create shared branches or unblock prerequisites |
| `prompts/A1_library.md` | ❌ | Prompt for library/core agent (if library work is needed) |
| `prompts/A2_cli.md` | ❌ | Prompt for CLI agent (if CLI work is needed) |
| `prompts/A3_tests.md` | ❌ | Prompt for tests agent (if test work is needed) |
| `prompts/A4_docs.md` | ❌ | Prompt for documentation agent (if docs work is needed) |
| `prompts/A5_integration.md` | ❌ | Prompt for integration (if integration is needed) |
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
| `A1_` | Library/core implementation | `A1_library.md` |
| `A2_` | CLI implementation | `A2_cli.md` |
| `A3_` | Tests implementation | `A3_tests.md` |
| `A4_` | Documentation | `A4_docs.md` |
| `A5_` | Integration and merge | `A5_integration.md` |

### B-Series: Post-Implementation Bug Fix Prompts

These prompts are added **after initial implementation** when bugs or issues are discovered during testing or integration. They are numbered sequentially and include a descriptive name.

| Prefix | Purpose | Naming Pattern |
|--------|---------|----------------|
| `B1_` | First bug fix | `B1_<component>_<fix-description>.md` |
| `B2_` | Second bug fix | `B2_<component>_<fix-description>.md` |
| `B3_` | Third bug fix | `B3_<component>_<fix-description>.md` |
| ... | Additional bug fixes | Continue numbering sequentially |

**Examples:**
- `B1_library_stress_edge_case.md` — Fix stress assignment edge case
- `B2_cli_encoding_issue.md` — Fix CLI encoding issue
- `B3_normalization_number_format.md` — Fix number formatting in normalizer

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

---

## Workpack Protocol v3 — Structured Handoffs (outputs/)

Workpack Protocol v3 introduces **structured handoffs** for reliable agent-to-agent communication and audit/replay capabilities.

### Key Rules

- **Declaration**: Workpacks v3 declare `Workpack Protocol Version: 3` in `00_request.md`.
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

### outputs/ + status enforcement (Protocol v3)

**Critical completion rules:**

1. **Output JSON is REQUIRED only when a prompt is marked completed** in `99_status.md`
   - Prompts not marked completed do NOT require output JSON yet
   - This allows incremental work without requiring immediate outputs

2. **Completion is INVALID unless BOTH conditions are met:**
   - ✅ `99_status.md` contains a completion marker (✅ Done, 🟢 Complete, etc.)
   - ✅ `outputs/<PROMPT>.json` exists and is properly updated

3. **Never include secrets in outputs:**
   - ❌ No API keys, tokens, passwords, or credentials
   - ✅ Use references to secure storage if needed

---

## Template

The `_template/` folder contains starter files for new workpacks:

```
workpacks/_template/
├── 00_request.md
├── 01_plan.md
├── prompts/
│   ├── A0_bootstrap.md
│   ├── A1_library.md
│   ├── A2_cli.md
│   ├── A3_tests.md
│   ├── A4_docs.md
│   ├── A5_integration.md
│   ├── B_template.md
│   └── PROMPT_STYLE_GUIDE.md
├── outputs/
│   ├── .gitkeep
│   └── README.md
└── 99_status.md
```

### Creating a New Workpack

1. Copy `_template/` to a new folder with the proper naming convention
2. Fill in `00_request.md` with the request details
3. Fill in `01_plan.md` with the work breakdown
4. Delete unused prompt templates from `prompts/`
5. Commit the workpack to git

---

## Protocol v3 Core Principles

1. **Agent-Centric**: Prompts describe WHAT to implement, not HOW. Agents are implementers, not copy-pasters.
2. **Semantic References**: Point to existing patterns by class/method name, NEVER by line numbers.
3. **80/20 Rule**: Maximum 20% of a prompt can be code (signatures only). 80%+ must be prose.
4. **Integration as Reviewer**: A5 agent validates all work, runs tests, and authorizes merge.

---

## FurlanG2P-Specific Notes

This is a **Python library project**. The agent prompts are structured around:

- **A1_library.md**: Core library implementation (`src/furlan_g2p/`)
- **A2_cli.md**: CLI implementation (`src/furlan_g2p/cli/`)
- **A3_tests.md**: Test implementation (`tests/`)
- **A4_docs.md**: Documentation (`docs/`, `README.md`, `README-pypi.md`)
- **A5_integration.md**: Integration, validation, and merge

### Verification Commands

```bash
# Install in development mode
pip install -e ".[dev]"

# Run tests
pytest tests/ -v

# Type checking
mypy src/

# Linting
ruff check src/ tests/

# Format check
ruff format --check src/ tests/

# Build distribution
python -m build
```

### Key Files to Reference

- `AGENTS.md` — Agent guidelines and conventions
- `docs/architecture.md` — Component interactions and design
- `docs/business_logic.md` — Algorithmic design details
- `docs/references.md` — Bibliography for business logic changes
- `pyproject.toml` — Project configuration and dependencies
