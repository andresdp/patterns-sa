# Findings — ADEPT compact FL Client Selector-only analysis: AG_NEWS/MLP, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL Client Selector-only analysis: AG_NEWS/MLP, all client counts (single-pattern profile); 150 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000277. 105 training rows, 45 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** M-S: 3 (2.86%); L-S: 48 (45.71%); L-M: 54 (51.43%).
- **Held-out tradeoff counts:** M-S: 1 (2.22%); L-S: 20 (44.44%); L-M: 24 (53.33%).
- **Evidence:** [executed notebook](../analysis-fl-rq-client_selector-text.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md); plots: [feature-importance__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png](../plots/feature-importance__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png); [quality-space__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

This exact configuration is profiled across client counts and all available environments. No competing policy is present inside this notebook, so comparisons are descriptive operating-profile evidence, not a pattern effect. Its observed region allocation is below.

```text
S-S  S-M  S-L       M-S  M-M  M-L       L-S       L-M  L-L
policy
ON,OFF,OFF  0.0  0.0  0.0  0.022222  0.0  0.0  0.444444  0.533333  0.0
```

In the held-out partition, **L-M** is the most common region (24/45, 53.33%). The next largest is L-S (20 rows, 44.44%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `low_spec_percentage`, `non_iid_percentage`, `Alpha Dirichlet Mean`, `CPU Mean`, `Total Clients`. Scenario-discovery candidates are [`low_spec_percentage`, `non_iid_percentage`, `Alpha Dirichlet Mean`, `CPU Mean`, `Total Clients`, `delay_percentage`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-client_selector-text.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

**CART Box 1, target L-M** — held-out status: Evaluated; composite test score 0.4000, coverage 0.2500, target hits 6 / 24, retained/test 6 / 45. Conditions: - `CPU Mean`: [10.125, 11.000]; - `Total Clients`: [5.999, 10.000]; - **Includes NaN / not-selected values:** No.

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
Held-out metrics: Runs retained by box: 6, Target runs inside box: 6, Target prevalence before box: 0.5333, Precision inside box: 1, Recall / target coverage: 0.2500, Absolute lift over held-out prevalence: 0.4667.


The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | L-S | PRIM Box 2 | Evaluated | 0.4421 | 0.3500 | 7 / 20 | 9 / 45 | 3 | — |
| 2 | L-M | CART Box 1 | Evaluated | 0.4000 | 0.2500 | 6 / 24 | 6 / 45 | 2 | — |
| 3 | L-M | PRIM Box 3 | Evaluated | 0.4000 | 0.2500 | 6 / 24 | 6 / 45 | 2 | — |
| 4 | L-S | CART Box 2 | Evaluated | 0 | 0.0500 | 1 / 20 | 3 / 45 | 4 | — |
| 5 | M-S | PRIM Box 1 | Evaluated | 0 | 0 | 0 / 1 | 3 / 45 | 2 | — |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-client_selector-text.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
