# Findings: `analysis-fl-rq-combined-patterns-stress-75-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All supported non-empty pattern configurations at common 75% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-75-image.ipynb](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__combined-patterns__clients-all__stress-75__environment-all.md](../boxes/boxes__task-image__combined-patterns__clients-all__stress-75__environment-all.md).
- **Plots:**
- [quality-space__task-image__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__combined-patterns__clients-all__stress-75__environment-all.png](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-75__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000084.
Data split: 252 train, 108 test.

--- Train Set Tradeoff Counts ---
  S,S: 30 (11.90%)
  S,M: 95 (37.70%)
  M,S: 21 (8.33%)
  M,M: 106 (42.06%)

--- Test Set Tradeoff Counts ---
  S,S: 14 (12.96%)
  S,M: 40 (37.04%)
  M,S: 9 (8.33%)
  M,M: 45 (41.67%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-5f75a666)

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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
* Tradeoff: M-S --> Group: ON
------------------------------
Grouping: message_compressor_pattern
  none
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,ON: 73% success
  2. ON,OFF,OFF: 20% success
  3. ON,ON,OFF: 7% success
  Top Policy -> ON,OFF,ON - Starr: 0.7333 - Regret: 0.1612
Robustness Ranking for Tradeoff: S-M
  1. OFF,ON,ON: 73% success
  2. OFF,OFF,ON: 71% success
  3. OFF,ON,OFF: 24% success
  Top Policy -> OFF,ON,ON - Starr: 0.7333 - Regret: 0.0866
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 1.8044
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,OFF: 27% success
  2. ON,OFF,ON: 13% success
  3. ON,ON,OFF: 7% success
  Top Policy -> ON,OFF,OFF - Starr: 0.2667 - Regret: 0.5556
Robustness Ranking for Tradeoff: M-M
  1. OFF,ON,OFF: 76% success
  2. ON,ON,OFF: 73% success
  3. ON,OFF,OFF: 31% success
  Top Policy -> OFF,ON,OFF - Starr: 0.7556 - Regret: 0.2376
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.0122
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 5.5655
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 5.5237
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 5.8169
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2]
Pattern Instances: varies in these runs, values [0, 1, 2, 3, 4, 5, 6, 8, 9, 10, 11]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                      270               3              0             10   
2                       90               3              1             11   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.476                 10.942  
2                                         0.457                  9.576  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    90      0.211                      0.442   
                     OFF,ON,OFF    90      7.333                      0.507   
                     ON,OFF,OFF    90      1.000                      0.480   
2                    OFF,ON,ON     30      7.733                      0.442   
                     ON,OFF,ON     30      1.000                      0.428   
                     ON,ON,OFF     30      2.667                      0.502   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 11.439  
                     OFF,ON,OFF                 13.543  
                     ON,OFF,OFF                  7.844  
