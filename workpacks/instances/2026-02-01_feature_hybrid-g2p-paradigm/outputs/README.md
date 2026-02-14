# Outputs

This folder contains handoff output JSON files for completed prompts.

## Protocol v3 Rules

- Each completed prompt produces `<PROMPT>.json` (same basename as the prompt)
- All JSONs must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`
- Outputs are created when a prompt is marked complete in `99_status.md`

## Expected Files

| Prompt | Output File | Status |
|--------|-------------|--------|
| A0_bootstrap | A0_bootstrap.json | Pending |
| A1_library | A1_library.json | Pending |
| A2_cli | A2_cli.json | Pending |
| A3_tests | A3_tests.json | Pending |
| A4_docs | A4_docs.json | Pending |
| A5_integration | A5_integration.json | Pending |

## Schema Reference

See `workpacks/WORKPACK_OUTPUT_SCHEMA.json` for the complete schema definition.
