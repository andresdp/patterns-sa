# Findings — ADEPT compact FL analysis: CIFAR-10/CNN 16k, 10 clients

## Scope and evidence

- **Case:** ADEPT compact FL analysis: CIFAR-10/CNN 16k, 10 clients (client-count configuration comparison); 390 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000028. 273 training rows, 117 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-S: 13 (4.76%); S-M: 76 (27.84%); M-S: 38 (13.92%); M-M: 146 (53.48%).
- **Held-out tradeoff counts:** S-S: 6 (5.13%); S-M: 33 (28.21%); M-S: 16 (13.68%); M-M: 62 (52.99%).
- **Evidence:** [executed notebook](../analysis-fl-rq-c10-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md); plots: [feature-importance__task-image__all-configurations__clients-10__environment-all.png](../plots/feature-importance__task-image__all-configurations__clients-10__environment-all.png); [quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

All eight complete configurations are compared within this fixed client-count stratum. The rows below show the share of each policy group in each outcome region; marginal active-pattern counts combine multiple configurations and should not be read as policy effects.

```text
S-S       S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
policy
OFF,OFF,OFF  0.000000  0.333333  0.0  0.166667  0.500000  0.0  0.0  0.0  0.0
OFF,OFF,ON   0.000000  0.800000  0.0  0.000000  0.200000  0.0  0.0  0.0  0.0
OFF,ON,OFF   0.000000  0.142857  0.0  0.142857  0.714286  0.0  0.0  0.0  0.0
OFF,ON,ON    0.000000  0.400000  0.0  0.200000  0.400000  0.0  0.0  0.0  0.0
ON,OFF,OFF   0.133333  0.200000  0.0  0.066667  0.600000  0.0  0.0  0.0  0.0
ON,OFF,ON    0.444444  0.222222  0.0  0.000000  0.333333  0.0  0.0  0.0  0.0
ON,ON,OFF    0.000000  0.066667  0.0  0.200000  0.733333  0.0  0.0  0.0  0.0
ON,ON,ON     0.000000  0.000000  0.0  0.333333  0.666667  0.0  0.0  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (62/117, 52.99%). The next largest is S-M (33 rows, 28.21%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Alpha Dirichlet Mean`, `delay_percentage`, `Client Selector Stress Percentage`, `JSD Mean`, `Pattern Types Active`. Scenario-discovery candidates are [`Alpha Dirichlet Mean`, `delay_percentage`, `Client Selector Stress Percentage`, `JSD Mean`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-c10-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

No non-empty, scoreable box is documented for this case; consult the report for unvalidated/empty target outcomes.

The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | M-S | CART Box 3 | Evaluated | 0.9677 | 0.9375 | 15 / 16 | 15 / 117 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | M-S | PRIM Box 3 | Evaluated | 0.9677 | 0.9375 | 15 / 16 | 15 / 117 | 2 | Representative for CART Box 3 |
| 3 | M-M | CART Box 1 | Evaluated | 0.9027 | 0.8226 | 51 / 62 | 51 / 117 | 3 | — |
| 4 | M-M | PRIM Box 4 | Evaluated | 0.9027 | 0.8226 | 51 / 62 | 51 / 117 | 4 | — |
| 5 | S-M | CART Box 2 | Evaluated | 0.9000 | 0.8182 | 27 / 33 | 27 / 117 | 2 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 6 | S-M | PRIM Box 2 | Evaluated | 0.9000 | 0.8182 | 27 / 33 | 27 / 117 | 2 | Representative for CART Box 2 |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-c10-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
