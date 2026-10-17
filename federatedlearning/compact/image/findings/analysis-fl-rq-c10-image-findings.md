# Findings: analysis-fl-rq-c10-image

## Scope and support

Image, CIFAR-10/CNN 16k; all eight configurations, fixed client count 10; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-c10-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000028.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (4.76%)
  S,M: 76 (27.84%)
  M,S: 38 (13.92%)
  M,M: 146 (53.48%)

--- Test Set Tradeoff Counts ---
  S,S: 6 (5.13%)
  S,M: 33 (28.21%)
  M,S: 16 (13.68%)
  M,M: 62 (52.99%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                               
Pattern Instances=0   0.00  0.55  0.0  0.09  0.36  0.0  0.0  0.0  0.0
Pattern Instances=1   0.22  0.21  0.0  0.05  0.51  0.0  0.0  0.0  0.0
Pattern Instances=3   0.10  0.20  0.0  0.00  0.70  0.0  0.0  0.0  0.0
Pattern Instances=6   0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=9   0.00  0.00  0.0  0.32  0.68  0.0  0.0  0.0  0.0
Pattern Instances=10  0.00  0.24  0.0  0.18  0.58  0.0  0.0  0.0  0.0
Pattern Instances=11  0.00  1.00  0.0  0.00  0.00  0.0  0.0  0.0  0.0<Figure size 800x445 with 2 Axes>                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.33  0.0  0.17  0.50  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.05  0.35  0.0  0.08  0.52  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.08  0.22  0.0  0.15  0.54  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.00  0.00  0.0  0.33  0.67  0.0  0.0  0.0  0.0<Figure size 800x340 with 2 Axes>Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     30   10   20    0
1                     88   14   60    8
2-3                   90   30   29   11Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x1656010d0>
```

See the [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-S
Running PRIM discovery for: S-S ...
Instances satisfying property: False    260
True      13
Name: count, dtype: int64
Total instances: (273, 4)
Running PRIM ... rhodium
3 possible boxes
* Key Rules: {'Alpha Dirichlet Mean': '[0.600, 0.675]', 'Client Selector Stress Percentage': '[22.500, 75.000]'}
* Discovery metrics: {'density': 0.7142857142857143, 'coverage': 0.7692307692307693, 'population_prevalence': 0.047619047619047616, 'lift': 0.6666666666666667, 'population_size': 273.0, 'total_targets': 13.0, 'samples_in_box': 14.0, 'targets_in_box': 10.0}
* Held-out metrics: {'density': 0.5, 'coverage': 0.5, 'population_prevalence': 0.05128205128205128, 'lift': 0.44871794871794873, 'population_size': 117.0, 'total_targets': 6.0, 'samples_in_box': 6.0, 'targets_in_box': 3.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    197
True      76
Name: count, dtype: int64
Total instances: (273, 4)
Running PRIM ... rhodium
5 possible boxes
* Key Rules: {'Alpha Dirichlet Mean': '[0.600, 0.825]', 'Client Selector Stress Percentage': '(not selected) or <= 35.000'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.8289473684210527, 'population_prevalence': 0.2783882783882784, 'lift': 0.7216117216117216, 'population_size': 273.0, 'total_targets': 76.0, 'samples_in_box': 63.0, 'targets_in_box': 63.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.8181818181818182, 'population_prevalence': 0.28205128205128205, 'lift': 0.717948717948718, 'population_size': 117.0, 'total_targets': 33.0, 'samples_in_box': 27.0, 'targets_in_box': 27.0}
------
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  6      6              3   
1   PRIM    S-M     117                 33     27             27   
2   PRIM    M-S     117                 16     15             15   
3   PRIM    M-M     117                 62     51             51   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.051            0.5            0.449                0.667   
1          0.282            1.0            0.718                0.722   
2          0.137            1.0            0.863                0.861   
3          0.530            1.0            0.470                0.465   

   test_recall_coverage  
0                 0.500  
1                 0.818  
2                 0.938  
3                 0.823  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 62     51             51   
1   CART    S-M     117                 33     27             27   
2   CART    M-S     117                 16     15             15   
3   CART    S-S     117                  6      3              1
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-c10-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-c10-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-c10-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-c10-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-c10-image.ipynb#cell-68); [box report](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md); [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__all-configurations__clients-10__environment-all.png).
