---
type: analysis component
title: Feature importance and sensitivity
description: FeatureImportanceAnalyzer identifies modeled parameters, handles optional NaNs, preprocesses numeric features, and ranks drivers with Random Forests.
tags: [feature-importance, sensitivity, machine-learning]
---

# Feature importance and sensitivity

`FeatureImportanceAnalyzer` is initialized with a `SystemDefinition`. `get_parameter_columns()` walks component and system parameters, filters by `ParameterType` inclusion flags, and retains columns whose canonical names are present. `preprocess_features()` applies optional-parameter sentinel transformation, selects numerics, fits `StandardScaler`, optionally removes rows containing any absolute z-score above `z_threshold`, and returns the processed frame, keep mask, and scaler metadata.

`compute_importance()` repeats semantic NaN transformation, fills remaining NaNs with zero for model compatibility, retains numeric columns, optionally runs feature-engine `SmartCorrelatedSelection` (Spearman threshold `0.8`, model-performance selection), and fits a `RandomForestRegressor` with 50 trees and the supplied random state. It returns descending importances and restores dropped correlated features as zero when selection is enabled.

Optional parameters are not ordinary missing data: [semantic support](../utilities/nan-and-support.md) maps their NaNs to a value just below the observed minimum before scaling. This keeps “not selected” discoverable as a region. Non-optional residual NaNs are filled only at the model boundary. The model expects numeric features; categorical policy labels should remain outside X.

Cross-domain invariant: all analyzers must retain the same row index while transforming parallel frames. Parameter names come from the model, configuration IDs are normalized to the same string-compatible keys used by the loader/contingency map, optional-NaN sentinels must be applied before scaling or tree fitting, and outcome masks must be built from the same discretized rows used by robustness and visualization. A new analyzer should accept prepared frames/masks rather than independently dropping or resetting rows; add an integration fixture that loads one definition, runs `define_tradeoffs`, splits once, and asserts identical indices through feature, contingency, metric, and plot inputs. Current tests cover each domain separately but do not fully prove this cross-domain invariant; unknown policy IDs, non-default indices, invalid KNN dimensions, and train/test mask drift remain coverage gaps.

Focused evidence: `tests/test_feature_importance.py` proves parameter discovery and that a synthetic influential feature ranks above a weaker one. Use deterministic `random_state` in comparisons, and validate that the parameter names in JSON and DataFrame columns agree before interpreting scores.
