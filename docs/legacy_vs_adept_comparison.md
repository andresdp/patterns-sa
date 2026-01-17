# ADEPT Framework vs. Legacy System: A Comparative Analysis

This document outlines the key evolution from the legacy `ArchSpace` system to the modern `ADEPT` framework (v3.0). It highlights improvements in usability, robustness, and analytical depth, using the **Gateway Offloading** pattern analysis as a case study.

---

## 1. Workflow Structure: Ad-Hoc vs. Session-Based

### Legacy Approach
Analysis required managing state manually across scattered variables. The user had to instantiate a specific pattern class and handle data loading explicitly.

*From `robustness-paper.ipynb`:*
```python
# Legacy imports
from archspace import GatewayOffloading
my_space = GatewayOffloading()
experiments_df, outcomes_df = my_space.load_results('./multi_N25.csv', reverse=True)
```

### ADEPT Approach
The `PatternAnalysis` session encapsulates the entire lifecycle. It uses a declarative `system.json` to define the architecture, decoupling the code from specific pattern logic.

*From `analysis-go.ipynb`:*
```python
# Unified session-based loading with validation
session = PatternAnalysis("Gateway_Offloading.json")
session.load(validate_integrity=True)
```
**Improvement**: Reduces boilerplate and ensures data consistency through Pydantic validation. The session object maintains the state of loaded data, defined tradeoffs, and train/test splits consistently.

---

## 2. Preprocessing Logic: Manual vs. Pipeline Hooks

### Legacy Approach
Preprocessing was often done outside the framework or via fragile custom logic inside pattern-specific classes.

### ADEPT Approach
ADEPT introduces a **Programmatic Preprocessor Hook** during the `load()` phase. This allows users to inject complex logic (renaming columns, deriving features like service rates `S_gw`) directly into the ingestion pipeline.

*Gateway Offloading Example:*
```python
def preprocess_go(df):
    # Rename raw simulation outputs to domain concepts
    df.rename(columns={'R0': 'response_time', 'Ugw': 'utilization'}, inplace=True)
    # Derive architectural parameters from raw times
    df['S_gw'] = 1.0 / df['r_gw']
    return df

session.load(preprocessor=preprocess_go)
```
**Improvement**: Centralizes data cleaning and feature engineering, ensuring that every analytical tool in the suite works with the same "sanitized" dataset.

---

## 3. Qualitative Abstraction: Tradeoffs as First-Class Citizens

### Legacy Approach
Users analyzed raw numeric distributions. "Tradeoffs" were often just visual clusters without a formal definition.

### ADEPT Approach
ADEPT formalizes architectural goals into **Tradeoffs** using automated engines (Discretization, Pareto, Thresholds). All subsequent analysis operates on these meaningful labels (e.g., "Fast-and-Cheap").

*Gateway Offloading Example:*
```python
# Create 9 qualitative regions using discretization bins
session.create_tradeoffs(
    method='discretization', 
    labels={'response_time': ['fast', 'avg', 'slow'], 'utilization': ['low', 'avg', 'high']}
)
```
**Improvement**: Moves the conversation from numbers ("response time < 250ms") to concepts ("Is it Fast?"), making results instantly communicable to stakeholders.

---

## 4. Scenario Discovery & "What-If" Simulation

### Legacy Approach
Scenario discovery (PRIM) found "Boxes" (rules), but evaluating their impact required manual code to filter dataframes and re-calculate metrics for each policy.

### ADEPT Approach
ADEPT integrates discovery with simulation. It not only finds the operational rules but automatically **simulates their application across all policies** to quantify the gain.

*Gateway Offloading Example:*
```python
# 1. Discover the "Operating Envelope" for the 'fast-low' tradeoff
boxes = session.discover_scenarios(tradeoff_names='fast-low', method='prim')

# 2. Automatically simulate the impact on all policies
fig = session.show_policy_robustness_comparison_heatmap(
    boxes=boxes, 
    metric='starr', 
    title="Robustness Gain: Baseline vs. Box-Constrained"
)
```
**Improvement**: Instantly answers the question: *"How much more robust does my system become if I enforce these parameter constraints?"* In the Gateway Offloading case, this highlights how specific offloading strategies become nearly deterministic when the workload is constrained.

---

## 5. Enhanced Visualization Suite

### Legacy Approach
Basic scatter plots often suffered from overplotting. Legends overlapped with data, and axis labels were often cryptic numeric IDs.

### ADEPT Approach
Visualizations are domain-aware and optimized for decision support.

*   **Intelligent Box Impact**: `show_box_impact_objective_space` highlights points satisfying a rule while fading the rest to gray. It automatically positions a text summary of the constraints in the "emptiest" corner of the plot.
*   **MDS-based Stability**: Visualizes high-dimensional parameter spaces in 2D to show how much "wiggle room" a design has before performance fails.
*   **Publication-Ready Layouts**: Automatic bottom-aligned legends, bottom-to-top Y-axis labels for bins, and enlarged markers for target regions.

---

## 6. Robustness Metrics: STARR & REGRET

### Legacy Approach
Focused primarily on success rates (what % of runs passed).

### ADEPT Approach
Introduces a dual-metric view:
*   **STARR (Reliability)**: The probability of hitting the target tradeoff.
*   **REGRET (Risk)**: If the design fails, how far away is it from success? (Standardized Euclidean distance).

**Improvement**: Captures the "severity" of failure, allowing architects to choose policies that are not just "reliable" but also "safe" (low regret) in the event of extreme environment changes.

---

## Summary Table

| Capability | Legacy System | ADEPT Framework (v3.0) |
| :--- | :--- | :--- |
| **Workflow State** | Disconnected variables | Encapsulated in `PatternAnalysis` session |
| **Schema Validation** | None (manual DF handling) | Declarative `system.json` + Pydantic |
| **Goal Definition** | Raw numbers / visual clusters | Formal `Tradeoff` entities |
| **Data Partitioning** | Manual splitting | Stratified train/test auto-splitting |
| **"What-If" Analysis** | Manual filtering scripts | Automated Improvement Matrix + Heatmaps |
| **Explainability** | Printed text stats | Intelligent Box Annotations + Impact Viz |

The ADEPT framework evolves the codebase from a collection of **analytical scripts** into a **decision-support system** that guides the user through a structured "Analysis Journey."