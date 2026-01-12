# ADEPT Analysis Journey: A Guide to Data-Driven Architectural Exploration

The ADEPT analysis journey is a structured pipeline designed to turn raw simulation data into actionable architectural knowledge. This document provides an in-depth look at each stage of the process, the typical questions it answers, and the specific functions to use.

---

## 0. Session Management (Lifecycle)
The `PatternAnalysis` session manages the state of your data and analysis. 

*   **Session Reset**: Use the `reset()` method to clear state.
    *   `reset(full=True)` (default): Clears everything (data, tradeoffs, splits, stats).
    *   `reset(full=False)`: **Partial Reset**. Keeps the loaded data and defined tradeoffs, but clears the data splits and feature statistics. Useful if you want to re-run scoring or discovery on a different random split without reloading the dataset.
*   **Early Data Splitting**: While splitting can happen anytime, it is ideally performed right after Tradeoffs are defined. Once `split_data()` is called, all subsequent analysis functions can target specific subsets of the data.

---

## 1. Tradeoff Definition (The Qualitative Shift)
Before analysis begins, we must translate raw numeric values (e.g., "124ms") into architectural concepts (e.g., "Fast"). This process, known as **Discretization**, allows us to group data points into "Tradeoff" regions.

### Typical Questions & Functions
1.  **"How should we categorize our performance metrics?"**
    *   *Answer with*: `define_tradeoffs(method='discretization', n_bins=3)`
    *   *Insight*: Splits metrics into Low/Avg/High, giving a quick overview of the data spread.
2.  **"Where are the optimal design points that balance conflicting goals?"**
    *   *Answer with*: `define_tradeoffs(method='pareto')` or `define_tradeoffs(method='pareto_epsilon')`
    *   *Insight*: Identifies the Pareto Front, filtering out sub-optimal designs.
3.  **"Does the system meet our strict Service Level Agreements (SLAs)?"**
    *   *Answer with*: `define_tradeoffs(method='threshold', params={'thresholds': {...}})`
    *   *Insight*: Applies hard limits (e.g., Latency < 200ms) to strictly classify success vs. failure.

### Tools & Methods
*   **Strategies**: Equal-Width Discretization, Pareto Frontiers, Epsilon-Pareto, Knee-Point Analysis, Thresholding.

---

## 2. Objective Space Exploration (Visual Confirmation)
Once tradeoffs are defined, we visualize them to confirm they align with our intuition and architectural requirements.

### Typical Questions & Functions
1.  **"What does the overall design space look like?"**
    *   *Answer with*: `show_quality_objective_space(x_metric='cost', y_metric='latency')`
    *   *Insight*: Shows the raw distribution of all simulation runs.
2.  **"Where do our 'High Reliability' solutions clump together?"**
    *   *Answer with*: `show_quality_objective_space(..., highlight_tradeoffs=[tradeoff_obj])`
    *   *Insight*: Overlays specific tradeoff regions on the scatter plot, revealing their shape and density.
3.  **"Are certain architectural policies restricting us to specific performance areas?"**
    *   *Answer with*: `show_quality_objective_space(..., highlight_policies=['policy_A', 'policy_B'])`
    *   *Insight*: Colors points by policy, showing if a decision (e.g., "Low Redundancy") forces the system into a specific corner of the objective space.

### Tools & Methods
*   **Plots**: Scatter Plots with subsets, tradeoff coloring, and policy highlighting.
*   **Overlays**: Point Overlay (density) and Rectangle Overlay (regions).

---

## 3. Relationship Analysis (Impact of Decisions)
This stage answers the critical question: *"If I choose Policy X, what is the probability I will land in Tradeoff Y?"*

### Typical Questions & Functions
1.  **"Which policy gives me the best chance of achieving my target tradeoff?"**
    *   *Answer with*: `get_policy_contingency_matrix(decision_key='...', normalization_mode='row')` or `show_policy_contingency(..., type='heatmap')`
    *   *Insight*: Shows the probability distribution. E.g., "Policy A -> 85% Success, Policy B -> 40% Success."
2.  **"Are there any policies that *guarantee* a specific outcome?"**
    *   *Answer with*: `get_deterministic_policies(decision_key='...', threshold=0.99)`
    *   *Insight*: Identifies choices with high predictability (low variance).
3.  **"Is this high-performance outcome *unique* to this expensive policy?"**
    *   *Answer with*: `get_exclusive_tradeoffs(decision_key='...')`
    *   *Insight*: Reveals if a desirable outcome is only reachable via one specific path, justifying its cost.

