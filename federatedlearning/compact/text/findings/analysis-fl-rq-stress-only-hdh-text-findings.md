# Findings: `analysis-fl-rq-stress-only-hdh-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** Exactly hdh ON and the other two patterns OFF; stress levels 25/50/75%; clients pooled; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-stress-only-hdh-text.ipynb](../analysis-fl-rq-stress-only-hdh-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__stress-ONLY-hdh__clients-all__environment-all.md](../boxes/boxes__task-text__stress-ONLY-hdh__clients-all__environment-all.md).
- **Plots:**
- [quality-space__task-text__stress-ONLY-hdh__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__stress-ONLY-hdh__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__stress-ONLY-hdh__clients-all__environment-all.png](../plots/feature-importance__task-text__stress-ONLY-hdh__clients-all__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000622.
Data split: 105 train, 45 test.

--- Train Set Tradeoff Counts ---
  M,M: 3 (2.86%)
  L,M: 96 (91.43%)
  L,L: 6 (5.71%)

--- Test Set Tradeoff Counts ---
  M,M: 0 (0.00%)
  L,M: 42 (93.33%)
  L,L: 3 (6.67%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,S: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,S: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__stress-ONLY-hdh__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: Total Clients
* Group: Total Clients=8 --> Tradeoff: L-M
* Group: Total Clients=10 --> Tradeoff: L-M
------------------------------
Grouping: low_spec_percentage
  none
------------------------------
Grouping: non_iid_percentage
* Group: non_iid_percentage=25 --> Tradeoff: L-M
* Group: non_iid_percentage=50 --> Tradeoff: L-M
------------------------------
Grouping: delay_percentage
  none
```

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
Warning: 'config_id' has a single policy group (['OFF,OFF,ON']) in the 'all' runs, so no tradeoff can be exclusive to one of them.
  none
------------------------------
Grouping: Total Clients
* Tradeoff: M-M --> Group: Total Clients=4
* Tradeoff: L-L --> Group: Total Clients=4
------------------------------
Grouping: low_spec_percentage
  none
------------------------------
Grouping: non_iid_percentage
* Tradeoff: M-M --> Group: non_iid_percentage=75
* Tradeoff: L-L --> Group: non_iid_percentage=75
------------------------------
Grouping: delay_percentage
  none
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 8.5669
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 8.2124
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 8.4227
Robustness Ranking for Tradeoff: M-S
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 3.2649
Robustness Ranking for Tradeoff: M-M
  1. OFF,OFF,ON: 2% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0200 - Regret: 2.1832
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.8663
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,ON: 0% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0000 - Regret: 2.1734
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,ON: 92% success
  Top Policy -> OFF,OFF,ON - Starr: 0.9200 - Regret: 0.0950
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,ON: 6% success
  Top Policy -> OFF,OFF,ON - Starr: 0.0600 - Regret: 1.7589
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: constant in these runs, values [1]
Pattern Instances: varies in these runs, values [1, 2, 3, 4, 5, 6, 8]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
1                      150               1              1              8   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
1                                         0.842                   14.0  
Per configuration:

                                 runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                
1                    OFF,OFF,ON   150      4.467                      0.842   

                                 avg_total_time (mean)  
Pattern Types Active config_id                          
1                    OFF,OFF,ON                   14.0
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-de5fb604)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S  L-M  L-L
policy                                                          
Pattern Instances=1  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
Pattern Instances=2  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
Pattern Instances=3  0.0  0.0  0.0  0.0  0.1  0.0  0.0  0.6  0.3
Pattern Instances=4  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
Pattern Instances=5  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
Pattern Instances=6  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
Pattern Instances=8  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
[figure rendered in notebook]
Pattern Types Active is constant in these runs: no stress levels to compare.
Runs and objective means by HDH Stress Percentage:

                       runs  final_val_accuracy (mean)  avg_total_time (mean)
HDH Stress Percentage                                                        
25.0                     30                      0.898                 11.830
50.0                     30                      0.847                 12.861
75.0                     90                      0.821                 15.103
Tradeoff counts by stress level:

tradeoff               L-L  L-M  M-M
HDH Stress Percentage               
25                       0   30    0
50                       0   30    0
75                       9   78    3
Within-level tradeoff shares (STARR) by HDH Stress Percentage:

                          S-S  S-M  S-L  M-S    M-M  M-L  L-S    L-M  L-L
policy                                                                   
HDH Stress Percentage=25  0.0  0.0  0.0  0.0  0.000  0.0  0.0  1.000  0.0
HDH Stress Percentage=50  0.0  0.0  0.0  0.0  0.000  0.0  0.0  1.000  0.0
HDH Stress Percentage=75  0.0  0.0  0.0  0.0  0.033  0.0  0.0  0.867  0.1
[figure rendered in notebook]
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-0e85d978)

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Client Selector Instances', 'Message Compressor Instances', 'low_spec_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']

Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Client Selector Instances', 'Message Compressor Instances', 'low_spec_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']

                                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean                            0.000000        0.524207
Batch Size                                      0.000000        0.000000
CPU Mean                                        0.021652        0.031490
Client Selector Criteria                        0.000000        0.000000
Client Selector Instances                       0.000000        0.000000
Client Selector Strategy                        0.000000        0.000000
Client Selector Stress Percentage               0.000000        0.000000
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
HDH Instances                                   0.000000        0.000000
HDH Latent Dim                                  0.000000        0.000000
HDH Learning Rate                               0.000000        0.000000
HDH Optimizer                                   0.000000        0.000000
HDH Stress Percentage                           0.675432        0.000000
JSD Mean                                        0.197031        0.113835
Learning Rate                                   0.000000        0.000000
Message Compressor Alg                          0.000000        0.000000
Message Compressor Instances                    0.000000        0.000000
Message Compressor Stress Percentage            0.000000        0.000000
N Rounds                                        0.000000        0.000000
Optimizer                                       0.000000        0.000000
Pattern Instances                               0.000000        0.000000
Pattern Types Active                            0.000000        0.000000
RAM Mean                                        0.000000        0.000000
Total Clients                                   0.076955        0.222470
delay_percentage                                0.020382        0.094784
low_spec_percentage                             0.008548        0.013213
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff M-M (M,M): lift=0.00
	Total Clients: [4.000, 6.000]
	Alpha Dirichlet Mean: [0.600, 0.688]
	JSD Mean: [0.000, 0.018]
 2. For tradeoff L-M (L,M): lift=0.07
	Total Clients: [6.000, 10.000]
 3. For tradeoff L-L (L,L): lift=0.27
	Total Clients: [4.000, 6.000]
	delay_percentage: [50.000, 75.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-5487f837)

```text
PRIM Box 1: M-M (M,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (12/12)
  ◦ HDH: ON (12/12)
  ◦ Message Compressor: OFF (12/12)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: ON (9/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ Alpha Dirichlet Mean [0.6, 0.688]
  ◦ JSD Mean [0, 0.0175]
• Other design conditions:
  ◦ Total Clients [4, 6]

PRIM Box 2: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (70/70)
  ◦ HDH: ON (70/70)
  ◦ Message Compressor: OFF (70/70)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (30/30)
  ◦ HDH: ON (30/30)
  ◦ Message Compressor: OFF (30/30)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [6, 10]

PRIM Box 3: L-L (L,L)
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
  ◦ delay percentage [50, 75] (%)
• Other design conditions:
  ◦ Total Clients [4, 6]

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (70/70)
  ◦ HDH: ON (70/70)
  ◦ Message Compressor: OFF (70/70)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (30/30)
  ◦ HDH: ON (30/30)
  ◦ Message Compressor: OFF (30/30)
• Operating envelope:
  ◦ No uncertainty conditions in this box
• Other design conditions:
  ◦ Total Clients [6, 10]

CART Box 2: L-L (L,L)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (4/4)
  ◦ HDH: ON (4/4)
  ◦ Message Compressor: OFF (4/4)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (3/3)
  ◦ HDH: ON (3/3)
  ◦ Message Compressor: OFF (3/3)
• Operating envelope:
  ◦ JSD Mean [0, 0.0175]
  ◦ delay percentage [50, 75] (%)
• Other design conditions:
  ◦ Total Clients [4, 6]
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    M-M      45                  0      9              0   
1   PRIM    L-M      45                 42     30             30   
2   PRIM    L-L      45                  3      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.221   
1          0.933          1.000            0.067                0.086   
2          0.067          0.333            0.267                0.514   

   test_recall_coverage  
0                   NaN  
1                 0.714  
2                 0.333  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M      45                 42     30             30   
1   CART    L-L      45                  3      3              1   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.933          1.000            0.067                0.086   
1          0.067          0.333            0.267                0.443   

   test_recall_coverage  
0                 0.714  
1                 0.333
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-6d04057a)

```text
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

     method      policy target       L-L       L-M  L-S  M-L  M-M  M-S  S-L  \
0  test set  OFF,OFF,ON         0.066667  0.933333  0.0  0.0  0.0  0.0  0.0   
1      prim  OFF,OFF,ON    L-L  0.333333  0.666667  0.0  0.0  0.0  0.0  0.0   
2      prim  OFF,OFF,ON    L-M  0.000000  1.000000  0.0  0.0  0.0  0.0  0.0   
3      prim  OFF,OFF,ON    M-M  0.333333  0.666667  0.0  0.0  0.0  0.0  0.0   
4      cart  OFF,OFF,ON    L-L  0.333333  0.666667  0.0  0.0  0.0  0.0  0.0   
5      cart  OFF,OFF,ON    L-M  0.000000  1.000000  0.0  0.0  0.0  0.0  0.0   

   S-M  S-S  
0  0.0  0.0  
1  0.0  0.0  
2  0.0  0.0  
3  0.0  0.0  
4  0.0  0.0  
5  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S       L-M       L-L
M-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.142857  1.000000
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.714286  0.000000
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.047619  0.333333
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-stress-only-hdh-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S       L-M       L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.714286  0.000000
L-L  0.0  0.0  0.0  0.0  0.0  0.0  0.0  0.047619  0.333333
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
