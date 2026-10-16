# Findings — ADEPT compact FL combined-pattern analysis: AG_NEWS/MLP — c8, 50% pattern stress by default

## Scope and evidence

- **Case:** ADEPT compact FL combined-pattern analysis: AG_NEWS/MLP — c8, 50% pattern stress by default (combined-pattern); 60 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.001173. 42 training rows, 18 held-out rows; fallback. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** M-S: 1 (2.38%); M-M: 1 (2.38%); L-S: 4 (9.52%); L-M: 36 (85.71%).
- **Held-out tradeoff counts:** M-S: 0 (0.00%); M-M: 0 (0.00%); L-S: 2 (11.11%); L-M: 16 (88.89%).
- **Evidence:** [executed notebook](../analysis-fl-rq-combined-patterns-c8-stress-50-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__combined-patterns__clients-8__stress-50__environment-all.md); plots: [feature-importance__task-text__combined-patterns__clients-8__stress-50__environment-all.png](../plots/feature-importance__task-text__combined-patterns__clients-8__stress-50__environment-all.png); [quality-space__task-text__combined-patterns__clients-8__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__combined-patterns__clients-8__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

This is the c8/50% shared-setting view: compare only combinations with observed support. Allocation by complete configuration is below. The all-three combination is absent from this subset and has no outcome evidence; the observed alternatives do not form a complete factorial comparison.

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
policy
OFF,OFF,ON  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  1.000000  0.0
OFF,ON,OFF  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  1.000000  0.0
OFF,ON,ON   0.0  0.0  0.0  0.0  0.0  0.0  0.000000  1.000000  0.0
ON,OFF,OFF  0.0  0.0  0.0  0.0  0.0  0.0  0.333333  0.666667  0.0
ON,OFF,ON   0.0  0.0  0.0  0.0  0.0  0.0  0.333333  0.666667  0.0
ON,ON,OFF   0.0  0.0  0.0  0.0  0.0  0.0  0.000000  1.000000  0.0
```

In the held-out partition, **L-M** is the most common region (16/18, 88.89%). The next largest is L-S (2 rows, 11.11%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `Pattern Instances`, `JSD Mean`, `CPU Mean`, `HDH Instances`, `Pattern Types Active`. Scenario-discovery candidates are [`Pattern Instances`, `JSD Mean`, `CPU Mean`, `HDH Instances`, `Pattern Types Active`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-combined-patterns-c8-stress-50-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 0.8966, coverage 0.8125, target hits 13 / 16, retained/test 13 / 18. Conditions: - `Pattern Instances`: [3.500, 12.000]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (21/31), ON (10/31)
  - HDH: OFF (14/31), ON (17/31)
  - Message Compressor: OFF (10/31), ON (21/31)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (9/13), ON (4/13)
  - HDH: OFF (6/13), ON (7/13)
  - Message Compressor: OFF (4/13), ON (9/13)
- **Operating envelope**:
  - Pattern Instances [3.5, 12]
```
Held-out metrics: Runs retained by box: 13, Target runs inside box: 13, Target prevalence before box: 0.8889, Precision inside box: 1, Recall / target coverage: 0.8125, Absolute lift over held-out prevalence: 0.1111.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-M | CART Box 1 | Evaluated | 0.8966 | 0.8125 | 13 / 16 | 13 / 18 | 1 | — |
| 2 | L-M | PRIM Box 4 | Evaluated | 0.8966 | 0.8125 | 13 / 16 | 13 / 18 | 2 | — |
| 3 | L-S | PRIM Box 3 | Evaluated | 0.3333 | 0.5000 | 1 / 2 | 3 / 18 | 2 | — |
| 4 | L-S | CART Box 2 | Evaluated: no held-out rows selected | 0 | 0 | 0 / 2 | 0 / 18 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-combined-patterns-c8-stress-50-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__combined-patterns__clients-8__stress-50__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
