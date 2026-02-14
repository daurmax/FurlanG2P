#!/usr/bin/env python3
"""
workpack_lint.py — Workpack Protocol v2/v3/v4 Linter

Validates workpacks in the ./workpacks/ directory.
- v2 workpacks: 00_request.md contains "Workpack Protocol Version: 2"
- v3 workpacks: 00_request.md contains "Workpack Protocol Version: 3"
- v4 workpacks: 00_request.md contains "Workpack Protocol Version: 4"

v3 adds code-block detection in prompts (WARNING).
v4 promotes code-blocks to ERROR, adds severity/verification/budget checks.

Exit codes:
  0 — All workpacks pass validation
  1 — One or more validation errors found
  2 — Warnings found and --strict flag is set

Usage:
  python workpacks/tools/workpack_lint.py [--strict]
  
Flags:
  --strict    Treat warnings as errors (exit code 2 if warnings found)

Environment:
  This script auto-creates and re-runs inside a Python virtual environment
  (tools/.venv/) when invoked outside one, ensuring isolation.
"""

import os
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Virtual-environment bootstrap — runs BEFORE any other imports
# ---------------------------------------------------------------------------
def _ensure_venv() -> None:
    """Ensure the script runs inside a virtual environment.

    If called outside a venv the function:
    1. Creates ``<script_dir>/.venv/`` (if absent).
    2. Re-executes the current script with the venv's Python interpreter.
    """
    # Already inside a venv — nothing to do.
    if sys.prefix != sys.base_prefix:
        return

    venv_dir = Path(__file__).resolve().parent / ".venv"

    if not venv_dir.exists():
        import venv as _venv  # noqa: delayed import – only needed once

        print(f"[lint] Creating virtual environment at {venv_dir} ...")
        _venv.create(str(venv_dir), with_pip=True)

    # Determine the venv Python path.
    if os.name == "nt":
        python = venv_dir / "Scripts" / "python.exe"
    else:
        python = venv_dir / "bin" / "python"

    if not python.exists():
        print(f"ERROR: venv Python not found at {python}", file=sys.stderr)
        sys.exit(1)

    print(f"[lint] Re-running inside venv: {venv_dir}")
    os.execv(str(python), [str(python)] + sys.argv)


_ensure_venv()
# ---------------------------------------------------------------------------
# From here on we are guaranteed to run inside the venv.
# ---------------------------------------------------------------------------

import argparse
import re
import json


# Languages that trigger code-block warnings in v3 prompts
CODE_BLOCK_LANGUAGES = {
    # C# / .NET
    "csharp", "cs", "c#",
    # Python
    "python", "py",
    # JavaScript / TypeScript
    "javascript", "js", "typescript", "ts", "jsx", "tsx",
    # Other common languages
    "java", "kotlin", "swift", "go", "rust", "ruby", "php",
    "sql", "xml", "html", "css", "scss", "sass",
    # Config formats (allowed in some contexts but flagged)
    "json", "yaml", "yml", "toml",
}

# Code blocks that are allowed (verification commands, output skeletons)
ALLOWED_CODE_BLOCK_LANGUAGES = {
    "bash", "sh", "shell", "powershell", "ps1", "cmd", "bat",
    "console", "terminal", "text", "plaintext", "diff",
}

# Marker to suppress code-block warning for a specific block
LINT_IGNORE_MARKER = "<!-- lint-ignore-code-block -->"


def get_workpacks_dir() -> Path:
    """Get the workpacks directory relative to this script or CWD."""
    # Try relative to script location first
    script_dir = Path(__file__).parent.parent.parent
    workpacks_dir = script_dir / "workpacks"
    if workpacks_dir.exists():
        return workpacks_dir
    
    # Fall back to CWD
    cwd_workpacks = Path.cwd() / "workpacks"
    if cwd_workpacks.exists():
        return cwd_workpacks
    
    # Try parent directories
    for parent in Path.cwd().parents:
        candidate = parent / "workpacks"
        if candidate.exists():
            return candidate
    
    raise FileNotFoundError("Could not find workpacks directory")


