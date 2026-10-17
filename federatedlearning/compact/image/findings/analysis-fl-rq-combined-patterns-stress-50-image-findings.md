# Findings: `analysis-fl-rq-combined-patterns-stress-50-image.ipynb`

## Case scope and support

- **Task:** image (CIFAR-10/CNN 16k).
- **Scope:** All supported non-empty pattern configurations at common 50% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-50-image.ipynb](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-image__combined-patterns__clients-all__stress-50__environment-all.md](../boxes/boxes__task-image__combined-patterns__clients-all__stress-50__environment-all.md).
- **Plots:**
- [quality-space__task-image__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-image__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-image__combined-patterns__clients-all__stress-50__environment-all.png](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-50__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000158.
Data split: 126 train, 54 test.

--- Train Set Tradeoff Counts ---
  S,S: 4 (3.17%)
  S,M: 32 (25.40%)
  M,S: 12 (9.52%)
  M,M: 78 (61.90%)

--- Test Set Tradeoff Counts ---
  S,S: 1 (1.85%)
  S,M: 14 (25.93%)
  M,S: 5 (9.26%)
  M,M: 34 (62.96%)
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
  L,M: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-image__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,ON,OFF --> Tradeoff: M-M
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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
* Tradeoff: S-S --> Group: ON,OFF,ON
------------------------------
Grouping: client_selector_pattern
* Tradeoff: S-S --> Group: ON
* Tradeoff: M-S --> Group: ON
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: S-S --> Group: OFF
------------------------------
Grouping: hdh_pattern
* Tradeoff: S-S --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. ON,OFF,ON: 17% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.1667 - Regret: 0.4946
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 60% success
  2. OFF,ON,ON: 57% success
  3. ON,OFF,ON: 33% success
  Top Policy -> OFF,OFF,ON - Starr: 0.6000 - Regret: 0.3740
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.3298
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,OFF: 30% success
  2. ON,OFF,ON: 20% success
  3. ON,ON,OFF: 7% success
  Top Policy -> ON,OFF,OFF - Starr: 0.3000 - Regret: 0.4770
Robustness Ranking for Tradeoff: M-M
  1. OFF,ON,OFF: 100% success
  2. ON,ON,OFF: 93% success
  3. ON,OFF,OFF: 67% success
  Top Policy -> OFF,ON,OFF - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.2800
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.1152
Robustness Ranking for Tradeoff: L-M

  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.0630
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.4653
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2]
Pattern Instances: varies in these runs, values [0, 1, 3, 4, 5, 6, 8, 9, 10]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                       90               3              0             10   
2                       90               3              1             10   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.515                 11.294  
2                                         0.492                 10.841  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    30      0.067                      0.478   
                     OFF,ON,OFF    30      7.333                      0.539   
                     ON,OFF,OFF    30      1.000                      0.529   
2                    OFF,ON,ON     30      7.533                      0.480   
                     ON,OFF,ON     30      1.000                      0.468   
                     ON,ON,OFF     30      4.667                      0.529   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 11.418  
                     OFF,ON,OFF                 13.215  
                     ON,OFF,OFF                  9.250  
2                    OFF,ON,ON                  12.562  
                     ON,OFF,ON                   8.471  
                     ON,ON,OFF                  11.488
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-de5fb604)

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                               
Pattern Instances=0   0.00  0.64  0.0  0.00  0.36  0.0  0.0  0.0  0.0
Pattern Instances=1   0.08  0.18  0.0  0.24  0.50  0.0  0.0  0.0  0.0
Pattern Instances=3   0.00  0.00  0.0  0.20  0.80  0.0  0.0  0.0  0.0
Pattern Instances=4   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=5   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=6   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=8   0.00  0.32  0.0  0.00  0.68  0.0  0.0  0.0  0.0
Pattern Instances=9   0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0
Pattern Instances=10  0.00  0.50  0.0  0.00  0.50  0.0  0.0  0.0  0.0
[figure rendered in notebook]
                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=1  0.00  0.21  0.0  0.10  0.69  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.06  0.30  0.0  0.09  0.56  0.0  0.0  0.0  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
