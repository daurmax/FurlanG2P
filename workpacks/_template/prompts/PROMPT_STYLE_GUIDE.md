# Prompt Style Guide — Workpack Protocol v5

> **Core Principle**: Prompts describe *what* to implement and *where* to find patterns, not *how* the code should look. Agents are **implementers**, not copy-pasters.

---

## Table of Contents

1. [Philosophy](#philosophy)
2. [The 80/20 Rule](#the-8020-rule)
3. [Prompt Structure](#prompt-structure)
4. [Reference Points](#reference-points)
5. [V-Series Prompts (v4)](#v-series-prompts-v4)
6. [Subagent Strategy (v4)](#subagent-strategy-v4)
7. [Task Tracking (v4)](#task-tracking-v4)
8. [B-Series Severity (v4)](#b-series-severity-v4)
9. [DAG Dependencies (v5)](#dag-dependencies-v5)
10. [Multi-Repo Awareness (v5)](#multi-repo-awareness-v5)
11. [Execution Cost Tracking (v5)](#execution-cost-tracking-v5)
12. [R-Series Retrospective (v5)](#r-series-retrospective-v5)
13. [Valid vs Invalid Examples](#valid-vs-invalid-examples)
14. [Anti-Patterns](#anti-patterns)
15. [Pre-Commit Checklist](#pre-commit-checklist)

---

## Philosophy

### Why No Code in Prompts?

When a prompt contains complete code implementations:

1. **Workpack generator does all the work** — Downstream agents become copy-pasters, defeating parallelization benefits.
2. **Code drift** — Embedded code becomes stale as the codebase evolves.
3. **Context bloat** — Large prompts consume token budgets unnecessarily.
4. **Lost learning** — Agents don't understand the codebase; they just paste.

### What Should Prompts Contain?

| Include | Exclude |
|---------|---------|
| High-level objectives | Complete class implementations |
| Behavioral requirements | Ready-to-paste code blocks |
| Semantic references to existing patterns | Line number references (fragile) |
| Interface/DTO signatures (when new) | Full method bodies |
| Verification commands | Implementation details agent can derive |

---

## The 80/20 Rule

**Maximum 20% of a prompt may contain code-like content**, and only:

- Interface signatures (when defining new contracts)
- DTO/record definitions (when defining new data structures)
- Configuration snippets (when specific format is required)
- Command examples (for verification/setup)

The remaining **80%+ must be prose**: objectives, requirements, reference points, acceptance criteria.

### How to Measure

Rough estimate: If you have 100 lines in a prompt, max 20 lines can be code fences. If you're exceeding this, refactor to use semantic references.

---

## Prompt Structure

Every v5 prompt follows this structure:

```markdown
---
depends_on: []   # YAML front-matter: prompt stems this depends on
repos: []        # YAML front-matter: repos this prompt touches
---
# <Agent Type> Agent Prompt

> One-line description of objective.

---

## READ FIRST

- List of files to read for context

## Context

Workpack name and one-line objective.

## Delivery Mode

PR-based or direct push.

## Objective

Detailed description of WHAT to accomplish (1-3 paragraphs).

## Reference Points

Semantic references to existing code patterns to follow.

## Implementation Requirements

Behavioral specifications the implementation must satisfy.

## Contracts (if applicable)

New interfaces/DTOs to define (signatures only, or reference to existing).

## Scope

In/out of scope items.

## Acceptance Criteria

Testable criteria checklist.

## Constraints

Hard rules that must not be violated.

## Verification

Commands to run and checklist to validate.

## Handoff Output (JSON)

Required output JSON skeleton.

## Stop Conditions

When to escalate vs continue.

## Deliverables

Final checklist of what must be delivered.
```

---

## Reference Points

Reference Points guide agents to existing patterns without embedding code.

### Semantic Reference Format

```markdown
## Reference Points

- **Service pattern**: Follow the structure of `G2PConverter` class in `src/furlan_g2p/converter.py`
- **Lexicon pattern**: Implement like `LexiconLookup` with the same lazy-loading style
- **CLI pattern**: Use `cli/main.py` as the template for CLI command structure
- **Module pattern**: Follow the `__init__.py` export pattern in `src/furlan_g2p/`
- **Error handling**: Apply the same try-except-log pattern used in existing modules
```

### What Makes a Good Reference?

| Good Reference | Bad Reference |
|----------------|---------------|
| `Follow the pattern of G2PConverter.convert method` | `See lines 45-120 of converter.py` |
| `Implement the Protocol like LexiconLookup does` | `Copy the code from LexiconLookup` |
| `Use the same registry pattern as in __init__.py` | `Add these 15 lines to __init__.py` |
| `Apply BaseProcessor lifecycle (setup/process/teardown)` | `Override these methods with this exact code` |

### Reference Stability

Prefer references that are **semantically stable**:

1. **Class/Interface names** — Change rarely
2. **Method names** — Change occasionally  
3. **File paths** — Change sometimes
4. **Line numbers** — Change frequently ❌ AVOID

---

## V-Series Prompts (v4)

Protocol v4 introduces **V-series verification prompts** as mandatory quality gates.

### V1 — Integration Verification (A5 gate)

The A5 integration prompt now acts as the **V1 gate**. It must:
- Run all test suites (`pytest`, `mypy`, `ruff`)
- Cross-check acceptance criteria from `00_request.md`
- Generate B-series prompts if blocking issues are found
- Block merge if verification fails

> **A5 is a fixed role name**: Never renumber it. The A5 prompt always exists and always runs verification.

### V2 — Post-Bugfix V-Loop

The V2 prompt (`V_bugfix_verify.md`) runs **iteratively** after B-series fixes:

1. All B-series fixes are applied
2. V2 runs verification (tests + AC cross-check)
3. If new issues found → new B-series created → V-loop continues
4. If all pass → merge authorized

> **Single prompt, multiple iterations**: Do NOT create V3, V4, etc. Re-run V2 with updated context. Track iterations via `"iteration"` field in output JSON.

### When V-Series Applies

| Scenario | V1 Required? | V2 Required? |
|----------|-------------|-------------|
| Clean A-series, no bugs | ✅ Yes (A5) | ❌ No |
| B-series bugs found | ✅ Yes (A5) | ✅ Yes |
| Multiple V-loop iterations | ✅ Yes (A5) | ✅ Yes (re-run) |

---

## Subagent Strategy (v4)

Protocol v4 introduces **subagent parallelization** guidance in prompts.

### When to Include Subagent Strategy

Add a `## Subagent Strategy` section when:
- The prompt involves work that can be split into independent parallel tasks
- The verification/review involves multiple independent checks
- The agent may benefit from spawning helper subagents

### Format

```markdown
## Subagent Strategy

This agent may spawn subagents for parallelizable tasks:

- **Subagent 1**: <task description>
- **Subagent 2**: <task description>

> Document subagent usage in the output JSON `handoff.summary`.
```

### Guidelines

- Subagent tasks must be **independent** (no shared mutable state)
- Each subagent should produce a clear, mergeable result
- The parent agent is responsible for integrating results
- Document subagent usage in the handoff output

---

## Task Tracking (v4)

Protocol v4 encourages agents to maintain a **structured todo list** to track multi-step work.

### Why Task Tracking?

- Complex prompts (A5, V2, multi-file implementations) involve many sequential/parallel steps
- Without explicit tracking, agents may lose context or skip steps
- A todo list provides visibility into progress and serves as a checkpoint mechanism

### When to Include Task Tracking

Add a `## Task Tracking` section when:
- The prompt involves more than 3 discrete steps
- The work spans multiple files or components
- Verification requires running multiple independent commands
- The agent may need to iterate (V-loop, multi-pass fixes)

### Format

```markdown
## Task Tracking

This prompt involves multi-step work. If your tool/model supports a structured todo list (e.g., `manage_todo_list`), use it to:

1. Break the work into discrete, trackable steps before starting
2. Mark each step in-progress before beginning and completed immediately after
3. Use the list as a checkpoint to avoid skipping steps

> Task tracking is optional if the tool/model does not support it, but strongly encouraged when available.
```

### Guidelines

- Keep todo items **action-oriented** and concise (3–7 words each)
- Mark only ONE item as in-progress at a time
- Mark tasks completed immediately — do not batch completions
- Task tracking is a recommendation, not a hard requirement (not all models/tools support it)

---

## DAG Dependencies (v5)

Protocol v5 introduces **DAG dependency declarations** via YAML front-matter.

### YAML Front-Matter Format

Every prompt (except A0_bootstrap) MUST include YAML front-matter:

```markdown
---
depends_on: [A0_bootstrap]   # Prompt stems this depends on
repos: [FurlanG2P]     # Repos this prompt touches
---
```

### Rules

- `depends_on` lists prompt **stems** (e.g., `A0_bootstrap`, not `A0_bootstrap.md`)
- `repos` lists repo folder names (e.g., `FurlanG2P`)
- A0_bootstrap has `depends_on: []` (no dependencies)
- The linter validates the DAG for cycles (`ERR_DAG_CYCLE`) and unknown references (`WARN_DAG_UNKNOWN_DEP`)
- Empty `repos: []` on A/B-series prompts (except A0) emits `WARN_MISSING_REPOS`

### DAG in 01_plan.md

The plan MUST include a DAG dependency table:

```markdown
## DAG Dependencies

| Prompt | depends_on | repos |
|--------|-----------|-------|
| A0_bootstrap | [] | [] |
| A1_library | [A0_bootstrap] | [FurlanG2P] |
| A2_cli | [A0_bootstrap] | [FurlanG2P] |
| A5_integration_meta | [A1_library, A2_cli] | [FurlanG2P] |
```

---

## Multi-Repo Awareness (v5)

Protocol v5 requires prompts and outputs to declare which repositories they touch.

### In Prompts

Declare via YAML front-matter `repos: [...]`.

### In Output JSON

Include the `repos` field listing all repos actually modified:

```json
"repos": ["FurlanG2P"]
```

### Purpose

- Detect potential conflicts between parallel prompts
- Enable smarter parallelization/scheduling
- Feed into R-series cost analysis

---

## Execution Cost Tracking (v5)

Protocol v5 requires output JSON to include execution metadata.

### Required Fields

```json
"execution": {
  "model": "claude-sonnet-4-20250514",
  "tokens_in": 15000,
  "tokens_out": 8000,
  "duration_ms": 45000
}
```

### Optional: Change Details

```json
"change_details": [
  { "repo": "FurlanG2P", "file": "src/furlan_g2p/services/new_service.py", "action": "created", "lines_added": 45, "lines_removed": 0 }
]
```

### Purpose

- Feed into R-series retrospective cost analysis
- Improve future effort estimation
- Track model efficiency across workpacks

---

## R-Series Retrospective (v5)

Protocol v5 introduces **R-series retrospective prompts**, executed after merge.

### When to Use

After a workpack is **fully merged**, execute `R1_retrospective.md` to capture:
- What went well / what didn't
- Root causes of issues
- B-series summary and execution cost
- Estimation accuracy (planned vs actual)
- Lessons learned
- Style guide update proposals

### Template

Use `_template/prompts/R_retrospective.md` as the template.

### Lifecycle Position

```
A0 → A1–A4 (parallel) → A5/V1 (verify) → [B-series] → V2 (V-loop) → MERGE → R1
```

---

## B-Series Severity (v4)

All B-series prompts must include a `## Severity` section.

### Mandatory Severity Table

```markdown
## Severity

| Level | Definition |
|-------|------------|
| **blocker** | Prevents merge; must fix before V-loop can pass |
| **major** | Significant defect; should fix in this workpack |
| **minor** | Low-impact; can defer to follow-up workpack |

**This bug is classified as: `<blocker|major|minor>`**
```

### Severity Rules

- **blocker**: The V-loop cannot pass until this is resolved
- **major**: Should be fixed, but V-loop can pass if only minor issues remain
- **minor**: Can be deferred; document in `handoff.known_issues`
- Severity must also be set in the output JSON `"severity"` field

### B-Series Budget

- **≤5 B-series**: Normal workflow
- **6–8 B-series**: Emit `"b_series_budget_warning": true` in V2 output
- **>8 B-series**: Suggest re-scoping; workpack may be too large

---

## Valid vs Invalid Examples

### ❌ INVALID: Complete Implementation

```markdown
## Step 3: Create the Service

Create `ExerciseService.cs`:

\`\`\`csharp
public class ExerciseService : IExerciseService
{
    private readonly IRepository<Exercise> _repository;
    private readonly ILogger<ExerciseService> _logger;
    
    public ExerciseService(IRepository<Exercise> repository, ILogger<ExerciseService> logger)
    {
        _repository = repository;
        _logger = logger;
    }
    
    public async Task<Exercise> GetByIdAsync(Guid id, CancellationToken ct)
    {
        _logger.LogInformation("Getting exercise {Id}", id);
        return await _repository.GetByIdAsync(id, ct);
    }
    
    // ... 50 more lines
}
\`\`\`
```

### ✅ VALID: Semantic Reference + Requirements

```markdown
## Implementation Requirements

### ExerciseService

Create a new service class `ExerciseService` implementing `IExerciseService`:

- **Pattern**: Follow the structure of `UserService` (constructor injection, async methods, logging)
- **Dependencies**: Inject `IRepository<Exercise>` and `ILogger<ExerciseService>`
- **Methods to implement**:
  - `GetByIdAsync(Guid id, CancellationToken ct)` — Retrieve single exercise
  - `GetAllAsync(CancellationToken ct)` — Retrieve all exercises
  - `CreateAsync(CreateExerciseDto dto, CancellationToken ct)` — Create new exercise
- **Logging**: Log at Information level for operations, Warning for not-found scenarios
- **Error handling**: Let exceptions bubble up (handled by middleware)
```

---

### ❌ INVALID: Line Number Reference

```markdown
## Reference Points

- See `UserService.cs` lines 23-45 for the pattern
- Copy the logic from `ExerciseController.cs:L89-L134`
```

### ✅ VALID: Method/Class Reference

```markdown
## Reference Points

- **Service structure**: Follow `UserService.CreateAsync` method pattern
- **Controller action**: Implement like `ExerciseController.GetById` action
```

---

### ❌ INVALID: Full DTO with Implementation

```markdown
\`\`\`csharp
public record CreateExerciseDto
{
    public string Name { get; init; } = string.Empty;
    public string Description { get; init; } = string.Empty;
    public ExerciseType Type { get; init; }
    public int Difficulty { get; init; }
    public List<string> Tags { get; init; } = new();
    public Guid CategoryId { get; init; }
    public bool IsActive { get; init; } = true;
    public DateTime? ScheduledFor { get; init; }
    public Dictionary<string, object> Metadata { get; init; } = new();
}
\`\`\`
```

### ✅ VALID: Contract Signature Only (when new)

```markdown
## Contracts

### CreateExerciseDto (new record)

| Property | Type | Notes |
|----------|------|-------|
| Name | string | Required, non-empty |
| Description | string | Optional |
| Type | ExerciseType | Enum defined in Domain |
| Difficulty | int | 1-5 scale |
| CategoryId | Guid | FK to Category |

> Place in `src/Contracts/Exercises/CreateExerciseDto.cs`
```

### ✅ ALSO VALID: Reference Existing Contract

```markdown
## Contracts

Use the existing `CreateExerciseDto` from `src/Contracts/Exercises/`. No modifications needed.
```

---

## Anti-Patterns

### 1. The Copy-Paste Prompt

❌ Prompt contains 200+ lines of code that agent just copies.

**Fix**: Extract semantic references, describe behavior, let agent implement.

### 2. The Line Number Trap

❌ "See lines 45-89 for the pattern"

**Fix**: "Follow the `ProcessRequest` method pattern in `RequestHandler`"

### 3. The Mega-Prompt

❌ Single prompt with 500+ lines covering everything.

**Fix**: Split into multiple prompts if work is parallelizable, or trim code to references.

### 4. The Implicit Pattern

❌ "Implement it like we always do"

**Fix**: Name the specific class/method that exemplifies "how we always do it"

### 5. The Stale Snippet

❌ Code in prompt doesn't match current codebase implementation.

**Fix**: Use semantic references that remain valid as code evolves.

---

## Pre-Commit Checklist

Before committing a v5 prompt, verify:

### Content Rules

- [ ] **No complete implementations** — No full class/method bodies in code blocks
- [ ] **80/20 rule** — Less than 20% of content is code fences
- [ ] **No line numbers** — All references are semantic (class/method names)
- [ ] **References are stable** — Referenced classes/methods exist and are unlikely to be renamed

### Structure Rules

- [ ] **Objective is clear** — One-line summary + detailed description
- [ ] **Reference Points exist** — At least one semantic reference for non-trivial work
- [ ] **Requirements are behavioral** — Describe WHAT, not HOW
- [ ] **Verification is runnable** — Commands can be executed as-is

### v4-Specific Rules

- [ ] **B-series has severity** — Every B-series prompt has `## Severity` with blocker/major/minor
- [ ] **V-series referenced** — V-loop is documented in plan if B-series exist
- [ ] **A5 is fixed** — A5 prompt exists and is not renumbered
- [ ] **Subagent strategy** — Present where parallelizable work exists
- [ ] **Task tracking** — Present in complex prompts (A5, V2, multi-step work)

### v5-Specific Rules

- [ ] **YAML front-matter** — `depends_on` and `repos` present in every prompt
- [ ] **DAG is acyclic** — No cycles in `depends_on` references
- [ ] **Repos declared** — A/B-series prompts (except A0) have non-empty `repos`
- [ ] **Execution in output** — Output JSON includes `execution` block
- [ ] **R-series planned** — `R1_retrospective.md` exists in prompts/

### Language Rules

- [ ] **English only** — All prompts in English
- [ ] **Imperative mood** — "Create a service", not "A service should be created"
- [ ] **Specific, not vague** — "UserService.CreateAsync pattern", not "the usual pattern"

---

## Linter Enforcement

The `workpack_lint.py` tool validates v3/v4/v5 prompts:

- **v3.0**: Code blocks in prompts emit WARNING
- **v4.0**: Code blocks in prompts emit ERROR (blocks CI)
- **v4.0**: Missing severity in B-series is ERROR
- **v4.0**: Missing verification prompt (no A5/V-series) is ERROR
- **v4.0**: B-series budget warnings (>5 WARN, >8 RESCOPE)
- **v5.0**: DAG cycle detection (`ERR_DAG_CYCLE`)
- **v5.0**: Unknown DAG dependency (`WARN_DAG_UNKNOWN_DEP`)
- **v5.0**: Missing repos in A/B-series (`WARN_MISSING_REPOS`)
- **v5.0**: Missing execution block in completed outputs (`WARN_MISSING_EXECUTION`)

Detected languages: `csharp`, `cs`, `python`, `py`, `typescript`, `ts`, `javascript`, `js`, `json`, `yaml`, `yml`, `bash`, `sh`, `powershell`, `ps1`, `sql`, `xml`, `html`, `css`, `java`, `kotlin`, `swift`, `go`, `rust`, `ruby`, `php`

### Exceptions

Some code blocks are allowed:

- Verification commands (bash/powershell for running tests)
- JSON output skeleton (required for handoff)
- Configuration snippets (when format is critical)

Use the `<!-- lint-ignore-code-block -->` comment immediately before a code block to suppress the warning for that specific block.