def get_workpack_version(workpack_path: Path) -> int:
    """
    Get the protocol version of a workpack from 00_request.md.
    
    Returns:
        3 for v3 workpacks
        2 for v2 workpacks
        0 for older/unknown workpacks
    """
    request_file = workpack_path / "00_request.md"
    if not request_file.exists():
        return 0
    
    try:
        content = request_file.read_text(encoding="utf-8")
        # Check for v5 first
        if re.search(r"Workpack Protocol Version:\s*5", content):
            return 5
        # Then v4
        if re.search(r"Workpack Protocol Version:\s*4", content):
            return 4
        # Then v3
        if re.search(r"Workpack Protocol Version:\s*3", content):
            return 3
        # Then v2
        if re.search(r"Workpack Protocol Version:\s*2", content):
            return 2
        return 0
    except Exception:
        return 0


def is_v2_workpack(workpack_path: Path) -> bool:
    """Check if workpack declares Protocol Version 2 in 00_request.md."""
    return get_workpack_version(workpack_path) == 2


def is_v3_workpack(workpack_path: Path) -> bool:
    """Check if workpack declares Protocol Version 3 in 00_request.md."""
    return get_workpack_version(workpack_path) == 3


def is_v5_workpack(workpack_path: Path) -> bool:
    """Check if workpack declares Protocol Version 5 in 00_request.md."""
    return get_workpack_version(workpack_path) == 5


def is_v4_workpack(workpack_path: Path) -> bool:
    """Check if workpack declares Protocol Version 4 in 00_request.md."""
    return get_workpack_version(workpack_path) == 4


def get_completed_prompts(workpack_path: Path) -> set:
    """
    Parse 99_status.md to find completed prompts.
    
    Accepted completion markers:
    A-series: 🟢 Complete, 🟢 Done, ✅ Applied, ✅ Done, ✅ Completed
    B-series: ✅ Fixed, ✅ Resolved, ✅ Done, ✅ Applied
    
    Returns a set of prompt basenames (e.g., {"A1_library", "B1_cli_fix"})
    """
    status_file = workpack_path / "99_status.md"
    if not status_file.exists():
        return set()
    
    completed = set()
    try:
        content = status_file.read_text(encoding="utf-8")
        
        # A-series accepted markers
        a_markers = r"(🟢\s*Complete|🟢\s*Done|✅\s*Applied|✅\s*Done|✅\s*Completed)"
        
        # B-series accepted markers (including ✅ Applied)
        b_markers = r"(✅\s*Fixed|✅\s*Resolved|✅\s*Done|✅\s*Applied)"
        
        # Look for A-series completions in table format: "| A1_library | ... | 🟢 Complete |"
        a_table_pattern = rf"\|\s*(A\d+_[\w_]+)\s*\|[^|]*{a_markers}"
        for match in re.finditer(a_table_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))
        
        # Also match simpler patterns: "A1_library ... 🟢 Complete" on same line
        a_simple_pattern = rf"(A\d+_[\w_]+)[^\n]*{a_markers}"
        for match in re.finditer(a_simple_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))
        
        # Look for B-series completions in table format: "| B1_xxx | ... | ✅ Fixed |"
        b_table_pattern = rf"\|\s*(B\d+_[\w_]+)\s*\|[^|]*{b_markers}"
        for match in re.finditer(b_table_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))
        
        # Also match simpler patterns: "B1_xxx ... ✅ Fixed" on same line
        b_simple_pattern = rf"(B\d+_[\w_]+)[^\n]*{b_markers}"
        for match in re.finditer(b_simple_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))

        # V-series completion markers
        v_markers = r"(✅\s*Passed|✅\s*Done|🟢\s*Complete|🟢\s*Done)"
        v_table_pattern = rf"\|\s*(V\d+_[\w_]+)\s*\|[^|]*{v_markers}"
        for match in re.finditer(v_table_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))
        v_simple_pattern = rf"(V\d+_[\w_]+)[^\n]*{v_markers}"
        for match in re.finditer(v_simple_pattern, content, re.IGNORECASE):
            completed.add(match.group(1))

    except Exception:
        pass
    
    return completed


