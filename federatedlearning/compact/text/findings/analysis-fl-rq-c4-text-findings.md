# Findings — ADEPT compact FL analysis: AG_NEWS/MLP, 4 clients

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with all pattern configurations, fixed at 4 clients. The filtered population contains 390 run rows; 273 are used for training and 117 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); grouped holdout by partition_seed; no fallback warning. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (273): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 3 (1.10%); M,M: 5 (1.83%); M,L: 0 (0.00%); L,S: 69 (25.27%); L,M: 184 (67.40%); L,L: 12 (4.40%)
- Held out (117): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 2 (1.71%); M,M: 0 (0.00%); M,L: 0 (0.00%); L,S: 31 (26.50%); L,M: 79 (67.52%); L,L: 5 (4.27%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-c4-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-c4-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['Alpha Dirichlet Mean', 'Client Selector Stress Percentage', 'delay_percentage', 'HDH Instances', 'Pattern Instances', 'HDH Stress Percentage', 'Message Compressor Stress Percentage', 'Pattern Types Active', 'CPU Mean']
Excluded fixed-scope features: ['Dataset', 'Model', 'Total Clients']
Key parameters (for scenario discovery): ['Alpha Dirichlet Mean', 'Client Selector Stress Percentage', 'delay_percentage', 'HDH Instances', 'Pattern Instances', 'HDH Stress Percentage', 'Message Compressor Stress Percentage']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.21
	Alpha Dirichlet Mean: [0.625, 0.812]
	Client Selector Stress Percentage: [35.000, 75.000]
 2. For tradeoff M-M (M,M): lift=0.00
	Alpha Dirichlet Mean: [0.625, 0.688]
	HDH Instances: [0.500, 3.000]
 3. For tradeoff L-S (L,S): lift=0.74
	delay_percentage: [0.000, 12.500]
	Client Selector Stress Percentage: [22.500, 75.000]
 4. For tradeoff L-M (L,M): lift=0.32
	Pattern Instances: [0.000, 5.500]
	HDH Instances: [0.000, 2.500]
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 22.500
 5. For tradeoff L-L (L,L): lift=0.37
	Alpha Dirichlet Mean: [0.625, 0.688]
	Pattern Instances: [2.500, 7.000]
	HDH Instances: [0.500, 3.000]
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...
 1. For tradeoff L-M (L,M): lift=0.32
	delay_percentage: [12.500, 100.000]
	Pattern Instances: [0.000, 5.499]
	Client Selector Stress Percentage: (not selected) or <= 22.497
	HDH Stress Percentage: (not selected) or <= 62.498
 2. For tradeoff L-S (L,S): lift=0.74
	delay_percentage: [0.000, 12.500]
 3. For tradeoff L-L (L,L): lift=0.62
	delay_percentage: [50.010, 100.000]
	Pattern Instances: [0.000, 5.000]
	Client Selector Stress Percentage: (not selected) or <= 62.498
	HDH Stress Percentage: [62.498, 75.000]

3 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__all-configurations__clients-4__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     117                  2      9              2   
1   PRIM    M-M     117                  0     14              0   
2   PRIM    L-S     117                 31      6              6   
3   PRIM    L-M     117                 79     45             45   
4   PRIM    L-L     117                  5     12              5   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.017          0.222            0.205                0.132   
1          0.000          0.000            0.000                0.138   
2          0.265          1.000            0.735                0.747   
3          0.675          1.000            0.325                0.326   
4          0.043          0.417            0.374                0.349   

   test_recall_coverage  
0                 1.000  
1                   NaN  
2                 0.194  
3                 0.570  
4                 1.000  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     117                 79     45             45   
1   CART    L-S     117                 31     15             15   
2   CART    L-L     117                  5      3              2   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.675          1.000            0.325                0.326   
1          0.265          1.000            0.735                0.747   
2          0.043          0.667            0.624                0.385   

   test_recall_coverage  
0                 0.570  
1                 0.484  
2                 0.400
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-c4-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__all-configurations__clients-4__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-c4-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__all-configurations__clients-4__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__all-configurations__clients-4__environment-all.png).
