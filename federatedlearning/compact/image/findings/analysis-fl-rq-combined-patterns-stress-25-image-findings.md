# Findings: analysis-fl-rq-combined-patterns-stress-25-image

## Scope and support

Image, CIFAR-10/CNN 16k; common enabled-pattern stress 25%; pooled clients 4/8/10; supported configurations only; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-18), cell 18:

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
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0   0.0  0.00  0.0  0.03  0.97  0.0  0.0  0.0  0.0
Pattern Instances=1   0.0  0.02  0.0  0.11  0.87  0.0  0.0  0.0  0.0
Pattern Instances=4   0.0  0.00  0.0  0.18  0.82  0.0  0.0  0.0  0.0
Pattern Instances=7   0.0  0.00  0.0  0.05  0.95  0.0  0.0  0.0  0.0
Pattern Instances=8   0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=9   0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=10  0.0  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0<Figure size 800x445 with 2 Axes>                        S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                
Pattern Types Active=1  0.0  0.00  0.0  0.04  0.96  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.0  0.01  0.0  0.08  0.91  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.0  0.00  0.0  0.17  0.83  0.0  0.0  0.0  0.0Counts by pattern-count group:
tradeoff             M-M  M-S  S-M
Pattern Count Group               
1                     86    4    0
2-3                  107   12    1Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x16382f250>
```

See the [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Criteria', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    146
True       1
Name: count, dtype: int64
Total instances: (147, 7)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'Message Compressor Alg': '{(not selected)}', 'JSD Mean': '[0.001, 0.015]', 'Pattern Types Active': '[1.500, 3.000]'}
* Discovery metrics: {'density': 0.07692307692307693, 'coverage': 1.0, 'population_prevalence': 0.006802721088435374, 'lift': 0.07012035583464156, 'population_size': 147.0, 'total_targets': 1.0, 'samples_in_box': 13.0, 'targets_in_box': 1.0}
* Held-out metrics: {'density': 0.0, 'coverage': nan, 'population_prevalence': 0.0, 'lift': 0.0, 'population_size': 63.0, 'total_targets': 0.0, 'samples_in_box': 6.0, 'targets_in_box': 0.0}
------------------------------
Discovering scenarios for: M-S
Running PRIM discovery for: M-S ...
Instances satisfying property: False    136
True      11
Name: count, dtype: int64
Total instances: (147, 7)
Running PRIM ... rhodium
4 possible boxes
* Key Rules: {'Total Clients': '[4.000, 6.000]', 'Client Selector Criteria': '{CPU}', 'HDH Batch Size': '[30.400, 32.000]'}
* Discovery metrics: {'density': 0.42857142857142855, 'coverage': 0.5454545454545454, 'population_prevalence': 0.07482993197278912, 'lift': 0.3537414965986394, 'population_size': 147.0, 'total_targets': 11.0, 'samples_in_box': 14.0, 'targets_in_box': 6.0}
* Held-out metrics: {'density': 0.3333333333333333, 'coverage': 0.4, 'population_prevalence': 0.07936507936507936, 'lift': 0.25396825396825395, 'population_size': 63.0, 'total_targets': 5.0, 'samples_in_box': 6.0, 'targets_in_box': 2.0}
---------------------
```

Held-out PRIM/CART performance (Section 13, cell 66):

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
2                 0.397  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      63                 58     42             41   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.921          0.976            0.056                0.082   

   test_recall_coverage  
0                 0.707
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-combined-patterns-stress-25-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-combined-patterns-stress-25-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-combined-patterns-stress-25-image.md); [quality-space plot](../plots/quality-space__task-image__combined-patterns__clients-all__stress-25__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__combined-patterns__clients-all__stress-25__environment-all.png).
