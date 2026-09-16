---
type: utility guide
title: Semantic NaN handling and support utilities
description: Missing-value semantics, validators, sorting helpers, and exception contracts shared by ADEPT analysis components.
tags: [utilities, nan, support]
---

# Semantic NaN handling and support utilities

`SemanticNaNHandler` distinguishes absent architecture choices from failed outcomes. `audit_nan_proportions()` returns overall and per-column percentages. `impute_outcomes()` applies `QualityObjective.nan_policy`: `worst_case` places missing maximize outcomes below the observed range and missing minimize outcomes above it; `fixed_value` uses `nan_value`; `drop` is left for the caller. `apply_sentinel_transformation()` maps NaNs only for parameters marked `optional=True` to a value just below the observed minimum and returns the sentinel map.

The session keeps outcome NaNs until `DataProcessor.define_tradeoffs()` so objective policy is available. Feature importance and discovery use sentinels before numeric algorithms. This ordering prevents a generic zero fill from turning “not selected” into a valid design value.

`SimpleValidator` checks required columns; `SystemLinter` performs the richer definition/data checks described in [validation](../architecture/validation-and-errors.md). `sorting.py` provides tradeoff label ordering used by session presentation. `exceptions.py` defines stable categories with optional structured details on `ADEPTError`.

Extension rule: add new semantic missing-value behavior to `SemanticNaNHandler` and cover both direction (`maximize`/`minimize`) and policy cases; do not implement ad hoc imputation inside an analyzer. No dedicated `tests/test_nan_handler.py` exists yet — `SemanticNaNHandler` is currently exercised only indirectly via `tests/test_linter.py`, `tests/test_loader.py`, feature-importance tests, and the manual `federatedlearning/test_*.py` diagnostic scripts / `test_nan_feature.ipynb`, none of which are pytest-safe end-to-end checks of the handler itself.
