# Findings: `analysis-fl-rq-combined-patterns-stress-25-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** All supported non-empty pattern configurations at common 25% stress; clients 4/8/10 pooled; all environments; baseline excluded.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-combined-patterns-stress-25-text.ipynb](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__combined-patterns__clients-all__stress-25__environment-all.md](../boxes/boxes__task-text__combined-patterns__clients-all__stress-25__environment-all.md).
- **Plots:**
- [quality-space__task-text__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__combined-patterns__clients-all__stress-25__environment-all.png](../plots/feature-importance__task-text__combined-patterns__clients-all__stress-25__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000081.
Data split: 147 train, 63 test.

--- Train Set Tradeoff Counts ---
  L,S: 8 (5.44%)
  L,M: 139 (94.56%)

--- Test Set Tradeoff Counts ---
  L,S: 4 (6.35%)
  L,M: 59 (93.65%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,S: 0 (0.00%) [not printed in either partition]
  M,M: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
* Group: OFF,OFF,ON --> Tradeoff: L-M
* Group: OFF,ON,OFF --> Tradeoff: L-M
* Group: OFF,ON,ON --> Tradeoff: L-M
------------------------------
Grouping: client_selector_pattern
* Group: OFF --> Tradeoff: L-M
------------------------------
Grouping: message_compressor_pattern
  none
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: client_selector_pattern
* Tradeoff: L-S --> Group: ON
------------------------------
Grouping: message_compressor_pattern
  none
------------------------------
Grouping: hdh_pattern
  none
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 17.1627
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 17.1065
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 17.4153
Robustness Ranking for Tradeoff: M-S
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.2878
Robustness Ranking for Tradeoff: M-M

  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.1291
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 6.9576
Robustness Ranking for Tradeoff: L-S
  1. ON,OFF,OFF: 10% success
  2. ON,OFF,ON: 10% success
  3. ON,ON,OFF: 10% success
  Top Policy -> ON,OFF,OFF - Starr: 0.1000 - Regret: 0.8807
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 100% success
  2. OFF,ON,OFF: 100% success
  3. OFF,ON,ON: 100% success
  Top Policy -> OFF,OFF,ON - Starr: 1.0000 - Regret: 0.0000
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 0% success
  2. OFF,ON,OFF: 0% success
  3. OFF,ON,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 3.2385
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: varies in these runs, values [1, 2, 3]
Pattern Instances: varies in these runs, values [1, 2, 3, 4, 5, 7, 8, 9, 10, 11, 12]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                       90               3              1             10   
2                       90               3              1             12   
3                       30               1              4             11   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.902                 11.485  
2                                         0.897                 11.308  
3                                         0.892                 11.254  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON    30      1.667                      0.898   
                     OFF,ON,OFF    30      7.333                      0.906   
                     ON,OFF,OFF    30      1.000                      0.901   
2                    OFF,ON,ON     30      9.000                      0.899   
                     ON,OFF,ON     30      2.467                      0.891   
                     ON,ON,OFF     30      6.667                      0.901   
3                    ON,ON,ON      30      8.133                      0.892   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                 11.830  
                     OFF,ON,OFF                 12.076  
                     ON,OFF,OFF                 10.548  
2                    OFF,ON,ON                  12.256  
                     ON,OFF,ON                  10.716  
                     ON,ON,OFF                  10.953  
3                    ON,ON,ON                   11.254
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L  M-S  M-M  M-L   L-S   L-M  L-L
policy                                                             
Pattern Instances=1   0.0  0.0  0.0  0.0  0.0  0.0  0.07  0.93  0.0
Pattern Instances=2   0.0  0.0  0.0  0.0  0.0  0.0  0.09  0.91  0.0
Pattern Instances=3   0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=4   0.0  0.0  0.0  0.0  0.0  0.0  0.14  0.86  0.0
Pattern Instances=5   0.0  0.0  0.0  0.0  0.0  0.0  0.16  0.84  0.0
Pattern Instances=7   0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=8   0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=9   0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=10  0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=11  0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
Pattern Instances=12  0.0  0.0  0.0  0.0  0.0  0.0  0.00  1.00  0.0
[figure rendered in notebook]
                        S-S  S-M  S-L  M-S  M-M  M-L   L-S   L-M  L-L
policy                                                               
Pattern Types Active=1  0.0  0.0  0.0  0.0  0.0  0.0  0.03  0.97  0.0
Pattern Types Active=2  0.0  0.0  0.0  0.0  0.0  0.0  0.07  0.93  0.0
Pattern Types Active=3  0.0  0.0  0.0  0.0  0.0  0.0  0.10  0.90  0.0
[figure rendered in notebook]
Counts by pattern-count group:

tradeoff             L-M  L-S
Pattern Count Group          
1                     87    3
2-3                  111    9
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x1660cb2d0>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'Message Compressor Alg', 'HDH Batch Size', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

                              final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                    0.000000        0.199303
Batch Size                              0.000000        0.000000
CPU Mean                                0.000000        0.000000
Client Selector Criteria                0.048732        0.562860
Client Selector Instances               0.000000        0.000000
Client Selector Strategy                0.000000        0.000000
Client Selector Value                   0.000000        0.000000
Data Distribution Diversity             0.000000        0.000000
Data Persistence Diversity              0.000000        0.000000
Epochs                                  0.000000        0.000000
HDH Batch Size                          0.000000        0.037907
HDH Beta 1                              0.000000        0.000000
HDH Beta 2                              0.000000        0.000000
HDH Discriminator                       0.000000        0.000000
HDH Epochs                              0.000000        0.000000
HDH Generator                           0.000000        0.000000
HDH Instances                           0.000000        0.000000
HDH Latent Dim                          0.000000        0.000000
HDH Learning Rate                       0.000000        0.000000
HDH Optimizer                           0.000000        0.000000
JSD Mean                                0.567376        0.000000
Learning Rate                           0.000000        0.000000
Message Compressor Alg                  0.000000        0.088636
Message Compressor Instances            0.000000        0.000000
N Rounds                                0.000000        0.000000
Optimizer                               0.000000        0.000000
Pattern Instances                       0.147030        0.000000
Pattern Types Active                    0.057162        0.111294
RAM Mean                                0.000000        0.000000
Total Clients                           0.179700        0.000000
delay_percentage                        0.000000        0.000000
low_spec_percentage                     0.000000        0.000000
non_iid_percentage                      0.000000        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff L-S (L,S): lift=0.27
	Total Clients: [4.000, 6.000]
	Client Selector Criteria: {CPU}
	Pattern Instances: [1.500, 12.000]
 2. For tradeoff L-M (L,M): lift=0.06
	Total Clients: [6.000, 10.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-5487f837)

```text
PRIM Box 1: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ Client Selector = ON (Strategy = Resource-Based; Criteria = CPU; Value = 2.0)
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: ON (20/20)
  ◦ HDH: OFF (7/20), ON (13/20)
  ◦ Message Compressor: OFF (6/20), ON (14/20)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: ON (9/9)
  ◦ HDH: OFF (3/9), ON (6/9)
  ◦ Message Compressor: OFF (3/9), ON (6/9)
• Operating envelope:
  ◦ Pattern Instances [1.5, 12]
• Other design conditions:
  ◦ Total Clients [4, 6]

PRIM Box 2: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (42/98), ON (56/98)
  ◦ HDH: OFF (42/98), ON (56/98)
  ◦ Message Compressor: OFF (42/98), ON (56/98)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/42), ON (24/42)
  ◦ HDH: OFF (18/42), ON (24/42)
  ◦ Message Compressor: OFF (18/42), ON (24/42)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (42/98), ON (56/98)
  ◦ HDH: OFF (42/98), ON (56/98)
  ◦ Message Compressor: OFF (42/98), ON (56/98)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (18/42), ON (24/42)
  ◦ HDH: OFF (18/42), ON (24/42)
  ◦ Message Compressor: OFF (18/42), ON (24/42)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [6, 10]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    L-S      63                  4      9              3   
1   PRIM    L-M      63                 59     42             42   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.063          0.333            0.270                0.246   
1          0.937          1.000            0.063                0.054   

   test_recall_coverage  
0                 0.750  
1                 0.712  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M      63                 59     42             42   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.937            1.0            0.063                0.054   

   test_recall_coverage  
0                 0.712
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.

      method      policy target  L-L       L-M       L-S  M-L  M-M  M-S  S-L  \
0   test set  OFF,OFF,ON         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
1   test set  OFF,ON,OFF         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
2   test set   OFF,ON,ON         0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
3   test set  ON,OFF,OFF         0.0  0.888889  0.111111  0.0  0.0  0.0  0.0   
4   test set   ON,OFF,ON         0.0  0.888889  0.111111  0.0  0.0  0.0  0.0   
5   test set   ON,ON,OFF         0.0  0.888889  0.111111  0.0  0.0  0.0  0.0   
6   test set    ON,ON,ON         0.0  0.888889  0.111111  0.0  0.0  0.0  0.0   
7       prim  OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
8       prim  OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
9       prim   OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
10      prim  ON,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
11      prim   ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
12      prim   ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
13      prim    ON,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
14      prim  OFF,OFF,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
15      prim  OFF,ON,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
16      prim   OFF,ON,ON    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
17      prim  ON,OFF,OFF    L-S  0.0  0.000000  0.000000  0.0  0.0  0.0  0.0   
18      prim   ON,OFF,ON    L-S  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
19      prim   ON,ON,OFF    L-S  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
20      prim    ON,ON,ON    L-S  0.0  0.666667  0.333333  0.0  0.0  0.0  0.0   
21      cart  OFF,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
22      cart  OFF,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
23      cart   OFF,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
24      cart  ON,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
25      cart   ON,OFF,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
26      cart   ON,ON,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
27      cart    ON,ON,ON    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   

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
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L   L-S       L-M  L-L
L-S  0.0  0.0  0.0  0.0  0.0  0.0  0.75  0.101695  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.00  0.711864  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-combined-patterns-stress-25-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S       L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.711864  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
