# Findings — ADEPT compact FL Client Selector stress-only analysis: CIFAR-10/CNN 16k, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL Client Selector stress-only analysis: CIFAR-10/CNN 16k, all client counts (stress-only); 150 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000267. 105 training rows, 45 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-S: 13 (12.38%); S-M: 15 (14.29%); M-S: 25 (23.81%); M-M: 52 (49.52%).
- **Held-out tradeoff counts:** S-S: 5 (11.11%); S-M: 6 (13.33%); M-S: 11 (24.44%); M-M: 23 (51.11%).
- **Evidence:** [executed notebook](../analysis-fl-rq-stress-only-client_selector-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__stress-ONLY-client_selector__clients-all__environment-all.md); plots: [quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-image__stress-ONLY-client_selector__clients-all__environment-all.png](../plots/feature-importance__task-image__stress-ONLY-client_selector__clients-all__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

The notebook varies only the focal pattern stress while holding the other two pattern decisions OFF and pooling client counts. Its stress-level means, region counts and within-level shares are reported below; the percentages alias paired environment percentages, so observed differences are not isolated pattern effects.

```text
runs  final_val_accuracy (mean)  \
Client Selector Stress Percentage
25.0                                 30                      0.535
50.0                                 30                      0.529
75.0                                 90                      0.480

                                   avg_total_time (mean)
Client Selector Stress Percentage
25.0                                              11.188
50.0                                               9.250
75.0                                               7.844
```

```text
tradeoff                           M-M  M-S  S-M  S-S
Client Selector Stress Percentage
25                                  27    3    0    0
50                                  20    9    1    0
75                                  28   24   20   18
```

```text
S-S    S-M  S-L    M-S    M-M  M-L  L-S  \
policy
Client Selector Stress Percentage=25  0.0  0.000  0.0  0.100  0.900  0.0  0.0
Client Selector Stress Percentage=50  0.0  0.033  0.0  0.300  0.667  0.0  0.0
Client Selector Stress Percentage=75  0.2  0.222  0.0  0.267  0.311  0.0  0.0

                                      L-M  L-L
policy
Client Selector Stress Percentage=25  0.0  0.0
Client Selector Stress Percentage=50  0.0  0.0
Client Selector Stress Percentage=75  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (23/45, 51.11%). The next largest is M-S (11 rows, 24.44%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `CPU Mean`, `Alpha Dirichlet Mean`, `Total Clients`, `delay_percentage`, `non_iid_percentage`. Scenario-discovery candidates are [`CPU Mean`, `Alpha Dirichlet Mean`, `Total Clients`, `delay_percentage`, `non_iid_percentage`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-stress-only-client_selector-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target M-M** — held-out status: Evaluated; composite test score 0.4138, coverage 0.2609, target hits 6 / 23, retained/test 6 / 45. Conditions: - `Total Clients`: [5.999, 10.000]; - `CPU Mean`: [10.125, 11.000]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: ON (14/14)
  - HDH: OFF (14/14)
  - Message Compressor: OFF (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: ON (6/6)
  - HDH: OFF (6/6)
  - Message Compressor: OFF (6/6)
- **Operating envelope**:
  - CPU Mean [10.1, 11]
- **Other design conditions**:
  - Total Clients [6, 10]
```
Held-out metrics: Runs retained by box: 6, Target runs inside box: 6, Target prevalence before box: 0.5111, Precision inside box: 1, Recall / target coverage: 0.2609, Absolute lift over held-out prevalence: 0.4889.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | S-M | PRIM Box 2 | Evaluated | 0.4583 | 0.5000 | 3 / 6 | 6 / 45 | 2 | — |
| 2 | M-M | CART Box 1 | Evaluated | 0.4138 | 0.2609 | 6 / 23 | 6 / 45 | 2 | — |
| 3 | M-M | PRIM Box 4 | Evaluated | 0.4138 | 0.2609 | 6 / 23 | 6 / 45 | 3 | — |
| 4 | M-S | PRIM Box 3 | Evaluated | 0.2744 | 0.1818 | 2 / 11 | 3 / 45 | 4 | — |
| 5 | S-S | PRIM Box 1 | Evaluated | 0.2222 | 0.2000 | 1 / 5 | 3 / 45 | 2 | — |
| 6 | S-S | CART Box 4 | Evaluated | 0.2222 | 0.2000 | 1 / 5 | 3 / 45 | 4 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-stress-only-client_selector-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__stress-ONLY-client_selector__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
