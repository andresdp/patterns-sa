# ADEPT Analysis Journey: A Guide to Data-Driven Architectural Exploration

The ADEPT analysis journey is a structured pipeline designed to turn raw simulation data into actionable architectural knowledge. This document provides an in-depth look at each stage of the process, the options available, and how to interpret the results.

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

*   **Why it matters**: Complex systems often have conflicting goals. By defining tradeoffs, we shift the focus from optimizing a single number to finding regions where multiple quality objectives reach a satisfying balance.
*   **Available Strategies**:
    *   **Equal-Width Discretization**: Splits the range of an objective into $N$ equal parts. Good for general exploration.
    *   **Pareto Frontiers**: Identifies points that represent the best possible compromises. No point on the frontier can be improved in one objective without being degraded in another.
    *   **Epsilon-Pareto**: A "fuzzy" Pareto approach that ignores small, insignificant differences, resulting in a cleaner frontier.
    *   **Knee-Point Analysis**: Automatically identifies the "elbow" of a curve—the region where you get the most improvement for the least cost.
    *   **Thresholding**: Sets hard engineering limits (e.g., "Reliability must be > 99.9%").

---

## 2. Objective Space Exploration (Visual Confirmation)
Once tradeoffs are defined, we visualize them to confirm they align with our intuition and architectural requirements.

*   **Scatter Plots**: We plot pairs of objectives (e.g., Cost vs. Execution Time).
    *   **Data Subsets**: Most visualization and analysis functions accept a `subset` parameter (`'all'`, `'train'`, or `'test'`). This allows you to verify if the patterns seen in the training data still hold true in the held-out test data.
    *   **Coloring by Tradeoff**: Highlights where the "Inexpensive-but-reliable" points cluster.
    *   **Coloring by Policy**: Shows if certain architectural decisions (e.g., "Serverless Deployment") naturally gravitate towards specific performance regions.
*   **Overlay Modes**:
    *   **Point Overlay**: Every sample is a dot. Best for seeing density and outliers.
    *   **Rectangle Overlay**: Draws bounding boxes for tradeoff regions. Best for visualizing the "target zones" without the noise of individual points.

---

## 3. Relationship Analysis (Impact of Decisions)
This stage answers the critical question: *"If I choose Policy X, what is the probability I will land in Tradeoff Y?"*

*   **The Contingency Matrix**: A cross-tabulation of Architectural Decisions vs. Tradeoff Membership. 
    *   **DataFrames**: You can retrieve the raw contingency table as a pandas DataFrame using `get_policy_contingency_matrix()`.
*   **Normalization Modes**:
    *   **Row Normalization (`row`)**: (Highly Recommended) For a specific decision (e.g., "Load Balancer: Round Robin"), it shows the percentage distribution across all tradeoffs. This allows you to say: *"Policy A leads to 'Fast' outcomes 80% of the time."*
    *   **Population Normalization (`population`)**: Shows the count relative to the total dataset. Useful for understanding which decisions are most frequent in the simulation.
*   **Analytical Helpers**:
    *   **Deterministic Policies**: `get_deterministic_policies()` identifies choices that *always* result in a specific tradeoff (High Predictability).
    *   **Exclusive Tradeoffs**: `get_exclusive_tradeoffs()` identifies quality outcomes that can *only* be achieved by one specific policy (Uniqueness).
    *   **Variable Policies**: `get_variable_policies()` flags decisions that lead to multiple possible tradeoffs (High Uncertainty).
*   **Visual Tools**:
    *   **Heatmaps**: Use color intensity to show "hotspots" where decisions and tradeoffs strongly correlate.
    *   **Sankey Diagrams**: Visualize the "flow" of probability. Ideal for multi-step architectural decisions where you want to see how choices aggregate into outcomes.

---

## 4. Feature Scoring (Sensitivity & Influence)
Not all parameters are created equal. Feature scoring uses Machine Learning (Random Forests) to rank which parameters (Levers, Uncertainties, or Constraints) actually "drive" the values of your quality objectives.

*   **Subset Recommendation**: Scoring should typically be performed on the `'train'` subset. You can then use the `'test'` subset to validate how well these features explain the outcomes in unseen scenarios.
*   **The Preprocessing Pipeline**:
    *   **Z-Score Standardization**: Since "Cost" ($) and "Latency" (ms) have different units, we use `StandardScaler` to put them on a uniform scale.
    *   **Outlier Removal**: We filter out simulation "noise" by removing points that fall outside $3\sigma$ of the mean.
*   **Advanced Selection**:
    *   **Smart Correlated Selection**: In many simulations, parameters are redundant. This step identifies groups of correlated features and keeps only the most predictive one, preventing the "dilution" of importance scores.
*   **Weighted Ranking**: Because an architecture must satisfy multiple stakeholders, you can assign weights to different objectives. ADEPT then produces a **Single Unified Ranking** of features that most affect the system's overall health.

---

## 5. Scenario Discovery (Finding the Envelope)
The final stage generates "Operational Rules" or "Envelopes." It finds the specific ranges of parameters that reliably produce target tradeoffs.

*   **Multi-Tradeoff Targeting**: You can pass a single name, a list of names, or `None` (targets all tradeoffs) to the discovery method.
*   **The Algorithms**:
    *   **PRIM (Patient Rule Induction Method)**: A "bottom-up" approach. If multiple tradeoffs are requested, PRIM runs iteratively for each one, finding the most concentrated box for every target.
    *   **CART (Decision Trees)**: A "top-down" approach. It partitions the entire space at once. If specific tradeoffs are requested, CART runs globally and then filters the results to only show the "leaves" that match your criteria.
*   **The "Success" Metrics**:
    *   **Population Prevalence**: The % of points in the whole dataset that meet the target (the "Baseline").
    *   **Box Density**: The % of points *inside the box* that meet the target.
    *   **Lift**: Calculated as `Density / Prevalence`. A Lift of 5.0 means that by following the box's rules, you are **5 times more likely** to achieve your target tradeoff than if you chose parameters randomly.
*   **De-standardization**: If standardization was applied during scoring, ADEPT automatically converts the rules back to the original units (e.g., converting a Z-score of 1.5 back to "5000 CPU Cycles").

---

## 6. Robustness Analysis (Quantifying Stability)
While Contingency Analysis tells you "how often" a policy hits a target, Robustness Analysis quantifies the stability of that performance under uncertainty.

*   **Metrics**:
    *   **STARR (Success Rate)**: Simply the probability of satisfying the tradeoff. (Range: 0.0 to 1.0, Higher is Better).
    *   **Regret (Distance to Satisfaction)**: If a system fails to meet the tradeoff, *how badly* did it miss? Regret measures the distance from the acceptable boundary. (Range: 0 to $\infty$, Lower is Better).
*   **Tools**:
    *   **Single Check**: `compute_robustness()` calculates the metric for one policy against one tradeoff.
    *   **Full Report**: `get_robustness_report()` generates a table (DataFrame) comparing all policies across all tradeoffs.
    *   **Visual Report**: `show_robustness_heatmap()` visualizes the report as a color-coded matrix, automatically using green scales for success rates (STARR) and red scales for error magnitudes (Regret).
    *   **Ranking**: `get_policy_robustness_ranking()` returns a sorted list of policies, ordered from most to least robust for a specific target. It automatically handles the sorting direction (descending for STARR, ascending for Regret).

---

## Conclusion
The Journey starts with **Defining what matters** (Tradeoffs), moves through **Understanding the impact of choices** (Contingency), identifies **What drives the system** (Scoring), and ends with **Actionable rules** (Discovery) for building robust architectures.