def detect_code_blocks_in_prompt(prompt_path: Path) -> list:
    """
    Detect code blocks in a prompt file that shouldn't contain code.
    
    Returns a list of (line_number, language, is_suppressed) tuples for each code block found.
    """
    code_blocks = []
    
    try:
        content = prompt_path.read_text(encoding="utf-8")
        lines = content.split('\n')
        
        # Pattern to match code block start: ```language
        code_block_pattern = re.compile(r'^```(\w+)?\s*$')
        
        prev_line_has_ignore = False
        
        for i, line in enumerate(lines, 1):
            # Check if previous line has the ignore marker
            if i > 1:
                prev_line = lines[i - 2]  # -2 because enumerate is 1-indexed
                prev_line_has_ignore = LINT_IGNORE_MARKER in prev_line
            
            match = code_block_pattern.match(line.strip())
            if match:
                language = match.group(1) or ""
                language_lower = language.lower()
                
                # Check if this is a flagged language
                if language_lower in CODE_BLOCK_LANGUAGES:
                    is_suppressed = prev_line_has_ignore
                    code_blocks.append((i, language, is_suppressed))
    
    except Exception:
        pass
    
    return code_blocks


def validate_v3_prompts(workpack_path: Path, version: int = 3) -> tuple:
    """
    Validate v3/v4 prompts for code-block violations.
    
    In v3: code blocks are warnings.
    In v4: code blocks are errors.
    
    Returns (errors, warnings) tuple.
    """
    errors = []
    warnings = []
    workpack_name = workpack_path.name
    
    prompts_dir = workpack_path / "prompts"
    if not prompts_dir.exists():
        return errors, warnings
    
    for prompt_file in prompts_dir.glob("*.md"):
        # Only check A*.md, B*.md, V*.md, and R*.md files
        if not re.match(r"^[ABVR]\d+", prompt_file.stem):
            continue
        
        code_blocks = detect_code_blocks_in_prompt(prompt_file)
        
        for line_num, language, is_suppressed in code_blocks:
            if is_suppressed:
                continue  # Skip suppressed warnings
            
            msg = (
                f"[{workpack_name}] Prompt '{prompt_file.stem}' line {line_num}: "
                f"Code block ```{language}``` found. "
                f"Protocol v{version} discourages code in prompts. "
                f"Use semantic references instead, or add '{LINT_IGNORE_MARKER}' above to suppress."
            )
            
            if version >= 4:
                # In v4, code blocks are errors
                errors.append(msg)
            else:
                # In v3, code blocks are warnings
                warnings.append(msg)
    
    return errors, warnings


