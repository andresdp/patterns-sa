# Findings: `analysis-fl-rq-combined-patterns-stress-25-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All supported non-empty pattern configurations at common 25% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-25-image.ipynb](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__combined-patterns__clients-all__stress-25__environment-all.md](../boxes/boxes__task-image__combined-patterns__clients-all__stress-25__environment-all.md).
- **Plots:**
- [quality-space__task-image__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__combined-patterns__clients-all__stress-25__environment-all.png](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-25__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-ddf2adea)

```text
Warning: Some stratification classes have < 2 samples. Falling back to random split.
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000035.
Data split: 147 train, 63 test.

--- Train Set Tradeoff Counts ---
  S,M: 1 (0.68%)
  M,S: 11 (7.48%)
  M,M: 135 (91.84%)

--- Test Set Tradeoff Counts ---
  S,M: 0 (0.00%)
  M,S: 5 (7.94%)
  M,M: 58 (92.06%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,ON,OFF --> Tradeoff: M-M
* Group: OFF,ON,ON --> Tradeoff: M-M
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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
* Tradeoff: S-M --> Group: ON,OFF,ON
------------------------------
Grouping: client_selector_pattern
* Tradeoff: S-M --> Group: ON
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: S-M --> Group: OFF
------------------------------
Grouping: hdh_pattern
* Tradeoff: S-M --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.3850
Robustness Ranking for Tradeoff: S-M
  1. ON,OFF,ON: 3% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.0333 - Regret: 1.6581
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 3.7547
Robustness Ranking for Tradeoff: M-S
  1. ON,ON,ON: 17% success
  2. ON,OFF,ON: 13% success
  3. ON,OFF,OFF: 10% success
  Top Policy -> ON,ON,ON - Starr: 0.1667 - Regret: 1.0261
Robustness Ranking for Tradeoff: M-M
  1. OFF,ON,OFF: 100% success
  2. OFF,ON,ON: 100% success
  3. OFF,OFF,ON: 97% success
  Top Policy -> OFF,ON,OFF - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 3.1259
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.6285
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.4180
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 7.1535
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2, 3]
Pattern Instances: varies in these runs, values [0, 1, 4, 7, 8, 9, 10]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                       90               3              0             10   
2                       90               3              1             10   
3                       30               1              4              9   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.536                 11.848  
2                                         0.533                 11.378  
3                                         0.531                 10.835  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    30      0.033                      0.536   
                     OFF,ON,OFF    30      7.333                      0.538   
                     ON,OFF,OFF    30      1.000                      0.535   
2                    OFF,ON,ON     30      7.467                      0.535   
                     ON,OFF,ON     30      1.000                      0.529   
                     ON,ON,OFF     30      6.667                      0.536   
3                    ON,ON,ON      30      6.667                      0.531   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 12.066  
                     OFF,ON,OFF                 12.292  
                     ON,OFF,OFF                 11.188  
2                    OFF,ON,ON                  12.064  
                     ON,OFF,ON                  10.823  
                     ON,ON,OFF                  11.248  
3                    ON,ON,ON                   10.835
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0   0.0  0.00  0.0  0.03  0.97  0.0  0.0  0.0  0.0
Pattern Instances=1   0.0  0.02  0.0  0.11  0.87  0.0  0.0  0.0  0.0
Pattern Instances=4   0.0  0.00  0.0  0.18  0.82  0.0  0.0  0.0  0.0
Pattern Instances=7   0.0  0.00  0.0  0.05  0.95  0.0  0.0  0.0  0.0
Pattern Instances=8   0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=9   0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=10  0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                        S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                
Pattern Types Active=1  0.0  0.00  0.0  0.04  0.96  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.0  0.01  0.0  0.08  0.91  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.0  0.00  0.0  0.17  0.83  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M
Pattern Count Group               
1                     86    4    0
2-3                  107   12    1
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x16382f250>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)

Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'Message Compressor Alg', 'HDH Batch Size', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.000000        0.200372
Batch Size                              0.000000        0.000000
CPU Mean                                0.000000        0.000000
Client Selector Criteria                0.007501        0.491206
Client Selector Instances               0.000000        0.000000
Client Selector Strategy                0.000000        0.000000
Client Selector Value                   0.000000        0.000000
Data Distribution Diversity             0.000000        0.000000
Data Persistence Diversity              0.000000        0.000000
Epochs                                  0.000000        0.000000
HDH Batch Size                          0.000000        0.097856
HDH Beta 1                              0.000000        0.000000
HDH Beta 2                              0.000000        0.000000
HDH Discriminator                       0.000000        0.000000
HDH Epochs                              0.000000        0.000000
HDH Generator                           0.000000        0.000000
HDH Instances                           0.001953        0.010715
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.049316        0.000000
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.000000        0.062154
Message Compressor Instances            0.008060        0.000000
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.000000        0.000000
Pattern Types Active                    0.007583        0.137697
RAM Mean                                0.000000        0.000000
Total Clients                           0.925585        0.000000
delay_percentage                        0.000000        0.000000
low_spec_percentage                     0.000000        0.000000
non_iid_percentage                      0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-M (S,M): lift=0.00
	Message Compressor Alg: {(not selected)}
	JSD Mean: [0.001, 0.015]
	Pattern Types Active: [1.500, 3.000]
 2. For tradeoff M-S (M,S): lift=0.25
	Total Clients: [4.000, 6.000]
	Client Selector Criteria: {CPU}
	HDH Batch Size: [30.400, 32.000]
 3. For tradeoff M-M (M,M): lift=0.04
	Total Clients: [6.000, 10.000]
	Message Compressor Alg: {zlib}
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ Message Compressor = OFF
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (13/13)
  ◦ HDH: ON (13/13)
  ◦ Message Compressor: OFF (13/13)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: ON (6/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ JSD Mean [0.000833, 0.015]
• Other design conditions:
  ◦ Pattern Types Active [1.5, 3]
• Other parameter conditions:
  ◦ Algorithm {(not selected)}

PRIM Box 2: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
  ◦ HDH = ON (HDH Batch Size = 32.0; HDH Beta 1 = 0.5; HDH Beta 2 = 0.999; HDH Discriminator = DCGANDiscriminator; HDH Epochs = 1.0; HDH Generator = DCGANGenerator; HDH Learning Rate = 0.0002; HDH Latent Dim = 100.0; HDH Optimizer = Adam)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (14/14)
  ◦ HDH: ON (14/14)
  ◦ Message Compressor: OFF (7/14), ON (7/14)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: ON (6/6)
  ◦ Message Compressor: OFF (3/6), ON (3/6)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [4, 6]

PRIM Box 3: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ Message Compressor = ON (Algorithm = zlib)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (28/56), ON (28/56)
  ◦ HDH: OFF (28/56), ON (28/56)
  ◦ Message Compressor: ON (56/56)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (12/24), ON (12/24)
  ◦ HDH: OFF (12/24), ON (12/24)
  ◦ Message Compressor: ON (24/24)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (30/72), ON (42/72)
  ◦ HDH: OFF (42/72), ON (30/72)
  ◦ Message Compressor: OFF (29/72), ON (43/72)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/42), ON (24/42)
  ◦ HDH: OFF (18/42), ON (24/42)
  ◦ Message Compressor: OFF (18/42), ON (24/42)
• Operating envelope:
  ◦ JSD Mean [-0.0015, 0.00583]
• Other design conditions:
  ◦ Total Clients [6, 10]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-M      63                  0      6              0   
1   PRIM    M-S      63                  5      6              2   
2   PRIM    M-M      63                 58     24             23   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.070   
1          0.079          0.333            0.254                0.354   
2          0.921          0.958            0.038                0.082   

   test_recall_coverage  
0                   NaN  
1                 0.400  
2                 0.397  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      63                 58     42             41   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.921          0.976            0.056                0.082   

   test_recall_coverage  
0                 0.707
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

      method      policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,ON         0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
1   test set  OFF,ON,OFF         0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
2   test set   OFF,ON,ON         0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
3   test set  ON,OFF,OFF         0.0  0.0  0.0  0.0  0.888889  0.111111  0.0   
4   test set   ON,OFF,ON         0.0  0.0  0.0  0.0  0.888889  0.111111  0.0   
5   test set   ON,ON,OFF         0.0  0.0  0.0  0.0  0.888889  0.111111  0.0   
6   test set    ON,ON,ON         0.0  0.0  0.0  0.0  0.777778  0.222222  0.0   
7       prim    ON,ON,ON    M-M  0.0  0.0  0.0  0.0  0.833333  0.166667  0.0   
8       prim  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
9       prim   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
10      prim  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
11      prim   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
12      prim   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
13      prim  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
14      prim    ON,ON,ON    M-S  0.0  0.0  0.0  0.0  0.666667  0.333333  0.0   
15      prim   ON,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
16      prim   ON,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.666667  0.333333  0.0   
17      prim  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
18      prim   OFF,ON,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
19      prim  OFF,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
20      prim  OFF,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
21      prim  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
22      prim   ON,OFF,ON    S-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
23      prim   OFF,ON,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
24      prim   ON,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
25      prim  OFF,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
26      prim    ON,ON,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
27      prim  OFF,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
28      cart  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
29      cart  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
30      cart   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
31      cart  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
32      cart   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
33      cart   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
34      cart    ON,ON,ON    M-M  0.0  0.0  0.0  0.0  0.833333  0.166667  0.0   

    S-M  S-S  
0   0.0  0.0  
1   0.0  0.0  
2   0.0  0.0  
3   0.0  0.0  
4   0.0  0.0  
5   0.0  0.0  
6   0.0  0.0  
7   0.0  0.0  
8   0.0  0.0  
9   0.0  0.0  
10  0.0  0.0  
11  0.0  0.0  
12  0.0  0.0  
13  0.0  0.0  
14  0.0  0.0  
15  0.0  0.0  
16  0.0  0.0  
17  0.0  0.0  
18  0.0  0.0  
19  0.0  0.0  
20  0.0  0.0  
21  0.0  0.0  
22  0.0  0.0  
23  0.0  0.0  
24  0.0  0.0  
25  0.0  0.0  
26  0.0  0.0  
27  0.0  0.0  
28  0.0  0.0  
29  0.0  0.0  
30  0.0  0.0  
31  0.0  0.0  
32  0.0  0.0  
33  0.0  0.0  
34  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
S-M  0.0  0.0  0.0  0.0  0.103448  0.0  0.0  0.0  0.0
M-S  0.0  0.0  0.0  0.4  0.068966  0.0  0.0  0.0  0.0
M-M  0.0  0.0  0.0  0.2  0.396552  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.0  0.0  0.0  0.2  0.706897  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
