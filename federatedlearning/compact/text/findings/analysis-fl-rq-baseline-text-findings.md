# Findings: `analysis-fl-rq-baseline-text.ipynb`

## Case scope and support

- **Task:** text (AG_NEWS/MLP).
- **Scope:** Baseline profile (OFF,OFF,OFF); clients 4/8/10 pooled; all environments.
- **Grouping unit:** one observed run. Compact client attributes are run-level aggregates.
- **Source notebook:** [analysis-fl-rq-baseline-text.ipynb](../analysis-fl-rq-baseline-text.ipynb); **scope guide:** [NOTEBOOK_STRATIFICATION.md](../NOTEBOOK_STRATIFICATION.md).
- **Box report:** [boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md).
- **Plots:**
- [quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png)
- [feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png)

The objective grid is shared across the campaign: accuracy and average total round time are each divided into S/M/L bins, giving nine possible regions. A region omitted from the observed split distribution has zero rows in that partition; this is sample absence, not evidence of infeasibility. For the exact total, train/test counts, all populated region counts, grouped split score, and features/rules, see the notebook evidence below.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The notebook's printed split diagnostics give the total support and the complete train and held-out region distributions, with omitted regions called out as zero in each partition. Objective-space plots show the individual observed runs; region allocations and robustness outputs are reproduced below where emitted. Interpret stress or pattern-count summaries as marginal groupings: they are not complete configuration comparisons. For combined-pattern stress, each supported configuration contributes 30 rows at 25% and 50%, and at 75% the single-pattern configurations contribute 90 rows each while pairwise configurations contribute 30 each; client count is pooled, so composition can differ by configuration.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The notebook reports feature importance as model-relative predictive credit, and PRIM/CART rules as joint conditions. Conditions may mix design choices with operating context and run-level descriptors; they are associations, not independent effects. The box report provides architectural interpretation. Held-out rates below are evaluated on the grouped test partition; where a target has zero held-out rows or a box retains zero rows, its precision/coverage is undefined or unavailable rather than zero. Section 11's policy matrices are separate policy-conditioned views, not a substitute for the all-patterns test baseline.

## Evidence from current notebook outputs

#### [Notebook cell 18 — `ddf2adea`](../analysis-fl-rq-baseline-text.ipynb#cell-ddf2adea)

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000000.
Data split: 126 train, 54 test.

--- Train Set Tradeoff Counts ---
  L,S: 21 (16.67%)
  L,M: 105 (83.33%)

--- Test Set Tradeoff Counts ---
  L,S: 9 (16.67%)
  L,M: 45 (83.33%)
  S,S: 0 (0.00%) [not printed in either partition]
  S,M: 0 (0.00%) [not printed in either partition]
  S,L: 0 (0.00%) [not printed in either partition]
  M,S: 0 (0.00%) [not printed in either partition]
  M,M: 0 (0.00%) [not printed in either partition]
  M,L: 0 (0.00%) [not printed in either partition]
  L,L: 0 (0.00%) [not printed in either partition]
```

#### [Notebook cell 28 — `2970e574`](../analysis-fl-rq-baseline-text.ipynb#cell-2970e574)

```text
Saved objective-space chart: plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png

[figure rendered in notebook]
```

#### [Notebook cell 33 — `5f75a666`](../analysis-fl-rq-baseline-text.ipynb#cell-5f75a666)

```text
Deterministic groups (all their runs fall in a single tradeoff)
------------------------------
Grouping: configuration
  none
------------------------------
Grouping: Total Clients
  none
------------------------------
Grouping: low_spec_percentage
* Group: low_spec_percentage=75 --> Tradeoff: L-M
------------------------------
Grouping: non_iid_percentage
* Group: non_iid_percentage=75 --> Tradeoff: L-M
------------------------------
Grouping: delay_percentage
* Group: delay_percentage=0 --> Tradeoff: L-S
* Group: delay_percentage=25 --> Tradeoff: L-M
* Group: delay_percentage=75 --> Tradeoff: L-M
* Group: delay_percentage=100 --> Tradeoff: L-M
```

#### [Notebook cell 34 — `505c4983`](../analysis-fl-rq-baseline-text.ipynb#cell-505c4983)

```text
Exclusive tradeoffs (reached by a single group of the grouping)
------------------------------
Grouping: configuration
Warning: 'config_id' has a single policy group (['OFF,OFF,OFF']) in the 'all' runs, so no tradeoff can be exclusive to one of them.
  none
------------------------------
Grouping: Total Clients
  none