def validate_v4_checks(workpack_path: Path) -> tuple:
    """
    Validate v4-specific rules:
    - ERR_NO_VERIFICATION: No A5_* or V#_* prompt exists
    - WARN_BUGFIX_NO_VERIFY: B-series present but no V#_* prompt
    - WARN_B_SERIES_BUDGET: >5 B-series prompts
    - WARN_B_SERIES_RESCOPE: >8 B-series prompts
    - ERR_SEVERITY_MISSING: B-series prompt without ## Severity section
    - WARN_VERSION_MISMATCH: Protocol version inconsistency in prompts
    
    Returns (errors, warnings) tuple.
    """
    errors = []
    warnings = []
    workpack_name = workpack_path.name
    
    prompts_dir = workpack_path / "prompts"
    if not prompts_dir.exists():
        return errors, warnings
    
    # Collect prompt types
    a_series = []
    b_series = []
    v_series = []
    a5_exists = False
    
    for prompt_file in prompts_dir.glob("*.md"):
        stem = prompt_file.stem
        if re.match(r"^A\d+", stem):
            a_series.append(prompt_file)
            if stem.startswith("A5"):
                a5_exists = True
        elif re.match(r"^B\d+", stem):
            b_series.append(prompt_file)
        elif re.match(r"^V\d+", stem):
            v_series.append(prompt_file)
    
    # ERR_NO_VERIFICATION: No A5 and no V-series prompt
    if not a5_exists and not v_series:
        errors.append(
            f"[{workpack_name}] ERR_NO_VERIFICATION: No A5_* or V#_* verification prompt found. "
            f"Protocol v4 requires at least one verification gate."
        )
    
    # WARN_BUGFIX_NO_VERIFY: B-series present but no V-series prompt
    if b_series and not v_series:
        warnings.append(
            f"[{workpack_name}] WARN_BUGFIX_NO_VERIFY: {len(b_series)} B-series prompt(s) found "
            f"but no V#_* verification prompt. Consider adding V2_bugfix_verify.md for V-loop."
        )
    
    # B-Series budget checks
    b_count = len(b_series)
    if b_count > 8:
        warnings.append(
            f"[{workpack_name}] WARN_B_SERIES_RESCOPE: {b_count} B-series prompts (>8). "
            f"Consider re-scoping this workpack — it may be too large."
        )
    elif b_count > 5:
        warnings.append(
            f"[{workpack_name}] WARN_B_SERIES_BUDGET: {b_count} B-series prompts (>5). "
            f"Bug count is elevated — monitor closely."
        )
    
    # ERR_SEVERITY_MISSING: B-series prompt without ## Severity
    for b_file in b_series:
        try:
            content = b_file.read_text(encoding="utf-8")
            if not re.search(r"^##\s+Severity", content, re.MULTILINE):
                errors.append(
                    f"[{workpack_name}] ERR_SEVERITY_MISSING: B-series prompt '{b_file.stem}' "
                    f"is missing a '## Severity' section. Required in Protocol v4."
                )
        except Exception:
            pass
    
    # WARN_VERSION_MISMATCH: Check prompts reference correct protocol version
    for prompt_file in prompts_dir.glob("*.md"):
        if not re.match(r"^[ABVR]", prompt_file.stem):
            continue
        try:
            content = prompt_file.read_text(encoding="utf-8")
            # Check for explicit v3 references that should be v4+
            if re.search(r"Protocol v3", content, re.IGNORECASE):
                warnings.append(
                    f"[{workpack_name}] WARN_VERSION_MISMATCH: Prompt '{prompt_file.stem}' "
                    f"references 'Protocol v3' but workpack is v4+. Update references."
                )
        except Exception:
            pass
    
    return errors, warnings


def _parse_yaml_front_matter(prompt_path: Path) -> dict:
    """Extract YAML front-matter (between --- markers) from a prompt file.

    Returns a dict with parsed keys, or empty dict if none found.
    Simple parser — handles ``key: value`` and ``key: [item, ...]`` lines.
    """
    try:
        lines = prompt_path.read_text(encoding="utf-8").splitlines()
    except Exception:
        return {}

    if not lines or lines[0].strip() != "---":
        return {}

    fm_lines: list[str] = []
    for line in lines[1:]:
        if line.strip() == "---":
            break
        fm_lines.append(line)
    else:
        return {}  # no closing ---

    result: dict = {}
    for line in fm_lines:
        m = re.match(r"^(\w[\w_]*):\s*(.*)$", line)
        if not m:
            continue
        key, raw = m.group(1), m.group(2).strip()
        # Parse inline list: [a, b, c]
        if raw.startswith("[") and raw.endswith("]"):
            items = [s.strip().strip("'\"") for s in raw[1:-1].split(",") if s.strip()]
            result[key] = items
        else:
            result[key] = raw
    return result


