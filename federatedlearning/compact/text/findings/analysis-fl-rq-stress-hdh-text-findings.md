# Findings — ADEPT compact FL HDH stress analysis: AG_NEWS/MLP, all client counts

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with HDH required ON; other pattern decisions vary; client counts 4, 8, and 10 pooled. The filtered population contains 480 run rows; 336 are used for training and 144 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); grouped holdout by partition_seed; no fallback warning. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (336): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 5 (1.49%); M,M: 8 (2.38%); M,L: 0 (0.00%); L,S: 63 (18.75%); L,M: 248 (73.81%); L,L: 12 (3.57%)
- Held out (144): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 2 (1.39%); M,M: 2 (1.39%); M,L: 0 (0.00%); L,S: 26 (18.06%); L,M: 109 (75.69%); L,L: 5 (3.47%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-stress-hdh-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-stress-hdh-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-hdh__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['HDH Stress Percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'JSD Mean', 'HDH Instances', 'Total Clients', 'Pattern Instances', 'Alpha Dirichlet Mean', 'CPU Mean', 'Message Compressor Stress Percentage', 'low_spec_percentage', 'Pattern Types Active']
Excluded predictors (fixed scope and exact aliases): ['Dataset', 'Model', 'non_iid_percentage']
Key parameters (for scenario discovery): ['HDH Stress Percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'JSD Mean', 'HDH Instances', 'Total Clients', 'Pattern Instances', 'Alpha Dirichlet Mean']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.19
	Total Clients: [4.000, 9.000]
	Pattern Instances: [1.500, 3.500]
	Client Selector Stress Percentage: [37.500, 75.000]
 2. For tradeoff M-M (M,M): lift=0.10
	Client Selector Stress Percentage: [47.500, 75.000]
	HDH Stress Percentage: [62.500, 75.000]
 3. For tradeoff L-S (L,S): lift=0.82
	delay_percentage: [0.000, 12.500]
	Client Selector Stress Percentage: [22.500, 75.000]
 4. For tradeoff L-M (L,M): lift=0.24
	Total Clients: [6.000, 10.000]
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
 5. For tradeoff L-L (L,L): lift=0.38
	Total Clients: [4.000, 6.000]
	Client Selector Stress Percentage: (not selected) or <= 47.500
	HDH Stress Percentage: [62.500, 75.000]
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...
 1. For tradeoff L-M (L,M): lift=0.24
	delay_percentage: [12.490, 100.000]
	Total Clients: [5.999, 10.000]
	Client Selector Stress Percentage: (not selected) or <= 37.493
 2. For tradeoff L-S (L,S): lift=0.82
	delay_percentage: [0.000, 12.490]
 3. For tradeoff L-L (L,L): lift=-0.03
	Client Selector Stress Percentage: (not selected) or <= 62.502
	HDH Instances: [2.499, 8.000]
	delay_percentage: [12.490, 50.010]
	JSD Mean: [0.000, 0.017]
	Pattern Instances: [1.000, 4.998]
	Total Clients: [4.000, 5.999]
 4. For tradeoff M-S (M,S): lift=-0.01
	delay_percentage: [12.490, 100.000]
	Pattern Instances: [1.499, 2.498]
	Total Clients: [5.999, 9.000]
	Client Selector Stress Percentage: [62.502, 75.000]

4 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-hdh__clients-all__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     144                  2     10              2   
1   PRIM    M-M     144                  2      9              1   
2   PRIM    L-S     144                 26      9              9   
3   PRIM    L-M     144                109     72             72   
4   PRIM    L-L     144                  5     12              5   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.014          0.200            0.186                0.223   
1          0.014          0.111            0.097                0.167   
2          0.181          1.000            0.819                0.812   
3          0.757          1.000            0.243                0.262   
4          0.035          0.417            0.382                0.357   

   test_recall_coverage  
0                 1.000  
1                 0.500  
2                 0.346  
3                 0.661  
4                 1.000  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     144                109     72             72   
1   CART    L-S     144                 26     18             18   
2   CART    L-L     144                  5      4              0   
3   CART    M-S     144                  2      2              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.757            1.0            0.243                0.262   
1          0.181            1.0            0.819                0.812   
2          0.035            0.0           -0.035                0.364   
3          0.014            0.0           -0.014                0.652   

   test_recall_coverage  
0                 0.661  
1                 0.692  
2                 0.000  
3                 0.000
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-stress-hdh-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-hdh__clients-all__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-stress-hdh-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-hdh__clients-all__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-hdh__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-hdh__clients-all__environment-all.png).
