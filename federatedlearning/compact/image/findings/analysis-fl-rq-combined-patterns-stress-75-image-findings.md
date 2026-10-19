# Findings: analysis-fl-rq-combined-patterns-stress-75-image

## Scope and support

Image, CIFAR-10/CNN 16k; common enabled-pattern stress 75%; pooled clients 4/8/10; supported configurations only; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-18), cell 18:

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
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

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
Pattern Instances=11  0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0<Figure size 800x585 with 2 Axes>                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=1  0.07  0.39  0.0  0.09  0.44  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.27  0.32  0.0  0.07  0.34  0.0  0.0  0.0  0.0<Figure size 800x270 with 2 Axes>Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
1                    120   24  106   20
2-3                   31    6   29   24Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x16374e050>
```

See the [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persisten
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-S
Running PRIM discovery for: S-S ...
Instances satisfying property: False    222
True      30
Name: count, dtype: int64
Total instances: (252, 5)
Running PRIM ... rhodium
6 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'Client Selector Criteria': '{CPU}', 'JSD Mean': '[0.010, 0.110]', 'delay_percentage': '[25.000, 50.000]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.43333333333333335, 'population_prevalence': 0.11904761904761904, 'lift': 0.8809523809523809, 'population_size': 252.0, 'total_targets': 30.0, 'samples_in_box': 13.0, 'targets_in_box': 13.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.2857142857142857, 'population_prevalence': 0.12962962962962962, 'lift': 0.8703703703703703, 'population_size': 108.0, 'total_targets': 14.0, 'samples_in_box': 4.0, 'targets_in_box': 4.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    157
True      95
Name: count, dtype: int64
Total instances: (252, 5)
Running PRIM ... rhodium
9 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'Client Selector Criteria': '{(not selected)}', 'JSD Mean': '[0.004, 0.120]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.5894736842105263, 'population_prevalence': 0.376984126984127, 'lift': 0.623015873015873, 'population_size': 252.0, 'total_targets': 95.0, 'samples_in_box': 56.0, 'targets_in_box': 56.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.6, 'population_prevalence': 0.37037037037037035, 'lift': 0.6296296296296297, 'population_size': 108.0, 'total_targets': 40.0, 'samples_in_box': 24.0
```

Held-out PRIM/CART performance (Section 13, cell 66):

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
3                 0.400  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    S-M     108                 40     30             30   
1   CART    M-M     108                 45     18             18   
2   CART    S-S     108                 14      4              4   
3   CART    M-S     108                  9      3              1
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-combined-patterns-stress-75-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-combined-patterns-stress-75-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-combined-patterns-stress-75-image.md); [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-75__environment-all.png).
