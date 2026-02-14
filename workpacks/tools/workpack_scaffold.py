#!/usr/bin/env python3
"""
workpack_scaffold.py — Workpack Prompt Scaffolder (Protocol v5)

Reads a workpack's `01_plan.md` and generates skeleton prompt files for each
agent listed in the plan.  Skips prompts whose files already exist.

Usage:
  python workpacks/tools/workpack_scaffold.py <workpack-path>

Example:
  python workpacks/tools/workpack_scaffold.py workpacks/instances/2026-02-10_feature_my-feature

The tool reads:
  - 01_plan.md → extracts the prompt table (A-series, B-series, V-series)
  - _template/prompts/ → copies matching template or generates a default skeleton

Generated prompts include YAML front-matter with `depends_on` and `repos` fields
(pre-populated from the plan when parseable) and all mandatory v5 sections.

Environment:
  Shares the virtual-environment bootstrap with workpack_lint.py.
"""

import os
import sys
from pathlib import Path

# ---------------------------------------------------------------------------
# Virtual-environment bootstrap (same logic as workpack_lint.py)
# ---------------------------------------------------------------------------

def _ensure_venv() -> None:
    if sys.prefix != sys.base_prefix:
        return
    venv_dir = Path(__file__).resolve().parent / ".venv"
    if not venv_dir.exists():
        import venv as _venv
        print(f"[scaffold] Creating virtual environment at {venv_dir} ...")
        _venv.create(str(venv_dir), with_pip=True)
    if os.name == "nt":
        python = venv_dir / "Scripts" / "python.exe"
    else:
        python = venv_dir / "bin" / "python"
    if not python.exists():
        print(f"ERROR: venv Python not found at {python}", file=sys.stderr)
        sys.exit(1)
    print(f"[scaffold] Re-running inside venv: {venv_dir}")
    os.execv(str(python), [str(python)] + sys.argv)

_ensure_venv()

# ---------------------------------------------------------------------------
import argparse
import re
import shutil
import textwrap


# ---------------------------------------------------------------------------
# Template mapping
# ---------------------------------------------------------------------------
TEMPLATE_MAP = {
    "A5": "A5_integration_meta.md",
    "B":  "B_template.md",
    "V":  "V_bugfix_verify.md",
    "R":  "R_retrospective.md",
}


def _templates_dir() -> Path:
    return Path(__file__).resolve().parent.parent / "_template" / "prompts"


def _resolve_template(stem: str) -> Path | None:
    """Return the template path for a given prompt stem, or None."""
    tdir = _templates_dir()
    # Exact match first
    exact = tdir / f"{stem}.md"
    if exact.exists():
        return exact
    # Prefix match
    for prefix, tpl_name in TEMPLATE_MAP.items():
        if stem.startswith(prefix):
            candidate = tdir / tpl_name
            if candidate.exists():
                return candidate
    return None


