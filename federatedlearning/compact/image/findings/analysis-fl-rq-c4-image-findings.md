# Findings: `analysis-fl-rq-c4-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All eight configurations; 4 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c4-image.ipynb](../analysis-fl-rq-c4-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__all-configurations__clients-4__environment-all.md](../boxes/boxes__task-image__all-configurations__clients-4__environment-all.md).
- **Plots:**
- [quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__all-configurations__clients-4__environment-all.png](../plots/feature-importance__task-image__all-configurations__clients-4__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c4-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000088.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 8 (2.93%)
  S,M: 10 (3.66%)
  M,S: 68 (24.91%)
  M,M: 187 (68.50%)

--- Test Set Tradeoff Counts ---
  S,S: 4 (3.42%)
  S,M: 4 (3.42%)
  M,S: 30 (25.64%)
  M,M: 79 (67.52%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c4-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c4-image.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
  none
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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c4-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
  none
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: S-S --> Group: OFF
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c4-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,ON: 17% success
  2. ON,OFF,OFF: 10% success
  3. OFF,OFF,ON: 4% success
  Top Policy -> ON,OFF,ON - Starr: 0.1667 - Regret: 1.2807
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 8% success
  2. OFF,OFF,OFF: 7% success
  3. OFF,ON,ON: 4% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0800 - Regret: 1.0330
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 2.3470
Robustness Ranking for Tradeoff: M-S
  1. ON,ON,ON: 47% success
  2. ON,OFF,OFF: 46% success
  3. ON,OFF,ON: 43% success
  Top Policy -> ON,ON,ON - Starr: 0.4667 - Regret: 0.5568
Robustness Ranking for Tradeoff: M-M
  1. OFF,OFF,ON: 86% success
  2. OFF,ON,OFF: 83% success
  3. OFF,OFF,OFF: 77% success
  Top Policy -> OFF,OFF,ON - Starr: 0.8600 - Regret: 0.0573
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 1.2383
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 4.9711
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 4.8518
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 5.0682
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c4-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 2, 3, 4, 5, 6]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              0              4   
2                      130               3              1              6   
3                       30               1              4              4   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.551                 12.795  
1                                         0.542                 11.434  
2                                         0.547                 10.365  
3                                         0.577                  9.777  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60       0.00                      0.551   
1                    OFF,OFF,ON     50       0.36                      0.517   
                     OFF,ON,OFF     70       4.00                      0.566   
                     ON,OFF,OFF     50       1.00                      0.534   
2                    OFF,ON,ON      50       4.30                      0.552   
                     ON,OFF,ON      30       1.00                      0.517   
                     ON,ON,OFF      50       3.40                      0.560   
3                    ON,ON,ON       30       4.00                      0.577   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 12.795  
1                    OFF,OFF,ON                  11.915  
                     OFF,ON,OFF                  13.217  
                     ON,OFF,OFF                   8.456  
2                    OFF,ON,ON                   11.912  
                     ON,OFF,ON                    7.333  
                     ON,ON,OFF                   10.637  
3                    ON,ON,ON                     9.777
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c4-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0  0.02  0.06  0.0  0.11  0.80  0.0  0.0  0.0  0.0
Pattern Instances=1  0.11  0.03  0.0  0.40  0.46  0.0  0.0  0.0  0.0
Pattern Instances=2  0.00  0.07  0.0  0.14  0.79  0.0  0.0  0.0  0.0
Pattern Instances=3  0.00  0.00  0.0  0.20  0.80  0.0  0.0  0.0  0.0
Pattern Instances=4  0.00  0.01  0.0  0.28  0.71  0.0  0.0  0.0  0.0
Pattern Instances=5  0.00  0.18  0.0  0.00  0.82  0.0  0.0  0.0  0.0
Pattern Instances=6  0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.07  0.0  0.17  0.77  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.04  0.04  0.0  0.20  0.72  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.04  0.02  0.0  0.31  0.63  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.00  0.00  0.0  0.47  0.53  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     46   10    4    0
1                    122   34    7    7
2-3                   98   54    3    5
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x168547610>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c4-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.732463        0.013870
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.005010        0.012864
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.133201        0.269801
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
HDH Instances                                   0.002330        0.001561
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.000000        0.000000
JSD Mean                                        0.107538        0.064095
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.005363
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.006285        0.000000
Pattern Types Active                            0.005494        0.011427
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.007680        0.621019
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c4-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=0.63
	Alpha Dirichlet Mean: [0.625, 0.688]
	Client Selector Stress Percentage: [35.000, 75.000]
 2. For tradeoff S-M (S,M): lift=0.30
	Alpha Dirichlet Mean: [0.625, 0.688]
	JSD Mean: (not selected) or <= 0.027
	delay_percentage: [0.000, 50.000]
	Client Selector Stress Percentage: (not selected) or <= 47.500
 3. For tradeoff M-S (M,S): lift=0.74
	JSD Mean: (not selected) or <= 0.019
	delay_percentage: [0.000, 12.500]
 4. For tradeoff M-M (M,M): lift=0.32
	Alpha Dirichlet Mean: [0.688, 0.875]
	JSD Mean: (not selected) or <= 0.019
	delay_percentage: [37.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 22.500
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c4-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-S (S,S)
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
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ Client Selector Stress Percentage [35, 75] (%)

PRIM Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (17/17)
  ◦ HDH: OFF (7/17), ON (10/17)
  ◦ Message Compressor: OFF (17/17)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ JSD Mean [-0.006, 0.0275]
  ◦ delay percentage [0, 50] (%)
  ◦ Client Selector Stress Percentage [20, 47.5] (%)

PRIM Box 3: M-S (M,S)
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
  ◦ JSD Mean [-0.006, 0.0188]
  ◦ delay percentage [0, 12.5] (%)

PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (55/55)
  ◦ HDH: OFF (42/55), ON (13/55)
  ◦ Message Compressor: OFF (14/55), ON (41/55)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (22/22)
  ◦ HDH: OFF (18/22), ON (4/22)
  ◦ Message Compressor: OFF (6/22), ON (16/22)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.688, 0.875]
  ◦ JSD Mean [-0.006, 0.0188]
  ◦ delay percentage [37.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 22.5] (%)

CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (56/56)
  ◦ HDH: OFF (56/56)
  ◦ Message Compressor: OFF (21/56), ON (35/56)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (24/24)
  ◦ HDH: OFF (24/24)
  ◦ Message Compressor: OFF (9/24), ON (15/24)
• Operating envelope:
  ◦ JSD Mean [-0.006, -0.00299]
  ◦ Alpha Dirichlet Mean [0.688, 0.875]
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 22.5] (%)

