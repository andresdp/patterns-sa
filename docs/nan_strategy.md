# Semantic NaN Handling Strategy for ADEPT

This document outlines the strategy for handling `NaN` (Not-a-Number) values within the ADEPT framework. Instead of treating `NaN` as missing data to be removed, ADEPT treats it as a **First-Class Semantic State** representing specific architectural conditions.

## 1. Semantic Definitions

In architectural simulation data, `NaN` typically has two distinct meanings:

*   **Inputs (Parameters/Levers):** Represents **"Option Not Selected"** or "Not Applicable." It is a valid design choice that the algorithm must learn from.
*   **Outputs (Quality Objectives):** Represents **"System Failure"** (e.g., a Timeout, Crash, or Invalid Configuration). It is a critical signal for robustness and tradeoff analysis.

## 2. Core Principles

*   **Optionality & Backward Compatibility:** NaN-related features are **non-mandatory**. Existing datasets without NaNs will continue to work without modification. The framework defaults to standard numeric behavior (e.g., zero-filling or dropping) unless explicit NaN metadata is provided in the `system.json`.
*   **Transparency:** Users should be alerted to the presence of NaNs during the initial data loading phase to avoid unexpected analysis results.

## 3. Metadata Specification (JSON)

To distinguish between parameters that are required and those that are optional, the system specification is extended:

### Parameters (Inputs)
*   `optional: bool` (default: `false`): If `true`, the system treats `NaN` as a valid "Not Selected" state.

### Quality Objectives (Outputs)
*   `nan_policy: str` (options: `"worst_case"`, `"drop"`, `"fixed_value"`): Defines how to impute failure states.
*   `nan_value: float` (optional): The specific value to use if `nan_policy` is `"fixed_value"`.

## 4. Pre-analysis Data Quality Checks

During the data loading phase (within `DataLoader` or `PatternAnalysis.load`), the framework will perform a high-level audit of data completeness:

*   **NaN Proportion Report:** Automatically calculate and display the percentage of `NaN` values for:
    *   **Inputs (Experiments):** Total and per-column.
    *   **Outputs (Outcomes):** Total and per-column.
    *   **Overall Dataset:** Total percentage.
*   **Threshold Warnings:** If the proportion of NaNs exceeds a configurable threshold (e.g., 50%) and no `optional` flag or `nan_policy` is defined, the framework will issue a warning recommending the definition of a semantic policy.

## 5. The Semantic Wrapper Pattern

Instead of modifying the underlying dataset in-place, ADEPT uses a **Just-in-Time (JIT) Wrapper** mechanism.

### A. Discovery Wrappers (CART & PRIM)
1.  **Transformation** (shared by both via `SemanticNaNHandler.apply_sentinel_transformation`, `adept/utils/nan_handler.py`):
    *   **Numeric optional parameters:** Mapped to a **Sentinel Value** (`min - (0.1 * range)`), just below the observed minimum.
    *   **Categorical (non-numeric) optional parameters:** Collapsed to a **binary presence flag** (`1.0` = selected, `0.0` = not selected/NaN), since RandomForest/PRIM/CART all require numeric input and cannot consume a raw category value. The original category value is discarded — only "was this selected" survives. (An earlier version of this doc described mapping categorical NaN to the string `"N/A"`; that was never implemented and is superseded by the presence-flag approach, verified against `federatedlearning/FLsystem_split.json`.)
2.  **Execution:** Runs the original algorithm on the transformed data.
3.  **Inverse Mapping:** After a box is discovered, the wrapper checks if the boundaries include the sentinel/`0.0` value.
    *   If yes, it updates the `Box` object with an `includes_na: bool` flag for that specific parameter.

### B. Feature Importance Wrapper
*   **Strategy:** Uses the same sentinel/presence-flag imputation as §5A, applied before `select_dtypes(number)` filters non-numeric columns.
*   **Benefit:** Allows Random Forests to calculate the **importance of the selection decision**. If disabling a feature (setting it to `NaN`) causes a major change in performance, the importance score will correctly reflect this.
*   **Caveat:** `PatternAnalysis.compute_feature_scores()` defaults `include_constraints=False` (`adept/core/session.py:2339`). Any optional parameter typed `"constraint"` — which is how all 13 FL pattern parameters are typed in `FLsystem_split.json` — is filtered out *before* this wrapper ever runs, regardless of `optional`. Call with `include_constraints=True` to actually exercise optional-parameter handling for such datasets; verified end-to-end on the FL dataset (18/18 parameters, including all 6 categorical ones, now receive non-zero importance scores).

