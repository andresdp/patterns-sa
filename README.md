# ADEPT Framework

<!-- ![ADEPT Logo](adept.png){width=50%} -->

<img src="adept.png" alt="ADEPT Logo" style="display: block; margin: 0 auto; width: 40%;"/>


 **ADEPT** (**A**rchitectural **D**esign **E**xploration and **P**attern **T**radeoffs) is a toolkit to perform sensitivity analysis, robustness quantification, and explainability of architectural tradeoffs.

## Overview

**ADEPT** is a Python-based framework for analyzing the performance and quality attributes of software architectural patterns. It provides a structured, data-driven approach to evaluate design decisions, discover "Operating Envelopes" via scenario discovery, and quantify robustness.

## Key Features

- **Coordinator Pattern Architecture**: Centralized orchestration (`ArchSpaceCore`) with specialized managers.
- **Robustness Quantification**: Metrics like STARR (Success Rate), REGRET (Risk), and Stability Radius.
- **Scenario Discovery**: Algorithms (PRIM, CART) to find parameter regions that guarantee specific tradeoffs.
- **Tradeoff Analysis**: Automated definition of performance regions using Discretization, Pareto Fronts, or Thresholds.
- **Advanced Visualization**: Interactive plots for Quality Objective Spaces, Robustness Heatmaps, and Feature Importance.

## Project Structure

The project is organized into a modular package structure:

### `adept/` (Core Framework)
*   **`core/`**: The backbone of the system.
    *   `coordinator.py`: The `ArchSpaceCore` orchestrator.
    *   `session.py`: `PatternAnalysis`, the primary user-facing class for interactive sessions.
    *   `models.py`: Pydantic data models (`SystemDefinition`, `Tradeoff`, `Box`).
    *   `loader.py`: `GenericDataLoader` for declarative data ingestion.
*   **`analysis/`**: Specialized analytical engines.
    *   `discovery.py`: PRIM and CART algorithms (`ScenarioDiscoveryManager`).
    *   `robustness.py`: Calculation of STARR, REGRET, and Stability Radius.
    *   `discretization.py`: Segmentation of continuous outcomes into qualitative regions.
    *   `feature_importance.py`: Random Forest-based sensitivity analysis.
    *   `contingency.py`: Analysis of Policy vs. Tradeoff relationships.
*   **`utils/`**: Shared utilities.
    *   `validation.py` & `linter.py`: Data integrity checks.
    *   `exceptions.py`: Custom error hierarchy.

### `patterns/` (Usage Examples)
Contains concrete case studies of architectural patterns. Each folder includes a `SystemDefinition` (JSON) and a Jupyter Notebook demonstrating the full analysis workflow.
*   **Active Patterns**: `CQRS`, `Gateway_Aggregation`, `Gateway_Offloading`, `Anti_Corruption_Layer`, `Pipes_and_Filters`.

## Installation

```bash
pip install -r requirements.txt
```

## Quick Start

To see the framework in action, please refer to the interactive notebooks in the `patterns/` directory.

*   **Recommended Starting Point**: `patterns/Gateway_Offloading/analysis-go.ipynb`

These notebooks demonstrate the standard workflow:
1.  **Load**: Ingest simulation data using a JSON definition.
2.  **Define**: Map raw metrics to architectural tradeoffs (e.g., "Fast & Cheap").
3.  **Analyze**: Compute feature importance and contingency tables.
4.  **Discover**: Find robust operating envelopes using PRIM.
5.  **Visualize**: Generate robustness heatmaps and objective space scatters.

## Documentation

For deep dives into the design and usage:

- `docs/software_architecture.md` - High-level component diagram.
- `docs/analysis_journey.md` - The logical flow of an ADEPT session.
- `docs/scenario_discovery_metrics.md` - Explanation of Density and Coverage.
- `docs/legacy_vs_adept_comparison.md` - Migration guide for v2 users.

## License

This project is licensed under the MIT License.