CART Box 2: M-S (M,S)
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

CART Box 3: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (2/2)
  ◦ HDH: ON (2/2)
  ◦ Message Compressor: OFF (2/2)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: no matching rows
  ◦ HDH: no matching rows
  ◦ Message Compressor: no matching rows
• Operating envelope:
  ◦ JSD Mean [0.0188, 0.0275]
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ delay percentage [12.5, 50] (%)
  ◦ Client Selector Stress Percentage [20, 22.5] (%)

CART Box 4: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (2/2)
  ◦ HDH: ON (2/2)
  ◦ Message Compressor: OFF (2/2)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: no matching rows
  ◦ HDH: no matching rows
  ◦ Message Compressor: no matching rows
• Operating envelope:
  ◦ JSD Mean [0.01, 0.035]
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [37.5, 75] (%)
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c4-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  4      6              4   
1   PRIM    S-M     117                  4      3              1   
2   PRIM    M-S     117                 30     15             15   
3   PRIM    M-M     117                 79     22             22   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.034          0.667            0.632                0.399   
1          0.034          0.333            0.299                0.199   
2          0.256          1.000            0.744                0.751   
3          0.675          1.000            0.325                0.315   

   test_recall_coverage  
0                 1.000  
1                 0.250  
2                 0.500  
3                 0.278  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 79     24             24   
1   CART    M-S     117                 30     15             15   
2   CART    S-M     117                  4      0              0   
3   CART    S-S     117                  4      0              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.675            1.0            0.325                0.315   
1          0.256            1.0            0.744                0.751   
2          0.034            NaN              NaN                0.963   
3          0.034            NaN              NaN                0.971   

   test_recall_coverage  
0                 0.304  
1                 0.500  
2                 0.000  
3                 0.000
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c4-image.ipynb#cell-6d04057a)

```text
method       policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,OFF         0.0  0.0  0.0  0.0  0.777778  0.166667  0.0   
1   test set   OFF,OFF,ON         0.0  0.0  0.0  0.0  0.933333  0.000000  0.0   
2   test set   OFF,ON,OFF         0.0  0.0  0.0  0.0  0.809524  0.142857  0.0   
3   test set    OFF,ON,ON         0.0  0.0  0.0  0.0  0.733333  0.200000  0.0   
4   test set   ON,OFF,OFF         0.0  0.0  0.0  0.0  0.333333  0.533333  0.0   
..       ...          ...    ...  ...  ...  ...  ...       ...       ...  ...   
67      cart  OFF,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
68      cart    OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
69      cart   OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
70      cart    ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
71      cart     ON,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   

         S-M       S-S  
0   0.055556  0.000000  
1   0.066667  0.000000  
2   0.047619  0.000000  
3   0.066667  0.000000  
4   0.000000  0.133333  
..       ...       ...  
67  0.000000  0.000000  
68  0.000000  0.000000  
69  0.000000  0.000000  
70  0.000000  0.000000  
71  0.000000  0.000000  

[72 rows x 12 columns]
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c4-image.ipynb#cell-380905a7)

```text
S-S   S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
S-S  1.0  0.00  0.0  0.066667  0.000000  0.0  0.0  0.0  0.0
S-M  0.0  0.25  0.0  0.000000  0.025316  0.0  0.0  0.0  0.0
M-S  0.0  0.00  0.0  0.500000  0.000000  0.0  0.0  0.0  0.0
M-M  0.0  0.00  0.0  0.000000  0.278481  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c4-image.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.0  0.0  0.0  0.0  0.303797  0.0  0.0  0.0  0.0
M-S  0.0  0.0  0.0  0.5  0.000000  0.0  0.0  0.0  0.0
S-M  0.0  0.0  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
S-S  0.0  0.0  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
