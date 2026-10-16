# Findings — ADEPT compact FL analysis: CIFAR-10/CNN 16k, 4 clients

## Scope and evidence

- **Case:** ADEPT compact FL analysis: CIFAR-10/CNN 16k, 4 clients (client-count configuration comparison); 390 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000088. 273 training rows, 117 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-S: 8 (2.93%); S-M: 10 (3.66%); M-S: 68 (24.91%); M-M: 187 (68.50%).
- **Held-out tradeoff counts:** S-S: 4 (3.42%); S-M: 4 (3.42%); M-S: 30 (25.64%); M-M: 79 (67.52%).
- **Evidence:** [executed notebook](../analysis-fl-rq-c4-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__all-configurations__clients-4__environment-all.md); plots: [feature-importance__task-image__all-configurations__clients-4__environment-all.png](../plots/feature-importance__task-image__all-configurations__clients-4__environment-all.png); [quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

All eight complete configurations are compared within this fixed client-count stratum. The rows below show the share of each policy group in each outcome region; marginal active-pattern counts combine multiple configurations and should not be read as policy effects.

```text
S-S       S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
policy
OFF,OFF,OFF  0.000000  0.055556  0.0  0.166667  0.777778  0.0  0.0  0.0  0.0
OFF,OFF,ON   0.000000  0.066667  0.0  0.000000  0.933333  0.0  0.0  0.0  0.0
OFF,ON,OFF   0.000000  0.047619  0.0  0.142857  0.809524  0.0  0.0  0.0  0.0
OFF,ON,ON    0.000000  0.066667  0.0  0.200000  0.733333  0.0  0.0  0.0  0.0
ON,OFF,OFF   0.133333  0.000000  0.0  0.533333  0.333333  0.0  0.0  0.0  0.0
ON,OFF,ON    0.222222  0.000000  0.0  0.444444  0.333333  0.0  0.0  0.0  0.0
ON,ON,OFF    0.000000  0.000000  0.0  0.333333  0.666667  0.0  0.0  0.0  0.0
ON,ON,ON     0.000000  0.000000  0.0  0.444444  0.555556  0.0  0.0  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (79/117, 67.52%). The next largest is M-S (30 rows, 25.64%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Alpha Dirichlet Mean`, `delay_percentage`, `Client Selector Stress Percentage`, `JSD Mean`, `CPU Mean`. Scenario-discovery candidates are [`Alpha Dirichlet Mean`, `delay_percentage`, `Client Selector Stress Percentage`, `JSD Mean`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-c4-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**PRIM Box 1, target S-S** — held-out status: Evaluated; composite test score 0.7914, coverage 1, target hits 4 / 4, retained/test 6 / 117. Conditions: - `Alpha Dirichlet Mean`: [0.625, 0.688]; - `Client Selector Stress Percentage`: [35.000, 75.000]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (7/14), ON (7/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (3/6), ON (3/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - Alpha Dirichlet Mean [0.625, 0.688]
  - Client Selector Stress Percentage [35, 75] (%)
```
Held-out metrics: Runs retained by box: 6, Target runs inside box: 4, Target prevalence before box: 0.0342, Precision inside box: 0.6667, Recall / target coverage: 1, Absolute lift over held-out prevalence: 0.6325.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | S-S | PRIM Box 1 | Evaluated | 0.7914 | 1 | 4 / 4 | 6 / 117 | 2 | — |
| 2 | M-S | CART Box 2 | Evaluated | 0.6667 | 0.5000 | 15 / 30 | 15 / 117 | 1 | — |
| 3 | M-S | PRIM Box 3 | Evaluated | 0.6667 | 0.5000 | 15 / 30 | 15 / 117 | 2 | — |
| 4 | M-M | CART Box 1 | Evaluated | 0.4660 | 0.3038 | 24 / 79 | 24 / 117 | 4 | — |
| 5 | M-M | PRIM Box 4 | Evaluated | 0.4356 | 0.2785 | 22 / 79 | 22 / 117 | 4 | — |
| 6 | S-M | PRIM Box 2 | Evaluated | 0.2767 | 0.2500 | 1 / 4 | 3 / 117 | 4 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-c4-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__all-configurations__clients-4__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
