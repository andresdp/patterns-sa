# Findings: `analysis-fl-rq-combined-patterns-stress-75-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All supported non-empty pattern configurations at common 75% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-75-text.ipynb](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__combined-patterns__clients-all__stress-75__environment-all.md](../boxes/boxes__task-text__combined-patterns__clients-all__stress-75__environment-all.md).
- **Plots:**
- [quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png](../plots/feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000328.
Data split: 252 train, 108 test.

--- Train Set Tradeoff Counts ---
  M,S: 6 (2.38%)
  M,M: 8 (3.17%)
  L,S: 51 (20.24%)
  L,M: 176 (69.84%)
  L,L: 11 (4.37%)

--- Test Set Tradeoff Counts ---
  M,S: 3 (2.78%)
  M,M: 1 (0.93%)
  L,S: 23 (21.30%)
  L,M: 76 (70.37%)
  L,L: 5 (4.63%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,ON,OFF --> Tradeoff: L-M
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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
* Tradeoff: M-S --> Group: ON
* Tradeoff: L-S --> Group: ON
* Tradeoff: L-L --> Group: OFF
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: M-S --> Group: OFF
------------------------------
Grouping: hdh_pattern
* Tradeoff: M-M --> Group: ON
* Tradeoff: L-L --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.5803
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.4567
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.4841
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,ON: 17% success
  2. ON,OFF,OFF: 4% success
  3. OFF,OFF,ON: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.1667 - Regret: 1.0104
Robustness Ranking for Tradeoff: M-M
  1. ON,OFF,ON: 17% success
  2. OFF,OFF,ON: 3% success
  3. OFF,ON,ON: 3% success
  Top Policy -> ON,OFF,ON - Starr: 0.1667 - Regret: 1.2072
Robustness Ranking for Tradeoff: M-L

  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 1.5655
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 59% success
  2. ON,OFF,ON: 53% success
  3. ON,ON,OFF: 17% success
  Top Policy -> ON,OFF,OFF - Starr: 0.5889 - Regret: 0.1692
Robustness Ranking for Tradeoff: L-M
  1. OFF,ON,OFF: 100% success
  2. OFF,OFF,ON: 87% success
  3. ON,ON,OFF: 83% success
  Top Policy -> OFF,ON,OFF - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: L-L
  1. OFF,ON,ON: 23% success
  2. OFF,OFF,ON: 10% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,ON,ON - Starr: 0.2333 - Regret: 0.3204
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2]
Pattern Instances: varies in these runs, values [1, 2, 3, 4, 6, 7, 8, 10, 14, 18]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                      270               3              1             10   
2                       90               3              1             18   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.851                 11.819  
2                                         0.817                 11.226  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    90      5.667                      0.821   
                     OFF,ON,OFF    90      7.333                      0.889   
                     ON,OFF,OFF    90      1.000                      0.842   
2                    OFF,ON,ON     30     13.000                      0.821   
                     ON,OFF,ON     30      2.167                      0.768   
                     ON,ON,OFF     30      2.667                      0.862   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 15.103  
                     OFF,ON,OFF                 13.611  
                     ON,OFF,OFF                  6.744  
2                    OFF,ON,ON                  16.397  
                     ON,OFF,ON                   7.292  
                     ON,ON,OFF                   9.989
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M   L-L
policy                                                                
Pattern Instances=1   0.0  0.0  0.0  0.04  0.00  0.0  0.61  0.35  0.00
Pattern Instances=2   0.0  0.0  0.0  0.16  0.08  0.0  0.36  0.40  0.00
Pattern Instances=3   0.0  0.0  0.0  0.02  0.10  0.0  0.12  0.62  0.15
Pattern Instances=4   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
Pattern Instances=6   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
Pattern Instances=7   0.0  0.0  0.0  0.00  0.10  0.0  0.00  0.20  0.70
Pattern Instances=8   0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
Pattern Instances=10  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
Pattern Instances=14  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
Pattern Instances=18  0.0  0.0  0.0  0.00  0.00  0.0  0.00  1.00  0.00
[figure rendered in notebook]
                        S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M   L-L
policy                                                                  
Pattern Types Active=1  0.0  0.0  0.0  0.01  0.01  0.0  0.20  0.74  0.03
Pattern Types Active=2  0.0  0.0  0.0  0.06  0.07  0.0  0.23  0.57  0.08
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-L  L-M  L-S  M-M  M-S
Pattern Count Group                         
1                      9  201   53    3    4
2-3                    7   51   21    6    5
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x167f344d0>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Message Compressor Alg', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Message Compressor Instances', 'HDH Instances', 'delay_percentage']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.000000        0.010397
Batch Size                              0.000000        0.000000
CPU Mean                                0.000000        0.010977
Client Selector Criteria                0.000000        0.741595
Client Selector Instances               0.000000        0.000000
Client Selector Strategy                0.000000        0.000000
Client Selector Value                   0.000000        0.000000
Data Distribution Diversity             0.000000        0.000000
Data Persistence Diversity              0.000000        0.000000
Epochs                                  0.000000        0.000000
HDH Batch Size                          0.000000        0.000000
HDH Beta 1                              0.000000        0.000000
HDH Beta 2                              0.000000        0.000000
HDH Discriminator                       0.000000        0.000000
HDH Epochs                              0.000000        0.000000
HDH Generator                           0.000000        0.000000
HDH Instances                           0.000000        0.063325
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.240095        0.000000
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.007117        0.000000
Message Compressor Instances            0.000000        0.007235
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.191245        0.000000
Pattern Types Active                    0.022670        0.012698
RAM Mean                                0.000000        0.000000
Total Clients                           0.045773        0.043182
delay_percentage                        0.011422        0.110591
low_spec_percentage                     0.012329        0.000000
non_iid_percentage                      0.469349        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.19
	Client Selector Criteria: {CPU}
	HDH Instances: [0.500, 8.000]
 2. For tradeoff M-M (M,M): lift=0.10
	Client Selector Criteria: {CPU}
	HDH Instances: [0.500, 8.000]
 3. For tradeoff L-S (L,S): lift=0.51
	Client Selector Criteria: {CPU}
	Pattern Instances: [1.000, 1.500]
	delay_percentage: [25.000, 50.000]
 4. For tradeoff L-M (L,M): lift=0.30
	Total Clients: [6.000, 10.000]
	Pattern Instances: [3.500, 18.000]
 5. For tradeoff L-L (L,L): lift=0.45
	HDH Instances: [0.500, 4.500]
	delay_percentage: [50.000, 75.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (16/16)
  ◦ HDH: ON (16/16)
  ◦ Message Compressor: OFF (16/16)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: ON (9/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ HDH Instances [0.5, 8]

PRIM Box 2: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (16/16)
  ◦ HDH: ON (16/16)
  ◦ Message Compressor: OFF (16/16)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: ON (9/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ HDH Instances [0.5, 8]

PRIM Box 3: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (47/47)
  ◦ HDH: OFF (42/47), ON (5/47)
  ◦ Message Compressor: OFF (47/47)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (18/18)
  ◦ HDH: OFF (18/18)
  ◦ Message Compressor: OFF (18/18)
• Operating envelope:
  ◦ Pattern Instances [1, 1.5]
  ◦ delay percentage [25, 50] (%)

PRIM Box 4: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (98/98)
  ◦ HDH: OFF (42/98), ON (56/98)
  ◦ Message Compressor: OFF (42/98), ON (56/98)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (42/42)
  ◦ HDH: OFF (18/42), ON (24/42)
  ◦ Message Compressor: OFF (18/42), ON (24/42)
• Operating envelope:
  ◦ Pattern Instances [3.5, 18]
• Other design conditions:
  ◦ Total Clients [6, 10]

PRIM Box 5: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (14/14)
  ◦ HDH: ON (14/14)
  ◦ Message Compressor: OFF (7/14), ON (7/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (6/6)
  ◦ HDH: ON (6/6)
  ◦ Message Compressor: OFF (3/6), ON (3/6)
• Operating envelope:
  ◦ HDH Instances [0.5, 4.5]
  ◦ delay percentage [50, 75] (%)

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (98/98)
  ◦ HDH: OFF (42/98), ON (56/98)
  ◦ Message Compressor: OFF (42/98), ON (56/98)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (42/42)
  ◦ HDH: OFF (18/42), ON (24/42)
  ◦ Message Compressor: OFF (18/42), ON (24/42)
• Operating envelope:
  ◦ Pattern Instances [3.5, 18]
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 2: L-S (L,S)
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
  ◦ non-IID percentage [25, 50] (%)
  ◦ delay percentage [25, 50] (%)
  ◦ JSD Mean [-0.0155, -0.00776]
  ◦ Pattern Instances [1, 1.5]
• Other design conditions:
  ◦ Total Clients [6, 9]

CART Box 3: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (3/3)
  ◦ HDH: ON (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ Pattern Instances [2.5, 3.5]
  ◦ delay percentage [50, 75] (%)
  ◦ JSD Mean [-0.00776, 0.0175]
• Other parameter conditions:
  ◦ Criteria {(not selected)}
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S     108                  3      9              2   
1   PRIM    M-M     108                  1      9              1   
2   PRIM    L-S     108                 23     18             13   
3   PRIM    L-M     108                 76     42             42   
4   PRIM    L-L     108                  5      6              3   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.028          0.222            0.194                0.164   
1          0.009          0.111            0.102                0.218   
2          0.213          0.722            0.509                0.606   
3          0.704          1.000            0.296                0.302   
4          0.046          0.500            0.454                0.599   

   test_recall_coverage  
0                 0.667  
1                 1.000  
2                 0.565  
3                 0.553  
4                 0.600  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M     108                 76     42             42   
1   CART    L-S     108                 23      3              2   
2   CART    L-L     108                  5      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.704          1.000            0.296                0.302   
1          0.213          0.667            0.454                0.655   
2          0.046          0.333            0.287                0.456   

   test_recall_coverage  
0                 0.553  
1                 0.087  
2                 0.200
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

      method      policy target       L-L       L-M       L-S  M-L       M-M  \
0   test set  OFF,OFF,ON         0.111111  0.888889  0.000000  0.0  0.000000   
1   test set  OFF,ON,OFF         0.000000  1.000000  0.000000  0.0  0.000000   
2   test set   OFF,ON,ON         0.222222  0.777778  0.000000  0.0  0.000000   
3   test set  ON,OFF,OFF         0.000000  0.370370  0.592593  0.0  0.000000   
4   test set   ON,OFF,ON         0.000000  0.222222  0.444444  0.0  0.111111   
5   test set   ON,ON,OFF         0.000000  0.666667  0.333333  0.0  0.000000   
6       prim  OFF,OFF,ON    L-L  0.333333  0.666667  0.000000  0.0  0.000000   
7       prim   ON,OFF,ON    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
8       prim  ON,OFF,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
9       prim  OFF,ON,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
10      prim   OFF,ON,ON    L-L  0.666667  0.333333  0.000000  0.0  0.000000   
11      prim   ON,ON,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
12      prim  OFF,ON,OFF    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
13      prim   ON,OFF,ON    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
14      prim   OFF,ON,ON    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
15      prim   ON,ON,OFF    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
16      prim  ON,OFF,OFF    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
17      prim  OFF,OFF,ON    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
18      prim   ON,ON,OFF    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
19      prim  OFF,ON,OFF    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
20      prim  OFF,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
21      prim   OFF,ON,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
22      prim  ON,OFF,OFF    L-S  0.000000  0.222222  0.722222  0.0  0.000000   
23      prim   ON,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
24      prim   ON,ON,OFF    M-M  0.000000  0.000000  0.000000  0.0  0.000000   
25      prim   ON,OFF,ON    M-M  0.000000  0.222222  0.444444  0.0  0.111111   
26      prim  ON,OFF,OFF    M-M  0.000000  0.000000  0.000000  0.0  0.000000   
27      prim  OFF,OFF,ON    M-M  0.000000  0.000000  0.000000  0.0  0.000000   
28      prim   OFF,ON,ON    M-M  0.000000  0.000000  0.000000  0.0  0.000000   
29      prim  OFF,ON,OFF    M-M  0.000000  0.000000  0.000000  0.0  0.000000   
30      prim  ON,OFF,OFF    M-S  0.000000  0.000000  0.000000  0.0  0.000000   
31      prim   OFF,ON,ON    M-S  0.000000  0.000000  0.000000  0.0  0.000000   
32      prim  OFF,OFF,ON    M-S  0.000000  0.000000  0.000000  0.0  0.000000   
33      prim   ON,ON,OFF    M-S  0.000000  0.000000  0.000000  0.0  0.000000   
34      prim   ON,OFF,ON    M-S  0.000000  0.222222  0.444444  0.0  0.111111   
35      prim  OFF,ON,OFF    M-S  0.000000  0.000000  0.000000  0.0  0.000000   
36      cart  OFF,OFF,ON    L-L  0.333333  0.666667  0.000000  0.0  0.000000   
37      cart   ON,OFF,ON    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
38      cart  ON,OFF,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
39      cart  OFF,ON,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
40      cart   OFF,ON,ON    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
41      cart   ON,ON,OFF    L-L  0.000000  0.000000  0.000000  0.0  0.000000   
42      cart  OFF,ON,OFF    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
43      cart   OFF,ON,ON    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
44      cart  ON,OFF,OFF    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
45      cart   ON,OFF,ON    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
46      cart  OFF,OFF,ON    L-M  0.000000  1.000000  0.000000  0.0  0.000000   
47      cart   ON,ON,OFF    L-M  0.000000  0.000000  0.000000  0.0  0.000000   
48      cart   OFF,ON,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
49      cart   ON,ON,OFF    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
50      cart  ON,OFF,OFF    L-S  0.000000  0.333333  0.666667  0.0  0.000000   
51      cart  OFF,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
52      cart   ON,OFF,ON    L-S  0.000000  0.000000  0.000000  0.0  0.000000   
53      cart  OFF,ON,OFF    L-S  0.000000  0.000000  0.000000  0.0  0.000000   

         M-S  S-L  S-M  S-S  
0   0.000000  0.0  0.0  0.0  
1   0.000000  0.0  0.0  0.0  
2   0.000000  0.0  0.0  0.0  
3   0.037037  0.0  0.0  0.0  
4   0.222222  0.0  0.0  0.0  
5   0.000000  0.0  0.0  0.0  
6   0.000000  0.0  0.0  0.0  
7   0.000000  0.0  0.0  0.0  
8   0.000000  0.0  0.0  0.0  
9   0.000000  0.0  0.0  0.0  
10  0.000000  0.0  0.0  0.0  
11  0.000000  0.0  0.0  0.0  
12  0.000000  0.0  0.0  0.0  
13  0.000000  0.0  0.0  0.0  
14  0.000000  0.0  0.0  0.0  
15  0.000000  0.0  0.0  0.0  
16  0.000000  0.0  0.0  0.0  
17  0.000000  0.0  0.0  0.0  
18  0.000000  0.0  0.0  0.0  
19  0.000000  0.0  0.0  0.0  
20  0.000000  0.0  0.0  0.0  
21  0.000000  0.0  0.0  0.0  
22  0.055556  0.0  0.0  0.0  
23  0.000000  0.0  0.0  0.0  
24  0.000000  0.0  0.0  0.0  
25  0.222222  0.0  0.0  0.0  
26  0.000000  0.0  0.0  0.0  
27  0.000000  0.0  0.0  0.0  
28  0.000000  0.0  0.0  0.0  
29  0.000000  0.0  0.0  0.0  
30  0.000000  0.0  0.0  0.0  
31  0.000000  0.0  0.0  0.0  
32  0.000000  0.0  0.0  0.0  
33  0.000000  0.0  0.0  0.0  
34  0.222222  0.0  0.0  0.0  
35  0.000000  0.0  0.0  0.0  
36  0.000000  0.0  0.0  0.0  
37  0.000000  0.0  0.0  0.0  
38  0.000000  0.0  0.0  0.0  
39  0.000000  0.0  0.0  0.0  
40  0.000000  0.0  0.0  0.0  
41  0.000000  0.0  0.0  0.0  
42  0.000000  0.0  0.0  0.0  
43  0.000000  0.0  0.0  0.0  
44  0.000000  0.0  0.0  0.0  
45  0.000000  0.0  0.0  0.0  
46  0.000000  0.0  0.0  0.0  
47  0.000000  0.0  0.0  0.0  
48  0.000000  0.0  0.0  0.0  
49  0.000000  0.0  0.0  0.0  
50  0.000000  0.0  0.0  0.0  
51  0.000000  0.0  0.0  0.0  
52  0.000000  0.0  0.0  0.0  
53  0.000000  0.0  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L       M-S  M-M  M-L       L-S       L-M  L-L
M-S  0.0  0.0  0.0  0.666667  1.0  0.0  0.173913  0.026316  0.0
M-M  0.0  0.0  0.0  0.666667  1.0  0.0  0.173913  0.026316  0.0
L-S  0.0  0.0  0.0  0.333333  0.0  0.0  0.565217  0.052632  0.0
L-M  0.0  0.0  0.0  0.000000  0.0  0.0  0.000000  0.552632  0.0
L-L  0.0  0.0  0.0  0.000000  0.0  0.0  0.000000  0.039474  0.6
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.552632  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.086957  0.013158  0.0
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.026316  0.2
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
