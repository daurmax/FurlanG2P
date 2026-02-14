# outputs/

This folder contains the **structured handoffs** produced by agents for Workpack Protocol v2.

## Rule
For every file in `prompts/<PROMPT>.md` there must be (once completed) a corresponding JSON file:
- `outputs/<PROMPT>.json`

Examples:
- `prompts/A1_library.md` → `outputs/A1_library.json`
- `prompts/B1_library_oov_handling.md` → `outputs/B1_library_oov_handling.json`

## Schema
Each JSON must conform to: `workpacks/WORKPACK_OUTPUT_SCHEMA.json`.

## Note
When creating a workpack, it is sufficient to create the folder; individual JSON files are created/updated when an agent completes its prompt.
