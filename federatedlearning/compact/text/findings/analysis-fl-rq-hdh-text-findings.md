# Findings — ADEPT compact FL HDH-only analysis: AG_NEWS/MLP, all client counts

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with HDH-only policy OFF,OFF,ON; client counts 4, 8, and 10 pooled. The filtered population contains 150 run rows; 105 are used for training and 45 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); grouped holdout by partition_seed; no fallback warning. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (105): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 0 (0.00%); M,M: 3 (2.86%); M,L: 0 (0.00%); L,S: 0 (0.00%); L,M: 96 (91.43%); L,L: 6 (5.71%)
- Held out (45): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 0 (0.00%); M,M: 0 (0.00%); M,L: 0 (0.00%); L,S: 0 (0.00%); L,M: 42 (93.33%); L,L: 3 (6.67%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['non_iid_percentage', 'Alpha Dirichlet Mean', 'JSD Mean', 'Total Clients', 'delay_percentage', 'CPU Mean', 'low_spec_percentage']
Excluded fixed-scope features: ['Dataset', 'Model']
Excluded pattern-stress aliases for profile analysis: ['Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Key parameters (for scenario discovery): ['non_iid_percentage', 'Alpha Dirichlet Mean', 'JSD Mean', 'Total Clients', 'delay_percentage', 'CPU Mean']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-M (M,M): lift=0.00
	Total Clients: [4.000, 6.000]
	Alpha Dirichlet Mean: [0.600, 0.688]
	JSD Mean: [0.000, 0.018]
 2. For tradeoff L-M (L,M): lift=0.07
	Total Clients: [6.000, 10.000]
 3. For tradeoff L-L (L,L): lift=0.27
	Total Clients: [4.000, 6.000]
	delay_percentage: [50.000, 75.000]
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...
 1. For tradeoff L-M (L,M): lift=0.07
	Total Clients: [5.999, 10.000]
 2. For tradeoff L-L (L,L): lift=0.27
	JSD Mean: [0.000, 0.018]
	Total Clients: [4.000, 5.999]
	delay_percentage: [50.000, 75.000]

2 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-M      45                  0      9              0   
1   PRIM    L-M      45                 42     30             30   
2   PRIM    L-L      45                  3      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.221   
1          0.933          1.000            0.067                0.086   
2          0.067          0.333            0.267                0.514   

   test_recall_coverage  
0                   NaN  
1                 0.714  
2                 0.333  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M      45                 42     30             30   
1   CART    L-L      45                  3      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.933          1.000            0.067                0.086   
1          0.067          0.333            0.267                0.443   

   test_recall_coverage  
0                 0.714  
1                 0.333
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).
