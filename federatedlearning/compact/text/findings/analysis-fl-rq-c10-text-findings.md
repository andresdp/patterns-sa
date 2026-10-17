# Findings: `analysis-fl-rq-c10-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All eight configurations; 10 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c10-text.ipynb](../analysis-fl-rq-c10-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__all-configurations__clients-10__environment-all.md](../boxes/boxes__task-text__all-configurations__clients-10__environment-all.md).
- **Plots:**
- [quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__all-configurations__clients-10__environment-all.png](../plots/feature-importance__task-text__all-configurations__clients-10__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c10-text.ipynb#cell-ddf2adea)

```text
Warning: Some stratification classes have < 2 samples. Falling back to random split.
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000032.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  M,S: 1 (0.37%)
  M,M: 2 (0.73%)
  L,S: 57 (20.88%)
  L,M: 213 (78.02%)

--- Test Set Tradeoff Counts ---
  M,S: 0 (0.00%)
  M,M: 1 (0.85%)
  L,S: 24 (20.51%)
  L,M: 92 (78.63%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c10-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c10-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,OFF,ON --> Tradeoff: L-M
------------------------------
Grouping: client_selector_pattern
  none
------------------------------
Grouping: message_compressor_pattern
  none
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c10-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
* Tradeoff: M-S --> Group: ON,OFF,OFF
* Tradeoff: M-M --> Group: ON,OFF,ON
------------------------------
Grouping: client_selector_pattern
* Tradeoff: M-S --> Group: ON
* Tradeoff: M-M --> Group: ON
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: M-S --> Group: OFF
* Tradeoff: M-M --> Group: OFF
------------------------------
Grouping: hdh_pattern
* Tradeoff: M-S --> Group: OFF
* Tradeoff: M-M --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c10-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.7212
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.7198
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.9063
Robustness Ranking for Tradeoff: M-S

  1. ON,OFF,OFF: 2% success
  2. OFF,OFF,OFF: 0% success
  3. OFF,OFF,ON: 0% success
  Top Policy -> ON,OFF,OFF - Starr: 0.0200 - Regret: 2.9092
Robustness Ranking for Tradeoff: M-M
  1. ON,OFF,ON: 10% success
  2. OFF,OFF,OFF: 0% success
  3. OFF,OFF,ON: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.1000 - Regret: 2.2129
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 3.8476
Robustness Ranking for Tradeoff: L-S

  1. ON,OFF,OFF: 42% success
  2. ON,ON,ON: 33% success
  3. ON,OFF,ON: 27% success
  Top Policy -> ON,OFF,OFF - Starr: 0.4200 - Regret: 0.1878
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 100% success
  2. OFF,ON,OFF: 86% success
  3. OFF,OFF,OFF: 83% success
  Top Policy -> OFF,OFF,ON - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 1.8380
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c10-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 15, 18]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              1             10   
2                      130               3              1             18   
3                       30               1              9             11   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.887                 10.736  
1                                         0.872                 10.997  
2                                         0.870                 10.510  
3                                         0.891                  9.733  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60      0.000                      0.887   
1                    OFF,OFF,ON     50      6.200                      0.840   
                     OFF,ON,OFF     70     10.000                      0.897   
                     ON,OFF,OFF     50      1.000                      0.868   
2                    OFF,ON,ON      50     13.800                      0.869   
                     ON,OFF,ON      30      2.933                      0.831   
                     ON,ON,OFF      50      7.200                      0.893   
3                    ON,ON,ON       30     10.700                      0.891   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 10.736  
1                    OFF,OFF,ON                  13.003  
                     OFF,ON,OFF                  11.443  
                     ON,OFF,OFF                   8.367  
2                    OFF,ON,ON                   11.840  
                     ON,OFF,ON                    9.497  
                     ON,ON,OFF                    9.788  
3                    ON,ON,ON                     9.733
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c10-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M  L-L
policy                                                               
Pattern Instances=0   0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.0
Pattern Instances=1   0.0  0.0  0.0  0.02  0.00  0.0  0.42  0.56  0.0
Pattern Instances=2   0.0  0.0  0.0  0.00  0.06  0.0  0.18  0.76  0.0
Pattern Instances=3   0.0  0.0  0.0  0.00  0.08  0.0  0.25  0.67  0.0
Pattern Instances=4   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=5   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=6   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=8   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=9   0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=10  0.0  0.0  0.0  0.00  0.00  0.0  0.15  0.85  0.0
Pattern Instances=11  0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=12  0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=15  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=18  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
[figure rendered in notebook]
                        S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M  L-L
policy                                                                 
Pattern Types Active=0  0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.0
Pattern Types Active=1  0.0  0.0  0.0  0.01  0.00  0.0  0.18  0.81  0.0
Pattern Types Active=2  0.0  0.0  0.0  0.00  0.02  0.0  0.23  0.75  0.0
Pattern Types Active=3  0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-M  L-S  M-M  M-S
Pattern Count Group                    
0                     50   10    0    0
1                    138   31    0    1
2-3                  117   40    3    0
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x160da4f10>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c10-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.726017        0.013964
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.009641        0.004562
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.103283        0.252644
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
HDH Instances                                   0.000000        0.055743
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.049768        0.000000
JSD Mean                                        0.000000        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.001961
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.081748        0.000000
Pattern Types Active                            0.015102        0.011429
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.014441        0.659697
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c10-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.00
	Alpha Dirichlet Mean: [0.600, 0.675]
	Client Selector Stress Percentage: [35.000, 75.000]
 2. For tradeoff M-M (M,M): lift=0.10
	Alpha Dirichlet Mean: [0.600, 0.825]
	Client Selector Stress Percentage: [35.000, 75.000]
 3. For tradeoff L-S (L,S): lift=0.79
	HDH Instances: [0.000, 4.500]
	delay_percentage: [0.000, 12.500]
 4. For tradeoff L-M (L,M): lift=0.21
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c10-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (7/14), ON (7/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (3/6), ON (3/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.6, 0.675]
  ◦ Client Selector Stress Percentage [35, 75] (%)

PRIM Box 2: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (21/21)
  ◦ HDH: OFF (7/21), ON (14/21)
  ◦ Message Compressor: OFF (21/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: OFF (3/9), ON (6/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.6, 0.825]
  ◦ Client Selector Stress Percentage [35, 75] (%)

PRIM Box 3: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/35), ON (14/35)
  ◦ HDH: OFF (21/35), ON (14/35)
  ◦ Message Compressor: OFF (7/35), ON (28/35)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/15), ON (6/15)
  ◦ HDH: OFF (9/15), ON (6/15)
  ◦ Message Compressor: OFF (3/15), ON (12/15)
• Operating envelope:
  ◦ HDH Instances [0, 4.5]
  ◦ delay percentage [0, 12.5] (%)

PRIM Box 4: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (140/182), ON (42/182)
  ◦ HDH: OFF (98/182), ON (84/182)
  ◦ Message Compressor: OFF (84/182), ON (98/182)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (60/78), ON (18/78)
  ◦ HDH: OFF (42/78), ON (36/78)
  ◦ Message Compressor: OFF (36/78), ON (42/78)
• Operating envelope:
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 37.5] (%)

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (140/182), ON (42/182)
  ◦ HDH: OFF (98/182), ON (84/182)
  ◦ Message Compressor: OFF (84/182), ON (98/182)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (60/78), ON (18/78)
  ◦ HDH: OFF (42/78), ON (36/78)
  ◦ Message Compressor: OFF (36/78), ON (42/78)
• Operating envelope:
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 37.5] (%)

CART Box 2: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/35), ON (14/35)
  ◦ HDH: OFF (21/35), ON (14/35)
  ◦ Message Compressor: OFF (7/35), ON (28/35)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/15), ON (6/15)
  ◦ HDH: OFF (9/15), ON (6/15)
  ◦ Message Compressor: OFF (3/15), ON (12/15)
• Operating envelope:
  ◦ delay percentage [0, 12.5] (%)
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c10-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     117                  0      6              0   
1   PRIM    M-M     117                  1      9              1   
2   PRIM    L-S     117                 24     15             15   
3   PRIM    L-M     117                 92     78             78   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.068   
1          0.009          0.111            0.103                0.088   
2          0.205          1.000            0.795                0.791   
3          0.786          1.000            0.214                0.220   

   test_recall_coverage  
0                   NaN  
1                 1.000  
2                 0.625  
3                 0.848  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     117                 92     78             78   
1   CART    L-S     117                 24     15             15   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.786            1.0            0.214                0.220   
1          0.205            1.0            0.795                0.791   

   test_recall_coverage  
0                 0.848  
1                 0.625
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c10-text.ipynb#cell-6d04057a)

```text
method       policy target  L-L       L-M       L-S  M-L       M-M  M-S  \
0   test set  OFF,OFF,OFF         0.0  0.833333  0.166667  0.0  0.000000  0.0   
1   test set   OFF,OFF,ON         0.0  1.000000  0.000000  0.0  0.000000  0.0   
2   test set   OFF,ON,OFF         0.0  0.857143  0.142857  0.0  0.000000  0.0   
3   test set    OFF,ON,ON         0.0  0.800000  0.200000  0.0  0.000000  0.0   
4   test set   ON,OFF,OFF         0.0  0.600000  0.400000  0.0  0.000000  0.0   
5   test set    ON,OFF,ON         0.0  0.666667  0.222222  0.0  0.111111  0.0   
6   test set    ON,ON,OFF         0.0  0.733333  0.266667  0.0  0.000000  0.0   
7   test set     ON,ON,ON         0.0  0.666667  0.333333  0.0  0.000000  0.0   
8       prim     ON,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
9       prim    ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
10      prim   ON,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
11      prim    ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
12      prim   OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
13      prim   OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
14      prim    OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
15      prim  OFF,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
16      prim   ON,OFF,OFF    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
17      prim     ON,ON,ON    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
18      prim   OFF,ON,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
19      prim   OFF,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
20      prim    OFF,ON,ON    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
21      prim    ON,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
22      prim  OFF,OFF,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
23      prim    ON,ON,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
24      prim  OFF,OFF,OFF    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
25      prim    ON,OFF,ON    M-M  0.0  0.500000  0.333333  0.0  0.166667  0.0   
26      prim   OFF,OFF,ON    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
27      prim     ON,ON,ON    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
28      prim    OFF,ON,ON    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
29      prim   OFF,ON,OFF    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
30      prim   ON,OFF,OFF    M-M  0.0  0.333333  0.666667  0.0  0.000000  0.0   
31      prim    ON,ON,OFF    M-M  0.0  0.000000  0.000000  0.0  0.000000  0.0   
32      prim     ON,ON,ON    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
33      prim    ON,ON,OFF    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
34      prim  OFF,OFF,OFF    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
35      prim   ON,OFF,OFF    M-S  0.0  0.333333  0.666667  0.0  0.000000  0.0   
36      prim   OFF,ON,OFF    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
37      prim   OFF,OFF,ON    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
38      prim    ON,OFF,ON    M-S  0.0  0.000000  0.666667  0.0  0.333333  0.0   
39      prim    OFF,ON,ON    M-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
40      cart  OFF,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
41      cart   OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
42      cart   OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
43      cart    OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
44      cart   ON,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
45      cart    ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
46      cart    ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
47      cart     ON,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.000000  0.0   
48      cart  OFF,OFF,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
49      cart   OFF,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
50      cart   OFF,ON,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
51      cart    OFF,ON,ON    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
52      cart   ON,OFF,OFF    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
53      cart    ON,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.000000  0.0   
54      cart    ON,ON,OFF    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   
55      cart     ON,ON,ON    L-S  0.0  0.000000  1.000000  0.0  0.000000  0.0   

    S-L  S-M  S-S  
0   0.0  0.0  0.0  
1   0.0  0.0  0.0  
2   0.0  0.0  0.0  
3   0.0  0.0  0.0  
4   0.0  0.0  0.0  
5   0.0  0.0  0.0  
6   0.0  0.0  0.0  
7   0.0  0.0  0.0  
8   0.0  0.0  0.0  
9   0.0  0.0  0.0  
10  0.0  0.0  0.0  
11  0.0  0.0  0.0  
12  0.0  0.0  0.0  
13  0.0  0.0  0.0  
14  0.0  0.0  0.0  
15  0.0  0.0  0.0  
16  0.0  0.0  0.0  
17  0.0  0.0  0.0  
18  0.0  0.0  0.0  
19  0.0  0.0  0.0  
20  0.0  0.0  0.0  
21  0.0  0.0  0.0  
22  0.0  0.0  0.0  
23  0.0  0.0  0.0  
24  0.0  0.0  0.0  
25  0.0  0.0  0.0  
26  0.0  0.0  0.0  
27  0.0  0.0  0.0  
28  0.0  0.0  0.0  
29  0.0  0.0  0.0  
30  0.0  0.0  0.0  
31  0.0  0.0  0.0  
32  0.0  0.0  0.0  
33  0.0  0.0  0.0  
34  0.0  0.0  0.0  
35  0.0  0.0  0.0  
36  0.0  0.0  0.0  
37  0.0  0.0  0.0  
38  0.0  0.0  0.0  
39  0.0  0.0  0.0  
40  0.0  0.0  0.0  
41  0.0  0.0  0.0  
42  0.0  0.0  0.0  
43  0.0  0.0  0.0  
44  0.0  0.0  0.0  
45  0.0  0.0  0.0  
46  0.0  0.0  0.0  
47  0.0  0.0  0.0  
48  0.0  0.0  0.0  
49  0.0  0.0  0.0  
50  0.0  0.0  0.0  
51  0.0  0.0  0.0  
52  0.0  0.0  0.0  
53  0.0  0.0  0.0  
54  0.0  0.0  0.0  
55  0.0  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c10-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
M-S  0.0  0.0  0.0  0.0  1.0  0.0  0.166667  0.010870  0.0
M-M  0.0  0.0  0.0  0.0  1.0  0.0  0.166667  0.043478  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.625000  0.000000  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.847826  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c10-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L    L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000  0.847826  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.625  0.000000  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
