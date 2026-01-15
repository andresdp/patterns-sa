# ADEPT Analysis Journey: A Guide to Data-Driven Architectural Exploration

The ADEPT analysis journey is a structured pipeline designed to turn raw simulation data into actionable architectural knowledge. This document provides an in-depth look at each stage of the process, the typical questions it answers, and the specific functions to use.

---

## 0. Session Management (Lifecycle)
The `PatternAnalysis` session manages the state of your data and analysis. 

*   **Session Reset**: Use the `reset()` method to clear state.
    *   `reset(full=True)` (default): Clears everything (data, tradeoffs, splits, stats).
    *   `reset(full=False)`: **Partial Reset**. Keeps the loaded data and defined tradeoffs, but clears the data splits and feature statistics.
*   **Early Data Splitting**: While splitting can happen anytime, it is ideally performed right after Tradeoffs are defined. Once `split_data()` is called, all subsequent analysis functions can target specific subsets of the data.

---

## 1. Tradeoff Definition (The Qualitative Shift)
Before analysis begins, we must translate raw numeric values (e.g., "124ms") into architectural concepts (e.g., "Fast"). This process, known as **Discretization**, allows us to group data points into "Tradeoff" regions.

### Typical Questions & Functions
1.  **"How should we categorize our performance metrics?"**
    *   *Answer with*: `create_tradeoffs(method='discretization', n_bins=3)`
    *   *Insight*: Splits metrics into Low/Avg/High, giving a quick overview of the data spread.
2.  **"Where are the optimal design points that balance conflicting goals?"**
    *   *Answer with*: `create_tradeoffs(method='pareto_epsilon', epsilon=0.05)`
    *   *Insight*: Identifies designs near the Pareto Front. v3.0 now distinguishes between "Out-Low" and "Out-High" regions for granular analysis.
3.  **"Does the system meet our strict Service Level Agreements (SLAs)?"**
    *   *Answer with*: `create_tradeoffs(method='threshold', thresholds={'latency': 200})`
    *   *Insight*: Applies hard limits to strictly classify success vs. failure.

### Tools & Methods
*   **Automated Configuration**: `create_tradeoffs()` is the unified entry point. It automatically calls `clear_tradeoffs()` and `define_tradeoffs()` to process data immediately.
*   **Membership Tracking**: Every `Tradeoff` object now tracks `has_points` and `point_count` automatically.

---

## 2. Objective Space Exploration (Visual Confirmation)
Visualize defined tradeoffs to confirm they align with architectural requirements.

### Typical Questions & Functions
1.  **"What does the overall design space look like?"**
    *   *Answer with*: `show_quality_objective_space(x_metric='cost', y_metric='latency')`
2.  **"Are certain policies restricting us to specific performance areas?"**
    *   *Answer with*: `show_quality_objective_space(..., highlight_policies=['policy_A', 'policy_B'])`
    *   *Insight*: Colors points by policy. v3.0 features intelligent **bottom-aligned legends** and **flipped Y-axis labels** for better readability.

### Tools & Methods
*   **Configurable Transparency**: Use `background_alpha` (default 0.6) to separate the overall distribution cloud from highlighted points.
*   **Enlarged Targets**: Tradeoff rectangles are now expanded by a small `eps` (default 0.01) to ensure visibility of narrow performance regions.

---

## 3. Relationship Analysis (Impact of Decisions)
*"If I choose Policy X, what is the probability I will land in Tradeoff Y?"*

### Typical Questions & Functions
1.  **"Which policy gives me the best chance of achieving my target tradeoff?"**
    *   *Answer with*: `show_policy_contingency(..., type='heatmap')`
2.  **"Is this high-performance outcome unique to this expensive policy?"**
    *   *Answer with*: `get_exclusive_tradeoffs(decision_key='...')`

### Tools & Methods
*   **Contingency Matrix**: Cross-tabulation of Policies vs. Tradeoffs.
*   **Visuals**: Heatmaps (Correlation), Sankey Diagrams (Flow).

---

## 4. Robustness Analysis (Quantifying Stability)
Robustness Analysis quantifies the stability of performance under parameter uncertainty.

### Typical Questions & Functions
1.  **"How much 'wiggle room' do we have in our parameters before failure?"**
    *   *Answer with*: `show_stability_radius(policy='A', tradeoff='Target')`
    *   *Insight*: Uses **MDS (Multi-Dimensional Scaling)** to project the high-dimensional parameter space into 2D. Shows a "Stability Bubble" around the nominal design center.
2.  **"Which policies should I shortlist for further testing?"**
    *   *Answer with*: `show_robustness_heatmap(metric='starr')`
3.  **"What happens if we apply optimized constraints to our policies?"**
    *   *Answer with*: `show_policy_robustness_comparison_heatmap(boxes=aligned_boxes)`
    *   *Insight (What-If)*: Side-by-side comparison of **Baseline** vs. **Improved** robustness, showing the impact of "Operating Envelopes."

### Tools & Methods
*   **Metrics**: STARR (Success Rate), REGRET (Distance to target), Stability Radius (Distance to failure).
*   **Visuals**: MDS Parameter Projection vs. Objective Space (Dual-Panel), Robustness Comparison Heatmaps.

---

## 5. Feature Scoring (Sensitivity & Influence)
ML-driven ranking of which parameters actually "drive" your quality objectives.

### Typical Questions & Functions
1.  **"Which system parameters matter most for 'Cost'?"**
    *   *Answer with*: `compute_feature_scores()`
2.  **"What is the single most critical parameter for global system health?"**
    *   *Answer with*: `get_weighted_feature_ranking(scores_df, weights=...)`

### Tools & Methods
*   **Algorithms**: Random Forest Regression, Smart Correlated Selection.
*   **Visuals**: Feature Importance Heatmaps.

---

## 6. Scenario Discovery (Finding the Envelope)
Generate operational rules that find the "Success Envelope" in the parameter space.

### Typical Questions & Functions
1.  **"What are the specific operating rules to ensure success?"**
    *   *Answer with*: `discover_scenarios(method='prim')`
    *   *Insight*: Returns a **Named Box** (e.g., "Box for Fast-Reliable") with density and coverage metrics.
2.  **"How do these constraints affect my policies visually?"**
    *   *Answer with*: `show_box_impact_objective_space(box=my_box)`
    *   *Insight*: Highlights only the points filtered by the box, retaining their policy colors. Includes an **intelligent inset summary** of constraints.

### Tools & Methods
*   **Algorithms**: PRIM, CART.
*   **Helpers**: `align_boxes_to_tradeoffs()` to map discovery results back to system tradeoffs for "What-If" analysis.

---

## Conclusion
The Journey starts with **Defining what matters** (Tradeoffs), moves through **Understanding the impact of choices** (Contingency) and **Quantifying Stability** (Robustness), identifies **What drives the system** (Scoring), and ends with **Actionable rules** (Discovery) and **What-If Simulations** for building resilient architectures.