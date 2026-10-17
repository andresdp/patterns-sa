# Findings: `analysis-fl-rq-c8-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All eight configurations; 8 clients; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-c8-text.ipynb](../analysis-fl-rq-c8-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__all-configurations__clients-8__environment-all.md](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md).
- **Plots:**
- [quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__all-configurations__clients-8__environment-all.png](../plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-c8-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000034.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  M,S: 4 (1.47%)
  M,M: 1 (0.37%)
  L,S: 53 (19.41%)
  L,M: 215 (78.75%)

--- Test Set Tradeoff Counts ---
  M,S: 1 (0.85%)
  M,M: 1 (0.85%)
  L,S: 23 (19.66%)
  L,M: 92 (78.63%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-c8-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-c8-text.ipynb#cell-5f75a666)

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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-c8-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
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
* Tradeoff: M-M --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-c8-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.0803
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.0732
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 9.2514
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,ON: 13% success
  2. ON,OFF,OFF: 2% success
  3. OFF,OFF,OFF: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.1333 - Regret: 1.8036
Robustness Ranking for Tradeoff: M-M
  1. ON,OFF,ON: 7% success
  2. OFF,OFF,OFF: 0% success
  3. OFF,OFF,ON: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.0667 - Regret: 1.8936
Robustness Ranking for Tradeoff: M-L

  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 3.6129
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 42% success
  2. ON,ON,ON: 33% success
  3. ON,ON,OFF: 22% success
  Top Policy -> ON,OFF,OFF - Starr: 0.4200 - Regret: 0.1617
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 100% success
  2. OFF,ON,OFF: 86% success
  3. OFF,OFF,OFF: 83% success
  Top Policy -> OFF,OFF,ON - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 1.7230
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-c8-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [0, 1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                       60               1              0              0   
1                      170               3              1              8   
2                      130               3              2             14   
3                       30               1              8              9   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.888                 10.949  
1                                         0.872                 11.219  
2                                         0.863                 10.816  
3                                         0.879                 10.089  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF    60      0.000                      0.888   
1                    OFF,OFF,ON     50      4.800                      0.844   
                     OFF,ON,OFF     70      8.000                      0.896   
                     ON,OFF,OFF     50      1.000                      0.866   
2                    OFF,ON,ON      50     11.200                      0.866   
                     ON,OFF,ON      30      2.833                      0.811   
                     ON,ON,OFF      50      5.800                      0.890   
3                    ON,ON,ON       30      8.800                      0.879   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 10.949  
1                    OFF,OFF,ON                  13.740  
                     OFF,ON,OFF                  11.704  
                     ON,OFF,OFF                   8.021  
2                    OFF,ON,ON                   12.347  
                     ON,OFF,ON                   10.034  
                     ON,ON,OFF                    9.753  
3                    ON,ON,ON                    10.089
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-c8-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M  L-L
policy                                                               
Pattern Instances=0   0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.0
Pattern Instances=1   0.0  0.0  0.0  0.02  0.00  0.0  0.42  0.56  0.0
Pattern Instances=2   0.0  0.0  0.0  0.16  0.00  0.0  0.05  0.79  0.0
Pattern Instances=3   0.0  0.0  0.0  0.04  0.07  0.0  0.15  0.74  0.0
Pattern Instances=4   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=5   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=6   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=7   0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=8   0.0  0.0  0.0  0.00  0.00  0.0  0.16  0.84  0.0
Pattern Instances=9   0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=10  0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
Pattern Instances=12  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
Pattern Instances=14  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.0
[figure rendered in notebook]
                        S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M  L-L
policy                                                                 
Pattern Types Active=0  0.0  0.0  0.0  0.00  0.00  0.0  0.17  0.83  0.0
Pattern Types Active=1  0.0  0.0  0.0  0.01  0.00  0.0  0.18  0.81  0.0
Pattern Types Active=2  0.0  0.0  0.0  0.03  0.02  0.0  0.19  0.76  0.0
Pattern Types Active=3  0.0  0.0  0.0  0.00  0.00  0.0  0.33  0.67  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-M  L-S  M-M  M-S
Pattern Count Group                    
0                     50   10    0    0
1                    138   31    0    1
2-3                  119   35    2    4
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x16556c4d0>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-c8-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.573575        0.006634
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.005457        0.006609
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.178100        0.274690
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
HDH Instances                                   0.000000        0.079361
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.109401        0.000000
JSD Mean                                        0.000000        0.000000
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.002961
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.069351        0.000000
Pattern Types Active                            0.043541        0.017956
RAM Mean                                        0.000000        0.000000
delay_percentage                                0.020576        0.611789
low_spec_percentage                             0.000000        0.000000
non_iid_percentage                              0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-c8-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.13
	Alpha Dirichlet Mean: [0.625, 0.812]
	Pattern Instances: [0.000, 3.500]
	Client Selector Stress Percentage: [35.000, 75.000]
 2. For tradeoff M-M (M,M): lift=-0.01
	Alpha Dirichlet Mean: [0.625, 0.688]
	Client Selector Stress Percentage: [35.000, 75.000]
 3. For tradeoff L-S (L,S): lift=0.80
	delay_percentage: [0.000, 12.500]
 4. For tradeoff L-M (L,M): lift=0.21
	delay_percentage: [12.500, 100.000]
	Client Selector Stress Percentage: (not selected) or <= 37.500
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-c8-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (19/19)
  ◦ HDH: OFF (7/19), ON (12/19)
  ◦ Message Compressor: OFF (19/19)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (3/7), ON (4/7)
  ◦ Message Compressor: OFF (7/7)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.625, 0.812]
  ◦ Pattern Instances [0, 3.5]
  ◦ Client Selector Stress Percentage [35, 75] (%)

PRIM Box 2: M-M (M,M)
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
  ◦ Client Selector Stress Percentage [20, 37.5] (%)
  ◦ delay percentage [12.5, 100] (%)

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

CART Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (1/1)
  ◦ HDH: ON (1/1)
  ◦ Message Compressor: OFF (1/1)
• Operating envelope:
  ◦ Client Selector Stress Percentage [62.5, 75] (%)
  ◦ Pattern Instances [0, 2.5]
  ◦ delay percentage [12.5, 37.5] (%)
  ◦ HDH Instances [0.5, 6]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-c8-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     117                  1      7              1   
1   PRIM    M-M     117                  1      6              0   
2   PRIM    L-S     117                 23     15             15   
3   PRIM    L-M     117                 92     78             78   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.009          0.143            0.134                0.196   
1          0.009          0.000           -0.009                0.068   
2          0.197          1.000            0.803                0.806   
3          0.786          1.000            0.214                0.212   

   test_recall_coverage  
0                 1.000  
1                 0.000  
2                 0.652  
3                 0.848  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     117                 92     78             78   
1   CART    L-S     117                 23     15             15   
2   CART    M-S     117                  1      1              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.786            1.0            0.214                0.212   
1          0.197            1.0            0.803                0.806   
2          0.009            0.0           -0.009                0.485   

   test_recall_coverage  
0                 0.848  
1                 0.652  
2                 0.000
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-c8-text.ipynb#cell-6d04057a)

```text
method       policy target  L-L       L-M       L-S  M-L  M-M  M-S  S-L  \
0   test set  OFF,OFF,OFF         0.0  0.833333  0.166667  0.0  0.0  0.0  0.0   
1   test set   OFF,OFF,ON         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
2   test set   OFF,ON,OFF         0.0  0.857143  0.142857  0.0  0.0  0.0  0.0   
3   test set    OFF,ON,ON         0.0  0.800000  0.200000  0.0  0.0  0.0  0.0   
4   test set   ON,OFF,OFF         0.0  0.533333  0.466667  0.0  0.0  0.0  0.0   
..       ...          ...    ...  ...       ...       ...  ...  ...  ...  ...   
59      cart   ON,OFF,OFF    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
60      cart    OFF,ON,ON    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
61      cart   OFF,ON,OFF    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
62      cart    ON,OFF,ON    M-S  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
63      cart     ON,ON,ON    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   

    S-M  S-S  
0   0.0  0.0  
1   0.0  0.0  
2   0.0  0.0  
3   0.0  0.0  
4   0.0  0.0  
..  ...  ...  
59  0.0  0.0  
60  0.0  0.0  
61  0.0  0.0  
62  0.0  0.0  
63  0.0  0.0  

[64 rows x 12 columns]
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-c8-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
M-S  0.0  0.0  0.0  1.0  1.0  0.0  0.086957  0.032609  0.0
M-M  0.0  0.0  0.0  1.0  0.0  0.0  0.086957  0.032609  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.652174  0.000000  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.847826  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-c8-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.847826  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.652174  0.000000  0.0
M-S  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.010870  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