### C. Tradeoff Processor Wrapper
*   **Strategy:** Automatically assigns any imputed "Worst Case" objective values to a dedicated **"FAILURE" bin**.
*   **Benefit:** Prevents survival bias. "Success" tradeoffs will no longer accidentally include points that actually timed out.

## 6. Visualization Strategy

Visualizing "Non-numeric states" on numeric axes requires specific treatments:

*   **`show_box_diagnostics` (Restriction Bars):**
    *   If `includes_na` is true, the bar is rendered with a distinct hatch pattern (e.g., `////`) starting from a dedicated "N/A" marker at the far left.
*   **`show_quality_objective_space` (Scatter Plot):**
    *   Imputed failure points are rendered on a dedicated "Failure Axis" or highlighted with an `X` marker to distinguish them from valid numeric results.
*   **`show_importance_heatmap`:**
    *   Remains unchanged, as the importance scores derived from sentinel values are mathematically consistent.

## 7. Impact Analysis

| Component | Status | Implementation Detail |
| :--- | :--- | :--- |
| **Data Models** | ✅ Complete | Added `optional` and `nan_policy` fields to `Parameter` and `QualityObjective` in `adept/core/models.py`. |
| **Data Loading** | ✅ Complete | Implemented `NaN` proportion check in `DataLoader` and `PatternAnalysis.load()`. |
| **Discovery** | ✅ Complete | Implemented `includes_na` logic in `Box` model and wrappers in `ScenarioDiscoveryManager`. |
| **Feature Importance** | ✅ Complete | Implemented sentinel value imputation in `FeatureImportanceAnalyzer`. |
| **Robustness** | ✅ Complete | No change needed; works with imputed failure states. |
| **Visuals** | ✅ Complete | `show_box_diagnostics()` in `VisualizationManager` derives `includes_na` from box limits and renders N/A hatching in both the bar chart and pairwise scatter/histogram. |
| **Testing** | ❌ Not Started | No automated (pytest) coverage exists for `SemanticNaNHandler` or the federated-learning data prep; only manual diagnostic scripts and a notebook. |

## 8. Implementation Plan

### Completed Phases ✅

1.  **Phase 1:** ✅ Updated `adept/core/models.py` to include the new metadata fields (`optional`, `nan_policy`, `nan_value`).
2.  **Phase 2:** ✅ Updated `adept/core/loader.py` and `adept/core/session.py` to include the `NaN` proportion audit during `load()`.
3.  **Phase 3:** ✅ Created `adept/utils/nan_handler.py` with the JIT transformation logic (`SemanticNaNHandler` class).
4.  **Phase 4:** ✅ Wrapped `ScenarioDiscoveryManager` and `FeatureImportanceAnalyzer` to use the handler.
5.  **Phase 5:** ✅ Updated the `Box` model to support `includes_na` in its limits definition.
6.  **Phase 6:** ✅ Completed visualization updates in `VisualizationManager` to render "N/A" states in box and scatter plots.
7.  **Phase 7:** ✅ Fixed the `includes_na` bug in `show_box_diagnostics()` (see §9, resolved).
8.  **Phase 8:** ✅ Created test system definition file (`federatedlearning/FLsystem.json`, plus `FLsystem_split.json`) with `optional`/`nan_policy` metadata for Federated Learning patterns.
9.  **Phase 9:** ✅ Created test notebook (`federatedlearning/test_nan_feature.ipynb`) for end-to-end NaN functionality.

### Remaining Phases ❌

11. **Phase 11:** Add automated pytest coverage — a `tests/test_nan_handler.py` for `SemanticNaNHandler` (policy × direction cases) is referenced by `openwiki/utilities/nan-and-support.md` as existing evidence but is not present in `tests/`.

### Phase 10: End-to-end validation — done, with findings ⚠️

Ran `federatedlearning/test_json_validation.py`, `test_split_json.py`, `test_manual_simple.py`, and `test_nan_feature.ipynb` (via `jupyter nbconvert --execute`) against the real FL data (`perfmodels` conda env). All four complete without errors — but that green run is misleading about what actually got exercised:

