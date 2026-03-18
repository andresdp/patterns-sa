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
1.  **Transformation:**
    *   **CART:** Maps `NaN` to a categorical string `"N/A"`.
    *   **PRIM:** Maps `NaN` to a **Sentinel Value** (e.g., `min - (0.1 * range)`).
2.  **Execution:** Runs the original algorithm on the transformed data.
3.  **Inverse Mapping:** After a box is discovered, the wrapper checks if the boundaries include the Sentinel Value or "N/A" category.
    *   If yes, it updates the `Box` object with an `includes_na: bool` flag for that specific parameter.

### B. Feature Importance Wrapper
*   **Strategy:** Uses Sentinel Value imputation.
*   **Benefit:** Allows Random Forests to calculate the **importance of the selection decision**. If disabling a feature (setting it to `NaN`) causes a major change in performance, the importance score will correctly reflect this.

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

| Component | Impact | Implementation Detail |
| :--- | :--- | :--- |
| **Data Models** | Medium | Add `optional` and `nan_policy` fields to `Parameter` and `QualityObjective`. |
| **Data Loading** | Low | Implement `NaN` proportion check in `DataLoader`. |
| **Discovery** | High | Implement `includes_na` logic in `Box` and wrappers in `ScenarioDiscoveryManager`. |
| **Robustness** | Low | No change needed if outputs are imputed as failures before masking. |
| **Visuals** | High | Update `VisualizationManager` to handle `includes_na` flags. |

## 8. Implementation Plan

1.  **Phase 1:** Update `adept/core/models.py` to include the new metadata fields.
2.  **Phase 2:** Update `adept/core/loader.py` and `adept/core/session.py` to include the `NaN` proportion audit during `load()`.
3.  **Phase 3:** Create `adept/utils/nan_handler.py` with the JIT transformation logic.
4.  **Phase 4:** Wrap `ScenarioDiscoveryManager` and `FeatureImportanceAnalyzer` to use the handler.
5.  **Phase 5:** Update the `Box` model to support `includes_na` in its limits definition.
6.  **Phase 6:** Refactor `VisualizationManager` to render the "N/A" states in box and scatter plots.
