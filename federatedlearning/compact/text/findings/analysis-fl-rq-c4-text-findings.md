# Findings — ADEPT compact FL analysis: AG_NEWS/MLP, 4 clients

## Scope and evidence

- **Case:** ADEPT compact FL analysis: AG_NEWS/MLP, 4 clients (client-count configuration comparison); 390 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000257. 273 training rows, 117 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** M-S: 3 (1.10%); M-M: 5 (1.83%); L-S: 69 (25.27%); L-M: 184 (67.40%); L-L: 12 (4.40%).
- **Held-out tradeoff counts:** M-S: 2 (1.71%); M-M: 0 (0.00%); L-S: 31 (26.50%); L-M: 79 (67.52%); L-L: 5 (4.27%).
- **Evidence:** [executed notebook](../analysis-fl-rq-c4-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__all-configurations__clients-4__environment-all.md); plots: [quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__all-configurations__clients-4__environment-all.png](../plots/feature-importance__task-text__all-configurations__clients-4__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

All eight complete configurations are compared within this fixed client-count stratum. The rows below show the share of each policy group in each outcome region; marginal active-pattern counts combine multiple configurations and should not be read as policy effects.

```text
S-S  S-M  S-L       M-S  M-M  M-L       L-S       L-M       L-L
policy
OFF,OFF,OFF  0.0  0.0  0.0  0.000000  0.0  0.0  0.166667  0.833333  0.000000
OFF,OFF,ON   0.0  0.0  0.0  0.000000  0.0  0.0  0.000000  0.866667  0.133333
OFF,ON,OFF   0.0  0.0  0.0  0.000000  0.0  0.0  0.142857  0.857143  0.000000
OFF,ON,ON    0.0  0.0  0.0  0.000000  0.0  0.0  0.200000  0.600000  0.200000
ON,OFF,OFF   0.0  0.0  0.0  0.066667  0.0  0.0  0.533333  0.400000  0.000000
ON,OFF,ON    0.0  0.0  0.0  0.111111  0.0  0.0  0.555556  0.333333  0.000000
ON,ON,OFF    0.0  0.0  0.0  0.000000  0.0  0.0  0.333333  0.666667  0.000000
ON,ON,ON     0.0  0.0  0.0  0.000000  0.0  0.0  0.444444  0.555556  0.000000
```

In the held-out partition, **L-M** is the most common region (79/117, 67.52%). The next largest is L-S (31 rows, 26.50%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Alpha Dirichlet Mean`, `Client Selector Stress Percentage`, `delay_percentage`, `HDH Instances`, `Pattern Instances`. Scenario-discovery candidates are [`Alpha Dirichlet Mean`, `Client Selector Stress Percentage`, `delay_percentage`, `HDH Instances`, `Pattern Instances`, `HDH Stress Percentage`, `Message Compressor Stress Percentage`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-c4-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 0.7258, coverage 0.5696, target hits 45 / 79, retained/test 45 / 117. Conditions: - `Client Selector Stress Percentage`: (not selected) or <= 22.497; - `delay_percentage`: [12.500, 100.000]; - `Pattern Instances`: [0.000, 5.499]; - `HDH Stress Percentage`: (not selected) or <= 62.498; - **Includes NaN / not-selected values:** `Client Selector Stress Percentage`, `HDH Stress Percentage`.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (77/105), ON (28/105)
  - Message Compressor: OFF (49/105), ON (56/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (33/45), ON (12/45)
  - Message Compressor: OFF (21/45), ON (24/45)
- **Operating envelope**:
  - Client Selector Stress Percentage [20, 22.5] (%)
  - delay percentage [12.5, 100] (%)
  - Pattern Instances [0, 5.5]
  - HDH Stress Percentage [20, 62.5] (%)
```
Held-out metrics: Runs retained by box: 45, Target runs inside box: 45, Target prevalence before box: 0.6752, Precision inside box: 1, Recall / target coverage: 0.5696, Absolute lift over held-out prevalence: 0.3248.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-M | CART Box 1 | Evaluated | 0.7258 | 0.5696 | 45 / 79 | 45 / 117 | 4 | — |
| 2 | L-M | PRIM Box 4 | Evaluated | 0.7258 | 0.5696 | 45 / 79 | 45 / 117 | 4 | — |
| 3 | L-S | CART Box 2 | Evaluated | 0.6522 | 0.4839 | 15 / 31 | 15 / 117 | 1 | — |
| 4 | L-L | PRIM Box 5 | Evaluated | 0.5618 | 1 | 5 / 5 | 12 / 117 | 3 | — |
| 5 | L-L | CART Box 3 | Evaluated | 0.4958 | 0.4000 | 2 / 5 | 3 / 117 | 4 | — |
| 6 | M-S | PRIM Box 1 | Evaluated | 0.3453 | 1 | 2 / 2 | 9 / 117 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-c4-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__all-configurations__clients-4__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
