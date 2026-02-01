# ML Interface Agent Prompt

> Define IExceptionModel interface and null implementation with optional [ml] extra.

---

## READ FIRST

1. `README.md` — Project overview
2. `AGENTS.md` — Agent guidelines
3. `src/furlan_g2p/core/interfaces.py` — Existing interface patterns
4. `pyproject.toml` — Current dependencies and extras
5. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/00_request.md` — Full requirements
6. `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/01_plan.md` — Work breakdown

---

## Context

This is part of workpack: `2026-02-01_feature_hybrid-g2p-paradigm`

**Objective**: Define the interface for optional ML-based exception models and set up the `[ml]` optional dependency group, keeping the base install lightweight.

---

## Delivery Mode

- **PR-based**: Create a PR targeting `feature/hybrid-g2p-paradigm`

---

## Objective

Create the abstraction layer for ML-based exception handling in the G2P pipeline. This prompt establishes:

1. **Interface contract** — What any exception model must implement
2. **Null implementation** — Default when ML is not installed
3. **Optional extra** — `pip install furlan-g2p[ml]` for ML dependencies
4. **Import guards** — Graceful degradation when ML deps missing

This enables future ML model implementations without coupling the core library to heavy dependencies.

---

## Reference Points

- **Interface pattern**: Follow ABC style from `core/interfaces.py`
- **Optional extras**: Study `pyproject.toml` for existing extras patterns
- **Lazy imports**: Use import guards pattern for optional dependencies

---

## Implementation Requirements

### 1. Create `src/furlan_g2p/ml/` package

Structure:
- `__init__.py` — Public exports with import guards
- `interfaces.py` — IExceptionModel interface
- `null_model.py` — NullExceptionModel implementation

### 2. IExceptionModel Interface

Define abstract base class:

**Methods**:
- `predict(word: str, dialect: str | None = None) -> ExceptionPrediction | None`
  - Returns prediction with IPA and confidence, or None if not confident
- `predict_batch(words: list[str], dialect: str | None = None) -> list[ExceptionPrediction | None]`
  - Batch prediction for efficiency
- `is_available() -> bool`
  - Check if model is loaded and ready
- `get_model_info() -> dict`
  - Return model metadata (name, version, etc.)

### 3. ExceptionPrediction Dataclass

Result type for predictions:
- `ipa: str` — Predicted IPA with stress
- `confidence: float` — Model confidence [0.0, 1.0]
- `source: str` — Model identifier
- `alternatives: list[tuple[str, float]]` — N-best with confidences (optional)

### 4. NullExceptionModel

Default implementation when ML is disabled:
- `predict()` always returns `None`
- `is_available()` returns `False`
- `get_model_info()` returns `{"name": "null", "available": False}`

This allows the pipeline to work without ML installed.

### 5. Update pyproject.toml

Add `[ml]` optional extra:

```toml
[project.optional-dependencies]
ml = [
    "torch>=2.0",
    "transformers>=4.30",
]
```

Note: These are placeholder deps. Actual model implementation will refine this.

### 6. Import Guards

In `ml/__init__.py`:
- Try to import ML dependencies
- If ImportError, export only NullExceptionModel
- Provide clear error message for missing deps
- Export `ML_AVAILABLE: bool` flag

### 7. Pipeline Integration Point

Define how the exception model integrates with the pipeline:
- Called after lexicon lookup fails
- Called after rules produce output (for reranking/correction)
- Confidence threshold determines if prediction is used

Document this in interface docstrings.

---

## Contracts

### IExceptionModel (interface)

| Method | Returns | Notes |
|--------|---------|-------|
| `predict(word, dialect)` | `ExceptionPrediction \| None` | Single prediction |
| `predict_batch(words, dialect)` | `list[ExceptionPrediction \| None]` | Batch |
| `is_available()` | `bool` | Model ready check |
| `get_model_info()` | `dict` | Metadata |

### ExceptionPrediction (dataclass)

| Field | Type | Notes |
|-------|------|-------|
| `ipa` | `str` | Predicted IPA |
| `confidence` | `float` | [0.0, 1.0] |
| `source` | `str` | Model ID |
| `alternatives` | `list[tuple[str, float]]` | N-best (optional) |

---

## Scope

### In Scope

- IExceptionModel interface
- ExceptionPrediction dataclass
- NullExceptionModel implementation
- `[ml]` optional extra in pyproject.toml
- Import guards
- Module documentation

### Out of Scope

- Actual ML model implementation (future work)
- Training infrastructure
- Model loading logic
- CLI for ML operations

---

## Acceptance Criteria

- [ ] `furlan_g2p.ml` is importable without ML dependencies
- [ ] `IExceptionModel` interface is defined
- [ ] `NullExceptionModel` works as default
- [ ] `pip install -e ".[ml]"` installs ML dependencies
- [ ] Import guards work correctly
- [ ] `ML_AVAILABLE` flag reflects actual state
- [ ] No ML imports in base package
- [ ] mypy passes

---

## Constraints

- **CRITICAL**: Base install must NOT require torch/transformers
- **CRITICAL**: Import guards must not slow down base imports
- Interface must be stable (unlikely to change)
- Keep placeholder deps minimal

---

## Verification

```bash
# Verify base install has no ML deps
pip install -e "."
python -c "from furlan_g2p.ml import NullExceptionModel, ML_AVAILABLE; print(f'ML_AVAILABLE={ML_AVAILABLE}')"

# Verify ML extra works
pip install -e ".[ml]"
python -c "from furlan_g2p.ml import ML_AVAILABLE; assert ML_AVAILABLE, 'ML should be available'"

mypy src/furlan_g2p/ml/
ruff check src/furlan_g2p/ml/
```

---

## Handoff Output (JSON) — REQUIRED

**Path**: `./workpacks/2026-02-01_feature_hybrid-g2p-paradigm/outputs/A5_ml_interface.json`

---

## Stop Conditions

- **STOP** if unsure about torch version requirements (research first)
- **CONTINUE** for interface design questions (use patterns from literature)

---

## Deliverables

- [ ] `src/furlan_g2p/ml/__init__.py`
- [ ] `src/furlan_g2p/ml/interfaces.py`
- [ ] `src/furlan_g2p/ml/null_model.py`
- [ ] Updated `pyproject.toml` with `[ml]` extra
- [ ] Handoff output JSON
- [ ] PR created
