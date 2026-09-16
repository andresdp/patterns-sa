---
type: development guide
title: Testing and development map
description: Authoritative commands, behavior-to-test routing, side effects, external dependencies, and safe change recipes for patterns-sa.
tags: [testing, development, pytest]
---

# Testing and development map

Set up an isolated Python environment and install `requirements.txt`; the repository is a Python package without a project manifest. The primary command is `pytest -q`. Focused commands are `pytest -q tests/test_loader.py`, `pytest -q tests/test_data_processor.py`, `pytest -q tests/test_linter.py`, `pytest -q tests/test_robustness_analyzer.py`, and analogous named files below.

| Behavior | Evidence | Narrow check/caveat |
|---|---|---|
| Pydantic models, aliases, coercion | `tests/test_definitions_models.py`, `test_tradeoff_entity.py` | `pytest -q tests/test_definitions_models.py tests/test_tradeoff_entity.py` |
| Coordinator/session delegation | `tests/test_archspace_core.py`, `test_explanation_manager.py` | no external JMT |
| JSON/CSV loading and partitioning | `tests/test_loader.py`, `tests/test_adaptive_loader.py` | tests create/remove fixture files; run from repo root |
| semantic/linter validation | `tests/test_linter.py`, `tests/test_validation.py` | distinguishes warnings from façade exceptions |
| discretization/Pareto/threshold | `tests/test_data_processor.py` | Pareto requires `paretoset` |
| PRIM/CART interfaces | `tests/test_scenario_discovery.py`, `test_scenario_discovery_paradigms.py`, `test_scenario_discovery_manager.py` | backend availability affects deep execution |
| STARR/robustness/tradeoff neighbors | `tests/test_robustness_analyzer.py`, `test_tradeoff_analyzer.py` | preserve aligned indices |
| contingency and feature importance | `tests/test_contingency.py`, `test_feature_importance.py` | numeric features and valid config map required |
| session behavior and failures | `tests/test_adaptive_loader.py`, `test_contingency.py`, `test_tradeoff_entity.py` | current session signatures override stale docs |
| federated preprocessing/JSON | `federatedlearning/test_json_validation.py`, `test_split_json.py`, `test_manual_simple.py` | diagnostic scripts; hard-coded host paths/working directories; not all are pytest-safe |
| legacy migration/plugins | `legacy/tests/test_analysis_session.py`, `test_behavioral_analysis.py`, `test_parameter_registry.py`, `test_pattern_migration.py`, `test_toy_plugin.py` | legacy compatibility surface |
| JMT simulations/notebooks | `patterns/*/runSim.py`, notebooks | no automated execution; Java/JMT, multiprocessing, file cleanup, and potentially large grids |

Loader tests write temporary `tests/test_data.csv` and `tests/test_system.json` and remove them in teardown. Simulation runners overwrite output CSVs, create temporary model/result files, append under a process lock, and shell-delete artifacts. Manual FL scripts may change working directory and assume local paths. Use copies or a disposable worktree for those workflows.

Change recipes: for a new schema field, update `adept/core/models.py`, exports if public, a representative JSON fixture, and model/linter tests; for a new analysis manager, implement a focused class, inject/delegate it through `ArchSpaceCore`, update exports only when intentionally public, and test the narrow façade; for a new tradeoff method, update `DataProcessor`, scheme/boundary outputs, session parameter validation, and fixture assertions; for a new external runner, first validate a one-row/small-grid dry run and document external prerequisites.

Existing docs such as `docs/analysis_journey.md`, `docs/usage.md`, and `DEPENDENCIES.md` are useful intent references but contain stale names/version ranges in places. Verify every command against current source before using it.
