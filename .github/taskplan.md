# ArchSpace Plugin-Driven Blueprint

This blueprint tracks the initial implementation plan for the plugin-driven `ArchSpace` refactor.

Goals
- Promote conceptual definitions to first-class dataclasses under `archspaces/definitions.py`.
- Introduce a plugin API with separate `ParserHook`, `MetricsHook`, and `ReportHook` under `archspaces/plugin_api.py`.
- Implement a minimal `Toy` plugin plus a pandas ETL and a mock-data generator to bootstrap tests and CI.
- Provide LLM/Frontend hooks later (`archspaces/llm_explainers.py`, `archspaces/frontend_adapter.py`).

Tasks (short)
- `archspaces/definitions.py`: dataclasses for `ArchitectureSpace`, `ConfigurationSpace`, `QualityObjective`.
 - `archspaces/definitions.py`: migrated dataclasses → Pydantic v2 `BaseModel` classes (completed).
- `archspaces/plugin_api.py`: plugin interfaces and `PluginRegistry`.
- `archspaces/plugins/toy.py`: Toy plugin implementing parser/metrics/report hooks.
- `patterns/Toy_Example/etl.py`: pandas-based normalizer.
- `patterns/Toy_Example/analysis.py`: runnable example using the Toy plugin.
- `tools/mock_generator.py`: small mock-data CSV generator for CI/tests.

Status: see repository TODO list (managed by automation).

Notes
- This file is intended to remain current and reflect task statuses and changes to the design.

Current status (quick):

- `archspaces/definitions.py`: completed
- `archspaces/plugin_api.py`: completed
- `archspaces/plugins/toy.py`: completed
- `patterns/Toy_Example/etl.py`: completed
- `patterns/Toy_Example/analysis.py`: completed
- `tools/mock_generator.py`: completed
- Tests & fixtures for Toy plugin: completed (tests/test_toy_plugin.py)
 - Tests & fixtures for Toy plugin: completed (tests/test_toy_plugin.py)
 - New unit tests for definitions models: added (tests/test_definitions_models.py)
- `archspaces/llm_explainers.py`: added (in-progress for extended features)
- `archspaces/frontend_adapter.py`: added (in-progress)
- `archspaces/reporting.py`: added (in-progress)

Next immediate work items:
- Add example usage of `LocalTemplateExplainer` in the Toy analysis and wire the `reporting` exports into the `analysis.py` run.
- Add CI workflow and update `requirements.txt` if needed.

Recent changes (dec 13, 2025):
- Converted `archspaces/definitions.py` from dataclasses to Pydantic v2 models with lightweight compatibility shims (`from_dict`, `dict`).
- Added `pydantic>=2.0,<3.0` to `requirements.txt`.
- Added `tests/test_definitions_models.py` to validate construction, nested validation, coercion, and backward-compatible shims.

Immediate next steps:
- Run the new tests locally or in CI: `pytest -q tests/test_definitions_models.py`.
- Audit codepaths that serialize or mutate `ArchitectureSpace` objects and update to use `.dict()`/`.model_dump()` or the provided shims if necessary.
- Continue implementing PRIM/CART adapters and strengthen `archspaces/validator.py` (pandera optional).

