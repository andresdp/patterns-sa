# Findings: ADEPT compact FL Client Selector stress analysis: CIFAR-10/CNN 16k, all client counts

## Scope and support

- **Task:** image, CIFAR-10 with CNN 16k. **Case:** Client Selector ON; other pattern decisions and client counts vary; all environments (overlaps other focal-pattern views).
- **Rows:** 480 total; 336 training and 144 held out. The unit is a run; the split groups by `partition_seed` (10 groups, 7/3 train/test). Grouped holdout by partition_seed: 3 of 10 groups held out; stratification score=0.000036..
- **Tradeoff counts (fixed accuracy × round-time grid):** training: S,S 34, S,M 28, M,S 84, M,M 190; held out: S,S 14, S,M 12, M,S 37, M,M 81. Regions absent from each list have zero rows in that partition; empty regions indicate no sampled runs, not infeasibility.
- Accuracy and time are discretized into S/M/L using the campaign's shared cut points; S/M/L mean value bands, not preference. Regions include low/medium accuracy × low/medium round time in these observed cases; see notebook Section 3 for exact edges and Section 4 for the split.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The observed occupancy is concentrated in the regions shown above. Outcome-space allocation and the configuration contingency tables in notebook Sections 4–5 describe complete pattern configurations and their denominators; marginal ON/OFF summaries pool multiple configurations. For this focal-pattern view, runs can overlap the other focal-pattern cases; the pattern-count summaries are derived descriptors and are not configuration identities.

Robustness/contingency outputs in Sections 5–6 show within-group region shares. They are descriptive allocations across sampled run conditions. No empty region should be read as impossible, and observed differences do not isolate a pattern effect. The Section 7 pattern-stress summaries are run-level aggregations; instance count and number of active pattern types are not interchangeable with a complete policy configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Feature rankings and exclusions are reported in Sections 8–10 and the feature-importance plot. Importance is relative predictive credit in this fitted slice; it is not a direction or causal effect. PRIM/CART rules are joint conditions, with design and context mixed according to the available features. See the linked box report for the full rule limits, architectural interpretation, discovery support, and not-selected/NaN coverage.

**PRIM held-out evaluation** (test baseline = target prevalence; Δ rate = box precision minus baseline; train lift is retained from the notebook's output):

```text
method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     144                 14      9              6   
1   PRIM    S-M     144                 12     18              5   
2   PRIM    M-S     144                 37     18             17   
3   PRIM    M-M     144                 81     36             33   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.097          0.667            0.569                0.741   
1          0.083          0.278            0.194                0.298   
2          0.257          0.944            0.688                0.750   
3          0.562          0.917            0.354                0.435   

   test_recall_coverage  
0                 0.429  
1                 0.417  
2                 0.459  
3                 0.407
```

**CART held-out evaluation:**

```text
method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     144                 81     36             33   
1   CART    M-S     144                 37     18             17   
2   CART    S-S     144                 14      6              6   
3   CART    S-M     144                 12      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.562          0.917            0.354                0.435   
1          0.257          0.944            0.688                0.750   
2          0.097          1.000            0.903                0.899   
3          0.083          0.333            0.250                0.345   

   test_recall_coverage  
0                 0.407  
1                 0.459  
2                 0.429  
3                 0.083
```

Metrics are read as held-out precision among retained test runs and target coverage among all held-out target runs. A target with zero held-out rows is not test-evaluable; NaN precision/coverage is undefined. Sparse targets warrant caution. Policy-specific before/boxed/gain and target-coverage matrices are in notebook Section 11 and must be read alongside retained counts; they describe policy-filtered cells, distinct from the all-run held-out summary above.

## Implications and limitations

- **For practitioners:** use a discovered conjunction as a candidate operating envelope for further runs in this exact case scope. Prefer rules with both useful coverage and adequate retained support; validate sparse or low-coverage boxes before treating them as an operating recommendation.
- **For researchers:** the grouped seed holdout provides out-of-sample evidence within this slice, but not independent replication across workloads or sampling regimes. The design and context conditions are observational; client attributes are run-level aggregates and can conceal within-run client imbalance.
- **Limitations:** available configurations and environment coverage are bounded by the campaign data; fixed discretization can leave empty cells; pooled or overlapping scopes limit cross-case attribution; predictive rankings and boxes do not establish causal effects.

## Supporting artifacts

- Notebook sections 3–11: [analysis-fl-rq-stress-client_selector-image.ipynb](../analysis-fl-rq-stress-client_selector-image.ipynb#section-4-data-splitting)
- Box report: [boxes__task-image__focal-pattern-client_selector__clients-all__environment-all.md](../boxes/boxes__task-image__focal-pattern-client_selector__clients-all__environment-all.md)
- Objective-space plot: [quality-space__task-image__focal-pattern-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__focal-pattern-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png)
- Feature-importance plot: [feature-importance__task-image__focal-pattern-client_selector__clients-all__environment-all.png](../plots/feature-importance__task-image__focal-pattern-client_selector__clients-all__environment-all.png)
