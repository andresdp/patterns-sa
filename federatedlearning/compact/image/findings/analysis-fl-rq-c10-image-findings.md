# Findings: `analysis-fl-rq-c10-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All eight configurations; 10 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c10-image.ipynb](../analysis-fl-rq-c10-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__all-configurations__clients-10__environment-all.md](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md).
- **Plots:**
- [quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__all-configurations__clients-10__environment-all.png](../plots/feature-importance__task-image__all-configurations__clients-10__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c10-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000028.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (4.76%)
  S,M: 76 (27.84%)
  M,S: 38 (13.92%)
  M,M: 146 (53.48%)

--- Test Set Tradeoff Counts ---
  S,S: 6 (5.13%)
  S,M: 33 (28.21%)
  M,S: 16 (13.68%)
  M,M: 62 (52.99%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c10-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c10-image.ipynb#cell-5f75a666)

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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c10-image.ipynb#cell-505c4983)

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

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c10-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,ON: 33% success
  2. ON,OFF,OFF: 16% success
  3. ON,ON,OFF: 2% success
  Top Policy -> ON,OFF,ON - Starr: 0.3333 - Regret: 0.3637
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 80% success
  2. OFF,ON,ON: 40% success
  3. OFF,OFF,OFF: 33% success
  Top Policy -> OFF,OFF,ON - Starr: 0.8000 - Regret: 0.1280
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 2.0199
Robustness Ranking for Tradeoff: M-S

  1. ON,ON,ON: 33% success
  2. OFF,ON,ON: 20% success
  3. ON,ON,OFF: 20% success
  Top Policy -> ON,ON,ON - Starr: 0.3333 - Regret: 0.4910
Robustness Ranking for Tradeoff: M-M
  1. ON,ON,OFF: 74% success
  2. OFF,ON,OFF: 71% success
  3. ON,ON,ON: 67% success
  Top Policy -> ON,ON,OFF - Starr: 0.7400 - Regret: 0.3772
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 2.1096
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 5.6763
Robustness Ranking for Tradeoff: L-M

  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 5.6712
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 6.0297
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c10-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 3, 6, 9, 10, 11]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              0             10   
2                      130               3              1             11   
3                       30               1              9             10   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.479                 10.955  
1                                         0.474                 10.668  
2                                         0.483                  9.916  
3                                         0.506                  9.110  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60      0.000                      0.479   
1                    OFF,OFF,ON     50      0.000                      0.433   
                     OFF,ON,OFF     70     10.000                      0.500   
                     ON,OFF,OFF     50      1.000                      0.477   
2                    OFF,ON,ON      50     10.020                      0.475   
                     ON,OFF,ON      30      1.000                      0.450   
                     ON,ON,OFF      50      7.200                      0.509   
3                    ON,ON,ON       30      9.033                      0.506   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 10.955  
1                    OFF,OFF,ON                  11.383  
                     OFF,ON,OFF                  11.328  
                     ON,OFF,OFF                   9.027  
2                    OFF,ON,ON                   10.442  
                     ON,OFF,ON                    8.868  
                     ON,ON,OFF                   10.019  
3                    ON,ON,ON                     9.110
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c10-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                               
Pattern Instances=0   0.00  0.55  0.0  0.09  0.36  0.0  0.0  0.0  0.0
Pattern Instances=1   0.22  0.21  0.0  0.05  0.51  0.0  0.0  0.0  0.0
Pattern Instances=3   0.10  0.20  0.0  0.00  0.70  0.0  0.0  0.0  0.0
Pattern Instances=6   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=9   0.00  0.00  0.0  0.32  0.68  0.0  0.0  0.0  0.0
Pattern Instances=10  0.00  0.24  0.0  0.18  0.58  0.0  0.0  0.0  0.0
Pattern Instances=11  0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.33  0.0  0.17  0.50  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.05  0.35  0.0  0.08  0.52  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.08  0.22  0.0  0.15  0.54  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.00  0.00  0.0  0.33  0.67  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     30   10   20    0
1                     88   14   60    8
2-3                   90   30   29   11
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x1656010d0>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c10-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.851260        0.010940
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.003892        0.000493
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.048093        0.195298
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
HDH Instances                                   0.000040        0.000005
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.000000        0.007698
JSD Mean                                        0.080682        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.003896        0.000373
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.000000        0.000000
Pattern Types Active                            0.007464        0.003054
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.004674        0.782139
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c10-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=0.45
	Alpha Dirichlet Mean: [0.600, 0.675]
	Client Selector Stress Percentage: [22.500, 75.000]
 2. For tradeoff S-M (S,M): lift=0.72
	Alpha Dirichlet Mean: [0.600, 0.825]
	Client Selector Stress Percentage: (not selected) or <= 35.000
 3. For tradeoff M-S (M,S): lift=0.86
	Alpha Dirichlet Mean: [0.825, 0.900]
	delay_percentage: [0.000, 12.500]
 4. For tradeoff M-M (M,M): lift=0.47
	Alpha Dirichlet Mean: [0.675, 0.900]
	JSD Mean: (not selected) or <= 0.013
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c10-image.ipynb#cell-5487f837)

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
  ◦ Alpha Dirichlet Mean [0.6, 0.675]
  ◦ Client Selector Stress Percentage [22.5, 75] (%)


PRIM Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (63/63)
  ◦ HDH: OFF (21/63), ON (42/63)
  ◦ Message Compressor: OFF (42/63), ON (21/63)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (27/27)
  ◦ HDH: OFF (9/27), ON (18/27)
  ◦ Message Compressor: OFF (18/27), ON (9/27)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.6, 0.825]
  ◦ Client Selector Stress Percentage [20, 35] (%)


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
  ◦ Alpha Dirichlet Mean [0.825, 0.9]
  ◦ delay percentage [0, 12.5] (%)

PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (77/119), ON (42/119)
  ◦ HDH: OFF (77/119), ON (42/119)
  ◦ Message Compressor: OFF (42/119), ON (77/119)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (33/51), ON (18/51)
  ◦ HDH: OFF (33/51), ON (18/51)
  ◦ Message Compressor: OFF (18/51), ON (33/51)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.675, 0.9]
  ◦ JSD Mean [-0.01, 0.0131]
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 37.5] (%)


CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (77/119), ON (42/119)
  ◦ HDH: OFF (77/119), ON (42/119)
  ◦ Message Compressor: OFF (42/119), ON (77/119)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (33/51), ON (18/51)
  ◦ HDH: OFF (33/51), ON (18/51)
  ◦ Message Compressor: OFF (18/51), ON (33/51)
• Operating envelope:
  ◦ Client Selector Stress Percentage [20, 37.5] (%)
  ◦ Alpha Dirichlet Mean [0.825, 0.9]
  ◦ delay percentage [12.5, 100] (%)

CART Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (63/63)
  ◦ HDH: OFF (21/63), ON (42/63)
  ◦ Message Compressor: OFF (42/63), ON (21/63)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (27/27)
  ◦ HDH: OFF (9/27), ON (18/27)
  ◦ Message Compressor: OFF (18/27), ON (9/27)
• Operating envelope:
  ◦ Client Selector Stress Percentage [20, 35] (%)
  ◦ Alpha Dirichlet Mean [0.6, 0.825]

CART Box 3: M-S (M,S)
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
  ◦ Alpha Dirichlet Mean [0.825, 0.9]
  ◦ delay percentage [0, 12.5] (%)

CART Box 4: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (8/8)
  ◦ HDH: OFF (7/8), ON (1/8)
  ◦ Message Compressor: OFF (8/8)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ Client Selector Stress Percentage [62.5, 75] (%)
  ◦ Alpha Dirichlet Mean [0.6, 0.825]
  ◦ JSD Mean [-0.01, 0.01]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c10-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  6      6              3   
1   PRIM    S-M     117                 33     27             27   
2   PRIM    M-S     117                 16     15             15   
3   PRIM    M-M     117                 62     51             51   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.051            0.5            0.449                0.667   
1          0.282            1.0            0.718                0.722   
2          0.137            1.0            0.863                0.861   
3          0.530            1.0            0.470                0.465   

   test_recall_coverage  
0                 0.500  
1                 0.818  
2                 0.938  
3                 0.823  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 62     51             51   
1   CART    S-M     117                 33     27             27   
2   CART    M-S     117                 16     15             15   
3   CART    S-S     117                  6      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.530          1.000            0.470                0.465   
1          0.282          1.000            0.718                0.722   
2          0.137          1.000            0.863                0.861   
3          0.051          0.333            0.282                0.452   

   test_recall_coverage  
0                 0.823  
1                 0.818  
2                 0.938  
3                 0.167
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c10-image.ipynb#cell-6d04057a)

```text
method       policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,OFF         0.0  0.0  0.0  0.0  0.500000  0.166667  0.0   
1   test set   OFF,OFF,ON         0.0  0.0  0.0  0.0  0.200000  0.000000  0.0   
2   test set   OFF,ON,OFF         0.0  0.0  0.0  0.0  0.714286  0.142857  0.0   
3   test set    OFF,ON,ON         0.0  0.0  0.0  0.0  0.400000  0.200000  0.0   
4   test set   ON,OFF,OFF         0.0  0.0  0.0  0.0  0.600000  0.066667  0.0   
..       ...          ...    ...  ...  ...  ...  ...       ...       ...  ...   
67      cart  OFF,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
68      cart    OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
69      cart   OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
70      cart    ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
71      cart     ON,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   

         S-M       S-S  
0   0.333333  0.000000  
1   0.800000  0.000000  
2   0.142857  0.000000  
3   0.400000  0.000000  
4   0.200000  0.133333  
..       ...       ...  
67  0.000000  0.000000  
68  0.000000  0.000000  
69  0.000000  0.000000  
70  0.000000  0.000000  
71  0.000000  0.000000  

[72 rows x 12 columns]
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c10-image.ipynb#cell-380905a7)

```text
S-S       S-M  S-L     M-S       M-M  M-L  L-S  L-M  L-L
S-S  0.5  0.090909  0.0  0.0000  0.000000  0.0  0.0  0.0  0.0
S-M  0.0  0.818182  0.0  0.0000  0.000000  0.0  0.0  0.0  0.0
M-S  0.0  0.000000  0.0  0.9375  0.000000  0.0  0.0  0.0  0.0
M-M  0.0  0.000000  0.0  0.0000  0.822581  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c10-image.ipynb#cell-807637a3)

```text
S-S       S-M  S-L     M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.000000  0.000000  0.0  0.0000  0.822581  0.0  0.0  0.0  0.0
S-M  0.000000  0.818182  0.0  0.0000  0.000000  0.0  0.0  0.0  0.0
M-S  0.000000  0.000000  0.0  0.9375  0.000000  0.0  0.0  0.0  0.0
S-S  0.166667  0.060606  0.0  0.0000  0.000000  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