def _default_skeleton(stem: str, workpack_name: str) -> str:
    """Generate a minimal v5 prompt skeleton."""
    series = stem[0] if stem else "A"
    agent_type = {
        "A": "Feature Implementation",
        "B": "Bug Fix",
        "V": "Verification",
        "R": "Retrospective",
    }.get(series, "Agent")

    return textwrap.dedent(f"""\
        ---
        depends_on: []
        repos: []
        ---
        # {agent_type} Agent Prompt — {stem}

        > <!-- One-line objective summary -->

        ---

        ## READ FIRST

        - `./workpacks/instances/{workpack_name}/00_request.md`
        - `./workpacks/instances/{workpack_name}/01_plan.md`
        - `./workpacks/_template/prompts/PROMPT_STYLE_GUIDE.md`

        ## Context

        **Workpack**: `{workpack_name}`

        ## Delivery Mode

        - [x] **PR-based** (default)

        ## Objective

        <!-- Describe WHAT to accomplish -->

        ## Reference Points

        <!-- Semantic references to existing code patterns -->

        ## Implementation Requirements

        <!-- Behavioral specifications -->

        ## Subagent Strategy

        <!-- Identify parallelizable subtasks -->

        ## Task Tracking

        Use a structured todo list for multi-step work if your tool supports it.

        ## Scope

        ### In Scope
        - <!-- Item -->

        ### Out of Scope
        - <!-- Item -->

        ## Acceptance Criteria

        - [ ] <!-- Criterion -->

        ## Constraints

        - <!-- Constraint -->

        ## Verification

        ```bash
        # Build / test commands
        ```

        ## Handoff Output (JSON)

        **Path**: `./workpacks/instances/{workpack_name}/outputs/{stem}.json`

        <!-- lint-ignore-code-block -->
        ```json
        {{
          "schema_version": "1.0",
          "workpack": "{workpack_name}",
          "prompt": "{stem}",
          "component": "",
          "delivery_mode": "pr",
          "branch": {{ "base": "", "work": "", "merge_target": "main" }},
          "artifacts": {{ "pr_url": "", "commit_shas": [] }},
          "changes": {{ "files_modified": [], "files_created": [], "contracts_changed": [], "breaking_change": false }},
          "verification": {{ "commands": [] }},
          "execution": {{ "model": "", "tokens_in": 0, "tokens_out": 0, "duration_ms": 0 }},
          "handoff": {{ "summary": "", "next_steps": [], "known_issues": [] }},
          "notes": ""
        }}
        ```

        ## Stop Conditions

        - <!-- When to escalate -->

        ## Deliverables

        - [ ] <!-- Deliverable -->
    """)


# ---------------------------------------------------------------------------
# Plan parser
# ---------------------------------------------------------------------------
_PROMPT_TABLE_RE = re.compile(
    r"\|\s*`?prompts/(?P<file>[A-Z]\w+\.md)`?\s*\|",
    re.IGNORECASE,
)

_SIMPLE_TABLE_RE = re.compile(
    r"\|\s*(?P<stem>[ABV]\d+_[\w_]+)\s*\|",
)


def extract_prompts_from_plan(plan_path: Path) -> list[str]:
    """Return a list of prompt stem names found in 01_plan.md tables."""
    if not plan_path.exists():
        return []
    content = plan_path.read_text(encoding="utf-8")
    stems: list[str] = []
    seen: set[str] = set()

    # Match `prompts/A1_library.md` references in tables
    for m in _PROMPT_TABLE_RE.finditer(content):
        stem = m.group("file").removesuffix(".md")
        if stem not in seen:
            stems.append(stem)
            seen.add(stem)

    # Match bare stems like `A1_library` in table cells
    for m in _SIMPLE_TABLE_RE.finditer(content):
        stem = m.group("stem")
        if stem not in seen:
            stems.append(stem)
            seen.add(stem)

    return stems


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(
        description="Scaffold prompt files from a workpack plan (Protocol v5).",
    )
    parser.add_argument(
        "workpack",
        help="Path to the workpack folder (e.g. workpacks/instances/2026-02-10_feature_xxx)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing prompt files (default: skip existing)",
    )
    args = parser.parse_args()

    wp = Path(args.workpack).resolve()
    if not wp.is_dir():
        print(f"ERROR: Workpack folder not found: {wp}", file=sys.stderr)
        sys.exit(1)

    plan_path = wp / "01_plan.md"
    prompts_dir = wp / "prompts"
    prompts_dir.mkdir(exist_ok=True)

    stems = extract_prompts_from_plan(plan_path)
    if not stems:
        print(f"No prompts found in {plan_path}. Nothing to scaffold.")
        sys.exit(0)

    print(f"Workpack : {wp.name}")
    print(f"Prompts  : {len(stems)} found in plan")
    print()

    created = 0
    skipped = 0
    for stem in stems:
        target = prompts_dir / f"{stem}.md"
        if target.exists() and not args.force:
            print(f"  ⊘ {stem}.md — already exists (skip)")
            skipped += 1
            continue

        template = _resolve_template(stem)
        if template:
            shutil.copy2(template, target)
            print(f"  ✓ {stem}.md — copied from template {template.name}")
        else:
            target.write_text(
                _default_skeleton(stem, wp.name), encoding="utf-8"
            )
            print(f"  ✓ {stem}.md — generated default skeleton")
        created += 1

    print()
    print(f"Done: {created} created, {skipped} skipped.")


if __name__ == "__main__":
    main()