def validate_v5_checks(workpack_path: Path) -> tuple:
    """
    Validate v5-specific rules:
    - ERR_DAG_CYCLE: Circular dependency in depends_on graph
    - WARN_DAG_UNKNOWN_DEP: depends_on references a prompt that doesn't exist
    - WARN_NO_RETROSPECTIVE: Merged workpack has no R-series prompt
    - WARN_MISSING_REPOS: Prompt front-matter has no repos field
    - WARN_MISSING_EXECUTION: Completed output JSON has no execution block

    Returns (errors, warnings) tuple.
    """
    errors = []
    warnings = []
    workpack_name = workpack_path.name

    prompts_dir = workpack_path / "prompts"
    if not prompts_dir.exists():
        return errors, warnings

    # Collect all prompt stems and their depends_on
    prompt_stems: set[str] = set()
    dag: dict[str, list[str]] = {}

    for pf in prompts_dir.glob("*.md"):
        stem = pf.stem
        if not re.match(r"^[ABVR]", stem):
            continue
        prompt_stems.add(stem)
        fm = _parse_yaml_front_matter(pf)
        deps = fm.get("depends_on", [])
        if isinstance(deps, list):
            dag[stem] = deps
        else:
            dag[stem] = []

        # WARN_MISSING_REPOS — only for A/B series
        if stem[0] in ("A", "B") and not stem.startswith("A0"):
            repos = fm.get("repos")
            if repos is not None and isinstance(repos, list) and len(repos) == 0:
                warnings.append(
                    f"[{workpack_name}] WARN_MISSING_REPOS: Prompt '{stem}' has empty "
                    f"'repos' in front-matter. Declare which repos it touches."
                )

    # DAG validation — unknown deps
    for stem, deps in dag.items():
        for dep in deps:
            if dep and dep not in prompt_stems:
                warnings.append(
                    f"[{workpack_name}] WARN_DAG_UNKNOWN_DEP: Prompt '{stem}' depends on "
                    f"'{dep}' which does not exist in prompts/."
                )

    # DAG validation — cycle detection (simple DFS)
    WHITE, GRAY, BLACK = 0, 1, 2
    color: dict[str, int] = {s: WHITE for s in dag}

    def _dfs(node: str) -> str | None:
        color[node] = GRAY
        for dep in dag.get(node, []):
            if dep not in color:
                continue
            if color[dep] == GRAY:
                return f"{dep} ↔ {node}"
            if color[dep] == WHITE:
                cycle = _dfs(dep)
                if cycle:
                    return cycle
        color[node] = BLACK
        return None

    for stem in dag:
        if color.get(stem) == WHITE:
            cycle = _dfs(stem)
            if cycle:
                errors.append(
                    f"[{workpack_name}] ERR_DAG_CYCLE: Circular dependency detected: {cycle}. "
                    f"Fix the depends_on fields to remove the cycle."
                )
                break  # one error is enough

    # WARN_MISSING_EXECUTION — check completed output JSONs for execution field
    outputs_dir = workpack_path / "outputs"
    if outputs_dir.exists():
        for out_file in outputs_dir.glob("*.json"):
            try:
                data = json.load(out_file.open(encoding="utf-8"))
                if "execution" not in data:
                    warnings.append(
                        f"[{workpack_name}] WARN_MISSING_EXECUTION: Output '{out_file.stem}.json' "
                        f"has no 'execution' block. v5 recommends tracking cost metrics."
                    )
            except Exception:
                pass  # JSON parse errors handled by validate_workpack

    return errors, warnings


