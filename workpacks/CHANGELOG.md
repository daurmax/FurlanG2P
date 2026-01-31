# Workpack Protocol Changelog

All notable changes to the Workpack Protocol are documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html) for protocol versions.

---

## [3.0] - 2026-02-01

### Added

- **Initial Workpack Protocol for FurlanG2P**: Adapted from Beorcje-Meta workpack system.
- **Agent-Centric Prompt Philosophy**: Prompts describe *what* to implement using semantic references, not *how* by embedding code.
- **PROMPT_STYLE_GUIDE.md**: Comprehensive guide for writing agent-centric prompts.
- **Integration Agent as Merge Reviewer**: A5 executes test suites (pytest, mypy, ruff) and validates work before merge.
- **Python-Specific Templates**: Adapted for Python library development workflow.

### Structure

- **A1_library.md**: Core library implementation (`src/furlan_g2p/`)
- **A2_cli.md**: CLI implementation (`src/furlan_g2p/cli/`)
- **A3_tests.md**: Test implementation (`tests/`)
- **A4_docs.md**: Documentation (`docs/`, `README.md`, `README-pypi.md`)
- **A5_integration.md**: Integration, validation, and merge

### Notes

- Protocol v3 is the initial version for this project
- Based on Beorcje-Meta workpack protocol v3
- Adapted for Python/pip development workflow