### Tools & Methods
*   **Contingency Matrix**: Cross-tabulation of Decisions vs. Outcomes.
*   **Visuals**: Heatmaps (Correlation), Sankey Diagrams (Flow).
*   **Helpers**: Deterministic Policies, Exclusive Tradeoffs, Variable Policies.

---

## 4. Robustness Analysis (Quantifying Stability)
While Contingency Analysis tells you "how often" a policy hits a target, Robustness Analysis quantifies the stability of that performance under uncertainty.

### Typical Questions & Functions
1.  **"How robust is Policy A against uncertainties?"**
    *   *Answer with*: `compute_robustness(policy='A', tradeoff='Target', metric='starr')`
    *   *Insight*: Returns the success rate (STARR). High score = High reliability.
2.  **"When Policy A fails, is it a minor glitch or a catastrophic breach?"**
    *   *Answer with*: `compute_robustness(policy='A', tradeoff='Target', metric='regret')`
    *   *Insight*: Returns the standardized distance from success (Regret). Low score = Safe failure; High score = Dangerous outlier.
3.  **"Which policies should I shortlist for further testing?"**
    *   *Answer with*: `get_policy_robustness_ranking(tradeoff='Target', metric='starr')` or `show_robustness_heatmap()`
    *   *Insight*: Provides a sorted list or visual comparison of all policies, allowing you to quickly filter out the unstable candidates.

### Tools & Methods
*   **Metrics**: STARR (Success Rate), Regret (Distance to Satisfaction).
*   **Reports**: Single Check, Full DataFrame Report, Ranking List, Heatmap Visualization.

---

## 5. Feature Scoring (Sensitivity & Influence)
Not all parameters are created equal. Feature scoring uses Machine Learning (Random Forests) to rank which parameters (Levers, Uncertainties, or Constraints) actually "drive" the values of your quality objectives.

### Typical Questions & Functions
1.  **"Which system parameters matter most for 'Cost'?"**
    *   *Answer with*: `compute_feature_scores(subset='train')`
    *   *Insight*: Returns a ranked list of feature importance scores for each objective.
2.  **"Are we over-complicating the model with irrelevant parameters?"**
    *   *Answer with*: `compute_feature_scores(use_smart_correlation=True)`
    *   *Insight*: Identifies and prunes redundant (highly correlated) features, simplifying the analysis.
3.  **"What is the single most critical parameter for the *overall* system health?"**
    *   *Answer with*: `get_weighted_feature_ranking(scores_df, weights={'cost': 0.5, 'latency': 0.5})`
    *   *Insight*: Aggregates scores across multiple objectives to find the global drivers.

### Tools & Methods
*   **Pipeline**: Z-Score Standardization, Outlier Removal (3$\sigma$).
*   **Algorithms**: Random Forest Regression, Smart Correlated Selection.

---

## 6. Scenario Discovery (Finding the Envelope)
The final stage generates "Operational Rules" or "Envelopes." It finds the specific ranges of parameters that reliably produce target tradeoffs.

### Typical Questions & Functions
1.  **"What are the specific operating rules (e.g., CPU < X) to ensure success?"**
    *   *Answer with*: `discover_scenarios(tradeoff_names=['MyTarget'], method='prim')`
    *   *Insight*: Returns a "Box" (rule set) that maximizes the density of successful cases.
2.  **"Can we find a broader, more flexible operational region?"**
    *   *Answer with*: `discover_scenarios(..., threshold=0.6)` (Lowering threshold)
    *   *Insight*: Relaxes the strictness of PRIM to find larger boxes, trading off some purity for coverage (Recall).
3.  **"How does the system behave across the *entire* design space?"**
    *   *Answer with*: `discover_scenarios(method='cart')`
    *   *Insight*: Uses Decision Trees to partition the whole space into regions, mapping every combination of inputs to its most likely outcome.

### Tools & Methods
*   **Algorithms**: PRIM (Patient Rule Induction Method), CART (Decision Trees).
*   **Metrics**: Population Prevalence (Baseline), Box Density (Purity), Lift (Improvement Factor).
*   **De-standardization**: Automatic conversion of Z-score rules back to original units.

---

## Conclusion
The Journey starts with **Defining what matters** (Tradeoffs), moves through **Understanding the impact of choices** (Contingency) and **Quantifying Stability** (Robustness), identifies **What drives the system** (Scoring), and ends with **Actionable rules** (Discovery) for building robust architectures.
