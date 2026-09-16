---
type: validation guide
title: Validation and error boundaries
description: Runtime validation layers that protect ADEPT JSON/data consistency and expose actionable exception categories.
tags: [validation, errors, linter]
---

# Validation and error boundaries

There are two distinct validation layers. `SimpleValidator` in `adept/utils/validation.py` checks a DataFrame against an explicitly supplied required-column list. `SystemLinter` in `adept/utils/linter.py` performs semantic checks against a parsed `SystemDefinition` and returns `LintIssue` objects rather than raising.

`GenericDataLoader.validate_data_integrity()` runs the linter after file loading and parameter injection. It prints success or non-error issues and emits warnings for `ERROR` issues; it does not abort loading. `ArchSpaceCore.validate()` is stricter at the façade boundary: it rejects `None`, non-DataFrames, and empty frames, then wraps validator failures in `ValidationError`.

The linter verifies quality-objective columns, component parameters (exact and component-prefixed candidates), configuration identification columns and configured IDs, supported tradeoff schemes, tradeoff objective references, and configuration component/decision/policy references. Supported schemes are `discretization`, `pareto`, `threshold`, `pareto_epsilon`, and `pareto_knee`. Legacy `component_policies` mappings are also checked.

The exception hierarchy in `adept/utils/exceptions.py` has `ADEPTError` at its root, with `DataLoadingError`, `ValidationError`, `DiscoveryError`, `ConfigurationError`, `AnalysisError`, `TradeoffDefinitionError`, and `VisualizationError`; `MissingDependencyError` records the missing package. `ArchSpaceCore.load_data()` converts loader failures to `DataLoadingError`, while domain methods may raise `ValueError`, `RuntimeError`, or domain exceptions for missing lifecycle state.

Focused evidence: `tests/test_linter.py` asserts valid definitions, missing objective/parameter/config columns, unsupported schemes, and invalid references; `tests/test_loader.py` proves a minimal definition loads and splits; `tests/test_archspace_core.py` covers façade-level validation/delegation. When debugging, validate the JSON with `SystemDefinition.model_validate()` first, then inspect linter issue strings and the final raw frame columns.
