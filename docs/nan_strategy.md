# Semantic NaN Handling Strategy for ADEPT

This document describes how ADEPT handles `NaN` (Not-a-Number) values, and the closely related numeric encoding of categorical parameters. Instead of treating `NaN` as missing data to be removed, ADEPT treats it as a **first-class semantic state** representing specific architectural conditions.

## 1. Semantic Definitions

In architectural simulation data, `NaN` typically has two distinct meanings:

*   **Inputs (Parameters/Levers):** **"Option Not Selected"** or "Not Applicable". A valid design choice that the algorithms must learn from (e.g. the settings of a pattern that is OFF).
*   **Outputs (Quality Objectives):** **"System Failure"** (e.g. a timeout, crash, or invalid configuration). A critical signal for robustness and tradeoff analysis.

Note that ADEPT itself can create input NaNs: when a configuration's policy does not bind a parameter, `GenericDataLoader` leaves that parameter empty for the configuration's runs.

## 2. Core Principles

*   **Optionality & Backward Compatibility:** NaN-related features are non-mandatory. Datasets without NaNs and without categorical parameters are processed exactly as before (verified on Gateway Offloading: identical boxes and robustness results).
*   **Transparency:** Users are alerted to NaNs and to undeclared NaN semantics when data is loaded.
*   **One encoding per analysis:** the numeric encoding of parameters is fitted once, on the training slice, and reused for every slice compared against its results (test slice, box evaluation, dataset bounds, plots).

## 3. Metadata Specification (JSON)

### Parameters (Inputs)
*   `optional: bool` (default: `false`): If `true`, `NaN` is a valid "Not Selected" state.

### Quality Objectives (Outputs)
*   `nan_policy: str` (`"worst_case"` default, `"drop"`, `"fixed_value"`): How failure states are handled (§5C).
*   `nan_value: float`: The value used when `nan_policy` is `"fixed_value"`.

## 4. Pre-analysis Data Quality Checks

*   **NaN Proportion Report** (`GenericDataLoader.report_nan_proportions`, `PatternAnalysis.load`): percentage of NaN cells for inputs (experiments) and outputs (outcomes), overall and per column.
*   **Threshold Warnings** (`SystemLinter._validate_nan_semantics`, run on every load):
    *   A **non-optional parameter that is NaN in ≥ 50% of rows** (`NAN_WARNING_THRESHOLD`) is flagged: its NaNs will be filled with `0.0`, which is rarely what NaN means. Declare it `optional` if NaN means "not selected".
    *   A **quality objective with NaNs and no explicit `nan_policy`** is flagged: those runs are silently treated as failures (`worst_case`). Declare the policy to make it explicit.
*   At load time, NaNs in non-optional **numeric** parameters are filled with `0.0` (with a printed note); optional parameters are left as NaN for the encoding in §5A.

## 5. The Semantic Wrapper Pattern

Instead of modifying the dataset in place, ADEPT encodes data **just in time** for each algorithm.

### A. Parameter Encoding (`FeatureEncoder`, `adept/utils/feature_encoding.py`)

RandomForest, PRIM and CART need numeric, NaN-free inputs. `FeatureEncoder` is fitted on the training slice and applied everywhere else:

| Parameter | Encoding |
|:---|:---|
| **Categorical** (any non-numeric column) | Ordinal codes `1..k` following the sorted category labels; `NaN` and categories unseen at fit time become `0` ("not selected"). A single-valued optional parameter is therefore a `0/1` presence flag. |
| **Numeric, optional, with NaNs** | `NaN` becomes a **sentinel** just below the observed minimum (`min - 0.1 * range`; `0.0` when the column is entirely NaN). |
| **Numeric, required** | Unchanged (remaining NaNs are filled with `0.0` by the callers). |

Categorical parameters used to be supported only when optional (collapsed to a presence flag); required ones such as a `Model` choice were silently dropped from feature scoring and crashed discovery. They are now first-class inputs.

`SemanticNaNHandler.apply_sentinel_transformation` remains available and uses the same encoder.

### B. Feature Importance
`FeatureImportanceAnalyzer.compute_importance` and `preprocess_features` encode with §5A before scoring/standardizing, so the **importance of a selection decision** (and of categorical choices) is measured. `compute_feature_scores()` still defaults to `include_constraints=False`; pass `include_constraints=True` when optional pattern parameters are typed `"constraint"`.

### C. Outcome NaN Policies (`DataProcessor.define_tradeoffs`)

| `nan_policy` | Discretization | Other methods (threshold, Pareto, clustering) |
|:---|:---|:---|
| `worst_case` | Bins are computed from **observed values only**; failed runs are labelled **`FAILURE`** and the scheme gets a `FAILURE` bin, so failures form their own tradeoff regions (e.g. `FAILURE-S`). | Failed runs get a value 10% of the range beyond the worst observed value, so they land in the unsatisfactory / sub-optimal side. |
| `drop` | Runs with a NaN outcome get no label and belong to **no tradeoff region**. | Same (a temporary worst-case value lets the method run; the label is then cleared). |
| `fixed_value` | NaN is replaced by `nan_value` before segmentation. | Same. |

