# Track Specification: Refactor and Standardize Pattern Analysis Scripts

## Goal
To execute the architectural refactoring of the `ArchSpace` framework as outlined in `docs/refactoring_proposal.md`, and subsequently migrate all pattern analysis logic from Jupyter notebooks to standardized Python scripts that utilize this new, modular architecture.

## Core Requirements
1.  **Framework Refactoring (Per `docs/refactoring_proposal.md`):**
    -   Decompose the `ArchSpace` "God Class" into single-responsibility components: `DataProcessor`, `RobustnessAnalyzer`, `ScenarioDiscoverer`, `TradeoffAnalyzer`.
    -   Implement the "Coordinator" pattern for `ArchSpace`.
    -   Implement the `ScenarioDiscoveryManager` and `ExplanationManager` with strategy patterns.

2.  **Declarative Data Loading (Per `docs/json_schema_usage.md`):**
    -   Implement a generic `DataLoader` that reads system definitions from JSON files.
    -   Ensure compatibility with the defined JSON schema (System, Component, Dataspace).

3.  **Pattern Migration:**
    -   Convert existing notebooks (`.ipynb`) in `patterns/` to standardized Python scripts (`analysis.py`).
    -   Update each pattern to include a `*.json` definition file.
    -   Ensure all patterns utilize the new, refactored `ArchSpace` components.

## In Scope
-   Refactoring `archspaces/` core modules.
-   Creating/Updating JSON definitions for all patterns.
-   Refactoring `patterns/Toy_Example/` as the proof-of-concept.
-   Refactoring all other existing patterns (`Gateway`, `CQRS`, `ACL`, etc.).

## Out of Scope
-   Adding new architectural patterns (only refactoring existing ones).
-   Changing the underlying simulation data (CSVs remain the same).

## Success Criteria
-   `ArchSpace` class is significantly smaller and delegates to helper classes.
-   `pytest` suite passes for the new framework components.
-   All patterns have a valid `*.json` definition.
-   All patterns run via `analysis.py` using the new framework and produce equivalent results to the legacy notebooks.