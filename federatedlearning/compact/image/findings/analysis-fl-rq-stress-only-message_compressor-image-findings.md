# Findings — ADEPT compact FL Message Compressor stress-only analysis: CIFAR-10/CNN 16k, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL Message Compressor stress-only analysis: CIFAR-10/CNN 16k, all client counts (stress-only); 210 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000081. 147 training rows, 63 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-M: 15 (10.20%); M-S: 21 (14.29%); M-M: 111 (75.51%).
- **Held-out tradeoff counts:** S-M: 7 (11.11%); M-S: 9 (14.29%); M-M: 47 (74.60%).
- **Evidence:** [executed notebook](../analysis-fl-rq-stress-only-message_compressor-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__stress-ONLY-message_compressor__clients-all__environment-all.md); plots: [quality-space__task-image__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-image__stress-ONLY-message_compressor__clients-all__environment-all.png](../plots/feature-importance__task-image__stress-ONLY-message_compressor__clients-all__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

The notebook varies only the focal pattern stress while holding the other two pattern decisions OFF and pooling client counts. Its stress-level means, region counts and within-level shares are reported below; the percentages alias paired environment percentages, so observed differences are not isolated pattern effects.

```text
runs  final_val_accuracy (mean)  \
Message Compressor Stress Percentage
0.0                                     30                      0.541
25.0                                    30                      0.538
50.0                                    30                      0.539
75.0                                    90                      0.507
100.0                                   30                      0.542

                                      avg_total_time (mean)
Message Compressor Stress Percentage
0.0                                                   4.490
25.0                                                 12.292
50.0                                                 13.215
75.0                                                 13.543
100.0                                                13.828
```

```text
tradeoff                              M-M  M-S  S-M
Message Compressor Stress Percentage
0                                       0   30    0
25                                     30    0    0
50                                     30    0    0
75                                     68    0   22
100                                    30    0    0
```

```text
S-S    S-M  S-L  M-S    M-M  M-L  \
policy
Message Compressor Stress Percentage=0    0.0  0.000  0.0  1.0  0.000  0.0
Message Compressor Stress Percentage=25   0.0  0.000  0.0  0.0  1.000  0.0
Message Compressor Stress Percentage=50   0.0  0.000  0.0  0.0  1.000  0.0
Message Compressor Stress Percentage=75   0.0  0.244  0.0  0.0  0.756  0.0
Message Compressor Stress Percentage=100  0.0  0.000  0.0  0.0  1.000  0.0

                                          L-S  L-M  L-L
policy
Message Compressor Stress Percentage=0    0.0  0.0  0.0
Message Compressor Stress Percentage=25   0.0  0.0  0.0
Message Compressor Stress Percentage=50   0.0  0.0  0.0
Message Compressor Stress Percentage=75   0.0  0.0  0.0
Message Compressor Stress Percentage=100  0.0  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (47/63, 74.60%). The next largest is M-S (9 rows, 14.29%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Message Compressor Stress Percentage`, `Message Compressor Instances`, `Alpha Dirichlet Mean`, `non_iid_percentage`, `CPU Mean`. Scenario-discovery candidates are [`Message Compressor Stress Percentage`, `Message Compressor Instances`, `Alpha Dirichlet Mean`, `non_iid_percentage`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

No non-empty, scoreable box is documented for this case; consult the report for unvalidated/empty target outcomes.

The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | M-S | CART Box 2 | Evaluated | 1 | 1 | 9 / 9 | 9 / 63 | 1 | — |
| 2 | M-S | PRIM Box 2 | Evaluated | 1 | 1 | 9 / 9 | 9 / 63 | 2 | — |
| 3 | M-M | CART Box 1 | Evaluated | 0.9783 | 0.9574 | 45 / 47 | 45 / 63 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 4 | M-M | PRIM Box 3 | Evaluated | 0.9783 | 0.9574 | 45 / 47 | 45 / 63 | 2 | Representative for CART Box 1 |
| 5 | S-M | PRIM Box 1 | Evaluated | 0.9231 | 0.8571 | 6 / 7 | 6 / 63 | 2 | — |
| 6 | S-M | CART Box 3 | Evaluated | 0.9231 | 0.8571 | 6 / 7 | 6 / 63 | 3 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__stress-ONLY-message_compressor__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
