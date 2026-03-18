# Semantic NaN Handling Strategy for ADEPT

This document outlines the strategy for handling `NaN` (Not-a-Number) values within the ADEPT framework. Instead of treating `NaN` as missing data to be removed, ADEPT treats it as a **First-Class Semantic State** representing specific architectural conditions.

## 1. Semantic Definitions

In architectural simulation data, `NaN` typically has two distinct meanings:

*   **Inputs (Parameters/Levers):** Represents **"Option Not Selected"** or "Not Applicable." It is a valid design choice that the algorithm must learn from.
*   **Outputs (Quality Objectives):** Represents **"System Failure"** (e.g., a Timeout, Crash, or Invalid Configuration). It is a critical signal for robustness and tradeoff analysis.

## 2. Metadata Specification (JSON)

To distinguish between parameters that are required and those that are optional, the system specification is extended:

### Parameters (Inputs)
*   `optional: bool` (default: `false`): If `true`, the system treats `NaN` as a valid "Not Selected" state.

### Quality Objectives (Outputs)
*   `nan_policy: str` (options: `"worst_case"`, `"drop"`, `"fixed_value"`): Defines how to impute failure states.
*   `nan_value: float` (optional): The specific value to use if `nan_policy` is `"fixed_value"`.

## 3. The Semantic Wrapper Pattern

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

## 4. Visualization Strategy

Visualizing "Non-numeric states" on numeric axes requires specific treatments:

*   **`show_box_diagnostics` (Restriction Bars):**
    *   If `includes_na` is true, the bar is rendered with a distinct hatch pattern (e.g., `////`) starting from a dedicated "N/A" marker at the far left.
*   **`show_quality_objective_space` (Scatter Plot):**
    *   Imputed failure points are rendered on a dedicated "Failure Axis" or highlighted with an `X` marker to distinguish them from valid numeric results.
*   **`show_importance_heatmap`:**
    *   Remains unchanged, as the importance scores derived from sentinel values are mathematically consistent.

## 5. Impact Analysis

| Component | Impact | Implementation Detail |
| :--- | :--- | :--- |
| **Data Models** | Medium | Add `optional` and `nan_policy` fields to `Parameter` and `QualityObjective`. |
| **Discovery** | High | Implement `includes_na` logic in `Box` and wrappers in `ScenarioDiscoveryManager`. |
| **Robustness** | Low | No change needed if outputs are imputed as failures before masking. |
| **Visuals** | High | Update `VisualizationManager` to handle `includes_na` flags. |

## 6. Implementation Plan

1.  **Phase 1:** Update `adept/core/models.py` to include the new metadata fields.
2.  **Phase 2:** Create `adept/utils/nan_handler.py` with the JIT transformation logic.
3.  **Phase 3:** Wrap `ScenarioDiscoveryManager` and `FeatureImportanceAnalyzer` to use the handler.
4.  **Phase 4:** Update the `Box` model to support `includes_na` in its limits definition.
5.  **Phase 5:** Refactor `VisualizationManager` to render the "N/A" states in box and scatter plots.
