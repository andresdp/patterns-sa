# Performance Metrics and Evaluation for Architectural Tradeoff Discovery

This document summarizes the metrics, methodologies, and philosophical challenges involved in evaluating algorithms (such as PRIM and CART) used for discovering architectural tradeoffs within the ADEPT framework.

## 1. The Evaluation Problem

The core task is **Subgroup Discovery**: identifying regions in the design parameter space (Parameter Space $X$) that map to specific, desirable regions in the quality objective space (Outcome Space $Y$).

Since algorithms like PRIM and CART generate **Axis-Parallel Hyper-Rectangles** (Boxes) to approximate these regions, evaluation must measure two distinct qualities:
1.  **Fidelity:** How accurately does the box capture the target tradeoff?
2.  **Explainability:** How simple and interpretable is the rule defined by the box?

## 2. Quantitative Metrics

To assess these qualities, we define the following metrics at the **Box** and **Algorithm** levels.

### 2.1. Individual Box Metrics (Per Tradeoff)

For a single discovered box $B$ targeting a specific tradeoff region $T$:

*   **Density (Precision):** The fraction of points inside Box $B$ that actually belong to Tradeoff $T$.
    $$ \text{Density} = \frac{|B \cap T|}{|B|} $$ 
    *   *Interpretation:* "If I apply this rule, how likely am I to get the desired result?"

*   **Coverage (Recall):** The fraction of all valid Tradeoff $T$ points that are captured by Box $B$.
    $$ \text{Coverage} = \frac{|B \cap T|}{|T|} $$ 
    *   *Interpretation:* "How much of the available 'good' design space did I find?"

*   **Complexity:** The number of parameters constrained by the box.
    *   *Interpretation:* Lower is better. A rule like `cache_size > 50` (Complexity=1) is better than `cache_size > 50 AND threads < 10 AND algo != 'A'` (Complexity=3).

### 2.2. Global Algorithm Scores

To compare algorithms (e.g., PRIM vs. CART) or tradeoff definition strategies, we aggregate individual box performance.

#### The Macro-Averaged F1 Score (Recommended)
We treat each Tradeoff Region as a distinct classification task and average the performance across all regions.

1.  **Compute F1 for each Tradeoff:** Harmonic mean of Density and Coverage.
2.  **Average:**
    $$ \text{Score} = \frac{1}{N} \sum_{i=1}^{N} F1_i $$ 

**Weighting Strategies:**
*   **Equal Weighting (Default):** Every tradeoff region counts equally. This rewards algorithms that find "Rare Gems" (small, high-value regions) just as much as massive, obvious regions.
*   **Frequency Weighting:** Weights each tradeoff by the number of data points it contains ($|T_i|$). This measures how well the algorithm explains the *bulk* of the data but penalizes discovery of rare solutions.

## 3. The "Meta-Problem": Topology Mismatch

Assessing the "best" tradeoff definition strategy is not a single optimization problem but a **Bi-Objective Pareto Optimization** between **Fidelity** and **Explainability**.

### 3.1. The Spaces
*   **Objective Space ($Y$):** Often low-dimensional (2-3 metrics) and continuous. Easy to define clean, rectangular "Sweet Spots."
*   **Parameter Space ($X$):** High-dimensional, mixed discrete/continuous.

### 3.2. The Friction
A single, contiguous "good" region in $Y$ often maps to **multiple, disjoint, or diagonal** shapes in $X$.
*   **The "Islands" Problem:** A "Low Latency" goal might be achieved by two completely different configurations (e.g., "High Cache" vs. "High Bandwidth"). A single box cannot capture both without including the "bad" space in between.
*   **The Diagonal Problem:** If parameters interact (e.g., $P_1 + P_2 < C$), the valid region is a triangle. A rectangular box approximates this poorly (stair-step effect), resulting in high complexity or low density.

### 3.3. Implications for Evaluation
When comparing strategies (e.g., Discretization vs. Pareto vs. Clustering):
*   **Discretization:** Often yields higher F1 (Accuracy) because it draws broad, arbitrary lines that are easy to hit.
*   **Pareto/Clustering:** Often yields lower F1 but higher semantic value. They define "perfect" regions that are physically harder to approximate with rectangles.

**Conclusion:** A strategy with a lower Global F1 score is not necessarily "worse"; it may simply be more ambitious (defining a harder-to-reach target). The ideal strategy maximizes F1 while minimizing Box Complexity.

## 4. Meta-Optimization: Exploring the Strategy Space

Finding the "best" tradeoff definition strategy for a given dataset can be framed as a **Meta-Optimization** problem. Since the range of candidate strategies (Discretization, Pareto, Clustering, etc.) and their hyperparameters (number of bins, epsilon, K) are predefined, we can use **Bayesian Optimization** (via toolkits like `Optuna`) to navigate this space.

### 4.1. Why Bayesian Optimization?
*   **Sample Efficiency:** Evaluating a strategy is expensive (requires running the tradeoff logic and discovery algorithms for multiple regions). Bayesian Optimization is designed to find optimal configurations with minimal trials.
*   **Conditional Parameters:** Different strategies have different parameters (e.g., `n_bins` for discretization vs. `epsilon` for Pareto). Tools like Optuna handle these "branching" search spaces natively.
*   **Multi-Objective Pareto Fronts:** Instead of picking one "winner," multi-objective optimization can identify the entire **Pareto Front of Strategies**, allowing the architect to choose between a "Highly Simple/Low Accuracy" strategy and a "Complex/High Accuracy" one.

### 4.2. Conceptual Workflow
1.  **Trial Configuration:** Sample a strategy method and its specific hyperparameters.
2.  **Execution:** Define tradeoffs and run the discovery algorithm (PRIM/CART).
3.  **Scoring:** Compute the Global Average F1 (Fidelity) and Average Complexity (Explainability).
4.  **Feedback:** Use the scores to inform the next trial, converging toward the most "natural" definitions of good/bad for that specific architectural pattern.

