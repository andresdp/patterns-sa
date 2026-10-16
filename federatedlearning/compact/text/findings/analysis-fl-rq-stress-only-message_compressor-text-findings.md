# Findings — ADEPT compact FL Message Compressor stress-only analysis: AG_NEWS/MLP, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL Message Compressor stress-only analysis: AG_NEWS/MLP, all client counts (stress-only); 210 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000000. 147 training rows, 63 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** L-S: 21 (14.29%); L-M: 126 (85.71%).
- **Held-out tradeoff counts:** L-S: 9 (14.29%); L-M: 54 (85.71%).
- **Evidence:** [executed notebook](../analysis-fl-rq-stress-only-message_compressor-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__stress-ONLY-message_compressor__clients-all__environment-all.md); plots: [quality-space__task-text__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__stress-ONLY-message_compressor__clients-all__environment-all.png](../plots/feature-importance__task-text__stress-ONLY-message_compressor__clients-all__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

The notebook varies only the focal pattern stress while holding the other two pattern decisions OFF and pooling client counts. Its stress-level means, region counts and within-level shares are reported below; the percentages alias paired environment percentages, so observed differences are not isolated pattern effects.

```text
runs  final_val_accuracy (mean)  \
Message Compressor Stress Percentage
0.0                                     30                      0.906
25.0                                    30                      0.906
50.0                                    30                      0.906
75.0                                    90                      0.889
100.0                                   30                      0.906

                                      avg_total_time (mean)
Message Compressor Stress Percentage
0.0                                                   4.498
25.0                                                 12.076
50.0                                                 13.005
75.0                                                 13.611
100.0                                                13.750
```

```text
tradeoff                              L-M  L-S
Message Compressor Stress Percentage
0                                       0   30
25                                     30    0
50                                     30    0
75                                     90    0
100                                    30    0
```

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S  \
policy
Message Compressor Stress Percentage=0    0.0  0.0  0.0  0.0  0.0  0.0  1.0
Message Compressor Stress Percentage=25   0.0  0.0  0.0  0.0  0.0  0.0  0.0
Message Compressor Stress Percentage=50   0.0  0.0  0.0  0.0  0.0  0.0  0.0
Message Compressor Stress Percentage=75   0.0  0.0  0.0  0.0  0.0  0.0  0.0
Message Compressor Stress Percentage=100  0.0  0.0  0.0  0.0  0.0  0.0  0.0

                                          L-M  L-L
policy
Message Compressor Stress Percentage=0    0.0  0.0
Message Compressor Stress Percentage=25   1.0  0.0
Message Compressor Stress Percentage=50   1.0  0.0
Message Compressor Stress Percentage=75   1.0  0.0
Message Compressor Stress Percentage=100  1.0  0.0
```

In the held-out partition, **L-M** is the most common region (54/63, 85.71%). The next largest is L-S (9 rows, 14.29%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Message Compressor Stress Percentage`, `Alpha Dirichlet Mean`, `non_iid_percentage`, `Message Compressor Instances`, `CPU Mean`. Scenario-discovery candidates are [`Message Compressor Stress Percentage`, `Alpha Dirichlet Mean`, `non_iid_percentage`, `Message Compressor Instances`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-stress-only-message_compressor-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 1, coverage 1, target hits 54 / 54, retained/test 54 / 63. Conditions: - `Message Compressor Stress Percentage`: [12.485, 100.000]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (126/126)
  - HDH: OFF (126/126)
  - Message Compressor: ON (126/126)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: OFF (54/54)
  - Message Compressor: ON (54/54)
- **Operating envelope**:
  - Message Compressor Stress Percentage [12.5, 100] (%)
```
Held-out metrics: Runs retained by box: 54, Target runs inside box: 54, Target prevalence before box: 0.8571, Precision inside box: 1, Recall / target coverage: 1, Absolute lift over held-out prevalence: 0.1429.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-M | CART Box 1 | Evaluated | 1 | 1 | 54 / 54 | 54 / 63 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | L-M | PRIM Box 2 | Evaluated | 1 | 1 | 54 / 54 | 54 / 63 | 1 | Representative for CART Box 1 |
| 3 | L-S | CART Box 2 | Evaluated | 1 | 1 | 9 / 9 | 9 / 63 | 1 | — |
| 4 | L-S | PRIM Box 1 | Evaluated | 1 | 1 | 9 / 9 | 9 / 63 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-stress-only-message_compressor-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__stress-ONLY-message_compressor__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
