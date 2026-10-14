# Findings — ADEPT compact FL Client Selector stress analysis: AG_NEWS/MLP, all client counts

## Scope and support

This case is AG_NEWS/MLP, all sampled environment settings, with Client Selector required ON; other pattern decisions vary; client counts 4, 8, and 10 pooled. The filtered population contains 480 run rows; 336 are used for training and 144 for held-out evaluation. The splitter keeps `partition_seed` groups intact (3 of 10 held out); grouped holdout by partition_seed; no fallback warning. It reports these region counts (the fixed grid uses accuracy × average total round time, and only observed regions appear):

- Train (336): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 8 (2.38%); M,M: 4 (1.19%); M,L: 0 (0.00%); L,S: 117 (34.82%); L,M: 207 (61.61%); L,L: 0 (0.00%)
- Held out (144): S,S: 0 (0.00%); S,M: 0 (0.00%); S,L: 0 (0.00%); M,S: 3 (2.08%); M,M: 2 (1.39%); M,L: 0 (0.00%); L,S: 50 (34.72%); L,M: 89 (61.81%); L,L: 0 (0.00%)

The shared grid bins accuracy as S 0.21–0.48, M 0.48–0.75, L 0.75–1.02 and average total time as S 1.56–9.51, M 9.51–17.45, L 17.45–25.39. Empty regions in this slice are unobserved, not ruled out. [Notebook, split and discretization outputs](federatedlearning/compact/text/analysis-fl-rq-stress-client_selector-text.ipynb#data-splitting).

## RQ1 — Tradeoffs and design associations

Observed runs occupy the regions listed above; the other cells in the nine-region grid have zero observed support in this slice. RQ1 compares complete pattern configurations where decisions vary; the notebook's contingency output uses configurations before marginal pattern summaries. For a single-configuration profile, the pattern decision is fixed and cannot be compared within that case. Client-count leaves hold count fixed; profile and focal-pattern leaves pool 4, 8, and 10 clients. The three focal-pattern views overlap because combinations with multiple patterns ON recur across branches. Pattern-count and instance-count summaries are derived run descriptors, not complete configurations or randomized pattern doses.

The region allocation and STARR-style membership stability are reported in the notebook's contingency and robustness sections. Interpret these as observed allocations under mixed sampled environment conditions, not isolated pattern effects. Accuracy and time are both minimized in the campaign, so L-S is the high-accuracy/short-time region and L-M is high-accuracy/medium-time. [Notebook, contingency and robustness outputs](federatedlearning/compact/text/analysis-fl-rq-stress-client_selector-text.ipynb#contingency-analysis), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png).

## RQ2 — Joint conditions and held-out what-if

The notebook's weighted feature ranking is relative predictive credit in this fitted slice; it is not a direction or effect estimate. Weighted feature ranking: ['Message Compressor Stress Percentage', 'Alpha Dirichlet Mean', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Total Clients', 'Pattern Instances', 'HDH Stress Percentage', 'Pattern Types Active']
Excluded predictors (fixed scope and exact aliases): ['Dataset', 'Model', 'low_spec_percentage']
Key parameters (for scenario discovery): ['Message Compressor Stress Percentage', 'Alpha Dirichlet Mean', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Total Clients', 'Pattern Instances', 'HDH Stress Percentage', 'Pattern Types Active']

PRIM discovery rules (training partition):

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.15
	Total Clients: [4.000, 9.000]
	Pattern Instances: [1.000, 2.500]
	non_iid_percentage: [37.500, 75.000]
 2. For tradeoff M-M (M,M): lift=0.11
	Pattern Instances: [1.500, 11.000]
	non_iid_percentage: [62.500, 75.000]
 3. For tradeoff L-S (L,S): lift=0.65
	delay_percentage: [0.000, 87.500]
	Message Compressor Stress Percentage: [-5.000, 12.500]
 4. For tradeoff L-M (L,M): lift=0.38
	Total Clients: [6.000, 10.000]
	Alpha Dirichlet Mean: [0.812, 0.900]
	Pattern Types Active: [1.500, 3.000]
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: [25.000, 62.500]
	HDH Stress Percentage: (not selected) or <= 62.500
```

CART rules (global partition fit):

```text
Running CART global discovery for all tradeoff combinations ...

 1. For tradeoff L-M (L,M): lift=0.38
	delay_percentage: [12.490, 100.000]
	Total Clients: [5.999, 10.000]
	Pattern Instances: [3.499, 11.000]
	Client Selector Stress Percentage: [25.000, 62.505]
 2. For tradeoff L-S (L,S): lift=0.65
	delay_percentage: [0.000, 12.490]
 3. For tradeoff M-S (M,S): lift=-0.02
	Pattern Instances: [1.499, 2.501]
	Client Selector Stress Percentage: [62.505, 75.000]
	Total Clients: [5.999, 10.000]
	delay_percentage: [12.490, 50.010]
	Alpha Dirichlet Mean: [0.613, 0.900]

3 non-empty CART box(es) discovered.
```

Architectural interpretation groups the rule conditions into policy choices and observed operating context; most rules are conjunctions of sampled context and derived run summaries, and a condition on a stress feature is applicable only when that pattern is selected. Where the box report marks NaN/not-selected inclusion, the rule also spans runs where that optional pattern was OFF. See the report for exact activation counts and complete condition interpretation: [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-client_selector__clients-all__environment-all.md).

Held-out evaluation of each fixed box (target prevalence before filtering, retained rows, precision, absolute percentage-point rate change, and target coverage) is shown below. An absent held-out target has undefined coverage, not zero coverage. Sparse targets remain weakly validated even when precision is high.

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     144                  3     12              2   
1   PRIM    M-M     144                  2      8              1   
2   PRIM    L-S     144                 50     18             18   
3   PRIM    L-M     144                 89     36             36   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.021          0.167            0.146                0.188   
1          0.014          0.125            0.111                0.223   
2          0.347          1.000            0.653                0.652   
3          0.618          1.000            0.382                0.384   

   test_recall_coverage  
0                 0.667  
1                 0.500  
2                 0.360  
3                 0.404  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     144                 89     33             33   
1   CART    L-S     144                 50     18             18   
2   CART    M-S     144                  3      2              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.618            1.0            0.382                0.384   
1          0.347            1.0            0.653                0.652   
2          0.021            0.0           -0.021                0.643   

   test_recall_coverage  
0                 0.371  
1                 0.360  
2                 0.000
```

The policy-specific before/boxed/gain and target-coverage matrices are in Section 11 of the notebook. Their zero cells can mean no retained support; the all-patterns-OFF profile is a distinct policy from the unrestricted test baseline. Filtering is a what-if over already observed held-out rows, not an intervention. [Notebook, feature/discovery/held-out results](federatedlearning/compact/text/analysis-fl-rq-stress-client_selector-text.ipynb#feature-importance-key-parameter-selection), [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-client_selector__clients-all__environment-all.png).

## Implications

- **Practitioners:** Treat the displayed rule as a candidate operating envelope for this AG_NEWS/MLP scope. Check retained support and coverage before using it to screen configurations; validate any rare-region rule on additional seeds and client conditions.
- **Researchers:** The evidence supports within-slice association and out-of-sample rule evaluation only. Client summaries are run-level aggregates; environment composition and grouped seeds limit transfer and causal interpretation.

## Case limitations and evidence

The case covers one task/model, ten seed groups, and compact run-level client summaries. Some region targets are rare or absent in test, and configuration/environment mixes are observational. Stress notebooks pool client counts and vary other pattern decisions; profile notebooks pool client counts but fix the pattern configuration. Source evidence: [executed notebook](federatedlearning/compact/text/analysis-fl-rq-stress-client_selector-text.ipynb), [box report](federatedlearning/compact/text/boxes/boxes__task-text__focal-pattern-client_selector__clients-all__environment-all.md), [quality-space plot](federatedlearning/compact/text/plots/quality-space__task-text__focal-pattern-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance plot](federatedlearning/compact/text/plots/feature-importance__task-text__focal-pattern-client_selector__clients-all__environment-all.png).
