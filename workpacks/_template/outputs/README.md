# Outputs Directory

This folder contains structured handoff JSON files produced by agents after completing their prompts.

## Naming Convention

Each output file is named exactly like its corresponding prompt:
- `prompts/A1_library.md` → `outputs/A1_library.json`
- `prompts/B1_g2p_edge_case.md` → `outputs/B1_g2p_edge_case.json`

## Schema

All output JSONs must conform to `workpacks/WORKPACK_OUTPUT_SCHEMA.json`.

## Rules

1. **Create on completion**: Output JSON is created when a prompt is marked complete in `99_status.md`
2. **Required fields**: See schema for required fields
3. **No secrets**: Never include API keys, tokens, or credentials
4. **Traceability**: Include commit SHAs and/or PR URLs

## Status

- Files in this folder indicate completed work
- Missing files for completed prompts indicate a protocol violation
