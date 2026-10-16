# Findings — ADEPT compact FL combined-pattern analysis: CIFAR-10/CNN 16k — c8, 50% pattern stress by default

## Scope and evidence

- **Case:** ADEPT compact FL combined-pattern analysis: CIFAR-10/CNN 16k — c8, 50% pattern stress by default (combined-pattern); 60 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.003642. 42 training rows, 18 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-S: 2 (4.76%); S-M: 14 (33.33%); M-S: 3 (7.14%); M-M: 23 (54.76%).
- **Held-out tradeoff counts:** S-S: 1 (5.56%); S-M: 5 (27.78%); M-S: 1 (5.56%); M-M: 11 (61.11%).
- **Evidence:** [executed notebook](../analysis-fl-rq-combined-patterns-c8-stress-50-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__combined-patterns__clients-8__stress-50__environment-all.md); plots: [feature-importance__task-image__combined-patterns__clients-8__stress-50__environment-all.png](../plots/feature-importance__task-image__combined-patterns__clients-8__stress-50__environment-all.png); [quality-space__task-image__combined-patterns__clients-8__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__combined-patterns__clients-8__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

This is the c8/50% shared-setting view: compare only combinations with observed support. Allocation by complete configuration is below. The all-three combination is absent from this subset and has no outcome evidence; the observed alternatives do not form a complete factorial comparison.

```text
S-S       S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
policy
OFF,OFF,ON  0.000000  0.666667  0.0  0.000000  0.333333  0.0  0.0  0.0  0.0
OFF,ON,OFF  0.000000  0.000000  0.0  0.000000  1.000000  0.0  0.0  0.0  0.0
OFF,ON,ON   0.000000  0.666667  0.0  0.000000  0.333333  0.0  0.0  0.0  0.0
ON,OFF,OFF  0.000000  0.000000  0.0  0.333333  0.666667  0.0  0.0  0.0  0.0
ON,OFF,ON   0.333333  0.333333  0.0  0.000000  0.333333  0.0  0.0  0.0  0.0
ON,ON,OFF   0.000000  0.000000  0.0  0.000000  1.000000  0.0  0.0  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (11/18, 61.11%). The next largest is S-M (5 rows, 27.78%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `JSD Mean`, `Pattern Instances`, `CPU Mean`, `Pattern Types Active`, `Alpha Dirichlet Mean`. Scenario-discovery candidates are [`JSD Mean`, `Pattern Instances`, `CPU Mean`, `Pattern Types Active`, `Alpha Dirichlet Mean`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-combined-patterns-c8-stress-50-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target M-M** — held-out status: Evaluated; composite test score 0.7059, coverage 0.5455, target hits 6 / 11, retained/test 6 / 18. Conditions: - `JSD Mean`: (not selected) or <= 0.010; - `Pattern Instances`: [3.001, 9.000]; - **Includes NaN / not-selected values:** `JSD Mean`.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (7/14), ON (7/14)
  - HDH: OFF (14/14)
  - Message Compressor: ON (14/14)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (3/6), ON (3/6)
  - HDH: OFF (6/6)
  - Message Compressor: ON (6/6)
- **Operating envelope**:
  - JSD Mean [0.00825, 0.0104]
  - Pattern Instances [3, 9]
```
Held-out metrics: Runs retained by box: 6, Target runs inside box: 6, Target prevalence before box: 0.6111, Precision inside box: 1, Recall / target coverage: 0.5455, Absolute lift over held-out prevalence: 0.3889.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | M-M | CART Box 1 | Evaluated | 0.7059 | 0.5455 | 6 / 11 | 6 / 18 | 2 | — |
| 2 | M-M | PRIM Box 4 | Evaluated | 0.7059 | 0.5455 | 6 / 11 | 6 / 18 | 2 | — |
| 3 | S-M | PRIM Box 2 | Evaluated | 0.4590 | 0.4000 | 2 / 5 | 3 / 18 | 3 | — |
| 4 | M-S | PRIM Box 3 | Evaluated | 0.4545 | 1 | 1 / 1 | 3 / 18 | 2 | — |
| 5 | S-M | CART Box 2 | Evaluated | 0.3333 | 0.2000 | 1 / 5 | 1 / 18 | 3 | — |
| 6 | M-S | CART Box 4 | Evaluated | 0 | 0 | 0 / 1 | 1 / 18 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-combined-patterns-c8-stress-50-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__combined-patterns__clients-8__stress-50__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