2                    OFF,ON,ON                  12.721  
                     ON,OFF,ON                   5.343  
                     ON,ON,OFF                  10.662
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                               
Pattern Instances=0   0.03  0.79  0.0  0.00  0.19  0.0  0.0  0.0  0.0
Pattern Instances=1   0.31  0.21  0.0  0.21  0.27  0.0  0.0  0.0  0.0
Pattern Instances=2   0.00  0.07  0.0  0.14  0.79  0.0  0.0  0.0  0.0
Pattern Instances=3   0.10  0.20  0.0  0.00  0.70  0.0  0.0  0.0  0.0
Pattern Instances=4   0.00  0.06  0.0  0.00  0.94  0.0  0.0  0.0  0.0
Pattern Instances=5   0.00  0.25  0.0  0.00  0.75  0.0  0.0  0.0  0.0
Pattern Instances=6   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=8   0.00  0.49  0.0  0.00  0.51  0.0  0.0  0.0  0.0
Pattern Instances=9   0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0
Pattern Instances=10  0.00  0.49  0.0  0.00  0.51  0.0  0.0  0.0  0.0
Pattern Instances=11  0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=1  0.07  0.39  0.0  0.09  0.44  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.27  0.32  0.0  0.07  0.34  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
1                    120   24  106   20
2-3                   31    6   29   24
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x16374e050>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'HDH Instances', 'delay_percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'HDH Batch Size', 'CPU Mean', 'RAM Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.544019        0.000000
Batch Size                              0.000000        0.000000
CPU Mean                                0.005891        0.011317
Client Selector Criteria                0.034129        0.318010
Client Selector Instances               0.000000        0.000000
Client Selector Strategy                0.000000        0.000000
Client Selector Value                   0.000000        0.000000
Data Distribution Diversity             0.000000        0.000000
Data Persistence Diversity              0.000000        0.000000
Epochs                                  0.000000        0.000000
HDH Batch Size                          0.000000        0.015684
HDH Beta 1                              0.000000        0.000000
HDH Beta 2                              0.000000        0.000000
HDH Discriminator                       0.000000        0.000000
HDH Epochs                              0.000000        0.000000
HDH Generator                           0.000000        0.000000
HDH Instances                           0.001465        0.000971
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.082820        0.000000
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.000000        0.000000
Message Compressor Instances            0.000000        0.000000
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.029897        0.005616
Pattern Types Active                    0.004091        0.008819
RAM Mean                                0.000000        0.000000
Total Clients                           0.291825        0.044792
delay_percentage                        0.005863        0.580090
low_spec_percentage                     0.000000        0.000000
non_iid_percentage                      0.000000        0.014701
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=0.87
	Total Clients: [6.000, 10.000]
	Client Selector Criteria: {CPU}
	JSD Mean: [0.010, 0.110]
	delay_percentage: [25.000, 50.000]
 2. For tradeoff S-M (S,M): lift=0.63
	Total Clients: [6.000, 10.000]
	Client Selector Criteria: {(not selected)}
	JSD Mean: [0.004, 0.120]
 3. For tradeoff M-S (M,S): lift=0.23
	Client Selector Criteria: {CPU}
	Alpha Dirichlet Mean: [0.613, 0.900]
	JSD Mean: (not selected) or <= 0.033
	delay_percentage: [25.000, 50.000]
 4. For tradeoff M-M (M,M): lift=0.58
	Client Selector Criteria: {(not selected)}
	Alpha Dirichlet Mean: [0.750, 0.900]
	JSD Mean: (not selected) or <= 0.051
	delay_percentage: [50.000, 75.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (13/13)
  ◦ HDH: ON (13/13)
  ◦ Message Compressor: OFF (13/13)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Operating envelope:
  ◦ JSD Mean [0.01, 0.11]
  ◦ delay percentage [25, 50] (%)
• Other design conditions:
  ◦ Total Clients [6, 10]

PRIM Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (56/56)
  ◦ HDH: ON (56/56)
  ◦ Message Compressor: OFF (42/56), ON (14/56)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (24/24)
  ◦ HDH: ON (24/24)
  ◦ Message Compressor: OFF (18/24), ON (6/24)
• Operating envelope:
  ◦ JSD Mean [0.004, 0.12]
• Other design conditions:
  ◦ Total Clients [6, 10]
• Other parameter conditions:
  ◦ Criteria {(not selected)}

PRIM Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (39/39)
  ◦ HDH: OFF (35/39), ON (4/39)
  ◦ Message Compressor: OFF (39/39)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (19/19)
  ◦ HDH: OFF (15/19), ON (4/19)
  ◦ Message Compressor: OFF (19/19)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.613, 0.9]
  ◦ JSD Mean [-0.012, 0.0325]
  ◦ delay percentage [25, 50] (%)

PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (42/42)
  ◦ HDH: OFF (42/42)
  ◦ Message Compressor: ON (42/42)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/18)
  ◦ HDH: OFF (18/18)
  ◦ Message Compressor: ON (18/18)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.75, 0.9]
  ◦ JSD Mean [-0.012, 0.0506]
  ◦ delay percentage [50, 75] (%)
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 1: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (70/70)
  ◦ HDH: OFF (14/70), ON (56/70)
  ◦ Message Compressor: OFF (42/70), ON (28/70)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (30/30)
  ◦ HDH: OFF (6/30), ON (24/30)
  ◦ Message Compressor: OFF (18/30), ON (12/30)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.6, 0.75]
• Other design conditions:
  ◦ Total Clients [6, 10]
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 2: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (42/42)
  ◦ HDH: OFF (42/42)
  ◦ Message Compressor: ON (42/42)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/18)
  ◦ HDH: OFF (18/18)
  ◦ Message Compressor: ON (18/18)
• Operating envelope:
  ◦ delay percentage [50, 75] (%)
  ◦ Alpha Dirichlet Mean [0.75, 0.9]
• Other parameter conditions:
  ◦ Criteria {(not selected)}

