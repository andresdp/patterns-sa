# Findings: analysis-fl-rq-combined-patterns-stress-50-image

## Scope and support

Image, CIFAR-10/CNN 16k; common enabled-pattern stress 50%; pooled clients 4/8/10; supported configurations only; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-18), cell 18:

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
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

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
Pattern Instances=10  0.00  0.50  0.0  0.00  0.50  0.0  0.0  0.0  0.0<Figure size 800x515 with 2 Axes>                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=1  0.00  0.21  0.0  0.10  0.69  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.06  0.30  0.0  0.09  0.56  0.0  0.0  0.0  0.0<Figure size 800x270 with 2 Axes>Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
1                     62    9   19    0
2-3                   50    8   27    5Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x1659ec290>
```

See the [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Message Comp
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-S
Running PRIM discovery for: S-S ...
Instances satisfying property: False    122
True       4
Name: count, dtype: int64
Total instances: (126, 5)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'CPU Mean': '[9.500, 10.125]', 'JSD Mean': '[0.024, 0.062]'}
* Discovery metrics: {'density': 0.4444444444444444, 'coverage': 1.0, 'population_prevalence': 0.031746031746031744, 'lift': 0.4126984126984127, 'population_size': 126.0, 'total_targets': 4.0, 'samples_in_box': 9.0, 'targets_in_box': 4.0}
* Held-out metrics: {'density': 0.0, 'coverage': 0.0, 'population_prevalence': 0.018518518518518517, 'lift': -0.018518518518518517, 'population_size': 54.0, 'total_targets': 1.0, 'samples_in_box': 4.0, 'targets_in_box': 0.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    94
True     32
Name: count, dtype: int64
Total instances: (126, 5)
Running PRIM ... rhodium
5 possible boxes
* Key Rules: {'Total Clients': '[9.000, 10.000]', 'CPU Mean': '[10.125, 11.000]', 'JSD Mean': '[0.014, 0.062]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.4375, 'population_prevalence': 0.25396825396825395, 'lift': 0.746031746031746, 'population_size': 126.0, 'total_targets': 32.0, 'samples_in_box': 14.0, 'targets_in_box': 14.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.42857142857142855, 'population_prevalence': 0.25925925925925924, 'lift': 0.7407407407407407, 'population_size': 54.0, 'total_targets': 14.0, 'samples_in_box': 6.0, 'targets_in_box': 6.0}
------------------------------
Discovering scenario
```

Held-out PRIM/CART performance (Section 13, cell 66):

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
3                 0.265  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      54                 34     18             18   
1   CART    S-M      54                 14      2              2   
2   CART    M-S      54                  5      1              0   
3   CART    S-S      54                  1      0              0
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/boxes__task-image__combined-patterns__clients-all__stress-50__environment-all.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-combined-patterns-stress-50-image.ipynb#cell-68); [box report](../boxes/boxes__task-image__combined-patterns__clients-all__stress-50__environment-all.md); [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-50__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-50__environment-all.png).
