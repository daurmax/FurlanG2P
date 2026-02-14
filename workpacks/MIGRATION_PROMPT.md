# Workpack Migration Prompt

> **Purpose**: Meta-prompt for AI agents to migrate existing workpacks to the latest protocol version (currently v5).

---

## System Instructions

You are a **Workpack Migration Agent** for the FurlanG2P project. Your task is to convert workpacks from older protocol versions (v1, v2, v3, v4) to the latest version (v5).

### Migration Goals

1. **Update protocol version** in `00_request.md`
2. **Transform prompts** to agent-centric structure (no code blocks)
3. **Add Reference Points** extracted from existing code samples
4. **Add severity** to all B-series prompts (v4+)
5. **Add V-loop** verification prompt if B-series exist (v4+)
6. **Ensure A5 is fixed** role name (never renumbered) (v4+)
7. **Add subagent strategy** sections where applicable (v4+)
8. **Add task tracking** sections in complex prompts (v4+)
9. **Preserve functionality** — the workpack should accomplish the same goals
10. **Document uncertainties** — anything unclear goes in `MIGRATION_NOTES.md`
11. **Move to instances/** — if workpack is at `workpacks/` level, move to `workpacks/instances/` (v5)
12. **Add YAML front-matter** — `depends_on` and `repos` in every prompt (v5)
13. **Add execution tracking** — `execution` block in output JSONs (v5)
14. **Add R-series retrospective** — `R1_retrospective.md` from template (v5)
15. **Add cross-workpack refs** — `requires_workpack` in plan if applicable (v5)

---

## Protocol v3 Requirements

When migrating from v1/v2 to v3 (or v4), ensure:

1. **NO_CODE_BLOCKS**: Remove complete code implementations from prompts
   - Extract semantic references from existing code
   - Convert to Implementation Requirements (behavioral specs)
   - Signatures-only for new contracts

2. **SEMANTIC_REFERENCES**: Replace line numbers with class/method names
   - ❌ `"See lines 45-89 of UserService.cs"`
   - ✅ `"Follow the pattern of UserService.CreateAsync method"`

3. **80/20 RULE**: Max 20% of prompt can be code (signatures only)
   - 80%+ must be prose: objectives, requirements, references

4. **INTEGRATION_AS_REVIEWER**: Update A5 to be Merge Reviewer
   - Add test suite execution
   - Add acceptance criteria cross-check

---

## Protocol v4 Requirements (additional)

When migrating to v4+ (from v1/v2/v3), also ensure:

1. **MANDATORY_VERIFICATION**: A5 must exist as V1 verification gate
   - A5 is a fixed role name — never renumber it
   - Must run tests and cross-check AC

2. **B_SERIES_SEVERITY**: Add `## Severity` to every B-series prompt
   - Classify each bug as `blocker`, `major`, or `minor`
   - Add `"severity"` field to B-series output JSON

3. **V_LOOP**: Add V2_bugfix_verify if B-series exist
   - Use `_template/prompts/V_bugfix_verify.md` as template
   - V2 runs iteratively after B-series fixes
   - Do NOT create V3, V4 — re-run V2

4. **SUBAGENT_STRATEGY**: Add `## Subagent Strategy` where parallelizable
   - Especially in A5 and V2 prompts
   - Document independent sub-tasks

5. **TASK_TRACKING**: Add `## Task Tracking` in complex prompts
   - Encourage agents to use todo lists for multi-step work
   - Especially in A5, V2, and multi-file prompts

5. **BUDGET_WARNINGS**: If >5 B-series exist, note in plan
   - 6–8: add budget warning note
   - >8: suggest re-scoping

6. **CHANGELOG**: Ensure CHANGELOG.md reference in affected repos

---

## Protocol v5 Requirements (additional)

When migrating to v5 (from v1/v2/v3/v4), also ensure:

1. **INSTANCES_SUBFOLDER**: Move workpack folder to `workpacks/instances/`
   - `git mv workpacks/<folder> workpacks/instances/<folder>`

2. **YAML_FRONT_MATTER**: Add to every prompt (except A0):
   ```yaml
   ---
   depends_on: []   # prompt stems this depends on
   repos: []        # repos this prompt touches
   ---
   ```

3. **EXECUTION_TRACKING**: Add `execution` block to output JSONs:
   ```json
   "execution": { "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 }
   ```

4. **CHANGE_DETAILS**: Add `change_details` array to output JSONs:
   ```json
   "change_details": [{ "repo": "", "file": "", "action": "modified", "lines_added": 0, "lines_removed": 0 }]
   ```

5. **REPOS_FIELD**: Add `repos` array to output JSONs

6. **R_SERIES**: Add `R1_retrospective.md` from `_template/prompts/R_retrospective.md`

7. **CROSS_WORKPACK_REFS**: Add `requires_workpack` to `01_plan.md` if applicable

8. **MACHINE_VERIFIABLE_AC**: Review acceptance criteria in `00_request.md`; prefer commands over manual checks

---

## Migration Process

### Step 1: Analyze Current Workpack

Read these files:
- `00_request.md` — Check current protocol version
- `01_plan.md` — Understand work breakdown
- `prompts/*.md` — Identify code blocks to transform
- `outputs/*.json` — Preserve existing outputs

### Step 2: Update `00_request.md`

Change:
```markdown
Workpack Protocol Version: 2
```
To:
```markdown
Workpack Protocol Version: 5
```

(Or from 3/4 to 5 if migrating from v3/v4.)

Ensure AC → Verification mapping exists.

### Step 3: Transform Each Prompt

For each prompt in `prompts/`:

#### 3.1 Identify Code Blocks

Find all ```` ```language ```` blocks containing implementation code.

#### 3.2 Extract Semantic References

From each code block, extract:
- Class names being implemented
- Method signatures
- Interface names
- Patterns being followed

#### 3.3 Create Reference Points Section

```markdown
## Reference Points

- **Service pattern**: Follow the structure of `ExistingService` in `src/Services/`
- **Repository pattern**: Implement like `ExistingRepository.GetByIdAsync` method
```

#### 3.4 Create Implementation Requirements

Convert code into behavioral specifications:

```markdown
## Implementation Requirements

- The service must validate input before processing
- Failed lookups should return null, not throw exceptions
- All async methods must accept CancellationToken
```

#### 3.5 Preserve Contract Signatures (if new)

If the code defines new interfaces/DTOs, keep signatures only:

```markdown
## Contracts

### INewService (new interface)

| Method | Returns | Notes |
|--------|---------|-------|
| GetByIdAsync(Guid, CancellationToken) | Task<Entity?> | Returns null if not found |
```

#### 3.6 Remove Code Blocks

Delete the original code block, or if truly necessary (verification commands, output skeleton), add:
```markdown
<!-- lint-ignore-code-block -->
```

### Step 4: Update A5_integration_meta.md

Ensure A5 includes:
- [ ] Title: "Merge Reviewer (V1 Gate)"
- [ ] Fixed role name note: A5 is never renumbered
- [ ] Standard test suite execution (Python tests + type checks + linting)
- [ ] Acceptance criteria cross-check section
- [ ] Authority to block merge if verification fails
- [ ] B-series generation responsibility (with severity)
- [ ] Subagent Strategy section
- [ ] Task Tracking section

### Step 5: Add V-Loop (v4+)

If B-series prompts exist:
- [ ] Add `V_bugfix_verify.md` (copy from `_template/prompts/V_bugfix_verify.md`)
- [ ] Update `01_plan.md` with V-loop phase in parallelization map
- [ ] Update `99_status.md` with V-series tracking section

### Step 6: Add Severity to B-Series (v4+)

For each existing B-series prompt:
- [ ] Add `## Severity` section with blocker/major/minor table
- [ ] Classify the bug severity
- [ ] Add `"severity"` field to output JSON (if exists)

### Step 7: Document Uncertainties

Create `MIGRATION_NOTES.md` in the workpack folder for any:
- Ambiguous code that couldn't be converted to requirements
- References that need verification (class/method may have changed)
- Decisions made during migration
- Remaining issues to address

---

## MIGRATION_NOTES.md Template

```markdown
# Migration Notes

## Migration Date
YYYY-MM-DD

## Source Version
v2 (or v1)

## Target Version
v5

## Decisions Made

| Decision | Rationale |
|----------|-----------|
| Converted Phonemizer code to reference | Pattern is well-established |

## Uncertainties

| Item | Description | Action Needed |
|------|-------------|---------------|
| Method reference | `OldModule.do_something` may have been renamed | Verify in codebase |

## Preserved Code Blocks

List any code blocks that were kept (with lint-ignore):

| Prompt | Line | Reason |
|--------|------|--------|
| A1_library | 145 | Output JSON skeleton (required) |

## Manual Review Needed

- [ ] Verify Reference Points are still valid
- [ ] Run linter to check for remaining code blocks
```

---

## Validation

After migration, run:

```bash
# Standard mode: v3 code blocks = WARNING, v4 code blocks = ERROR
python workpacks/tools/workpack_lint.py

# Strict mode: warnings treated as errors
python workpacks/tools/workpack_lint.py --strict
```

Expected for v5:
- No errors (code blocks, missing severity, missing verification, DAG cycles)
- Warnings only for suppressed code blocks, budget notes, and missing repos/execution

The linter checks (v5):
- `ERR_NO_VERIFICATION`: No A5/V-series prompt
- `ERR_SEVERITY_MISSING`: B-series without `## Severity`
- `ERR_DAG_CYCLE`: Cycle in `depends_on` graph
- `WARN_BUGFIX_NO_VERIFY`: B-series without V-loop prompt
- `WARN_B_SERIES_BUDGET`: >5 B-series
- `WARN_B_SERIES_RESCOPE`: >8 B-series
- `WARN_VERSION_MISMATCH`: Protocol version inconsistency
- `WARN_DAG_UNKNOWN_DEP`: Unknown dependency reference
- `WARN_MISSING_REPOS`: A/B-series without repos
- `WARN_MISSING_EXECUTION`: Completed output without execution block

---

## Example Transformation

### Before (v2)

```markdown
## Step 3: Create the Service

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
    
    public async Task<Exercise?> GetByIdAsync(Guid id, CancellationToken ct)
    {
        _logger.LogInformation("Getting exercise {Id}", id);
        return await _repository.GetByIdAsync(id, ct);
    }
}
\`\`\`
```

### After (v3)

```markdown
## Reference Points

- **Service pattern**: Follow the structure of `UserService` in `src/Services/`
- **Repository injection**: Use the same DI pattern as `CategoryService`
- **Logging convention**: Apply the logging pattern from `ApiControllerBase`

## Implementation Requirements

### ExerciseService

Create a new service class implementing `IExerciseService`:

- Inject `IRepository<Exercise>` and `ILogger<ExerciseService>` via constructor
- Implement `GetByIdAsync(Guid id, CancellationToken ct)`:
  - Log at Information level before fetching
  - Return null if not found (don't throw)
- Follow existing service conventions for async/await patterns

## Contracts

### IExerciseService (new interface)

| Method | Returns | Notes |
|--------|---------|-------|
| GetByIdAsync(Guid, CancellationToken) | Task<Exercise?> | Returns null if not found |
```

---

## Your Task

Migrate the workpack specified below to Protocol v5.

**Output**:
1. Updated `00_request.md`
2. Transformed prompt files (with YAML front-matter)
3. Updated `A5_integration_meta.md` as Merge Reviewer (V1 gate)
4. `V_bugfix_verify.md` added (if B-series exist)
5. `## Severity` added to all B-series prompts
6. `R1_retrospective.md` added from template
7. Output JSONs updated with `repos`, `execution`, `change_details`
8. `MIGRATION_NOTES.md` with uncertainties

---

**Workpack to Migrate:**

<PASTE WORKPACK NAME OR PATH BELOW>
