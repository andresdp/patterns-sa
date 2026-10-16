# Findings — ADEPT compact FL baseline analysis: CIFAR-10/CNN 16k, all client counts

## Scope and evidence

- **Case:** ADEPT compact FL baseline analysis: CIFAR-10/CNN 16k, all client counts (baseline profile); 180 of 2340 compact campaign rows retained; all-environment view.
- **Split:** Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000027. 126 training rows, 54 held-out rows; no rare-class fallback reported. Grouping by `partition_seed` keeps seed groups intact.
- **Training tradeoff counts:** S-M: 31 (24.60%); M-S: 21 (16.67%); M-M: 74 (58.73%).
- **Held-out tradeoff counts:** S-M: 13 (24.07%); M-S: 9 (16.67%); M-M: 32 (59.26%).
- **Evidence:** [executed notebook](../analysis-fl-rq-baseline-image.ipynb); [regenerated PRIM/CART report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md); plots: [feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../plots/feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png); [quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ1 — Observed tradeoffs and design alternatives

This exact configuration is profiled across client counts and all available environments. No competing policy is present inside this notebook, so comparisons are descriptive operating-profile evidence, not a pattern effect. Its observed region allocation is below.

```text
S-S       S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
policy
OFF,OFF,OFF  0.0  0.240741  0.0  0.166667  0.592593  0.0  0.0  0.0  0.0
```

In the held-out partition, **M-M** is the most common region (32/54, 59.26%). The next largest is S-M (13 rows, 24.07%).

The occupied regions and shares above describe this filtered run-level sample. Empty regions mean no observed runs in this scope, not infeasibility. In cases pooling client counts or environments, treat those dimensions as mixed context; in stress-only cases, the stress feature is tied to its paired environment percentage. The analysis is observational.

## RQ2 — Joint conditions, feature roles, and held-out what-if evidence

**Feature-ranking trend in this case.** The leading ADEPT weighted ranks are `delay_percentage`, `Alpha Dirichlet Mean`, `Total Clients`, `CPU Mean`. Scenario-discovery candidates are [`delay_percentage`, `Alpha Dirichlet Mean`, `Total Clients`]. These are model-relative predictive credits, not directions or effects. See [Section 8](../analysis-fl-rq-baseline-image.ipynb#8-Feature-Importance--Key-Parameter-Selection).

**Highest-ranked architectural boxes in the regenerated report:**

No non-empty, scoreable box is documented for this case; consult the report for unvalidated/empty target outcomes.

The report's global ranking is reproduced here for the leading boxes; retain its full target-by-target table for the remaining boxes, duplicate marks, NaN/not-selected flags, and discovery metrics.

| Global rank | Target | Box | Held-out status | Test score | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |
|---:|:---|:---|:---|---:|---:|---:|---:|---:|:---|
| 1 | M-S | CART Box 3 | Evaluated | 1 | 1 | 9 / 9 | 9 / 54 | 1 | Near duplicate of PRIM Box 2 (condition similarity 100%; held-out membership Jaccard 100%) |
| 2 | M-S | PRIM Box 2 | Evaluated | 1 | 1 | 9 / 9 | 9 / 54 | 1 | Representative for CART Box 3 |
| 3 | S-M | PRIM Box 1 | Evaluated | 0.9600 | 0.9231 | 12 / 13 | 12 / 54 | 2 | — |
| 4 | S-M | CART Box 2 | Evaluated | 0.9600 | 0.9231 | 12 / 13 | 12 / 54 | 3 | — |
| 5 | M-M | CART Box 1 | Evaluated | 0.9153 | 0.8438 | 27 / 32 | 27 / 54 | 2 | Near duplicate of PRIM Box 3 (condition similarity 100%; held-out membership Jaccard 100%) |
| 6 | M-M | PRIM Box 3 | Evaluated | 0.9153 | 0.8438 | 27 / 32 | 27 / 54 | 2 | Representative for CART Box 1 |

A boxed held-out what-if is a restriction of existing test runs. It can enrich a discrete target region within this sample; it does not change the FL design or establish future robustness. Check held-out support and coverage before treating a rule as actionable. See [Section 11 and policy matrices](../analysis-fl-rq-baseline-image.ipynb#11-What-if-analysis-robustness-after-applying-box-rules) and the complete [box report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md).

## Practical and research implications

- **For practitioners:** Use the best-supported joint box as a candidate operating envelope to monitor or validate; make only the policy decisions explicitly constrained by its architectural prescription. Avoid adopting rules with sparse retained support, zero held-out target support, or low target coverage as general guidance.
- **For researchers:** The feature ordering and box boundaries are specific to this filtered case and grouped holdout. Confirm the same pattern in another relevant stratum or a controlled follow-up; do not interpret feature importance, stress aliases, or box rules causally.

## Case limitations

Compact client characteristics are aggregated run-level values; they can hide client-level imbalance and round behavior. The ten-seed grouped holdout leaves limited support for rare regions. The box report and notebook provide the full feature set, all box conditions, and metrics.
