# Findings — ADEPT compact FL HDH-only analysis: CIFAR-10/CNN 16k, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL HDH-only analysis: CIFAR-10/CNN 16k, all client counts (single-pattern profile); 150 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000425. 105 training rows, 45 held-out rows; fallback. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-S: 2 (1.90%); S-M: 57 (54.29%); M-S: 1 (0.95%); M-M: 45 (42.86%).
- **Held-out tradeoff counts:** S-S: 0 (0.00%); S-M: 25 (55.56%); M-S: 0 (0.00%); M-M: 20 (44.44%).
- **Evidence:** [executed notebook](../analysis-fl-rq-hdh-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.md); plots: [quality-space__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.png](../plots/feature-importance__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

This exact configuration is profiled across client counts and all available environments. No competing policy is present inside this notebook, so comparisons are descriptive operating-profile evidence, not a pattern effect. Its observed region allocation is below.

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
policy
OFF,OFF,ON  0.0  0.555556  0.0  0.0  0.444444  0.0  0.0  0.0  0.0
```

In the held-out partition, **S-M** is the most common region (25/45, 55.56%). The next largest is M-M (20 rows, 44.44%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `JSD Mean`, `delay_percentage`, `Total Clients`, `Alpha Dirichlet Mean`, `HDH Instances`. Scenario-discovery candidates are [`JSD Mean`, `delay_percentage`, `Total Clients`, `Alpha Dirichlet Mean`, `HDH Instances`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-hdh-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target S-M** — held-out status: Evaluated; composite test score 0.8188, coverage 0.7600, target hits 19 / 25, retained/test 20 / 45. Conditions: - `Total Clients`: [5.999, 10.000]; - `JSD Mean`: [0.018, 0.081]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (54/54)
  - HDH: ON (54/54)
  - Message Compressor: OFF (54/54)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (20/20)
  - HDH: ON (20/20)
  - Message Compressor: OFF (20/20)
- **Operating envelope**:
  - JSD Mean [0.0181, 0.081]
- **Other design conditions**:
  - Total Clients [6, 10]
```
Held-out metrics: Runs retained by box: 20, Target runs inside box: 19, Target prevalence before box: 0.5556, Precision inside box: 0.9500, Recall / target coverage: 0.7600, Absolute lift over held-out prevalence: 0.3944.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | S-M | CART Box 1 | Evaluated | 0.8188 | 0.7600 | 19 / 25 | 20 / 45 | 2 | — |
| 2 | S-M | PRIM Box 2 | Evaluated | 0.8188 | 0.7600 | 19 / 25 | 20 / 45 | 3 | — |
| 3 | M-M | CART Box 2 | Evaluated | 0.5714 | 0.4000 | 8 / 20 | 8 / 45 | 1 | — |
| 4 | M-M | PRIM Box 4 | Evaluated | 0.1600 | 0.1000 | 2 / 20 | 3 / 45 | 4 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-hdh-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