1                     62    9   19    0
2-3                   50    8   27    5
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x1659ec290>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Message Compressor Instances', 'HDH Instances']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'HDH Instances']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.000000        0.000000
Batch Size                              0.000000        0.000000
CPU Mean                                0.015884        0.159004
Client Selector Criteria                0.000000        0.000000
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
HDH Instances                           0.005634        0.001051
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.733924        0.306676
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.000000        0.000000
Message Compressor Instances            0.014667        0.000000
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.000000        0.370676
Pattern Types Active                    0.007180        0.053165
RAM Mean                                0.000000        0.000000
Total Clients                           0.222711        0.109428
delay_percentage                        0.000000        0.000000
low_spec_percentage                     0.000000        0.000000
non_iid_percentage                      0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff S-S (S,S): lift=-0.02
	Total Clients: [6.000, 10.000]
	CPU Mean: [9.500, 10.125]
	JSD Mean: [0.024, 0.062]
 2. For tradeoff S-M (S,M): lift=0.74
	Total Clients: [9.000, 10.000]
	CPU Mean: [10.125, 11.000]
	JSD Mean: [0.014, 0.062]
 3. For tradeoff M-S (M,S): lift=0.57
	Total Clients: [4.000, 6.000]
	CPU Mean: [9.500, 10.125]
	JSD Mean: (not selected) or <= 0.032
	Pattern Instances: [0.000, 2.000]
 4. For tradeoff M-M (M,M): lift=0.37
	Total Clients: [4.000, 6.000]
	CPU Mean: [10.125, 10.875]
	JSD Mean: (not selected) or <= 0.029
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-5487f837)

