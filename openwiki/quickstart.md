---
type: wiki entrypoint
title: patterns-sa code wiki quickstart
description: Navigation map for ADEPT, architectural pattern experiments, federated-learning data preparation, legacy compatibility, operations, and tests.
tags: [quickstart, navigation, repository]
---

# patterns-sa code wiki quickstart

This wiki documents **patterns-sa**, centered on ADEPT: a Pydantic-configured, pandas-based framework for architectural sensitivity analysis, tradeoff definition, scenario discovery, robustness quantification, explainability, and visualization. Start with [architecture overview](./architecture/overview.md), then follow the relevant domain page rather than scanning the directory tree.

## Map

- **Architecture and contracts:** [architecture overview](./architecture/overview.md), [data contract](./architecture/data-contract.md), [validation/errors](./architecture/validation-and-errors.md).
- **Runtime workflow:** [PatternAnalysis session](./core/session-workflow.md), [data loading](./core/data-loading.md).
- **Analysis domains:** [tradeoffs](./analysis/tradeoffs.md), [scenario discovery](./analysis/scenario-discovery.md), [robustness](./analysis/robustness.md), [decision impact](./analysis/decision-impact.md), [feature importance](./analysis/feature-importance.md), [explanations/visualization](./analysis/explanations-and-visualization.md).
- **Support:** [semantic NaNs and utilities](./utilities/nan-and-support.md), [testing/development](./testing-and-development.md).
- **Experiments:** [pattern catalog](./patterns/overview.md), [JMT simulation recipes](./patterns/simulation-recipes.md), [federated learning](./federated-learning/overview.md), [legacy case studies](./legacy/overview.md), [operations/CI](./legacy-and-operations.md).

## Concepts and APIs

`SystemDefinition` is the root JSON contract. `GenericDataLoader` turns its `DataSpace` into aligned raw, experiment, outcome, and optional trace frames. `PatternAnalysis` is the stateful façade; `ArchSpaceCore` is the injectable coordinator. Outcomes become `DiscretizationScheme` labels and `Tradeoff` memberships, which can drive PRIM/CART `Box` discovery, contingency matrices, feature importance, and STARR/REGRET/stability-radius metrics. Figures are returned by `VisualizationManager`; explanations use `ExplanationManager` strategies.

## Intent routing

| Intent/change area | Canonical wiki page | Source entrypoints/symbols | Focused evidence | Minimal validation |
|---|---|---|---|---|
| Add/change JSON model | [data contract](./architecture/data-contract.md) | `adept/core/models.py`, `SystemDefinition`, `QualityObjective`, `Tradeoff` | `tests/test_definitions_models.py` | `pytest -q tests/test_definitions_models.py` |
| Change CSV/config loading | [data loading](./core/data-loading.md) | `GenericDataLoader.load`, `_load_from_definition`, `_apply_parameter_bindings` | `tests/test_loader.py`, `tests/test_adaptive_loader.py` | `pytest -q tests/test_loader.py tests/test_adaptive_loader.py` |
| Add tradeoff method | [tradeoffs](./analysis/tradeoffs.md) | `DataProcessor.define_tradeoffs` | `tests/test_data_processor.py` | `pytest -q tests/test_data_processor.py` |
| Change discovery/boxes | [scenario discovery](./analysis/scenario-discovery.md) | `ScenarioDiscoveryManager`, `PRIMDiscovery`, `CARTDiscovery`, `BoxEvaluator` | discovery tests | focused discovery tests with optional backends |
| Change robustness metric | [robustness](./analysis/robustness.md) | `RobustnessAnalyzer`, `PatternAnalysis.compute_robustness` | `tests/test_robustness_analyzer.py` | `pytest -q tests/test_robustness_analyzer.py` |
| Analyze policy decisions | [decision impact](./analysis/decision-impact.md) | `ContingencyAnalyzer`, `TradeoffAnalyzer` | `tests/test_contingency.py`, `test_tradeoff_analyzer.py` | those two test files |
| Change sensitivity/NaN semantics | [feature importance](./analysis/feature-importance.md), [utilities](./utilities/nan-and-support.md) | `FeatureImportanceAnalyzer`, `SemanticNaNHandler` | `tests/test_feature_importance.py`, NaN tests | focused tests plus numeric fixture |
| Add plotting/explanation strategy | [explanations/visualization](./analysis/explanations-and-visualization.md) | `ExplanationManager`, `VisualizationManager` | `tests/test_explanation_manager.py` | focused test with non-interactive backend |
| Change FL CSV preparation | [federated learning](./federated-learning/overview.md) | `split_ap_list`, `FLsystem*.json` | FL diagnostic scripts | copy input, run script, inspect IDs |
| Change pattern simulation | [simulation recipes](./patterns/simulation-recipes.md) | family `runSim.py`, JMT models | no automated simulation suite | one-row/small-grid JMT run |
| Change compatibility/legacy | [legacy overview](./legacy/overview.md) | legacy sessions/plugins/registry | `legacy/tests/*` | targeted legacy tests |
| Change documentation automation | [operations/CI](./legacy-and-operations.md) | `.github/workflows/openwiki-update.yml` | workflow diff/CLI validation | inspect generated PR, links, Mermaid |

## Validation baseline

For a normal ADEPT change, run the narrow focused test first, then `pytest -q` if dependencies and time permit. Keep full Git history for OpenWiki automation, use isolated data copies for scripts that overwrite files, and do not run large simulation Cartesian products without estimating rows. Optional PRIM/CART and Pareto dependencies are conditional checks, not reasons to mislabel a core unit-test failure.

## Backlog

- Notebook execution and JMT simulation paths remain manually validated because they require Java/JMT, generated files, multiprocessing, and potentially large parameter grids; source runners and artifact boundaries are documented in [simulation recipes](./patterns/simulation-recipes.md).
- Legacy AWS Petshop and Poli Milano workflows are cataloged as historical case studies; their current runtime parity with ADEPT is not asserted without focused migration evidence.