* **`FLsystem_split.json` already declares all 13 FL pattern parameters as `optional: true`**, under `system.components.fl_system.parameters` (not under `dataspace` — an earlier version of this note incorrectly claimed no `parameters` block existed). `dataspace.discovery_options.auto_detect_parameters`/`auto_detect_objectives` are red herrings: `discovery_options` is a free-form `Dict[str, Any]` (`adept/core/models.py:401`) and the loader only ever reads `csv_delimiter` from it (`adept/core/loader.py:293-295`) — those two auto-detect flags are not consumed anywhere.
* **The real cause is a default argument, not a missing flag.** `PatternAnalysis.compute_feature_scores()` defaults `include_constraints=False` (`adept/core/session.py:2339`), and all 13 FL pattern parameters are typed `"type": "constraint"` in the JSON. `get_parameter_columns()` filters them out by type *before* `X` is built, so `apply_sentinel_transformation` never even sees them — this exactly matches the observed log line `Original features (numeric only): ['Total Clients', 'N Rounds', 'Batch Size', 'Learning Rate', 'Epochs']` (the 5 system-level `lever` params) on every outcome, and the resulting `0.0` importance scores across the board.
* `discover_scenarios()` does *not* have this problem — it calls `get_parameter_columns()` with no override, so its default `include_constraints=True` keeps all 13 pattern parameters in play, and parameter names are correctly synced from their JSON dict keys via `ArchitecturalPattern._sync_parameter_names` (`adept/core/models.py:96-101`), so sentinel transformation is exercised there. PRIM still finds **0 boxes** for the `best_val_f1`/`level_1` tradeoff (32 rows, 25/7 split) — plausibly just a small-sample/threshold effect rather than a wiring bug, but unconfirmed either way. Because no boxes were found, the box-diagnostics cell (guarded by `if boxes:`) produced no output, so the `includes_na` hatching fix from §9 is still confirmed only by code inspection, never by an actual render.
* `test_split_json.py`'s own "Pattern Column Values" check (looking for `client_selector_pattern`/`message_compressor_pattern`/`hdh_pattern` in `experiments_df.columns`) silently prints nothing — those three *derived join-key* columns (from `preprocess_csv.py`) are present in the CSV but not declared as parameters and so are absent from `experiments_df`; the script doesn't assert on this, so it passes without anyone noticing.
* The parts of the framework that don't depend on `optional`/type filtering — the NaN proportion audit and `QualityObjective.nan_policy` (`worst_case`/`nan_value`) on the 5 outcomes — are confirmed working end-to-end: the audit reports 45.17% experiment-cell NaN correctly, and outcomes load with 0% NaN.

**Conclusion:** the FL system JSON is correctly configured; the gap was that `compute_feature_scores()`'s `include_constraints=False` default silently excluded every "pattern not selected" parameter from feature importance, and non-numeric optional parameters had no transformation path at all (only numeric sentinel imputation existed). Both are now addressed:

* `SemanticNaNHandler.apply_sentinel_transformation` (`adept/utils/nan_handler.py`) now branches on dtype: numeric optional parameters keep the sentinel-below-minimum treatment; categorical ones are collapsed to a binary presence flag (`1.0`/`0.0`). See §5A/§5B.
* Callers still need `include_constraints=True` for datasets (like this FL one) where the optional parameters are typed `"constraint"` — `compute_feature_scores()`'s default remains `False` (a broader default-vs-typing question, not changed here since it affects call sites beyond this dataset).

Verified on the real FL data: `session.compute_feature_scores(include_constraints=True)` now returns non-zero importance scores for all 18 parameters, including all 6 previously-dropped categorical ones (e.g. `Message Compressor Alg` scores 0.35 for `best_val_f1`). `discover_scenarios()` was not re-verified for box-count changes after this fix — still an open follow-up, along with actually rendering `show_box_diagnostics()` against a real `includes_na` box.

## 9. Known Issues

### Visualization Bug in `show_box_diagnostics()` — Resolved

**Issue (historical):** The `show_box_diagnostics()` function in `adept/analysis/visualization.py` referenced an undefined variable `includes_na`, raising `NameError` when visualizing boxes with N/A parameters.

**Resolution:** `includes_na` is now derived from `box.limits[...]['includes_na']` at the top of the function (`adept/analysis/visualization.py:694-698`) and consumed by both the bar-chart hatching (`:721-732`) and the pairwise scatter/histogram hatching (`:798`, `:806`). No open visualization bug is known at this time.
