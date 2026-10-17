# Findings: `analysis-fl-rq-stress-only-client_selector-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** Exactly client selector ON and the other two patterns OFF; stress levels 25/50/75%; clients pooled; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-stress-only-client_selector-image.ipynb](../analysis-fl-rq-stress-only-client_selector-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__stress-ONLY-client_selector__clients-all__environment-all.md](../boxes/boxes__task-image__stress-ONLY-client_selector__clients-all__environment-all.md).
- **Plots:**
- [quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__stress-ONLY-client_selector__clients-all__environment-all.png](../plots/feature-importance__task-image__stress-ONLY-client_selector__clients-all__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000267.
Data split: 105 train, 45 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (12.38%)
  S,M: 15 (14.29%)
  M,S: 25 (23.81%)
  M,M: 52 (49.52%)

--- Test Set Tradeoff Counts ---
  S,S: 5 (11.11%)
  S,M: 6 (13.33%)
  M,S: 11 (24.44%)
  M,M: 23 (51.11%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: Total Clients
  none
------------------------------
Grouping: low_spec_percentage
  none
------------------------------
Grouping: non_iid_percentage
  none
------------------------------
Grouping: delay_percentage
  none
```

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
Warning: 'config_id' has a single policy group (['ON,OFF,OFF']) in the 'all' runs, so no tradeoff can be exclusive to one of them.
  none
------------------------------
Grouping: Total Clients
  none
------------------------------
Grouping: low_spec_percentage
* Tradeoff: S-S --> Group: low_spec_percentage=75
------------------------------
Grouping: non_iid_percentage
  none
------------------------------
Grouping: delay_percentage
* Tradeoff: S-S --> Group: delay_percentage=25
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,OFF: 12% success
  Top Policy -> ON,OFF,OFF - Starr: 0.1200 - Regret: 0.8175
Robustness Ranking for Tradeoff: S-M
  1. ON,OFF,OFF: 14% success
  Top Policy -> ON,OFF,OFF - Starr: 0.1400 - Regret: 1.0587
Robustness Ranking for Tradeoff: S-L
  1. ON,OFF,OFF: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0000 - Regret: 2.5428
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,OFF: 24% success
  Top Policy -> ON,OFF,OFF - Starr: 0.2400 - Regret: 0.5187
Robustness Ranking for Tradeoff: M-M
  1. ON,OFF,OFF: 50% success
  Top Policy -> ON,OFF,OFF - Starr: 0.5000 - Regret: 0.6727
Robustness Ranking for Tradeoff: M-L
  1. ON,OFF,OFF: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0000 - Regret: 2.4072
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0000 - Regret: 4.7853
Robustness Ranking for Tradeoff: L-M
  1. ON,OFF,OFF: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0000 - Regret: 4.8390
Robustness Ranking for Tradeoff: L-L
  1. ON,OFF,OFF: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0000 - Regret: 5.3786
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: constant in these runs, values [1]
Pattern Instances: constant in these runs, values [1]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                      150               1              1              1   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.501                  8.794  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    ON,OFF,OFF   150        1.0                      0.501   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    ON,OFF,OFF                  8.794
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-de5fb604)

```text
Pattern Instances is constant in these runs: no stress levels to compare.
Pattern Types Active is constant in these runs: no stress levels to compare.
Runs and objective means by Client Selector Stress Percentage:

                                   runs  final_val_accuracy (mean)  \
Client Selector Stress Percentage                                    
25.0                                 30                      0.535   
50.0                                 30                      0.529   
75.0                                 90                      0.480   

                                   avg_total_time (mean)  
Client Selector Stress Percentage                         
25.0                                              11.188  
50.0                                               9.250  
75.0                                               7.844  
Tradeoff counts by stress level:

tradeoff                           M-M  M-S  S-M  S-S
Client Selector Stress Percentage                    
25                                  27    3    0    0
50                                  20    9    1    0
75                                  28   24   20   18
Within-level tradeoff shares (STARR) by Client Selector Stress Percentage:

                                      S-S    S-M  S-L    M-S    M-M  M-L  L-S  \
policy                                                                          
Client Selector Stress Percentage=25  0.0  0.000  0.0  0.100  0.900  0.0  0.0   
Client Selector Stress Percentage=50  0.0  0.033  0.0  0.300  0.667  0.0  0.0   
Client Selector Stress Percentage=75  0.2  0.222  0.0  0.267  0.311  0.0  0.0   

                                      L-M  L-L  
policy                                          
Client Selector Stress Percentage=25  0.0  0.0  
Client Selector Stress Percentage=50  0.0  0.0  
Client Selector Stress Percentage=75  0.0  0.0  
[figure rendered in notebook]
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.375117        0.158864
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.160011        0.389341
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.000000        0.000000
Client Selector Value                           0.000000        0.000000
Data Distribution Diversity                     0.000000        0.000000
Data Persistence Diversity                      0.000000        0.000000
Epochs                                          0.000000        0.000000
HDH Batch Size                                  0.000000        0.000000
HDH Beta 1                                      0.000000        0.000000
HDH Beta 2                                      0.000000        0.000000
HDH Discriminator                               0.000000        0.000000
HDH Epochs                                      0.000000        0.000000
HDH Generator                                   0.000000        0.000000
HDH Instances                                   0.000000        0.000000
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.000000        0.000000
JSD Mean                                        0.000000        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.000000
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.000000        0.000000
Pattern Types Active                            0.000000        0.000000
RAM Mean                                        0.000000        0.000000
Total Clients                                   0.314474        0.090813
delay_percentage                                0.006660        0.297848
non_iid_percentage                              0.143738        0.063134
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=0.22
	CPU Mean: [8.000, 8.125]
	non_iid_percentage: [50.000, 75.000]
 2. For tradeoff S-M (S,M): lift=0.37
	Total Clients: [6.000, 10.000]
	non_iid_percentage: [50.000, 75.000]
 3. For tradeoff M-S (M,S): lift=0.42
	Total Clients: [4.000, 6.000]
	CPU Mean: [8.125, 8.875]
	Alpha Dirichlet Mean: [0.750, 0.900]
	delay_percentage: [25.000, 50.000]
 4. For tradeoff M-M (M,M): lift=0.49
	Total Clients: [6.000, 10.000]
	CPU Mean: [10.125, 11.000]
	non_iid_percentage: [25.000, 50.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ CPU Mean [8, 8.12]
  ◦ non-IID percentage [50, 75] (%)


PRIM Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (14/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (6/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ non-IID percentage [50, 75] (%)
• Other design conditions:
  ◦ Total Clients [6, 10]

PRIM Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ CPU Mean [8.12, 8.88]
  ◦ Alpha Dirichlet Mean [0.75, 0.9]
  ◦ delay percentage [25, 50] (%)
• Other design conditions:
  ◦ Total Clients [4, 6]

PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (14/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (6/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ CPU Mean [10.1, 11]
  ◦ non-IID percentage [25, 50] (%)
• Other design conditions:
  ◦ Total Clients [6, 10]


CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (14/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (6/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ CPU Mean [10.1, 11]
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ CPU Mean [8, 8.87]
  ◦ delay percentage [50, 75] (%)
• Other design conditions:
  ◦ Total Clients [9, 10]

CART Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ CPU Mean [8, 8.87]
  ◦ delay percentage [25, 50] (%)
  ◦ Alpha Dirichlet Mean [0.75, 0.9]
• Other design conditions:
  ◦ Total Clients [9, 10]

CART Box 4: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ CPU Mean [8, 8.87]
  ◦ delay percentage [25, 50] (%)
  ◦ Alpha Dirichlet Mean [0.6, 0.612]
• Other design conditions:
  ◦ Total Clients [6, 10]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S      45                  5      3              1   
1   PRIM    S-M      45                  6      6              3   
2   PRIM    M-S      45                 11      3              2   
3   PRIM    M-M      45                 23      6              6   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.111          0.333            0.222                0.448   
1          0.133          0.500            0.367                0.286   
2          0.244          0.667            0.422                0.762   
3          0.511          1.000            0.489                0.505   

   test_recall_coverage  
0                 0.200  
1                 0.500  
2                 0.182  
3                 0.261  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      45                 23      6              6   
1   CART    S-M      45                  6      3              0   
2   CART    M-S      45                 11      3              0   
3   CART    S-S      45                  5      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.511          1.000            0.489                0.505   
1          0.133          0.000           -0.133                0.429   
2          0.244          0.000           -0.244                0.190   
3          0.111          0.333            0.222                0.448   

   test_recall_coverage  
0                 0.261  
1                 0.000  
2                 0.000  
3                 0.200
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

     method      policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0  test set  ON,OFF,OFF         0.0  0.0  0.0  0.0  0.511111  0.244444  0.0   
1      prim  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
2      prim  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.333333  0.666667  0.0   
3      prim  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  0.166667  0.000000  0.0   
4      prim  ON,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.333333  0.000000  0.0   
5      cart  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
6      cart  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.666667  0.000000  0.0   
7      cart  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
8      cart  ON,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.333333  0.000000  0.0   

        S-M       S-S  
0  0.133333  0.111111  
1  0.000000  0.000000  
2  0.000000  0.000000  
3  0.500000  0.333333  
4  0.333333  0.333333  
5  0.000000  0.000000  
6  0.000000  0.333333  
7  0.000000  0.000000  
8  0.333333  0.333333
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-380905a7)

```text
S-S       S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
S-S  0.2  0.166667  0.0  0.000000  0.043478  0.0  0.0  0.0  0.0
S-M  0.4  0.500000  0.0  0.000000  0.043478  0.0  0.0  0.0  0.0
M-S  0.0  0.000000  0.0  0.181818  0.043478  0.0  0.0  0.0  0.0
M-M  0.0  0.000000  0.0  0.000000  0.260870  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-807637a3)

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.0  0.000000  0.0  0.0  0.260870  0.0  0.0  0.0  0.0
S-M  0.0  0.000000  0.0  0.0  0.130435  0.0  0.0  0.0  0.0
M-S  0.2  0.000000  0.0  0.0  0.086957  0.0  0.0  0.0  0.0
S-S  0.2  0.166667  0.0  0.0  0.043478  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
