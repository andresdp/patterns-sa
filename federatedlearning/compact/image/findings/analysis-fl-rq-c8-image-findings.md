# Findings: `analysis-fl-rq-c8-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All eight configurations; 8 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c8-image.ipynb](../analysis-fl-rq-c8-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__all-configurations__clients-8__environment-all.md](../boxes/boxes__task-image__all-configurations__clients-8__environment-all.md).
- **Plots:**
- [quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__all-configurations__clients-8__environment-all.png](../plots/feature-importance__task-image__all-configurations__clients-8__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c8-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000010.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (4.76%)
  S,M: 73 (26.74%)
  M,S: 42 (15.38%)
  M,M: 145 (53.11%)

--- Test Set Tradeoff Counts ---
  S,S: 6 (5.13%)
  S,M: 31 (26.50%)
  M,S: 18 (15.38%)
  M,M: 62 (52.99%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c8-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c8-image.ipynb#cell-5f75a666)

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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c8-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
* Tradeoff: S-S --> Group: ON
------------------------------
Grouping: message_compressor_pattern
  none
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c8-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,ON: 40% success
  2. ON,OFF,OFF: 10% success
  3. ON,ON,ON: 3% success
  Top Policy -> ON,OFF,ON - Starr: 0.4000 - Regret: 0.4178
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 76% success
  2. OFF,ON,ON: 34% success
  3. OFF,OFF,OFF: 33% success
  Top Policy -> OFF,OFF,ON - Starr: 0.7600 - Regret: 0.1908
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 2.0699
Robustness Ranking for Tradeoff: M-S

  1. ON,ON,ON: 33% success
  2. OFF,ON,ON: 20% success
  3. ON,ON,OFF: 20% success
  Top Policy -> ON,ON,ON - Starr: 0.3333 - Regret: 0.4627
Robustness Ranking for Tradeoff: M-M
  1. ON,ON,OFF: 74% success
  2. OFF,ON,OFF: 71% success
  3. ON,ON,ON: 60% success
  Top Policy -> ON,ON,OFF - Starr: 0.7400 - Regret: 0.4346
Robustness Ranking for Tradeoff: M-L

  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 1.9388
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 5.9940
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 5.9693
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 6.2872
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c8-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 3, 5, 7, 8, 9]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              0              8   
2                      130               3              1              9   
3                       30               1              7              8   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.495                 11.254  
1                                         0.488                 10.763  
2                                         0.491                  9.867  
3                                         0.512                  9.113  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60      0.000                      0.495   
1                    OFF,OFF,ON     50      0.080                      0.453   
                     OFF,ON,OFF     70      8.000                      0.511   
                     ON,OFF,OFF     50      1.000                      0.491   
2                    OFF,ON,ON      50      8.160                      0.490   
                     ON,OFF,ON      30      1.000                      0.457   
                     ON,ON,OFF      50      5.800                      0.513   
3                    ON,ON,ON       30      7.033                      0.512   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 11.254  
1                    OFF,OFF,ON                  11.383  
                     OFF,ON,OFF                  11.651  
                     ON,OFF,OFF                   8.899  
2                    OFF,ON,ON                   10.674  
                     ON,OFF,ON                    8.436  
                     ON,ON,OFF                    9.918  
3                    ON,ON,ON                     9.113
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c8-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0  0.00  0.52  0.0  0.09  0.39  0.0  0.0  0.0  0.0
Pattern Instances=1  0.20  0.23  0.0  0.12  0.45  0.0  0.0  0.0  0.0
Pattern Instances=3  0.10  0.20  0.0  0.00  0.70  0.0  0.0  0.0  0.0
Pattern Instances=5  0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=7  0.02  0.02  0.0  0.32  0.64  0.0  0.0  0.0  0.0
Pattern Instances=8  0.00  0.22  0.0  0.18  0.60  0.0  0.0  0.0  0.0
Pattern Instances=9  0.00  0.25  0.0  0.12  0.62  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.33  0.0  0.17  0.50  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.03  0.34  0.0  0.11  0.52  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.10  0.19  0.0  0.16  0.55  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.03  0.03  0.0  0.33  0.60  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     30   10   20    0
1                     88   19   58    5
2-3                   89   31   26   14
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x16369d090>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c8-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.927944        0.016907
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.003950        0.087136
Client Selector Criteria                        0.000000        0.079254
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.029537        0.000000
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
HDH Instances                                   0.002995        0.000548
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.010870        0.012824
JSD Mean                                        0.000000        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.006564        0.003472
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.000000        0.000000
Pattern Types Active                            0.011048        0.008361
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.007092        0.791499
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c8-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=0.62
	Client Selector Criteria: {CPU}
	CPU Mean: [8.250, 8.875]
	Alpha Dirichlet Mean: [0.625, 0.812]
 2. For tradeoff S-M (S,M): lift=0.74
	Client Selector Criteria: {(not selected)}
	Alpha Dirichlet Mean: [0.625, 0.688]
 3. For tradeoff M-S (M,S): lift=0.85
	Client Selector Criteria: {(not selected)}
	Alpha Dirichlet Mean: [0.688, 0.875]
	delay_percentage: [0.000, 12.500]
 4. For tradeoff M-M (M,M): lift=0.47
	Client Selector Criteria: {(not selected)}
	Alpha Dirichlet Mean: [0.812, 0.875]
	delay_percentage: [12.500, 100.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c8-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (7/14), ON (7/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (3/6), ON (3/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ CPU Mean [8.25, 8.88]
  ◦ Alpha Dirichlet Mean [0.625, 0.812]

PRIM Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (49/49)
  ◦ HDH: OFF (21/49), ON (28/49)
  ◦ Message Compressor: OFF (35/49), ON (14/49)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (9/21), ON (12/21)
  ◦ Message Compressor: OFF (15/21), ON (6/21)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
• Other parameter conditions:
  ◦ Criteria {(not selected)}


PRIM Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (14/21), ON (7/21)
  ◦ Message Compressor: OFF (7/21), ON (14/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: OFF (6/9), ON (3/9)
  ◦ Message Compressor: OFF (3/9), ON (6/9)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.688, 0.875]
  ◦ delay percentage [0, 12.5] (%)
• Other parameter conditions:
  ◦ Criteria {(not selected)}

PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (77/77)
  ◦ HDH: OFF (56/77), ON (21/77)
  ◦ Message Compressor: OFF (28/77), ON (49/77)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (33/33)
  ◦ HDH: OFF (24/33), ON (9/33)
  ◦ Message Compressor: OFF (12/33), ON (21/33)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.812, 0.875]
  ◦ delay percentage [12.5, 100] (%)
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (77/77)
  ◦ HDH: OFF (56/77), ON (21/77)
  ◦ Message Compressor: OFF (28/77), ON (49/77)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (33/33)
  ◦ HDH: OFF (24/33), ON (9/33)
  ◦ Message Compressor: OFF (12/33), ON (21/33)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.813, 0.875]
  ◦ delay percentage [12.5, 100] (%)
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (49/49)
  ◦ HDH: OFF (21/49), ON (28/49)
  ◦ Message Compressor: OFF (35/49), ON (14/49)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (9/21), ON (12/21)
  ◦ Message Compressor: OFF (15/21), ON (6/21)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (14/21), ON (7/21)
  ◦ Message Compressor: OFF (7/21), ON (14/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: OFF (6/9), ON (3/9)
  ◦ Message Compressor: OFF (3/9), ON (6/9)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.813, 0.875]
  ◦ delay percentage [0, 12.5] (%)
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 4: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (7/14), ON (7/14)
  ◦ Message Compressor: OFF (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (3/6), ON (3/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.813]
  ◦ CPU Mean [8.25, 8.88]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c8-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  6      6              4   
1   PRIM    S-M     117                 31     21             21   
2   PRIM    M-S     117                 18      9              9   
3   PRIM    M-M     117                 62     33             33   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.051          0.667            0.615                0.595   
1          0.265          1.000            0.735                0.733   
2          0.154          1.000            0.846                0.846   
3          0.530          1.000            0.470                0.469   

   test_recall_coverage  
0                 0.667  
1                 0.677  
2                 0.500  
3                 0.532  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 62     33             33   
1   CART    S-M     117                 31     21             21   
2   CART    M-S     117                 18      9              9   
3   CART    S-S     117                  6      6              4   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.530          1.000            0.470                0.469   
1          0.265          1.000            0.735                0.733   
2          0.154          1.000            0.846                0.846   
3          0.051          0.667            0.615                0.595   

   test_recall_coverage  
0                 0.532  
1                 0.677  
2                 0.500  
3                 0.667
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c8-image.ipynb#cell-6d04057a)

```text
method       policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,OFF         0.0  0.0  0.0  0.0  0.500000  0.166667  0.0   
1   test set   OFF,OFF,ON         0.0  0.0  0.0  0.0  0.266667  0.000000  0.0   
2   test set   OFF,ON,OFF         0.0  0.0  0.0  0.0  0.714286  0.142857  0.0   
3   test set    OFF,ON,ON         0.0  0.0  0.0  0.0  0.466667  0.200000  0.0   
4   test set   ON,OFF,OFF         0.0  0.0  0.0  0.0  0.466667  0.200000  0.0   
..       ...          ...    ...  ...  ...  ...  ...       ...       ...  ...   
67      cart  OFF,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
68      cart    OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
69      cart   OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
70      cart    ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
71      cart     ON,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   

         S-M       S-S  
0   0.333333  0.000000  
1   0.733333  0.000000  
2   0.142857  0.000000  
3   0.333333  0.000000  
4   0.200000  0.133333  
..       ...       ...  
67  0.000000  0.000000  
68  0.000000  0.000000  
69  0.000000  0.000000  
70  0.000000  0.000000  
71  0.000000  0.000000  

[72 rows x 12 columns]
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c8-image.ipynb#cell-380905a7)

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
S-S  0.666667  0.064516  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
S-M  0.000000  0.677419  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
M-S  0.000000  0.000000  0.0  0.5  0.000000  0.0  0.0  0.0  0.0
M-M  0.000000  0.000000  0.0  0.0  0.532258  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c8-image.ipynb#cell-807637a3)

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.000000  0.000000  0.0  0.0  0.532258  0.0  0.0  0.0  0.0
S-M  0.000000  0.677419  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
M-S  0.000000  0.000000  0.0  0.5  0.000000  0.0  0.0  0.0  0.0
S-S  0.666667  0.064516  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
