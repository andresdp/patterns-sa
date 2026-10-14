# Findings: ADEPT compact FL baseline analysis: CIFAR-10/CNN 16k, all client counts

## Scope and support

- **Task:** image, CIFAR-10 with CNN 16k. **Case:** Fixed OFF,OFF,OFF baseline; client counts 4, 8, and 10 pooled; all environments.
- **Rows:** 180 total; 126 training and 54 held out. The unit is a run; the split groups by `partition_seed` (10 groups, 7/3 train/test). Grouped holdout by partition_seed: 3 of 10 groups held out; stratification score=0.000027..
- **Tradeoff counts (fixed accuracy × round-time grid):** training: S,M 31, M,S 21, M,M 74; held out: S,M 13, M,S 9, M,M 32. Regions absent from each list have zero rows in that partition; empty regions indicate no sampled runs, not infeasibility.
- Accuracy and time are discretized into S/M/L using the campaign's shared cut points; S/M/L mean value bands, not preference. Regions include low/medium accuracy × low/medium round time in these observed cases; see notebook Section 3 for exact edges and Section 4 for the split.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The observed occupancy is concentrated in the regions shown above. Outcome-space allocation and the configuration contingency tables in notebook Sections 4–5 describe complete pattern configurations and their denominators; marginal ON/OFF summaries pool multiple configurations. This case fixes client count or one complete policy, as stated in the scope; conclusions apply to this slice.

Robustness/contingency outputs in Sections 5–6 show within-group region shares. They are descriptive allocations across sampled run conditions. No empty region should be read as impossible, and observed differences do not isolate a pattern effect. The Section 7 pattern-stress summaries are run-level aggregations; instance count and number of active pattern types are not interchangeable with a complete policy configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Feature rankings and exclusions are reported in Sections 8–10 and the feature-importance plot. Importance is relative predictive credit in this fitted slice; it is not a direction or causal effect. PRIM/CART rules are joint conditions, with design and context mixed according to the available features. See the linked box report for the full rule limits, architectural interpretation, discovery support, and not-selected/NaN coverage.

**PRIM held-out evaluation** (test baseline = target prevalence; Δ rate = box precision minus baseline; train lift is retained from the notebook's output):

```text
method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-M      54                 13     12             12   
1   PRIM    M-S      54                  9      9              9   
2   PRIM    M-M      54                 32     27             27   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.241            1.0            0.759                0.754   
1          0.167            1.0            0.833                0.833   
2          0.593            1.0            0.407                0.413   

   test_recall_coverage  
0                 0.923  
1                 1.000  
2                 0.844
```

**CART held-out evaluation:**

```text
method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      54                 32     27             27   
1   CART    S-M      54                 13     12             12   
2   CART    M-S      54                  9      9              9   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.593            1.0            0.407                0.413   
1          0.241            1.0            0.759                0.754   
2          0.167            1.0            0.833                0.833   

   test_recall_coverage  
0                 0.844  
1                 0.923  
2                 1.000
```

Metrics are read as held-out precision among retained test runs and target coverage among all held-out target runs. A target with zero held-out rows is not test-evaluable; NaN precision/coverage is undefined. Sparse targets warrant caution. Policy-specific before/boxed/gain and target-coverage matrices are in notebook Section 11 and must be read alongside retained counts; they describe policy-filtered cells, distinct from the all-run held-out summary above.

## Implications and limitations

- **For practitioners:** use a discovered conjunction as a candidate operating envelope for further runs in this exact case scope. Prefer rules with both useful coverage and adequate retained support; validate sparse or low-coverage boxes before treating them as an operating recommendation.
- **For researchers:** the grouped seed holdout provides out-of-sample evidence within this slice, but not independent replication across workloads or sampling regimes. The design and context conditions are observational; client attributes are run-level aggregates and can conceal within-run client imbalance.
- **Limitations:** available configurations and environment coverage are bounded by the campaign data; fixed discretization can leave empty cells; pooled or overlapping scopes limit cross-case attribution; predictive rankings and boxes do not establish causal effects.

## Supporting artifacts

- Notebook sections 3–11: [analysis-fl-rq-baseline-image.ipynb](../analysis-fl-rq-baseline-image.ipynb#section-4-data-splitting)
- Box report: [boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md)
- Objective-space plot: [quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png)
- Feature-importance plot: [feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../plots/feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png)
