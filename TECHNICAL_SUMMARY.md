# Technical Summary: SEAL & Prompt Eval Tool

## Current Environment
- **Projects**: `seal` (FastAPI) and `prompt-eval-tool` (Streamlit).
- **Shared dependency**: `tilli-prompts` (schemas, prompts, upcoming logging/config modules).
- **Runtime**: Python 3.12 virtualenvs, Gemini API (`GOOGLE_API_KEY`).

## What Works Today
- SEAL API responds reliably (`uvicorn app.main:app --reload`).
- Prompt Eval Tool launches (`streamlit run app.py`) and supports manual SEAL output evaluation.
- `tilli-prompts` available for editable or Git-based installs.

## Setup Gaps & Fixes
- No unified `SETUP.md` or dependency pre-flight check.  
  *Action*: add startup validation and troubleshooting guide.
- Prompt Eval Tool still depends on manual JSON copy; lacks API pull.  
  *Action*: implement “Fetch from SEAL API” connector (stretch goal).
- Missing documentation on shared package usage in both repos.  
  *Action*: reference integration guide and consolidate instructions.

## Code Structure Improvements
- **Import Consolidation**: SEAL still references local prompts/schemas; needs migration to `tilli_prompts` with safe fallback helper.
- **Schema Duplication**: keep authoritative definitions in `tilli-prompts` and delete local copies post-migration.
- **Logging/CSV**: create shared `tilli_prompts.logging.CSVLogger` and adopt in both repos.
- **Model Config**: introduce shared `ModelConfig`/`EvaluationConfig` for consistent LLM settings.

## Developer Experience Enhancements
- Add dependency checking (`check_dependencies()`) to surface missing packages early.
- Expand docs: `SETUP.md`, troubleshooting section, links to `TILLI_PLATFORM_INTEGRATION.md`.
- Improve Streamlit usability: clarify instructions, prefill sample payloads, add error messaging around API calls.

## Consolidation Opportunities
- **Schemas**: house all Pydantic models in `tilli_prompts.schemas`; ensure parity via tests.
- **Logging**: centralize CSV logging utilities in shared package; optional SEAL export endpoint.
- **Model Configuration**: share tuning defaults across API and evaluator; document presets.

## Optional Stretch Items
- Streamlit “Fetch from SEAL API” button; handle auth and status feedback.
- Unified evaluation schema bridging SEAL output with evaluator input.
- `/evaluate` endpoint in SEAL combining generation + evaluation for end-to-end automation.

## Next Steps & Ownership
1. Ship shared import migration PR (SEAL + Prompt Eval Tool).  
2. Publish shared logging/config modules in `tilli-prompts`.  
3. Update setup docs and dependency checks.  
4. Schedule stretch tasks as bandwidth allows.

## Status Tracking
- Shared package integration plan: see `TECHNICAL_CONSOLIDATION_PROPOSAL.md`.
- Improvement ideas documented above satisfy the “short technical summary” deliverable.
- Diagram and roadmap for shared prompts integration already included in the proposal doc.