This prevents survival bias: "success" tradeoffs no longer include runs that actually failed.

### D. Discovered Boxes
Box limits live in the encoded space. After discovery (with or without `standardize`), `PatternAnalysis` annotates each box using the fitted encoder:
*   `box.includes_na[param] = True` when the box covers the parameter's "not selected" value (sentinel or code `0`).
*   `box.categorical_levels[param]` lists the categories in code order.
*   `box.readable_limits()` returns limits in the parameters' own terms: `{'in': [categories]}` for categorical parameters (with `'(not selected)'` listed first when covered), `{'min', 'max'}` otherwise, plus `'includes_na': True` where relevant.
*   `box.describe_limits()` returns one string per parameter for labels and summaries: `'{squeezenet1_1}'`, `'{(not selected), zlib}'`, `'(not selected) or <= 0.60'`, `'[1.00, 3.00]'`.

## 6. Visualization Strategy

*   **`show_box_diagnostics` (restriction bars and pair plots):** when `box.includes_na[param]` is true, the "not selected" end of the bar is hatched (`///`), and so are the pair-plot regions. For categorical parameters the hatched part spans code `0` up to half-way to code `1`.
*   **Original values instead of codes (`show_original_values=True`, the default)** in `show_box_diagnostics` and `show_box_impact_objective_space`:
    *   restriction bars of categorical and optional parameters are labelled with `box.describe_limits()` (e.g. `{CNN 16k}`, `{(not selected)}`) instead of encoded min/max values;
    *   pair-plot and histogram axes of categorical parameters get one tick per category, plus `N/A` at code `0` when optional; numeric optional parameters keep their numeric ticks plus an `N/A` tick at the sentinel;
    *   the what-if constraint summary (`show_box_summary=True`) lists the same decoded conditions.

    Points and box rectangles stay in the encoded space, so the geometry is unchanged; only labels differ. Pass `show_original_values=False` to see the codes the boxes were learned on.
*   **`show_quality_objective_space`:** not yet specialized; runs with a NaN objective are simply not drawn (the imputation only feeds tradeoff definition, `outcomes_df` keeps the NaN).
*   **`show_importance_heatmap`:** unchanged; encoded importance scores are directly comparable.

## 7. Status

| Component | Status | Implementation |
| :--- | :--- | :--- |
| **Data Models** | ✅ | `Parameter.optional`, `QualityObjective.nan_policy`/`nan_value`, `Box.includes_na`/`categorical_levels`/`readable_limits()` (`adept/core/models.py`). |
| **Data Loading** | ✅ | NaN proportion audit (`loader.py`, `session.py`). |
| **Lint warnings** | ✅ | `SystemLinter._validate_nan_semantics` (§4). |
| **Parameter encoding** | ✅ | `FeatureEncoder` (§5A), fitted on train and shared by scoring, discovery, box evaluation and plots. |
| **Outcome policies** | ✅ | `worst_case` with `FAILURE` bin, `drop`, `fixed_value` (§5C). |
| **Boxes** | ✅ | `includes_na` and category decoding for standardized and non-standardized discovery (§5D). |
| **Visuals** | ✅ / ⚠️ | Box diagnostics hatching and original-value labels (`show_original_values`) work; a dedicated failure marker in the objective-space scatter is not implemented. |
| **Testing** | ✅ | `tests/test_nan_handler.py`, `test_feature_encoding.py`, `test_outcome_nan_policies.py`, `test_box_encoding.py`, `test_feature_importance.py`. |

## 8. Known Limitations

*   **Ordinal codes impose an order on categories.** PRIM/CART boxes on a categorical parameter are ranges of codes, i.e. sets of *consecutive* categories in sorted order. With 2-3 categories this is harmless; for many unordered categories a one-hot encoding would be more faithful.
*   **Stability-radius analysis** (`RobustnessAnalyzer.compute_stability_radius`, MDS plots) still uses numeric parameters only.
*   **Required parameters with a few NaNs** (below the 50% warning threshold) are filled silently: `0.0` for numeric ones, code `0` for categorical ones.

## 9. History

*   **Initial implementation:** metadata fields, NaN audit, `SemanticNaNHandler` with numeric sentinels, `includes_na` in discovery, FL test specs (`federatedlearning/FLsystem*.json`).
*   **Categorical presence flags:** optional categorical parameters collapsed to `0/1` flags; feature scoring needed `include_constraints=True` for FL's constraint-typed pattern parameters.
*   **Train/test encoding consistency (2026-09):** the test slice and box evaluation were encoded differently from the training slice (crashes on categorical flags, NaN in test data); fixed by fitting once on train and reusing it.
*   **Strengthening (2026-09):** `FeatureEncoder` with categorical codes (required categorical parameters such as `Model` now usable), `includes_na` set for standardized discovery and actually read by the plots (it was stored on the box but read from inside the limits, so hatching never rendered), `FAILURE` bin and `drop` policy, NaN-semantics lint warnings.
