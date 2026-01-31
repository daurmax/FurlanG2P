# Prompt Style Guide — Workpack Protocol v3

> **Core Principle**: Prompts describe *what* to implement and *where* to find patterns, not *how* the code should look. Agents are **implementers**, not copy-pasters.

---

## Table of Contents

1. [Philosophy](#philosophy)
2. [The 80/20 Rule](#the-8020-rule)
3. [Prompt Structure](#prompt-structure)
4. [Reference Points](#reference-points)
5. [Valid vs Invalid Examples](#valid-vs-invalid-examples)
6. [Anti-Patterns](#anti-patterns)
7. [Pre-Commit Checklist](#pre-commit-checklist)

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
| Function/class signatures (when new) | Full method bodies |
| Verification commands | Implementation details agent can derive |

---

## The 80/20 Rule

**Maximum 20% of a prompt may contain code-like content**, and only:

- Function/class signatures (when defining new contracts)
- Type definitions (when defining new data structures)
- Configuration snippets (when specific format is required)
- Command examples (for verification/setup)

The remaining **80%+ must be prose**: objectives, requirements, reference points, acceptance criteria.

### How to Measure

Rough estimate: If you have 100 lines in a prompt, max 20 lines can be code fences. If you're exceeding this, refactor to use semantic references.

---

## Prompt Structure

Every v3 prompt follows this structure:

```markdown
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

New classes/functions to define (signatures only, or reference to existing).

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

- **Normalizer pattern**: Follow the structure of `Normalizer` class in `src/furlan_g2p/normalization/normalizer.py`
- **Rule engine pattern**: Implement like `RuleEngine` with the same configuration injection style
- **CLI command pattern**: Use `ipa_command` as the template for CLI subcommands
- **Error handling**: Apply the same try-except-log pattern used in `cli/main.py`
```

### What Makes a Good Reference?

| Good Reference | Bad Reference |
|----------------|---------------|
| `Follow the pattern of Normalizer.normalize method` | `See lines 45-120 of normalizer.py` |
| `Implement like RuleEngine does` | `Copy the code from RuleEngine` |
| `Use the same DI pattern as in phonology/` | `Add these 15 lines to __init__.py` |
| `Apply the validation pattern from tokenizer` | `Override these methods with this exact code` |

### Reference Stability

Prefer references that are **semantically stable**:

1. **Class/Function names** — Change rarely
2. **Method names** — Change occasionally  
3. **File paths** — Change sometimes
4. **Line numbers** — Change frequently ❌ AVOID

---

## Valid vs Invalid Examples

### ❌ INVALID: Complete Implementation

```markdown
## Step 3: Create the Service

Create `phoneme_service.py`:

\`\`\`python
class PhonemeService:
    def __init__(self, lexicon: Lexicon):
        self._lexicon = lexicon
    
    def convert(self, word: str) -> str:
        if word in self._lexicon:
            return self._lexicon[word]
        return self._apply_rules(word)
    
    # ... 50 more lines
\`\`\`
```

### ✅ VALID: Semantic Reference + Requirements

```markdown
## Implementation Requirements

Create `PhonemeService` class in `src/furlan_g2p/g2p/`:

- Follow the pattern of `Normalizer` class in `src/furlan_g2p/normalization/`
- Accept `Lexicon` and `RuleEngine` via constructor injection
- Implement `convert(word: str) -> str | None` method
- Return `None` for words not found in lexicon and not processable by rules
- All public methods must have type hints and docstrings
- Log at DEBUG level when falling back to rule-based conversion
```

### ❌ INVALID: Line Number References

```markdown
See lines 45-89 of normalizer.py for the pattern.
Modify line 123 of tokenizer.py.
```

### ✅ VALID: Semantic References

```markdown
See the `Normalizer.normalize` method for the pattern.
Modify the `Tokenizer.split_sentences` method.
```

---

## Anti-Patterns

### ❌ Vague References

```markdown
Implement it like we usually do.
Follow the standard pattern.
```

### ❌ Overly Prescriptive

```markdown
Add this exact code:
\`\`\`python
# 100 lines of code
\`\`\`
```

### ❌ Missing Verification

```markdown
## Verification

Make sure it works.
```

### ✅ Concrete Verification

```markdown
## Verification

### Commands

\`\`\`bash
pytest tests/test_phoneme_service.py -v
mypy src/furlan_g2p/g2p/phoneme_service.py
\`\`\`

### Checklist

- [ ] All tests pass
- [ ] Type checking passes
- [ ] `furlang2p ipa "test"` returns expected output
```

---

## FurlanG2P-Specific Guidelines

### Module Structure References

| Module | Description | Example Pattern |
|--------|-------------|-----------------|
| `normalization/` | Text normalization | `Normalizer` class with `normalize(text)` method |
| `tokenization/` | Sentence/word splitting | `Tokenizer` class with iterator pattern |
| `g2p/` | Grapheme-to-phoneme | `RuleEngine` with `apply(word)` method |
| `phonology/` | IPA, syllables, stress | Stateless functions with type hints |
| `cli/` | Command-line interface | Click commands with `@click.command()` decorator |

### Coding Standards Reference

Always mention:
- Check `AGENTS.md` for coding standards
- Check `docs/references.md` for linguistic sources
- Use type hints everywhere
- Follow ruff/mypy configurations in `pyproject.toml`

---

## Pre-Commit Checklist

Before committing a prompt, verify:

- [ ] **80/20 Rule**: Max 20% code, 80%+ prose
- [ ] **No complete implementations**: Only signatures if needed
- [ ] **Semantic references**: Class/method names, not line numbers
- [ ] **Clear objective**: One-paragraph description of WHAT
- [ ] **Verification commands**: Specific pytest/mypy/ruff commands
- [ ] **Handoff JSON**: Template included
- [ ] **Scope defined**: In/out of scope clear
- [ ] **Constraints listed**: Critical rules marked
