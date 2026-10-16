# Findings — ADEPT compact FL baseline analysis: AG_NEWS/MLP, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL baseline analysis: AG_NEWS/MLP, all client counts (baseline profile); 180 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000000. 126 training rows, 54 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** L-S: 21 (16.67%); L-M: 105 (83.33%).
- **Held-out tradeoff counts:** L-S: 9 (16.67%); L-M: 45 (83.33%).
- **Evidence:** [executed notebook](../analysis-fl-rq-baseline-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md); plots: [quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png).

## RQ1 — Observed tradeoffs and design alternatives

This exact configuration is profiled across client counts and all available environments. No competing policy is present inside this notebook, so comparisons are descriptive operating-profile evidence, not a pattern effect. Its observed region allocation is below.

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
policy
OFF,OFF,OFF  0.0  0.0  0.0  0.0  0.0  0.0  0.166667  0.833333  0.0
```

In the held-out partition, **L-M** is the most common region (45/54, 83.33%). The next largest is L-S (9 rows, 16.67%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `delay_percentage`, `non_iid_percentage`, `Total Clients`, `low_spec_percentage`, `CPU Mean`. Scenario-discovery candidates are [`delay_percentage`, `non_iid_percentage`, `Total Clients`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-baseline-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 1, coverage 1, target hits 45 / 45, retained/test 45 / 54. Conditions: - `delay_percentage`: [12.488, 100.000]; - **Includes NaN / not-selected values:** No.

Architectural reading (joint rule):

```text
- **Design prescription**:
  - No pattern policy is required by the box conditions
- **Observed pattern activation — training partition (rows matching this box)**:
  - Client Selector: OFF (105/105)
  - HDH: OFF (105/105)
  - Message Compressor: OFF (105/105)
- **Observed pattern activation — held-out partition (rows matching this box)**:
  - Client Selector: OFF (45/45)
  - HDH: OFF (45/45)
  - Message Compressor: OFF (45/45)
- **Operating envelope**:
  - delay percentage [12.5, 100] (%)
```
Held-out metrics: Runs retained by box: 45, Target runs inside box: 45, Target prevalence before box: 0.8333, Precision inside box: 1, Recall / target coverage: 1, Absolute lift over held-out prevalence: 0.1667.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-M | CART Box 1 | Evaluated | 1 | 1 | 45 / 45 | 45 / 54 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | L-M | PRIM Box 2 | Evaluated | 1 | 1 | 45 / 45 | 45 / 54 | 1 | Representative for CART Box 1 |
| 3 | L-S | CART Box 2 | Evaluated | 1 | 1 | 9 / 9 | 9 / 54 | 1 | — |
| 4 | L-S | PRIM Box 1 | Evaluated | 1 | 1 | 9 / 9 | 9 / 54 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-baseline-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
