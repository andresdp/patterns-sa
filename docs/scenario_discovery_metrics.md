# Scenario Discovery: Density, Coverage, and Architectural Strategy

In the ADEPT framework, **Scenario Discovery** algorithms (PRIM and CART) are used to find "Operating Envelopes"—specific regions in the parameter space where a chosen architectural policy reliably meets desired quality attribute tradeoffs.

The quality of these discovered envelopes is measured by two competing metrics: **Density** and **Coverage**.

---

## 1. Core Concepts

### Density (Precision / Reliability)
*   **Definition**: The proportion of simulation runs *inside the discovered box* that successfully meet the target tradeoff.
    *   $\text{Density} = \frac{\text{Successes inside Box}}{\text{Total Points inside Box}}$
*   **Architectural Interpretation**: **Reliability**.
    *   A density of 1.0 (100%) means the design is **deterministic** under these constraints. If you stay within the envelope, the system *will* work.
    *   Low density means the design is risky; even with these constraints, failure is possible.

### Coverage (Recall / Applicability)
*   **Definition**: The proportion of *all successful runs in the entire dataset* that are captured by this box.
    *   $\text{Coverage} = \frac{\text{Successes inside Box}}{\text{Total Successes in Dataset}}$
*   **Architectural Interpretation**: **Generalizability**.
    *   High coverage means this rule explains the primary mechanism for success. The constraints are broad and applicable to most situations.
    *   Low coverage means this rule finds only a "niche" solution. There are other ways to make the system work that this specific rule doesn't cover.

---

## 2. Tuning the Algorithms

You can control the compromise between Density and Coverage using parameters in `session.discover_scenarios()`.

### PRIM (Patient Rule Induction Method)
PRIM iteratively "peels" away non-target data to maximize Density.

*   **`threshold` (Target Density)**: The most direct control.
    *   **High (e.g., 0.95)**: Demands extreme purity. Results in smaller boxes (Lower Coverage) but high Reliability.
    *   **Low (e.g., 0.60)**: Accepts noisier boxes. Results in larger boxes (Higher Coverage) but lower Reliability.
*   **`mass_min` (Minimum Support)**: The minimum fraction of data the box must contain.
    *   **High Value**: Forces PRIM to find broad, general rules (Higher Coverage).
    *   **Low Value**: Allows PRIM to zoom in on tiny "sweet spots" (Higher Density).

### CART (Classification and Regression Trees)
CART splits the entire space into regions.

*   **`min_samples_leaf` / `mass_min`**: Minimum size of a leaf node (box).
    *   **High Value**: Forces broad segments (Higher Coverage).
    *   **Low Value**: Allows specific, granular segments (Higher Density).
*   **`max_depth`**: Complexity of the rules.
    *   **Low Depth**: Simple rules (e.g., just 1-2 parameters). Good for explainability and Coverage.
    *   **High Depth**: Complex, multi-parameter interaction rules. Good for Density.

---

## 3. Strategic Application

### Case A: Safety-Critical Systems (Prioritize Density)
*   **Goal**: Guarantee performance SLAs (e.g., Latency < 50ms).
*   **Strategy**: Set `threshold=0.95` or higher.
*   **Outcome**: You get a strict "Operating Envelope". It might be narrow (e.g., "Load must be < 500 RPS"), but you can trust it.

### Case B: Exploratory Analysis (Prioritize Coverage)
*   **Goal**: Understand the general drivers of performance.
*   **Strategy**: Set `threshold=0.6` or use CART with `max_depth=2`.
*   **Outcome**: You get broad rules (e.g., "Generally, having a Cache Size > 1GB is good"). This helps in early-stage design to pick the right direction.