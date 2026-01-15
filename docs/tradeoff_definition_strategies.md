# Tradeoff Definition Strategies in ADEPT

This document summarizes the different strategies available in the **ADEPT** framework for defining architectural tradeoffs. A "tradeoff" in ADEPT represents a specific region of interest within the multi-dimensional outcome space (e.g., "Low Cost & High Reliability").

Defining these regions effectively is crucial for discovering the architectural decisions (parameters) that lead to them.

## 1. Discretization-Based Exploration
**Scheme Name:** `discretization`

This is the default, exploratory approach. It simplifies continuous outcome variables into categorical bins (e.g., "Low", "Average", "High"), making it easier to reason about the solution space intuitively.

*   **Logic:**
    *   Outcomes are divided into `N` bins (default: 3).
    *   Bin boundaries can be determined automatically (equal width) or via user-defined ranges.
    *   **Labels:** Users can provide custom labels (e.g., "Fast", "Slow") or let the system generate defaults (`level_1`, `level_2`).
*   **Use Case:** Initial exploration, stakeholder communication, and understanding broad trends.
*   **Example JSON:**
    ```json
    {
      "name": "Fast-and-Cheap",
      "scheme": "discretization",
      "elements": { "executionTime": "low", "cost": "low" }
    }
    ```

## 2. Pareto-Based Strategies
These strategies leverage the concept of **Pareto Dominance** to identify optimal or near-optimal solutions. They require defining whether each objective should be maximized or minimized.

### 2.1 Pareto Nadir Point (Standard Pareto)
**Scheme Name:** `pareto` (or `pareto_nadir`)

This strategy segments the space based on the "boundary of acceptability" defined by the Pareto front itself.

*   **Logic:**
    1.  Compute the Pareto front.
    2.  Identify the **Nadir Point** (the worst value for each objective *within* the Pareto set).
    3.  Define the "Pareto-Compliant" region as the hyperbox bounded by these Nadir values.
*   **Behavior:** Effectively filters out clearly sub-optimal solutions that fall outside the range of the Pareto front.
*   **Use Case:** Filtering for solutions that are at least "in the game" relative to the best known designs.

### 2.2 Pareto Epsilon-Dominance
**Scheme Name:** `pareto_epsilon`

This strategy relaxes the strict Pareto condition to include "good enough" solutions.

*   **Logic:**
    1.  Compute the strict Pareto front.
    2.  Normalize the data.
    3.  Expand the front by a tolerance $\epsilon$ (e.g., 5%).
    4.  Any solution within distance $\epsilon$ of a Pareto-optimal point is labeled **"Epsilon-Optimal"**.
*   **Use Case:** Robust design. Finding solutions that are practically indistinguishable from the optimum given simulation noise or uncertainty.
*   **Configuration:** Requires an `epsilon` parameter (e.g., `0.05`).
*   **Visualization Note:** Since Epsilon-Optimal solutions are defined by their distance to the multi-dimensional Pareto front, they don't have a single threshold per objective. The visualization shows the **projection** (envelope) of all compliant points onto each axis.

### 2.3 Pareto Knee-Point
**Scheme Name:** `pareto_knee`

This strategy focuses on the "sweet spot" of the trade-off curve—the point of maximum curvature where marginal gains in one objective require large sacrifices in another.

*   **Logic:**
    1.  Compute the Pareto front.
    2.  Find the point on the front closest to the "Utopia Point" (ideal min/max) in normalized space.
    3.  Label this point (and optionally its neighbors within a tolerance) as the **"Knee"**.
*   **Use Case:** Finding the single most balanced design solution.
*   **Configuration:** Supports an optional `tolerance` parameter to define a "Knee Region" rather than a single point.
*   **Visualization Note:** Similar to Epsilon-Dominance, the Knee is a multi-dimensional property. The dashed lines in plots represent the min/max values of the objective at the detected knee point(s).

## 3. Static Thresholds
**Scheme Name:** `threshold`

This strategy applies hard constraints defined by the user, independent of the data distribution.

*   **Logic:**
    *   The user provides specific cutoff values for each objective.
    *   Outcomes meeting the criteria (e.g., `latency <= 200`) are labeled **"Satisfactory"**.
    *   Those failing are labeled **"Unsatisfactory"**.