```text
PRIM Box 1: S-S (S,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: ON (9/9)
  ◦ Message Compressor: OFF (9/9)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Operating envelope:
  ◦ CPU Mean [9.5, 10.1]
  ◦ JSD Mean [0.0238, 0.062]
• Other design conditions:
  ◦ Total Clients [6, 10]


PRIM Box 2: S-M (S,M)
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
  ◦ CPU Mean [10.1, 11]
  ◦ JSD Mean [0.0138, 0.062]
• Other design conditions:
  ◦ Total Clients [9, 10]


PRIM Box 3: M-S (M,S)
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
  ◦ CPU Mean [9.5, 10.1]
  ◦ JSD Mean [-0.0018, 0.0325]
  ◦ Pattern Instances [0, 2]
• Other design conditions:
  ◦ Total Clients [4, 6]


PRIM Box 4: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (7/21), ON (14/21)
  ◦ Message Compressor: OFF (7/21), ON (14/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: OFF (3/9), ON (6/9)
  ◦ Message Compressor: OFF (3/9), ON (6/9)
• Operating envelope:
  ◦ CPU Mean [10.1, 10.9]
  ◦ JSD Mean [-0.0018, 0.0287]
• Other design conditions:
  ◦ Total Clients [4, 6]


CART Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (25/39), ON (14/39)
  ◦ HDH: OFF (35/39), ON (4/39)
  ◦ Message Compressor: ON (39/39)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (12/18), ON (6/18)
  ◦ HDH: OFF (15/18), ON (3/18)
  ◦ Message Compressor: ON (18/18)
• Operating envelope:
  ◦ Pattern Instances [3.5, 10]
  ◦ JSD Mean [-0.0018, 0.0113]

CART Box 2: S-M (S,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (12/12)
  ◦ HDH: ON (12/12)
  ◦ Message Compressor: OFF (6/12), ON (6/12)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (2/2)
  ◦ HDH: ON (2/2)
  ◦ Message Compressor: OFF (1/2), ON (1/2)
• Operating envelope:
  ◦ CPU Mean [10.9, 11]
  ◦ JSD Mean [0.025, 0.062]

CART Box 3: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (3/3)
  ◦ HDH: ON (3/3)
  ◦ Message Compressor: OFF (3/3)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (1/1)
  ◦ HDH: ON (1/1)
  ◦ Message Compressor: OFF (1/1)
• Operating envelope:
  ◦ CPU Mean [9.5, 10.1]
  ◦ JSD Mean [0.0113, 0.0187]

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
  ◦ CPU Mean [9.5, 10.1]
  ◦ JSD Mean [0.043, 0.0487]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S      54                  1      4              0   
1   PRIM    S-M      54                 14      6              6   
2   PRIM    M-S      54                  5      6              4   
3   PRIM    M-M      54                 34      9              9   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.019          0.000           -0.019                0.413   
1          0.259          1.000            0.741                0.746   
2          0.093          0.667            0.574                0.333   
3          0.630          1.000            0.370                0.381   

   test_recall_coverage  
0                 0.000  
1                 0.429  
2                 0.800  
3                 0.265  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      54                 34     18             18   
1   CART    S-M      54                 14      2              2   
2   CART    M-S      54                  5      1              0   
3   CART    S-S      54                  1      0              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.630            1.0            0.370                0.381   
1          0.259            1.0            0.741                0.746   
2          0.093            0.0           -0.093                0.571   
3          0.019            NaN              NaN                0.968   

   test_recall_coverage  
0                 0.529  
1                 0.143  
2                 0.000  
3                 0.000
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
      method      policy target  L-L  L-M  L-S  M-L       M-M       M-S  S-L  \
0   test set  OFF,OFF,ON         0.0  0.0  0.0  0.0  0.444444  0.000000  0.0   
1   test set  OFF,ON,OFF         0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
2   test set   OFF,ON,ON         0.0  0.0  0.0  0.0  0.444444  0.000000  0.0   
3   test set  ON,OFF,OFF         0.0  0.0  0.0  0.0  0.666667  0.333333  0.0   
4   test set   ON,OFF,ON         0.0  0.0  0.0  0.0  0.222222  0.222222  0.0   
5   test set   ON,ON,OFF         0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
6       prim  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
7       prim   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
8       prim  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
9       prim  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
10      prim   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
11      prim   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
12      prim  OFF,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
13      prim  OFF,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
14      prim   ON,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.333333  0.666667  0.0   
15      prim   OFF,ON,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
16      prim   ON,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
17      prim  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.333333  0.666667  0.0   
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
30      cart   OFF,ON,ON    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
31      cart  OFF,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
32      cart   ON,OFF,ON    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
33      cart  ON,OFF,OFF    M-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
34      cart  OFF,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
35      cart   ON,ON,OFF    M-M  0.0  0.0  0.0  0.0  1.000000  0.000000  0.0   
36      cart  ON,OFF,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
37      cart   ON,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
38      cart   OFF,ON,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
39      cart   ON,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
40      cart  OFF,ON,OFF    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
41      cart  OFF,OFF,ON    M-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
42      cart   OFF,ON,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
43      cart   ON,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
44      cart  ON,OFF,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
45      cart  OFF,ON,OFF    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
46      cart  OFF,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
47      cart   ON,OFF,ON    S-M  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
48      cart  OFF,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
49      cart   OFF,ON,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
50      cart  ON,OFF,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
51      cart  OFF,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
52      cart   ON,OFF,ON    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   
53      cart   ON,ON,OFF    S-S  0.0  0.0  0.0  0.0  0.000000  0.000000  0.0   

         S-M       S-S  
0   0.555556  0.000000  
1   0.000000  0.000000  
2   0.555556  0.000000  
3   0.000000  0.000000  
4   0.444444  0.111111  
5   0.000000  0.000000  
6   0.000000  0.000000  
7   0.000000  0.000000  
8   0.000000  0.000000  
9   0.000000  0.000000  
10  0.000000  0.000000  
11  0.000000  0.000000  
12  0.000000  0.000000  
13  0.000000  0.000000  
14  0.000000  0.000000  
15  0.000000  0.000000  
16  0.000000  0.000000  
17  0.000000  0.000000  
18  0.000000  0.000000  
19  0.000000  0.000000  
20  0.000000  0.000000  
21  0.000000  0.000000  
22  1.000000  0.000000  
23  1.000000  0.000000  
24  0.000000  0.000000  
25  1.000000  0.000000  
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
38  0.000000  0.000000  
39  0.000000  1.000000  
40  0.000000  0.000000  
41  0.000000  0.000000  
42  1.000000  0.000000  
43  0.000000  0.000000  
44  0.000000  0.000000  
45  0.000000  0.000000  
46  1.000000  0.000000  
47  0.000000  0.000000  
48  0.000000  0.000000  
49  0.000000  0.000000  
50  0.000000  0.000000  
51  0.000000  0.000000  
52  0.000000  0.000000  
53  0.000000  0.000000
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-380905a7)

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
S-S  0.0  0.285714  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
S-M  0.0  0.428571  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
M-S  0.0  0.000000  0.0  0.8  0.058824  0.0  0.0  0.0  0.0
M-M  0.0  0.000000  0.0  0.0  0.264706  0.0  0.0  0.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-807637a3)

```text
S-S       S-M  S-L  M-S       M-M  M-L  L-S  L-M  L-L
M-M  0.0  0.000000  0.0  0.0  0.529412  0.0  0.0  0.0  0.0
S-M  0.0  0.142857  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
M-S  1.0  0.000000  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
S-S  0.0  0.000000  0.0  0.0  0.000000  0.0  0.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