def validate_workpack(workpack_path: Path, schema_path: Path) -> list:
    """
    Validate a v2 workpack.
    
    Returns a list of error messages (empty if valid).
    """
    errors = []
    workpack_name = workpack_path.name
    
    # Check outputs/ directory exists
    outputs_dir = workpack_path / "outputs"
    if not outputs_dir.exists():
        errors.append(f"[{workpack_name}] Missing outputs/ directory (required for Protocol v2)")
    
    # Check prompts/ directory exists
    prompts_dir = workpack_path / "prompts"
    if not prompts_dir.exists():
        errors.append(f"[{workpack_name}] Missing prompts/ directory")
        return errors  # Can't continue without prompts
    
    # Check schema exists
    if not schema_path.exists():
        errors.append(f"[{workpack_name}] Schema file not found: {schema_path}")
    
    # Get completed prompts from status
    completed_prompts = get_completed_prompts(workpack_path)
    
    # Check each completed prompt has a corresponding output JSON
    for prompt_file in prompts_dir.glob("*.md"):
        # Only check A*.md, B*.md, V*.md, R*.md files
        if not re.match(r"^[ABVR]\d+", prompt_file.stem):
            continue
        
        prompt_basename = prompt_file.stem
        
        # Only validate if the prompt is marked complete
        if prompt_basename in completed_prompts:
            output_file = outputs_dir / f"{prompt_basename}.json"
            if not output_file.exists():
                errors.append(
                    f"[{workpack_name}] Prompt '{prompt_basename}' is marked complete but "
                    f"output JSON is missing: outputs/{prompt_basename}.json"
                )
            else:
                # Validate JSON is parseable
                try:
                    with open(output_file, "r", encoding="utf-8") as f:
                        data = json.load(f)
                    
                    # Basic schema validation (check required fields)
                    required_fields = [
                        "schema_version", "workpack", "prompt", "component",
                        "delivery_mode", "branch", "changes", "verification", "handoff"
                    ]
                    for field in required_fields:
                        if field not in data:
                            errors.append(
                                f"[{workpack_name}] Output '{prompt_basename}.json' "
                                f"missing required field: {field}"
                            )
                    
                    # Validate workpack and prompt field values match actual names
                    if "workpack" in data and data["workpack"] != workpack_name:
                        errors.append(
                            f"[{workpack_name}] Output '{prompt_basename}.json' "
                            f"has workpack='{data['workpack']}' but should be '{workpack_name}'"
                        )
                    
                    if "prompt" in data and data["prompt"] != prompt_basename:
                        errors.append(
                            f"[{workpack_name}] Output '{prompt_basename}.json' "
                            f"has prompt='{data['prompt']}' but should be '{prompt_basename}'"
                        )
                    
                    # Check nested required fields
                    if "branch" in data:
                        for bf in ["base", "work", "merge_target"]:
                            if bf not in data["branch"]:
                                errors.append(
                                    f"[{workpack_name}] Output '{prompt_basename}.json' "
                                    f"missing branch.{bf}"
                                )
                    
                    if "changes" in data:
                        for cf in ["files_modified", "files_created", "contracts_changed", "breaking_change"]:
                            if cf not in data["changes"]:
                                errors.append(
                                    f"[{workpack_name}] Output '{prompt_basename}.json' "
                                    f"missing changes.{cf}"
                                )
                    
                    if "verification" in data:
                        if "commands" not in data["verification"]:
                            errors.append(
                                f"[{workpack_name}] Output '{prompt_basename}.json' "
                                f"missing verification.commands"
                            )
                    
                    if "handoff" in data:
                        for hf in ["summary", "next_steps", "known_issues"]:
                            if hf not in data["handoff"]:
                                errors.append(
                                    f"[{workpack_name}] Output '{prompt_basename}.json' "
                                    f"missing handoff.{hf}"
                                )
                
                except json.JSONDecodeError as e:
                    errors.append(
                        f"[{workpack_name}] Output '{prompt_basename}.json' "
                        f"is not valid JSON: {e}"
                    )
    
    return errors


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Workpack Protocol v2/v3/v4/v5 Linter",
        epilog="Validates workpacks for protocol compliance."
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Treat warnings as errors (exit code 2 if warnings found)"
    )
    args = parser.parse_args()
    
    print("Workpack Protocol Linter (v2/v3/v4/v5)")
    print("=" * 40)
    
    try:
        workpacks_dir = get_workpacks_dir()
    except FileNotFoundError as e:
        print(f"ERROR: {e}")
        sys.exit(1)
    
    print(f"Scanning: {workpacks_dir}")
    if args.strict:
        print("Mode: --strict (warnings treated as errors)")
    
    schema_path = workpacks_dir / "WORKPACK_OUTPUT_SCHEMA.json"
    
    all_errors = []
    all_warnings = []
    v2_count = 0
    v3_count = 0
    v4_count = 0
    v5_count = 0
    skipped_count = 0
    
    # Determine scan directories.
    # v5 uses instances/ subfolder; also scan top-level for legacy workpacks.
    scan_dirs: list[Path] = []
    instances_dir = workpacks_dir / "instances"
    if instances_dir.exists():
        scan_dirs.append(instances_dir)
    scan_dirs.append(workpacks_dir)  # legacy fallback

    seen: set[str] = set()

    for scan_root in scan_dirs:
        for item in sorted(scan_root.iterdir()):
            if not item.is_dir():
                continue
            if item.name.startswith("_"):
                continue  # Skip _template and other underscore-prefixed folders
            if item.name in ("tools", "instances"):
                continue  # Skip tools and instances when scanning top-level
            if item.name in seen:
                continue  # avoid double-counting if somehow present in both
            seen.add(item.name)
        
            version = get_workpack_version(item)
        
            if version == 5:
                v5_count += 1
                print(f"  ✓ Validating v5 workpack: {item.name}")
                errors = validate_workpack(item, schema_path)
                all_errors.extend(errors)
                v_errors, v_warnings = validate_v3_prompts(item, version=5)
                all_errors.extend(v_errors)
                all_warnings.extend(v_warnings)
                v4_check_errors, v4_check_warnings = validate_v4_checks(item)
                all_errors.extend(v4_check_errors)
                all_warnings.extend(v4_check_warnings)
                v5_check_errors, v5_check_warnings = validate_v5_checks(item)
                all_errors.extend(v5_check_errors)
                all_warnings.extend(v5_check_warnings)
            elif version == 4:
                v4_count += 1
                print(f"  ✓ Validating v4 workpack: {item.name}")
                errors = validate_workpack(item, schema_path)
                all_errors.extend(errors)
                v4_errors, v4_warnings = validate_v3_prompts(item, version=4)
                all_errors.extend(v4_errors)
                all_warnings.extend(v4_warnings)
                v4_check_errors, v4_check_warnings = validate_v4_checks(item)
                all_errors.extend(v4_check_errors)
                all_warnings.extend(v4_check_warnings)
            elif version == 3:
                v3_count += 1
                print(f"  ✓ Validating v3 workpack: {item.name}")
                errors = validate_workpack(item, schema_path)
                all_errors.extend(errors)
                v3_errors, v3_warnings = validate_v3_prompts(item, version=3)
                all_errors.extend(v3_errors)
                all_warnings.extend(v3_warnings)
            elif version == 2:
                v2_count += 1
                print(f"  ✓ Validating v2 workpack: {item.name}")
                errors = validate_workpack(item, schema_path)
                all_errors.extend(errors)
            else:
                skipped_count += 1
                print(f"  - Skipping (not v2/v3/v4/v5): {item.name}")
    
    print()
    print(f"Summary: {v5_count} v5 + {v4_count} v4 + {v3_count} v3 + {v2_count} v2 workpacks validated, {skipped_count} skipped")
    
    # Print warnings
    if all_warnings:
        print()
        print("WARNINGS:")
        print("-" * 40)
        for warning in all_warnings:
            print(f"  ⚠ {warning}")
        print()
        print(f"Total warnings: {len(all_warnings)}")
    
    # Print errors
    if all_errors:
        print()
        print("ERRORS FOUND:")
        print("-" * 40)
        for error in all_errors:
            print(f"  ✗ {error}")
        print()
        print(f"Total errors: {len(all_errors)}")
        sys.exit(1)
    elif all_warnings and args.strict:
        print()
        print("✗ Warnings found and --strict mode enabled")
        sys.exit(2)
    else:
        print()
        print("✓ All workpacks pass validation")
        sys.exit(0)


if __name__ == "__main__":
    main()
