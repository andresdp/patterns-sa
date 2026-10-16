# Findings — ADEPT compact FL analysis: AG_NEWS/MLP, 8 clients

## Scope and evidence

- **Case:** ADEPT compact FL analysis: AG_NEWS/MLP, 8 clients (client-count configuration comparison); 390 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000034. 273 training rows, 117 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** M-S: 4 (1.47%); M-M: 1 (0.37%); L-S: 53 (19.41%); L-M: 215 (78.75%).
- **Held-out tradeoff counts:** M-S: 1 (0.85%); M-M: 1 (0.85%); L-S: 23 (19.66%); L-M: 92 (78.63%).
- **Evidence:** [executed notebook](../analysis-fl-rq-c8-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md); plots: [quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__all-configurations__clients-8__environment-all.png](../plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

All eight complete configurations are compared within this fixed client-count stratum. The rows below show the share of each policy group in each outcome region; marginal active-pattern counts combine multiple configurations and should not be read as policy effects.

```text
S-S  S-M  S-L       M-S       M-M  M-L       L-S       L-M  L-L
policy
OFF,OFF,OFF  0.0  0.0  0.0  0.000000  0.000000  0.0  0.166667  0.833333  0.0
OFF,OFF,ON   0.0  0.0  0.0  0.000000  0.000000  0.0  0.000000  1.000000  0.0
OFF,ON,OFF   0.0  0.0  0.0  0.000000  0.000000  0.0  0.142857  0.857143  0.0
OFF,ON,ON    0.0  0.0  0.0  0.000000  0.000000  0.0  0.200000  0.800000  0.0
ON,OFF,OFF   0.0  0.0  0.0  0.000000  0.000000  0.0  0.466667  0.533333  0.0
ON,OFF,ON    0.0  0.0  0.0  0.111111  0.111111  0.0  0.000000  0.777778  0.0
ON,ON,OFF    0.0  0.0  0.0  0.000000  0.000000  0.0  0.266667  0.733333  0.0
ON,ON,ON     0.0  0.0  0.0  0.000000  0.000000  0.0  0.333333  0.666667  0.0
```

In the held-out partition, **L-M** is the most common region (92/117, 78.63%). The next largest is L-S (23 rows, 19.66%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `delay_percentage`, `Alpha Dirichlet Mean`, `Client Selector Stress Percentage`, `HDH Stress Percentage`, `HDH Instances`. Scenario-discovery candidates are [`delay_percentage`, `Alpha Dirichlet Mean`, `Client Selector Stress Percentage`, `HDH Stress Percentage`, `HDH Instances`, `Pattern Instances`, `Pattern Types Active`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-c8-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 0.9176, coverage 0.8478, target hits 78 / 92, retained/test 78 / 117. Conditions: - `Client Selector Stress Percentage`: (not selected) or <= 37.500; - `delay_percentage`: [12.500, 100.000]; - **Includes NaN / not-selected values:** `Client Selector Stress Percentage`.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (140/182), ON (42/182)
  - HDH: OFF (98/182), ON (84/182)
  - Message Compressor: OFF (84/182), ON (98/182)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (60/78), ON (18/78)
  - HDH: OFF (42/78), ON (36/78)
  - Message Compressor: OFF (36/78), ON (42/78)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 37.5] (%)
  - delay percentage [12.5, 100] (%)
```
Held-out metrics: Runs retained by box: 78, Target runs inside box: 78, Target prevalence before box: 0.7863, Precision inside box: 1, Recall / target coverage: 0.8478, Absolute lift over held-out prevalence: 0.2137.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-M | CART Box 1 | Evaluated | 0.9176 | 0.8478 | 78 / 92 | 78 / 117 | 2 | Near duplicate of PRIM Box 4 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | L-M | PRIM Box 4 | Evaluated | 0.9176 | 0.8478 | 78 / 92 | 78 / 117 | 2 | Representative for CART Box 1 |
| 3 | L-S | CART Box 2 | Evaluated | 0.7895 | 0.6522 | 15 / 23 | 15 / 117 | 1 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 4 | L-S | PRIM Box 3 | Evaluated | 0.7895 | 0.6522 | 15 / 23 | 15 / 117 | 1 | Representative for CART Box 2 |
| 5 | M-S | PRIM Box 1 | Evaluated | 0.2386 | 1 | 1 / 1 | 7 / 117 | 3 | — |
| 6 | M-M | PRIM Box 2 | Evaluated | 0 | 0 | 0 / 1 | 6 / 117 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-c8-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
