# Technical Consolidation Proposal

## Summary
- Adopt the shared `tilli-prompts` package (available via Git and editable install) as the common dependency for SEAL and Prompt-Eval-Tool.
- Provide a clear setup workflow so both repos automatically resolve the package and surface helpful diagnostics when it is missing.
- Consolidate overlapping schema, logging, and model-configuration logic into the package while maintaining backward-compatible fallbacks.

## Current State
- `tilli-prompts` is already published in the org’s GitHub account and can be installed locally with `pip install -e ../tilli-prompts` or directly from Git (`pip install git+https://github.com/keithesanks-prog/tilli-prompts.git`).
- Prompt-Eval-Tool has partial adoption; SEAL still imports from `app.prompts` and `app.schemas`.
- Documentation gaps remain (`SETUP.md`, troubleshooting steps, dependency checks).

```mermaid
flowchart TB

    subgraph Shared Package
        TP[tilli-prompts<br/>schemas + prompts + logging + config]
    end

    subgraph SEAL_API
        direction TB
        GW[llm/gateway.py]
        CURR[llm/curriculum_gateway.py]
        STREAM[/POST /stream (FastAPI endpoint)/]
    end

    subgraph PromptEval
        direction TB
        UI[Streamlit app.py]
        EVAL[judge.py + logging]
    end

    TP --> GW
    TP --> CURR
    TP --> UI
    TP --> EVAL

    %% Streaming data flow
    UI -->|Send JSON payload (scores, metadata)| STREAM
    STREAM -->|Streamed results (tokens)| UI
    STREAM -->|Structured plan (JSON)| EVAL

    %% Future API integration
    EVAL -->|Optional: /evaluate endpoint| STREAM

    %% Visual emphasis on shared base
    GW -.-> TP
    CURR -.-> TP
    EVAL -.-> TP
```

## Proposed Work Breakdown

### 1. Shared Package Integration (Quick Win)
- **Goal**: Both repos import prompts and schemas from `tilli_prompts`.
- **Steps**:
  1. Confirm `tilli-prompts` remains installable via Git (`pip install git+https://github.com/keithesanks-prog/tilli-prompts.git`) and editable checkout (`pip install -e ../tilli-prompts`).
  2. Update SEAL imports (`app/main.py`, `app/llm/gateway.py`, `app/llm/curriculum_gateway.py`) to use `tilli_prompts` with a safe fallback helper (`safe_import_tilli_prompts()` already outlined in `TECHNICAL_IMPROVEMENTS_COMPLETE.md`). _Status: not yet shipped—flagged for upcoming PR._
  3. Add a startup dependency check that raises/logs an actionable message if the package is missing. _Status: still pending._
- **Deliverable**: PR touching SEAL and Prompt-Eval-Tool with updated imports and setup notes. _Future work._

### 2. Schema Consolidation
- **Goal**: Eliminate duplicate schema definitions.
- **Steps**:
  1. Move remaining SEAL-specific schema updates into `tilli-prompts/tilli_prompts/schemas/`. _Future work: not yet merged._
  2. Confirm parity by running tests in both repos and validating API responses. _Future work._
  3. Remove obsolete local schema folders after successful validation. _Future work pending consolidation._
- **Deliverable**: PR in SEAL referencing `TECHNICAL_IMPROVEMENTS_STATUS.md` section “Schema Definitions”.

### 3. Logging / CSV Utilities (Shared Module)
- **Goal**: Provide a single CSV logging utility usable by both systems.
- **Steps**:
  1. Add `tilli_prompts/logging/csv_logger.py` (per outline in `TECHNICAL_IMPROVEMENTS_STATUS.md`). _Planned._
  2. Export `CSVLogger` via `tilli_prompts.logging`. _Planned._
  3. Update Prompt-Eval-Tool to import the shared logger; optionally add SEAL CSV export endpoint. _Planned._
- **Deliverable**: PR in `tilli-prompts` (new module) + follow-up PRs in downstream repos.

### 4. Model Configuration Sharing
- **Goal**: Standardize LLM generation settings.
- **Steps**:
  1. Implement `tilli_prompts/config/models.py` with `ModelConfig` and `EvaluationConfig` classes (`TECHNICAL_IMPROVEMENTS_STATUS.md`, “Model Configuration”). _Planning stage._
  2. Update SEAL gateway and Prompt-Eval-Tool judge to consume the shared configuration. _Future work._
  3. Document recommended presets (“conservative”, “enhanced”, “creative”). _Future work._
- **Deliverable**: PR in `tilli-prompts` plus adoption PRs.

### 5. Setup & Troubleshooting Docs
- **Goal**: Reduce onboarding friction.
- **Steps**:
  1. Create/finish `SETUP.md` in SEAL (installation, dependency check, troubleshooting). _Still to-do._
  2. Update Prompt-Eval-Tool docs to mirror the dependency expectations. _Scheduled._
  3. Link the integration guide (`TILLI_PLATFORM_INTEGRATION.md`) from both repos. _Scheduled._
- **Deliverable**: Documentation-only PRs.

### 6. Alternatives Considered
- **Git submodule** (`tilli-prompts/` as a submodule in both repos): viable if teams prefer a tightly coupled checkout; rejected for now because editable installs already meet the need with less tooling overhead.
- **Symbolic link / relative import** for local dev: simple for single-machine setups but breaks in CI and production packaging; we’ll keep it as a fallback tip in SETUP docs for quick experiments.
- Decision: stick with the shared package approach while keeping the other options documented as fallback paths for contributors (to be captured in SETUP.md).

### 7. Optional Stretch Work (Future)
- **Prompt Eval Tool ↔ SEAL API connector**: add “Fetch from SEAL API” button that hits `/score`; may expand to `/evaluate` once consolidated schema is complete. _Not started._
- **Unified evaluation schema**: map SEAL output to evaluation inputs directly via shared `tilli_prompts.schemas`. _Dependent on schema consolidation._
- **/evaluate endpoint** in SEAL: wraps generation + evaluation for end-to-end workflows. _Future roadmap item._

## Testing & Validation
- Run existing unit/integration tests in both repos after switching to shared imports.
- Hit SEAL’s `/health` and `/score` endpoints with and without `tilli-prompts` installed to verify fallback logic.
- Smoke-test Prompt-Eval-Tool flows to ensure logging/config refactors behave identically.

## Next Steps
- Decide whether to treat `tilli-prompts` as a Git submodule or a Git-based `pip` dependency for deployment; both workflows are compatible with the install instructions above.
- Schedule the work in the order listed (shared package → consolidation → logging → config → docs).
- Track progress in the TECHNICAL_IMPROVEMENTS_* docs to keep status current.