*   **Use Case:** SLA compliance, hard requirements, and filtering for viability.
*   **Example JSON:**
    ```json
    {
      "name": "SLA_Compliance",
      "scheme": "threshold",
      "params": {
        "thresholds": { "response_time": 200, "availability": 0.99 }
      },
      "elements": { "response_time": "Satisfactory", "availability": "Satisfactory" }
    }
    ```

## 4. Clustering-Based Exploration (Experimental)
**Scheme Name:** `clustering` (internally `kmeans_k{N}`)

This advanced strategy uses **Univariate K-Means Clustering** to discover the "natural" groupings within the data distribution, rather than imposing equal-width bins.

*   **Logic:**
    *   For each objective, the system tests clustering with $k$ ranging from `min_k` to `max_k` (default 2-5).
    *   It calculates the **Silhouette Score** for each $k$ to determine the optimal number of clusters.
    *   Bin boundaries are set at the midpoints between cluster centroids.
*   **Use Case:** Finding data-driven performance modes (e.g., distinguishing "Normal Operation" from "Degraded" and "Failed" states without knowing the thresholds beforehand).
*   **Labels:** Generated dynamically as `C1`, `C2`, `C3`... (Cluster 1 to Cluster N).

## Summary Table

| Strategy | Goal | Key Parameters | Labels Generated |
| :--- | :--- | :--- | :--- |
| **Discretization** | General exploration | `n_bins`, `ranges`, `labels` | User-defined or `level_N` |
| **Clustering** | Natural grouping discovery | `min_k`, `max_k` | `C1`, `C2`, ... `CN` |
| **Pareto Nadir** | Bounding box of optimality | *None* | `Pareto-Compliant` |
| **Pareto Epsilon** | Robust optimality | `epsilon` (0.0-1.0) | `Epsilon-Optimal` |
| **Pareto Knee** | Balanced "sweet spot" | `tolerance` | `Knee` / `Off-Knee` |
| **Threshold** | Hard constraints | `thresholds` (dict) | `Satisfactory` / `Unsatisfactory` |

## 5. Programmatic Definition (Automated)

Instead of defining tradeoffs manually in the JSON file, you can generate them programmatically using `session.create_tradeoffs()`. This is useful for exploring all possible combinations of outcomes without verbose configuration.

### Programmatic Configuration Reference

| Method | Mandatory Parameters | Optional Parameters | Description |
| :--- | :--- | :--- | :--- |
| `discretization` | *None* | `n_bins`, `labels`, `objectives`, `ranges` | Full combinatorial grid of bins. |
| `clustering` | *None* | `min_k`, `max_k`, `objectives` | Data-driven bins using K-Means. |
| `threshold` | `thresholds` (dict) | `labels` | Satisfactory vs Unsatisfactory logic. |
| `pareto` | *None* | `objectives`, `labels` | Pareto-Efficient vs Sub-Optimal. |
| `pareto_epsilon` | `epsilon` (float) | `objectives`, `labels` | Epsilon-Optimal vs Out. |

### Usage Example

```python
# 1. Discretization (Full Grid)
# Generates all combinations of Low/High for cost and latency
session.create_tradeoffs(
    method='discretization', 
    labels={'cost': ['low', 'high'], 'latency': ['fast', 'slow']},
    objectives=['cost', 'latency']
)

# 2. Clustering (Data-Driven)
# Automatically finds optimal bins (2-5) for each objective
session.create_tradeoffs(method='clustering', min_k=2, max_k=5)

# 3. Static Thresholds (Compliance)
# Generates all combinations of Satisfactory/Unsatisfactory
# Supports custom operators: <, <=, >, >=
thresholds = {
    'latency': (200, '<'),      # Strict limit
    'availability': (0.99, '>=') # Minimum requirement
}
session.create_tradeoffs(method='threshold', thresholds=thresholds)

# 4. Pareto Efficiency (Optimality)
# Generates combinations of Pareto-Efficient vs Sub-Optimal
session.create_tradeoffs(method='pareto', objectives=['cost', 'latency'])

# 5. Epsilon-Pareto (Robust Optimality)
# Generates combinations of Epsilon-Optimal vs Out
session.create_tradeoffs(method='pareto_epsilon', epsilon=0.05)
```