CART Box 3: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (12/12)
  ◦ HDH: ON (12/12)
  ◦ Message Compressor: OFF (12/12)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Operating envelope:
  ◦ JSD Mean [0.004, 0.0975]
  ◦ Alpha Dirichlet Mean [0.6, 0.75]
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 4: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (7/7)
  ◦ HDH: OFF (7/7)
  ◦ Message Compressor: OFF (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: OFF (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ JSD Mean [-0.012, -0.00601]
  ◦ Alpha Dirichlet Mean [0.6, 0.75]
• Other design conditions:
  ◦ Total Clients [4, 6]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     108                 14      4              4   
1   PRIM    S-M     108                 40     24             24   
2   PRIM    M-S     108                  9     19              6   
3   PRIM    M-M     108                 45     18             18   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.130          1.000            0.870                0.881   
1          0.370          1.000            0.630                0.623   
2          0.083          0.316            0.232                0.404   
3          0.417          1.000            0.583                0.579   

   test_recall_coverage  
0                 0.286  
1                 0.600  
2                 0.667  
3                 0.400  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    S-M     108                 40     30             30   
1   CART    M-M     108                 45     18             18   
2   CART    S-S     108                 14      4              4   
3   CART    M-S     108                  9      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.370          1.000            0.630                0.623   
1          0.417          1.000            0.583                0.579   
2          0.130          1.000            0.870                0.881   
3          0.083          0.333            0.250                0.345   

   test_recall_coverage  
0                 0.750  
1                 0.400  
2                 0.286  
3                 0.111
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

      method      policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,ON         0.0  0.0  0.0  0.0  0.296296  0.000000  0.0   
1   test set  OFF,ON,OFF         0.0  0.0  0.0  0.0  0.740741  0.000000  0.0   
2   test set   OFF,ON,ON         0.0  0.0  0.0  0.0  0.333333  0.000000  0.0   
3   test set  ON,OFF,OFF         0.0  0.0  0.0  0.0  0.296296  0.259259  0.0   
4   test set   ON,OFF,ON         0.0  0.0  0.0  0.0  0.111111  0.111111  0.0   
5   test set   ON,ON,OFF         0.0  0.0  0.0  0.0  0.555556  0.111111  0.0   
6       prim  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
7       prim   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
8       prim  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
9       prim  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
10      prim   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
11      prim   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
12      prim  OFF,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
13      prim  OFF,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
14      prim   ON,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.250000  0.0   
15      prim   OFF,ON,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
16      prim   ON,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
17      prim  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.133333  0.333333  0.0   
18      prim   ON,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
19      prim   ON,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
20      prim  OFF,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
21      prim  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
22      prim   OFF,ON,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
23      prim  OFF,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
24      prim  ON,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
25      prim   ON,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
26      prim   OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
27      prim  OFF,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
28      prim   ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
29      prim  OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
30      cart   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
31      cart  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
32      cart   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
33      cart  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
34      cart  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
35      cart   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
36      cart  OFF,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
37      cart   ON,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
38      cart  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.333333  0.0   
39      cart   OFF,ON,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
40      cart  OFF,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
41      cart   ON,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
42      cart  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
43      cart   ON,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
44      cart  OFF,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
45      cart   ON,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
46      cart  OFF,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
47      cart   OFF,ON,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
48      cart   OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
49      cart   ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
50      cart  ON,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
51      cart  OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
52      cart   ON,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
53      cart  OFF,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   

         S-M       S-S  
0   0.703704  0.000000  
1   0.259259  0.000000  
2   0.666667  0.000000  
3   0.185185  0.259259  
4   0.111111  0.666667  
5   0.222222  0.111111  
6   0.000000  0.000000  
7   0.000000  0.000000  
8   0.000000  0.000000  
9   0.000000  0.000000  
10  0.000000  0.000000  
11  0.000000  0.000000  
12  0.000000  0.000000  
13  0.000000  0.000000  
14  0.000000  0.750000  
15  0.000000  0.000000  
16  0.000000  0.000000  
17  0.200000  0.333333  
18  0.000000  0.000000  
19  0.000000  0.000000  
20  0.000000  0.000000  
21  0.000000  0.000000  
22  1.000000  0.000000  
23  1.000000  0.000000  
24  0.000000  0.000000  
25  0.000000  1.000000  
26  0.000000  0.000000  
27  0.000000  0.000000  
28  0.000000  0.000000  
29  0.000000  0.000000  
30  0.000000  0.000000  
31  0.000000  0.000000  
32  0.000000  0.000000  
33  0.000000  0.000000  
34  0.000000  0.000000  
35  0.000000  0.000000  
36  0.000000  0.000000  
37  0.000000  0.000000  
38  0.000000  0.666667  
39  0.000000  0.000000  
40  0.000000  0.000000  
41  0.000000  0.000000  
42  0.000000  0.000000  
43  0.000000  0.000000  
44  1.000000  0.000000  
45  0.000000  0.000000  
46  1.000000  0.000000  
47  1.000000  0.000000  
48  0.000000  0.000000  
49  0.000000  0.000000  
50  0.000000  0.000000  
51  0.000000  0.000000  
52  0.000000  1.000000  
53  0.000000  0.000000
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-380905a7)

```text
S-S    S-M  S-L       M-S       M-M  M-L  L-S  L-M  L-L
S-S  0.285714  0.000  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0
S-M  0.000000  0.600  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0
M-S  0.571429  0.075  0.0  0.666667  0.044444  0.0  0.0  0.0  0.0
M-M  0.000000  0.000  0.0  0.000000  0.400000  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-807637a3)

```text
S-S   S-M  S-L       M-S  M-M  M-L  L-S  L-M  L-L
S-M  0.000000  0.75  0.0  0.000000  0.0  0.0  0.0  0.0  0.0
M-M  0.000000  0.00  0.0  0.000000  0.4  0.0  0.0  0.0  0.0
S-S  0.285714  0.00  0.0  0.000000  0.0  0.0  0.0  0.0  0.0
M-S  0.142857  0.00  0.0  0.111111  0.0  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
