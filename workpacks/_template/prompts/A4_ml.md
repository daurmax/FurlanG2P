# ML Agent Prompt

> ML agent for FurlanG2P. Handles the optional ML exception-model interface, training pipelines, and model integration behind the `[ml]` extra.

> **v5**: This template includes YAML front-matter. Fill in `depends_on` and `repos` before use.

---

## YAML Front-Matter (v5)

```yaml
---
depends_on: [A1_library]    # ML interface depends on core library types
repos: [FurlanG2P]          # repos this prompt touches
---
```

---

## READ FIRST

1. `./README.md` — Project overview, ML extra section
2. `./AGENTS.md` — Agent guidelines
3. `./src/furlan_g2p/ml/` — Existing ML interface and null implementation
4. `./workpacks/instances/<workpack>/00_request.md` — Original request
5. `./workpacks/instances/<workpack>/01_plan.md` — Full plan
6. `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md` — Prompt conventions (v5)

---

## Context

This is part of workpack: `YYYY-MM-DD_<category>_<short-slug>`

**Objective**: <!-- One-line summary of the ML work to be done -->

---

## Delivery Mode

- **PR-based**: Open a PR targeting `main` and link it in `99_status.md`.
- **Direct push**: Push directly to `main`; record commits in `99_status.md`.

---

## Primary Modules

| Module | Path | Purpose |
|--------|------|---------|
| ML interface | `src/furlan_g2p/ml/` | Exception model ABC, null impl, model loading |
| Services | `src/furlan_g2p/services/` | Pipeline orchestration (ML integration point) |

---

## Objective

<!--
Describe WHAT ML changes must be accomplished.
FurlanG2P uses a hybrid G2P design: lexicon → rules → optional ML exception model.
Focus on the ML exception model interface, training/inference pipeline, or model integration.
-->

---

## Reference Points

<!--
Example:
- **ML interface**: Follow the ABC in `src/furlan_g2p/ml/base.py`
- **Null implementation**: See `NullExceptionModel` for the no-op pattern
- **Integration point**: See `Phonemizer.phonemize` method for where ML is invoked
-->

---

## Implementation Requirements

<!--
Example:
- Implement a concrete exception model using the existing ABC
- Model must be loaded lazily (not at import time)
- All ML dependencies must be behind the `[ml]` optional extra
- Model inference must return results compatible with the Phonemizer pipeline
-->

- Requirement 1
- Requirement 2

---

## Constraints

- **CRITICAL**: ML dependencies MUST be optional — behind `[ml]` extra in `pyproject.toml`
- **CRITICAL**: Base install (`pip install furlan-g2p`) MUST NOT require ML dependencies
- Model loading must be lazy (import-time should not fail without ML deps)
- Follow the existing ABC interface in `src/furlan_g2p/ml/`
- Follow ruff/mypy configs in `pyproject.toml`

---

## Verification

```bash
# Verify base install works without ML deps
pip install -e .
python -c "from furlan_g2p import Phonemizer; print('OK')"

# Verify ML install works
pip install -e ".[ml,dev]"
python -m pytest tests/ -v -k ml
mypy src/furlan_g2p/ml/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/instances/<workpack>/outputs/A4_ml.json`

<!-- lint-ignore-code-block -->
```json
{
  "schema_version": "1.0",
  "workpack": "<workpack>",
  "prompt": "A4_ml",
  "component": "ml",
  "delivery_mode": "<pr|direct_push>",
  "branch": { "base": "<base-branch>", "work": "<work-branch>", "merge_target": "main" },
  "repos": ["FurlanG2P"],
  "artifacts": { "pr_url": "", "commit_shas": [] },
  "changes": { "files_modified": [], "files_created": [], "contracts_changed": [], "breaking_change": false },
  "change_details": [],
  "verification": {
    "commands": [
      {"cmd": "pip install -e \".[ml,dev]\"", "result": "pass"},
      {"cmd": "python -m pytest tests/ -v -k ml", "result": "pass"},
      {"cmd": "mypy src/furlan_g2p/ml/", "result": "pass"}
    ],
    "regression_added": false,
    "regression_notes": ""
  },
  "execution": { "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 },
  "handoff": { "summary": "", "next_steps": [], "known_issues": [] },
  "notes": ""
}
```

---

## Stop Conditions

Stop and escalate if:

- ML ABC interface requires changes (coordinate with A1_library)
- Training data format is undefined
- Model size or dependency constraints are unclear

---

## Deliverables

- [ ] ML changes implemented
- [ ] Base install still works without ML deps
- [ ] ML tests pass with `[ml]` extra
- [ ] Output JSON created
