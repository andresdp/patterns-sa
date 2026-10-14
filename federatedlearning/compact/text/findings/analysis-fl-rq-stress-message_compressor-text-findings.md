# Findings — ADEPT compact FL Message Compressor stress analysis: AG_NEWS/MLP, all client counts

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with Message Compressor required ON; other pattern decisions vary; client counts 4, 8, and 10 pooled. The filtered population contains 600 run rows; 420 are used for training and 180 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); stratification fallback warning; grouped holdout remains by partition_seed. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (420): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 0 (0.00%); M,M: 1 (0.24%); M,L: 0 (0.00%); L,S: 93 (22.14%); L,M: 321 (76.43%); L,L: 5 (1.19%)
- Held out (180): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 0 (0.00%); M,M: 0 (0.00%); M,L: 0 (0.00%); L,S: 40 (22.22%); L,M: 137 (76.11%); L,L: 3 (1.67%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-stress-message_compressor-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-stress-message_compressor-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['Message Compressor Stress Percentage', 'Alpha Dirichlet Mean', 'non_iid_percentage', 'Client Selector Stress Percentage', 'HDH Instances', 'Pattern Instances', 'HDH Stress Percentage', 'Message Compressor Instances', 'Pattern Types Active', 'CPU Mean', 'low_spec_percentage']
Excluded predictors (fixed scope and exact aliases): ['Dataset', 'Model', 'delay_percentage']
Key parameters (for scenario discovery): ['Message Compressor Stress Percentage', 'Alpha Dirichlet Mean', 'non_iid_percentage', 'Client Selector Stress Percentage', 'HDH Instances', 'Pattern Instances', 'HDH Stress Percentage', 'Message Compressor Instances']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-M (M,M): lift=0.00
	HDH Instances: [1.500, 8.000]
	non_iid_percentage: [62.500, 75.000]
 2. For tradeoff L-S (L,S): lift=0.78
	Message Compressor Stress Percentage: [0.000, 12.500]
 3. For tradeoff L-M (L,M): lift=0.24
	Message Compressor Instances: [3.500, 10.000]
	Client Selector Stress Percentage: (not selected) or <= 62.500
	Message Compressor Stress Percentage: [12.500, 100.000]
	HDH Stress Percentage: (not selected) or <= 37.500
 4. For tradeoff L-L (L,L): lift=0.32
	Message Compressor Instances: [1.000, 6.000]
	non_iid_percentage: [37.500, 75.000]
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...
 1. For tradeoff L-M (L,M): lift=0.24
	Message Compressor Stress Percentage: [12.508, 100.000]
	HDH Stress Percentage: (not selected) or <= 37.495
	Message Compressor Instances: [3.499, 10.000]
 2. For tradeoff L-S (L,S): lift=0.78
	Message Compressor Stress Percentage: [0.000, 12.508]
 3. For tradeoff L-L (L,L): lift=0.98
	Message Compressor Stress Percentage: [12.508, 100.000]
	HDH Stress Percentage: [62.501, 75.000]
	Pattern Instances: [2.000, 10.498]
	Message Compressor Instances: [3.499, 10.000]

3 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-message_compressor__clients-all__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-M     180                  0      9              0   
1   PRIM    L-S     180                 40     36             36   
2   PRIM    L-M     180                137    102            102   
3   PRIM    L-L     180                  3      9              3   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.045   
1          0.222          1.000            0.778                0.779   
2          0.761          1.000            0.239                0.236   
3          0.017          0.333            0.317                0.226   

   test_recall_coverage  
0                   NaN  
1                 0.900  
2                 0.745  
3                 1.000  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     180                137    102            102   
1   CART    L-S     180                 40     36             36   
2   CART    L-L     180                  3      3              3   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.761            1.0            0.239                0.236   
1          0.222            1.0            0.778                0.779   
2          0.017            1.0            0.983                0.560   

   test_recall_coverage  
0                 0.745  
1                 0.900  
2                 1.000
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-stress-message_compressor-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-message_compressor__clients-all__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-stress-message_compressor-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-message_compressor__clients-all__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-message_compressor__clients-all__environment-all.png).