------------------------------
Grouping: low_spec_percentage
* Tradeoff: L-S --> Group: low_spec_percentage=25
------------------------------
Grouping: non_iid_percentage
* Tradeoff: L-S --> Group: non_iid_percentage=25
------------------------------
Grouping: delay_percentage
* Tradeoff: L-S --> Group: delay_percentage=0
```

#### [Notebook cell 39 — `796d4445`](../analysis-fl-rq-baseline-text.ipynb#cell-796d4445)

```text
Robustness Ranking for Tradeoff: S-S
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 12.8419
Robustness Ranking for Tradeoff: S-M
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 12.8263
Robustness Ranking for Tradeoff: S-L
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 12.9725
Robustness Ranking for Tradeoff: M-S
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 4.5061
Robustness Ranking for Tradeoff: M-M
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 4.4511
Robustness Ranking for Tradeoff: M-L
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 4.8436
Robustness Ranking for Tradeoff: L-S
  1. OFF,OFF,OFF: 17% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.1667 - Regret: 0.7925
Robustness Ranking for Tradeoff: L-M
  1. OFF,OFF,OFF: 83% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.8333 - Regret: 0.2676
Robustness Ranking for Tradeoff: L-L
  1. OFF,OFF,OFF: 0% success
  Top Policy -> OFF,OFF,OFF - Starr: 0.0000 - Regret: 1.8190
Overall Robustness Heatmap (STARR):

[figure rendered in notebook]
```

#### [Notebook cell 42 — `61da6b5b`](../analysis-fl-rq-baseline-text.ipynb#cell-61da6b5b)

```text
Pattern Types Active: constant in these runs, values [0]
Pattern Instances: constant in these runs, values [0]
Per stress level (S_types):

                      runs  configurations  instances_min  instances_max  \
Pattern Types Active                                                       
0                      180               1              0              0   

                      final_val_accuracy (mean)  avg_total_time (mean)  
Pattern Types Active                                                    
0                                         0.889                 11.286  
Per configuration:

                                  runs  instances  final_val_accuracy (mean)  \
Pattern Types Active config_id                                                 
0                    OFF,OFF,OFF   180        0.0                      0.889   

                                  avg_total_time (mean)  
Pattern Types Active config_id                           
0                    OFF,OFF,OFF                 11.286
```

#### [Notebook cell 43 — `de5fb604`](../analysis-fl-rq-baseline-text.ipynb#cell-de5fb604)

```text
Pattern Instances is constant in these runs: no stress levels to compare.
Pattern Types Active is constant in these runs: no stress levels to compare.
Counts by pattern-count group:

tradeoff             L-M  L-S
Pattern Count Group          
0                    150   30
Within-group tradeoff shares:

<pandas.io.formats.style.Styler at 0x162045850>
```

#### [Notebook cell 48 — `0e85d978`](../analysis-fl-rq-baseline-text.ipynb#cell-0e85d978)

```text
Excluded constant parameters from feature scoring (train): ['N Rounds', 'Model', 'Dataset', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']

Features selected: ['Total Clients', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Scoring features for outcome: avg_total_time (on subset: train)
Original features (numerically encoded): ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'delay_percentage']

                      final_val_accuracy  avg_total_time
Alpha Dirichlet Mean            0.000000        0.002572
CPU Mean                        0.000000        0.003081
Total Clients                   0.057442        0.042308
delay_percentage                0.018589        0.952039
low_spec_percentage             0.009314        0.000000
non_iid_percentage              0.914654        0.000000
```

#### [Notebook cell 56 — `914700be`](../analysis-fl-rq-baseline-text.ipynb#cell-914700be)

```text
Summary of PRIM boxes:
 1. For tradeoff L-S (L,S): lift=0.83
	non_iid_percentage: [25.000, 50.000]
	delay_percentage: [0.000, 12.500]
 2. For tradeoff L-M (L,M): lift=0.17
	delay_percentage: [12.500, 100.000]
```

#### [Notebook cell 62 — `5487f837`](../analysis-fl-rq-baseline-text.ipynb#cell-5487f837)

```text
PRIM Box 1: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (21/21)
  ◦ Message Compressor: OFF (21/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: OFF (9/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ non-IID percentage [25, 50] (%)
  ◦ delay percentage [0, 12.5] (%)

PRIM Box 2: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (105/105)
  ◦ HDH: OFF (105/105)
  ◦ Message Compressor: OFF (105/105)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (45/45)
  ◦ HDH: OFF (45/45)
  ◦ Message Compressor: OFF (45/45)
• Operating envelope:
  ◦ delay percentage [12.5, 100] (%)

CART Box 1: L-M (L,M)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (105/105)
  ◦ HDH: OFF (105/105)
  ◦ Message Compressor: OFF (105/105)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (45/45)
  ◦ HDH: OFF (45/45)
  ◦ Message Compressor: OFF (45/45)
• Operating envelope:
  ◦ delay percentage [12.5, 100] (%)

CART Box 2: L-S (L,S)
Architectural interpretation
• Design prescription:
  ◦ No pattern policy is required by the box conditions
• Observed pattern activation — training partition (rows matching this box):
  ◦ Client Selector: OFF (21/21)
  ◦ HDH: OFF (21/21)
  ◦ Message Compressor: OFF (21/21)
• Observed pattern activation — held-out partition (rows matching this box):
  ◦ Client Selector: OFF (9/9)
  ◦ HDH: OFF (9/9)
  ◦ Message Compressor: OFF (9/9)
• Operating envelope:
  ◦ delay percentage [0, 12.5] (%)
```

#### [Notebook cell 66 — `heldout-box-summary-all`](../analysis-fl-rq-baseline-text.ipynb#cell-heldout-box-summary-all)

```text
PRIM: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    L-S      54                  9      9              9   
1   PRIM    L-M      54                 45     45             45   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.167            1.0            0.833                0.833   
1          0.833            1.0            0.167                0.167   

   test_recall_coverage  
0                   1.0  
1                   1.0  
CART: held-out support, precision, lift and target coverage

  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    L-M      54                 45     45             45   
1   CART    L-S      54                  9      9              9   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.833            1.0            0.167                0.167   
1          0.167            1.0            0.833                0.833   

   test_recall_coverage  
0                   1.0  
1                   1.0
```

#### [Notebook cell 68 — `6d04057a`](../analysis-fl-rq-baseline-text.ipynb#cell-6d04057a)

```text
Warning: policy group 'ON,OFF,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

Warning: policy group 'ON,OFF,OFF' has no runs in the data; skipped.

Warning: policy group 'OFF,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'OFF,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,OFF' has no runs in the data; skipped.
Warning: policy group 'ON,OFF,ON' has no runs in the data; skipped.
Warning: policy group 'OFF,ON,ON' has no runs in the data; skipped.
Warning: policy group 'ON,ON,ON' has no runs in the data; skipped.

     method       policy target  L-L       L-M       L-S  M-L  M-M  M-S  S-L  \
0  test set  OFF,OFF,OFF         0.0  0.833333  0.166667  0.0  0.0  0.0  0.0   
1      prim  OFF,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
2      prim  OFF,OFF,OFF    L-S  0.0  0.000000  1.000000  0.0  0.0  0.0  0.0   
3      cart  OFF,OFF,OFF    L-M  0.0  1.000000  0.000000  0.0  0.0  0.0  0.0   
4      cart  OFF,OFF,OFF    L-S  0.0  0.000000  1.000000  0.0  0.0  0.0  0.0   

   S-M  S-S  
0  0.0  0.0  
1  0.0  0.0  
2  0.0  0.0  
3  0.0  0.0  
4  0.0  0.0
```

#### [Notebook cell 70 — `380905a7`](../analysis-fl-rq-baseline-text.ipynb#cell-380905a7)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S  L-M  L-L
L-S  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
```

#### [Notebook cell 73 — `807637a3`](../analysis-fl-rq-baseline-text.ipynb#cell-807637a3)

```text
S-S  S-M  S-L  M-S  M-M  M-L  L-S  L-M  L-L
L-M  0.0  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0
L-S  0.0  0.0  0.0  0.0  0.0  0.0  1.0  0.0  0.0
```

## Conditional implications and limitations

**Practitioners.** Treat any discovered conjunction as a candidate envelope to validate in this task and scope. Check its held-out retained support and target coverage before using it operationally; the filter describes already observed runs and does not simulate changing policies.

**Researchers.** These are observational, all-environment slices; pattern and operating-condition composition can differ, and pooled client counts or marginal pattern-count groupings do not isolate effects. The split groups by `partition_seed`; rare-class fallback diagnostics in the notebook govern how well the held-out distribution matches. Run-level client aggregation hides client-level imbalance and round-level variation.

**Case-specific limitations:** interpret only the observed task/configuration/stress slice. Empty regions and unsupported configuration/stress combinations do not establish impossibility. See the linked notebook, box report, and both plots for the primary evidence.
