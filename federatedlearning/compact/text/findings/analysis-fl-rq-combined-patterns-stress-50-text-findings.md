# Findings: `analysis-fl-rq-combined-patterns-stress-50-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All supported non-empty pattern configurations at common 50% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-50-text.ipynb](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__combined-patterns__clients-all__stress-50__environment-all.md](../boxes/boxes__task-text__combined-patterns__clients-all__stress-50__environment-all.md).
- **Plots:**
- [quality-space__task-text__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__combined-patterns__clients-all__stress-50__environment-all.png](../plots/feature-importance__task-text__combined-patterns__clients-all__stress-50__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-ddf2adea)

```text
Warning: Some stratification classes have < 2 samples. Falling back to random split.
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000439.
Data split: 126 train, 54 test.

--- Train Set Tradeoff Counts ---
  M,S: 2 (1.59%)
  M,M: 1 (0.79%)
  L,S: 14 (11.11%)
  L,M: 108 (85.71%)
  L,L: 1 (0.79%)

--- Test Set Tradeoff Counts ---
  M,S: 0 (0.00%)
  M,M: 0 (0.00%)
  L,S: 7 (12.96%)
  L,M: 47 (87.04%)
  L,L: 0 (0.00%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,OFF,ON --> Tradeoff: L-M
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

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
* Tradeoff: M-S --> Group: ON,OFF,ON
* Tradeoff: M-M --> Group: ON,OFF,ON
* Tradeoff: L-L --> Group: OFF,ON,ON
------------------------------
Grouping: client_selector_pattern
* Tradeoff: M-S --> Group: ON
* Tradeoff: M-M --> Group: ON
* Tradeoff: L-S --> Group: ON
* Tradeoff: L-L --> Group: OFF
------------------------------
Grouping: message_compressor_pattern
* Tradeoff: M-S --> Group: OFF
* Tradeoff: M-M --> Group: OFF
* Tradeoff: L-L --> Group: ON
------------------------------
Grouping: hdh_pattern
* Tradeoff: M-S --> Group: ON
* Tradeoff: M-M --> Group: ON
* Tradeoff: L-L --> Group: ON
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 8.0355
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 7.9390
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 8.1048
Robustness Ranking for Tradeoff: M-S
  1. ON,OFF,ON: 7% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.0667 - Regret: 1.7328
Robustness Ranking for Tradeoff: M-M
  1. ON,OFF,ON: 3% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> ON,OFF,ON - Starr: 0.0333 - Regret: 1.7380
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.7177
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 40% success
  2. ON,OFF,ON: 23% success
  3. ON,ON,OFF: 7% success
  Top Policy -> ON,OFF,OFF - Starr: 0.4000 - Regret: 0.2079
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 100% success
  2. OFF,ON,OFF: 100% success
  3. OFF,ON,ON: 97% success
  Top Policy -> OFF,OFF,ON - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: L-L
  1. OFF,ON,ON: 3% success
  2. OFF,OFF,ON: 0% success
  3. OFF,ON,OFF: 0% success
  Top Policy -> OFF,ON,ON - Starr: 0.0333 - Regret: 0.9665
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2]
Pattern Instances: varies in these runs, values [1, 2, 3, 4, 5, 6, 8, 10, 12, 15]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                       90               3              1             10   
2                       90               3              1             15   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.882                 11.360  
2                                         0.852                 11.946  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    30      3.667                      0.847   
                     OFF,ON,OFF    30      7.333                      0.906   
                     ON,OFF,OFF    30      1.000                      0.892   
2                    OFF,ON,ON     30     11.000                      0.847   
                     ON,OFF,ON     30      3.000                      0.815   
                     ON,ON,OFF     30      4.667                      0.893   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 12.861  
                     OFF,ON,OFF                 13.005  
                     ON,OFF,OFF                  8.215  
2                    OFF,ON,ON                  14.630  
                     ON,OFF,ON                  10.183  
                     ON,ON,OFF                  11.024
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L  M-S   M-M  M-L   L-S   L-M   L-L
policy                                                               
Pattern Instances=1   0.0  0.0  0.0  0.0  0.00  0.0  0.39  0.61  0.00
Pattern Instances=2   0.0  0.0  0.0  0.1  0.00  0.0  0.10  0.81  0.00
Pattern Instances=3   0.0  0.0  0.0  0.0  0.06  0.0  0.41  0.53  0.00
Pattern Instances=4   0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
Pattern Instances=5   0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
Pattern Instances=6   0.0  0.0  0.0  0.0  0.00  0.0  0.00  0.95  0.05
Pattern Instances=8   0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
Pattern Instances=10  0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
Pattern Instances=12  0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
Pattern Instances=15  0.0  0.0  0.0  0.0  0.00  0.0  0.00  1.00  0.00
[figure rendered in notebook]
                        S-S  S-M  S-L   M-S   M-M  M-L   L-S   L-M   L-L
policy                                                                  
Pattern Types Active=1  0.0  0.0  0.0  0.00  0.00  0.0  0.13  0.87  0.00
Pattern Types Active=2  0.0  0.0  0.0  0.02  0.01  0.0  0.10  0.86  0.01
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-L  L-M  L-S  M-M  M-S
Pattern Count Group                         
1                      0   78   12    0    0
2-3                    1   77    9    1    2
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x168027210>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'Message Compressor Alg', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'RAM Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Message Compressor Instances', 'HDH Instances']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.000000        0.000000
Batch Size                              0.000000        0.000000
CPU Mean                                0.000000        0.000000
Client Selector Criteria                0.080737        0.550234
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
HDH Instances                           0.000000        0.045499
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.732814        0.000000
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.003238        0.000000
Message Compressor Instances            0.000000        0.021785
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.101361        0.184135
Pattern Types Active                    0.010426        0.110310
RAM Mean                                0.000000        0.000000
Total Clients                           0.071425        0.088037
delay_percentage                        0.000000        0.000000
low_spec_percentage                     0.000000        0.000000
non_iid_percentage                      0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff M-S (M,S): lift=0.00
	Total Clients: [4.000, 9.000]
	Client Selector Criteria: {CPU}
	HDH Instances: [0.500, 2.500]
 2. For tradeoff M-M (M,M): lift=0.00
	JSD Mean: [0.007, 0.070]
	HDH Instances: [0.500, 5.000]
 3. For tradeoff L-S (L,S): lift=0.20
	Total Clients: [4.000, 6.000]
	Client Selector Criteria: {CPU}
	Pattern Types Active: [1.000, 1.500]
	Pattern Instances: [1.000, 4.000]
	HDH Instances: [0.000, 2.500]
 4. For tradeoff L-M (L,M): lift=0.13
	Total Clients: [6.000, 10.000]
	JSD Mean: (not selected) or <= 0.032
	Pattern Instances: [4.500, 15.000]
 5. For tradeoff L-L (L,L): lift=0.00
	Total Clients: [4.000, 6.000]
	Pattern Instances: [4.500, 15.000]
	HDH Instances: [0.500, 5.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-S (M,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: ON (9/9)
  ◦ Message Compressor: OFF (9/9)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (6/6)
  ◦ HDH: ON (6/6)
  ◦ Message Compressor: OFF (6/6)
• Operating envelope:
  ◦ HDH Instances [0.5, 2.5]
• Other design conditions:
  ◦ Total Clients [4, 9]


PRIM Box 2: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (12/15), ON (3/15)
  ◦ HDH: ON (15/15)
  ◦ Message Compressor: OFF (9/15), ON (6/15)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (8/11), ON (3/11)
  ◦ HDH: ON (11/11)
  ◦ Message Compressor: OFF (7/11), ON (4/11)
• Operating envelope:
  ◦ JSD Mean [0.007, 0.07]
  ◦ HDH Instances [0.5, 5]

PRIM Box 3: L-S (L,S)
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
  ◦ Pattern Instances [1, 4]
  ◦ HDH Instances [0, 2.5]
• Other design conditions:
  ◦ Total Clients [4, 6]
  ◦ Pattern Types Active [1, 1.5]

PRIM Box 4: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (34/49), ON (15/49)
  ◦ HDH: OFF (28/49), ON (21/49)
  ◦ Message Compressor: OFF (8/49), ON (41/49)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (15/22), ON (7/22)
  ◦ HDH: OFF (12/22), ON (10/22)
  ◦ Message Compressor: OFF (4/22), ON (18/22)
• Operating envelope:
  ◦ JSD Mean [-0.007, 0.0315]
  ◦ Pattern Instances [4.5, 15]
• Other design conditions:
  ◦ Total Clients [6, 10]

PRIM Box 5: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (7/7)
  ◦ HDH: ON (7/7)
  ◦ Message Compressor: ON (7/7)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (3/3)
  ◦ HDH: ON (3/3)
  ◦ Message Compressor: ON (3/3)
• Operating envelope:
  ◦ Pattern Instances [4.5, 15]
  ◦ HDH Instances [0.5, 5]
• Other design conditions:
  ◦ Total Clients [4, 6]

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (42/64), ON (22/64)
  ◦ HDH: OFF (28/64), ON (36/64)
  ◦ Message Compressor: OFF (22/64), ON (42/64)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/27), ON (9/27)
  ◦ HDH: OFF (12/27), ON (15/27)
  ◦ Message Compressor: OFF (9/27), ON (18/27)
• Operating envelope:
  ◦ Pattern Instances [3.5, 15]
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 2: L-S (L,S)
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
  ◦ HDH Instances [0, 1.5]
  ◦ JSD Mean [-0.007, -0.0035]
  ◦ Pattern Instances [1, 2]
• Other design conditions:
  ◦ Total Clients [4, 6]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-S      54                  0      6              0   
1   PRIM    M-M      54                  0     11              0   
2   PRIM    L-S      54                  7      3              1   
3   PRIM    L-M      54                 47     22             22   
4   PRIM    L-L      54                  0      3              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0           0.00          0.000            0.000                0.206   
1           0.00          0.000            0.000                0.059   
2           0.13          0.333            0.204                0.460   
3           0.87          1.000            0.130                0.143   
4           0.00          0.000            0.000                0.135   

   test_recall_coverage  
0                   NaN  
1                   NaN  
2                 0.143  
3                 0.468  
4                   NaN  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M      54                 47     27             27   
1   CART    L-S      54                  7      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0           0.87          1.000            0.130                0.143   
1           0.13          0.333            0.204                0.460   

   test_recall_coverage  
0                 0.574  
1                 0.143
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

      method      policy target  L-L       L-M       L-S  M-L  M-M  M-S  S-L  \
0   test set  OFF,OFF,ON         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
1   test set  OFF,ON,OFF         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
2   test set   OFF,ON,ON         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
3   test set  ON,OFF,OFF         0.0  0.555556  0.444444  0.0  0.0  0.0  0.0   
4   test set   ON,OFF,ON         0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
5   test set   ON,ON,OFF         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
6       prim  OFF,OFF,ON    L-L  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
7       prim   ON,OFF,ON    L-L  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
8       prim  ON,OFF,OFF    L-L  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
9       prim  OFF,ON,OFF    L-L  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
10      prim   OFF,ON,ON    L-L  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
11      prim   ON,ON,OFF    L-L  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
12      prim  OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
13      prim   ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
14      prim   OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
15      prim   ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
16      prim  ON,OFF,OFF    L-M  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
17      prim  OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
18      prim   ON,ON,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
19      prim  OFF,ON,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
20      prim  OFF,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
21      prim   OFF,ON,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
22      prim  ON,OFF,OFF    L-S  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
23      prim   ON,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
24      prim   ON,ON,OFF    M-M  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
25      prim   ON,OFF,ON    M-M  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
26      prim  ON,OFF,OFF    M-M  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
27      prim  OFF,OFF,ON    M-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
28      prim   OFF,ON,ON    M-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
29      prim  OFF,ON,OFF    M-M  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
30      prim  ON,OFF,OFF    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
31      prim   OFF,ON,ON    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
32      prim  OFF,OFF,ON    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
33      prim   ON,ON,OFF    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
34      prim   ON,OFF,ON    M-S  0.0  0.500000  0.500000  0.0  0.0  0.0  0.0   
35      prim  OFF,ON,OFF    M-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
36      cart  OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
37      cart  OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
38      cart   OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
39      cart  ON,OFF,OFF    L-M  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
40      cart   ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
41      cart   ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
42      cart  OFF,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
43      cart  OFF,ON,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
44      cart   OFF,ON,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
45      cart  ON,OFF,OFF    L-S  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
46      cart   ON,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
47      cart   ON,ON,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   

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
35  0.0  0.0  
36  0.0  0.0  
37  0.0  0.0  
38  0.0  0.0  
39  0.0  0.0  
40  0.0  0.0  
41  0.0  0.0  
42  0.0  0.0  
43  0.0  0.0  
44  0.0  0.0  
45  0.0  0.0  
46  0.0  0.0  
47  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
M-S  0.0  0.0  0.0  0.0  0.0  0.0  0.428571  0.063830  0.0
M-M  0.0  0.0  0.0  0.0  0.0  0.0  0.142857  0.212766  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.142857  0.042553  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.468085  0.0
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.063830  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-50-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L       L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.000000  0.574468  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.142857  0.042553  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
