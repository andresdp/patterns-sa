# Findings: `analysis-fl-rq-c4-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All eight configurations; 4 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c4-text.ipynb](../analysis-fl-rq-c4-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__all-configurations__clients-4__environment-all.md](../boxes/boxes__task-text__all-configurations__clients-4__environment-all.md).
- **Plots:**
- [quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__all-configurations__clients-4__environment-all.png](../plots/feature-importance__task-text__all-configurations__clients-4__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c4-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000257.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  M,S: 3 (1.10%)
  M,M: 5 (1.83%)
  L,S: 69 (25.27%)
  L,M: 184 (67.40%)
  L,L: 12 (4.40%)

--- Test Set Tradeoff Counts ---
  M,S: 2 (1.71%)
  M,M: 0 (0.00%)
  L,S: 31 (26.50%)
  L,M: 79 (67.52%)
  L,L: 5 (4.27%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c4-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c4-text.ipynb#cell-5f75a666)

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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c4-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
* Tradeoff: M-S --> Group: ON
* Tradeoff: L-L --> Group: OFF
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: M-S --> Group: OFF
------------------------------
Grouping: hdh_pattern
* Tradeoff: M-M --> Group: ON
* Tradeoff: L-L --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c4-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 7.8507
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 7.8135
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 7.9211
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,ON: 10% success
  2. ON,OFF,OFF: 4% success
  3. OFF,OFF,OFF: 0% success

  Top Policy -> ON,OFF,ON - Starr: 0.1000 - Regret: 1.9913
Robustness Ranking for Tradeoff: M-M
  1. OFF,OFF,ON: 6% success
  2. ON,OFF,ON: 3% success
  3. OFF,ON,ON: 2% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0600 - Regret: 1.8522
Robustness Ranking for Tradeoff: M-L

  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 3.0316
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 52% success
  2. ON,OFF,ON: 47% success
  3. ON,ON,ON: 43% success
  Top Policy -> ON,OFF,OFF - Starr: 0.5200 - Regret: 0.3086
Robustness Ranking for Tradeoff: L-M
  1. OFF,ON,OFF: 86% success
  2. OFF,OFF,OFF: 83% success
  3. OFF,OFF,ON: 76% success
  Top Policy -> OFF,ON,OFF - Starr: 0.8571 - Regret: 0.1140
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 18% success
  2. OFF,ON,ON: 16% success
  3. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.1800 - Regret: 0.6169
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c4-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 2, 3, 4, 5, 6, 7]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              1              4   
2                      130               3              1              7   
3                       30               1              4              5   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.892                 12.172  
1                                         0.872                 11.870  
2                                         0.875                 10.922  
3                                         0.905                  9.683  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60      0.000                      0.892   
1                    OFF,OFF,ON     50      2.400                      0.842   
                     OFF,ON,OFF     70      4.000                      0.903   
                     ON,OFF,OFF     50      1.000                      0.856   
2                    OFF,ON,ON      50      5.600                      0.882   
                     ON,OFF,ON      30      1.867                      0.834   
                     ON,ON,OFF      50      3.400                      0.892   
3                    ON,ON,ON       30      4.900                      0.905   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 12.172  
1                    OFF,OFF,ON                  15.257  
                     OFF,ON,OFF                  12.923  
                     ON,OFF,OFF                   7.008  
2                    OFF,ON,ON                   13.349  
                     ON,OFF,ON                    8.660  
                     ON,ON,OFF                    9.852  
3                    ON,ON,ON                     9.683
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c4-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M   L-L
policy                                                               
Pattern Instances=0  0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.00
Pattern Instances=1  0.0  0.0  0.0  0.03  0.00  0.0  0.45  0.52  0.00
Pattern Instances=2  0.0  0.0  0.0  0.07  0.02  0.0  0.24  0.67  0.00
Pattern Instances=3  0.0  0.0  0.0  0.00  0.07  0.0  0.10  0.62  0.21
Pattern Instances=4  0.0  0.0  0.0  0.00  0.00  0.0  0.23  0.77  0.00
Pattern Instances=5  0.0  0.0  0.0  0.00  0.00  0.0  0.39  0.61  0.00
Pattern Instances=6  0.0  0.0  0.0  0.00  0.00  0.0  0.00  0.90  0.10
Pattern Instances=7  0.0  0.0  0.0  0.00  0.10  0.0  0.00  0.20  0.70
[figure rendered in notebook]
                        S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M   L-L
policy                                                                  
Pattern Types Active=0  0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.00
Pattern Types Active=1  0.0  0.0  0.0  0.01  0.02  0.0  0.21  0.71  0.05
Pattern Types Active=2  0.0  0.0  0.0  0.02  0.02  0.0  0.32  0.58  0.06
Pattern Types Active=3  0.0  0.0  0.0  0.00  0.00  0.0  0.43  0.57  0.00
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-L  L-M  L-S  M-M  M-S
Pattern Count Group                         
0                      0   50   10    0    0
1                      9  120   36    3    2
2-3                    8   93   54    2    3
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x163cc7d50>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c4-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.590083        0.013295
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.008907        0.011914
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.233023        0.356109
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
HDH Instances                                   0.000000        0.134361
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.066078        0.000000
JSD Mean                                        0.000000        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.045067
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.074255        0.000000
Pattern Types Active                            0.021267        0.015477
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.006386        0.423777
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c4-text.ipynb#cell-914700be)

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

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c4-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-S (M,S)
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
  ◦ Alpha Dirichlet Mean [0.625, 0.812]
  ◦ Client Selector Stress Percentage [35, 75] (%)

PRIM Box 2: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (28/32), ON (4/32)
  ◦ HDH: ON (32/32)
  ◦ Message Compressor: OFF (25/32), ON (7/32)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (12/14), ON (2/14)
  ◦ HDH: ON (14/14)
  ◦ Message Compressor: OFF (11/14), ON (3/14)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ HDH Instances [0.5, 3]

PRIM Box 3: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: OFF (7/14), ON (7/14)
  ◦ Message Compressor: ON (14/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: OFF (3/6), ON (3/6)
  ◦ Message Compressor: ON (6/6)
• Operating envelope:
  ◦ delay percentage [0, 12.5] (%)
  ◦ Client Selector Stress Percentage [22.5, 75] (%)

PRIM Box 4: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (105/105)
  ◦ HDH: OFF (77/105), ON (28/105)
  ◦ Message Compressor: OFF (49/105), ON (56/105)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (45/45)
  ◦ HDH: OFF (33/45), ON (12/45)
  ◦ Message Compressor: OFF (21/45), ON (24/45)
• Operating envelope:
  ◦ Pattern Instances [0, 5.5]
  ◦ HDH Instances [0, 2.5]
  ◦ delay percentage [12.5, 100] (%)
  ◦ Client Selector Stress Percentage [20, 22.5] (%)

PRIM Box 5: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (28/28)
  ◦ HDH: ON (28/28)
  ◦ Message Compressor: OFF (21/28), ON (7/28)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (12/12)
  ◦ HDH: ON (12/12)
  ◦ Message Compressor: OFF (9/12), ON (3/12)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.688]
  ◦ Pattern Instances [2.5, 7]
  ◦ HDH Instances [0.5, 3]

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (105/105)
  ◦ HDH: OFF (77/105), ON (28/105)
  ◦ Message Compressor: OFF (49/105), ON (56/105)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (45/45)
  ◦ HDH: OFF (33/45), ON (12/45)
  ◦ Message Compressor: OFF (21/45), ON (24/45)
• Operating envelope:
  ◦ Client Selector Stress Percentage [20, 22.5] (%)
  ◦ delay percentage [12.5, 100] (%)
  ◦ Pattern Instances [0, 5.5]
  ◦ HDH Stress Percentage [20, 62.5] (%)

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

CART Box 3: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (7/7)
  ◦ HDH: ON (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (3/3)
  ◦ HDH: ON (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ Client Selector Stress Percentage [20, 62.5] (%)
  ◦ delay percentage [50, 100] (%)
  ◦ Pattern Instances [0, 5]
  ◦ HDH Stress Percentage [62.5, 75] (%)
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c4-text.ipynb#cell-heldout-box-summary-all)

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

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c4-text.ipynb#cell-6d04057a)

```text
method       policy target       L-L       L-M       L-S  M-L  M-M  \
0   test set  OFF,OFF,OFF         0.000000  0.833333  0.166667  0.0  0.0   
1   test set   OFF,OFF,ON         0.133333  0.866667  0.000000  0.0  0.0   
2   test set   OFF,ON,OFF         0.000000  0.857143  0.142857  0.0  0.0   
3   test set    OFF,ON,ON         0.200000  0.600000  0.200000  0.0  0.0   
4   test set   ON,OFF,OFF         0.000000  0.400000  0.533333  0.0  0.0   
..       ...          ...    ...       ...       ...       ...  ...  ...   
67      cart    ON,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.0   
68      cart   OFF,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.0   
69      cart  OFF,OFF,OFF    L-S  0.000000  0.000000  1.000000  0.0  0.0   
70      cart    ON,ON,OFF    L-S  0.000000  0.000000  1.000000  0.0  0.0   
71      cart     ON,ON,ON    L-S  0.000000  0.000000  1.000000  0.0  0.0   

         M-S  S-L  S-M  S-S  
0   0.000000  0.0  0.0  0.0  
1   0.000000  0.0  0.0  0.0  
2   0.000000  0.0  0.0  0.0  
3   0.000000  0.0  0.0  0.0  
4   0.066667  0.0  0.0  0.0  
..       ...  ...  ...  ...  
67  0.000000  0.0  0.0  0.0  
68  0.000000  0.0  0.0  0.0  
69  0.000000  0.0  0.0  0.0  
70  0.000000  0.0  0.0  0.0  
71  0.000000  0.0  0.0  0.0  

[72 rows x 12 columns]
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c4-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
M-S  0.0  0.0  0.0  1.0  0.0  0.0  0.193548  0.012658  0.0
M-M  0.0  0.0  0.0  0.5  0.0  0.0  0.032258  0.088608  1.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.193548  0.000000  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.569620  0.0
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.088608  1.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c4-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.569620  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.483871  0.000000  0.0
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.012658  0.4
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
