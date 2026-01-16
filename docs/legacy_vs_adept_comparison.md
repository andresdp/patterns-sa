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
from archspace import show_feature_scores, show_tradeoff_distribution

# Manual instantiation and loading
my_space = GatewayOffloading()
experiments_df, outcomes_df = my_space.load_results('./multi_N25.csv', reverse=True)
```

### ADEPT Approach
The `PatternAnalysis` session encapsulates the entire lifecycle. It uses a declarative `system.json` to define the architecture, decoupling the code from specific pattern logic.

*From `analysis-go.ipynb`:*
```python
# Unified import
from adept import PatternAnalysis

# Session-based loading with validation
session = PatternAnalysis("Gateway_Offloading.json")
session.load(validate_integrity=True)
```
**Improvement**: Reduces boilerplate and ensures data consistency through Pydantic validation.

---

## 2. Qualitative Abstraction: Tradeoffs as First-Class Citizens

### Legacy Approach
Users analyzed raw numeric distributions. "Tradeoffs" were often just visual clusters without a formal definition in the data structure.

### ADEPT Approach
ADEPT formalizes architectural goals into **Tradeoffs** using automated engines (Discretization, Pareto, Thresholds). All subsequent analysis operates on these meaningful labels (e.g., "Fast-and-Cheap").

*Code Example:*
```python
# Automatically generate 9 tradeoff regions based on "Low/Avg/High" bins
session.create_tradeoffs(
    method='discretization', 
    labels={'response_time': ['fast', 'avg', 'slow'], 'utilization': ['low', 'avg', 'high']}
)
```
**Improvement**: Moves the conversation from numbers ("< 200ms") to concepts ("Fast"), making results communicable to stakeholders.

---

## 3. Discovery & "What-If" Simulation

### Legacy Approach
Scenario discovery (PRIM) was a standalone step. The user received a "Box" (rules) but had to write custom code to verify if applying those rules actually improved the system.

### ADEPT Approach
ADEPT integrates discovery with simulation. It not only finds the rules but automatically **simulates their application** to quantify the gain.

*Code Example:*
```python
# 1. Discover rules (Boxes)
boxes = session.discover_scenarios(method='prim')

# 2. Simulate impact: Baseline vs. Improved Robustness
fig = session.show_policy_robustness_comparison_heatmap(
    boxes=boxes, 
    metric='starr', 
    title="Impact of Applying Discovered Operating Envelopes"
)
```
**Improvement**: Instantly answers, *"How much stability do we gain by enforcing these rules?"* (e.g., STARR increases from 40% to 95%).

---

## 4. Enhanced Visualization Suite

### Legacy Approach
Basic scatter plots often suffered from overplotting and unclear labeling. Legends overlapped with data, and axis labels were static.

### ADEPT Approach
Visualizations are domain-aware and polished for publication/reporting.

*   **Box Impact Plot**: `show_box_impact_objective_space` highlights *only* the points satisfying a rule, fading the rest to gray. It includes an intelligent inset summary of the constraints.
*   **Stability Radius**: Uses MDS to project high-dimensional design spaces into 2D, visualizing the "wiggle room" before failure.
*   **Readability**: Legends are automatically moved to the bottom, Y-axis labels are flipped for vertical reading, and hit targets are enlarged for visibility.

---

## 5. Robustness Metrics: STARR & REGRET

### Legacy Approach
Focused primarily on simple success rates.

### ADEPT Approach
Introduces a dual-metric view to capture both reliability and risk.
*   **STARR (Reliability)**: "What is the probability of success?" (e.g., 0.95)
*   **REGRET (Risk)**: "If we fail, how bad is it?" (Standardized distance from the target).

*Code Example:*
```python
# Get a ranking of policies based on reliability AND risk
ranking = session.get_policy_robustness_ranking(
    tradeoff_name='fast-low', 
    metric='regret'
)
```

## Summary

The ADEPT framework evolves the codebase from a set of **calculation scripts** into a **decision-support system**. It guides the user through a structured "Analysis Journey"—from defining qualitative goals to discovering and verifying the operational rules that achieve them.
