# Track Specification: ADEPT Framework Implementation

## Goal
To implement the **ADEPT** (Architectural Decision Exploration and Pattern Tradeoffs) framework, evolving the existing ArchSpace toolkit into a unified system for data-driven architectural analysis. This track focuses on core data modeling, enhanced discretization-based exploration, and migration of existing patterns to the new ADEPT architecture.

## Core Requirements
1.  **ADEPT Core Modeling:**
    -   Implement the parameter hierarchy (Levers, Uncertainties, Outcomes) at System, Pattern, and Infrastructure levels.
    -   Support for **Adaptive Processes** and **Behavioral Traces** to analyze temporal behavior in stateful systems (e.g., Federated Learning).
    -   Reorganize the framework into the modular structure proposed in `docs/functional.md`.

2.  **Enhanced Discretization Paradigm:**
    -   Formalize `QualityBin` and `DiscretizationScheme` entities.
    -   Integrate discretization-based scenario discovery (PRIM/CART) into the unified ADEPT API.

3.  **Pattern Migration:**
    -   Convert legacy notebooks and scripts to use the ADEPT `SystemDefinition` (JSON) and `ArchSpaceCore` coordinator.
    -   Support both static (microservices) and adaptive (FL) patterns.

## In Scope
-   Reorganizing `archspaces/` into `adept/` or an equivalent modular structure.
-   Implementing advanced metadata parsing in `DataLoader`.
-   Migrating all existing patterns (`Toy`, `Gateway`, `CQRS`, `ACL`, `FL`, `AWS_Petshop`).
-   Implementing the `LLMExplainerStrategy`.

## Out of Scope
-   Experiment Orchestration / Simulation execution (sampling and simulation remain external for now).
-   Pareto-Epsilon Optimization paradigm (deferred to a future track).

## Success Criteria
-   The framework supports the Lever/Uncertainty/Outcome parameter hierarchy.
-   Adaptive processes can be loaded and analyzed via behavioral traces.
-   All existing patterns are migrated to standardized `analysis.py` scripts and `*.json` definitions.
-   `pytest` suite passes for all ADEPT core components and migrated patterns.
