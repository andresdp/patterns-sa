# Findings — ADEPT compact FL analysis: AG_NEWS/MLP, 8 clients

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with all pattern configurations, fixed at 8 clients. The filtered population contains 390 run rows; 273 are used for training and 117 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); grouped holdout by partition_seed; no fallback warning. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (273): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 4 (1.47%); M,M: 1 (0.37%); M,L: 0 (0.00%); L,S: 53 (19.41%); L,M: 215 (78.75%); L,L: 0 (0.00%)
- Held out (117): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 1 (0.85%); M,M: 1 (0.85%); M,L: 0 (0.00%); L,S: 23 (19.66%); L,M: 92 (78.63%); L,L: 0 (0.00%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-c8-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-c8-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['delay_percentage', 'Alpha Dirichlet Mean', 'Client Selector Stress Percentage', 'HDH Stress Percentage', 'HDH Instances', 'Pattern Instances', 'Pattern Types Active', 'CPU Mean', 'Message Compressor Stress Percentage']
Excluded fixed-scope features: ['Dataset', 'Model', 'Total Clients']
Key parameters (for scenario discovery): ['delay_percentage', 'Alpha Dirichlet Mean', 'Client Selector Stress Percentage', 'HDH Stress Percentage', 'HDH Instances', 'Pattern Instances', 'Pattern Types Active']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.13
	Alpha Dirichlet Mean: [0.625, 0.812]
	Pattern Instances: [0.000, 3.500]
	Client Selector Stress Percentage: [35.000, 75.000]
 2. For tradeoff M-M (M,M): lift=-0.01
	Alpha Dirichlet Mean: [0.625, 0.688]
	Client Selector Stress Percentage: [35.000, 75.000]
 3. For tradeoff L-S (L,S): lift=0.80
	delay_percentage: [0.000, 12.500]
 4. For tradeoff L-M (L,M): lift=0.21
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...
 1. For tradeoff L-M (L,M): lift=0.21
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
 2. For tradeoff L-S (L,S): lift=0.80
	delay_percentage: [0.000, 12.500]
 3. For tradeoff M-S (M,S): lift=-0.01
	HDH Instances: [0.500, 6.000]
	Pattern Instances: [0.000, 2.499]
	delay_percentage: [12.500, 37.485]
	Client Selector Stress Percentage: [62.498, 75.000]

3 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__all-configurations__clients-8__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     117                  1      7              1   
1   PRIM    M-M     117                  1      6              0   
2   PRIM    L-S     117                 23     15             15   
3   PRIM    L-M     117                 92     78             78   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.009          0.143            0.134                0.196   
1          0.009          0.000           -0.009                0.068   
2          0.197          1.000            0.803                0.806   
3          0.786          1.000            0.214                0.212   

   test_recall_coverage  
0                 1.000  
1                 0.000  
2                 0.652  
3                 0.848  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     117                 92     78             78   
1   CART    L-S     117                 23     15             15   
2   CART    M-S     117                  1      1              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.786            1.0            0.214                0.212   
1          0.197            1.0            0.803                0.806   
2          0.009            0.0           -0.009                0.485   

   test_recall_coverage  
0                 0.848  
1                 0.652  
2                 0.000
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-c8-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-c8-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__all-configurations__clients-8__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png).
