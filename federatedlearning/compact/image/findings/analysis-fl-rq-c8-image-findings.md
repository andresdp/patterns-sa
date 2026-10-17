# Findings: analysis-fl-rq-c8-image

## Scope and support

Image, CIFAR-10/CNN 16k; all eight configurations, fixed client count 8; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-c8-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000010.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (4.76%)
  S,M: 73 (26.74%)
  M,S: 42 (15.38%)
  M,M: 145 (53.11%)

--- Test Set Tradeoff Counts ---
  S,S: 6 (5.13%)
  S,M: 31 (26.50%)
  M,S: 18 (15.38%)
  M,M: 62 (52.99%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0  0.00  0.52  0.0  0.09  0.39  0.0  0.0  0.0  0.0
Pattern Instances=1  0.20  0.23  0.0  0.12  0.45  0.0  0.0  0.0  0.0
Pattern Instances=3  0.10  0.20  0.0  0.00  0.70  0.0  0.0  0.0  0.0
Pattern Instances=5  0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0
Pattern Instances=7  0.02  0.02  0.0  0.32  0.64  0.0  0.0  0.0  0.0
Pattern Instances=8  0.00  0.22  0.0  0.18  0.60  0.0  0.0  0.0  0.0
Pattern Instances=9  0.00  0.25  0.0  0.12  0.62  0.0  0.0  0.0  0.0<Figure size 800x445 with 2 Axes>                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.33  0.0  0.17  0.50  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.03  0.34  0.0  0.11  0.52  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.10  0.19  0.0  0.16  0.55  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.03  0.03  0.0  0.33  0.60  0.0  0.0  0.0  0.0<Figure size 800x340 with 2 Axes>Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     30   10   20    0
1                     88   19   58    5
2-3                   89   31   26   14Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x16369d090>
```

See the [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'Data Distribution
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
* Key Rules: {'Client Selector Criteria': '{CPU}', 'CPU Mean': '[8.250, 8.875]', 'Alpha Dirichlet Mean': '[0.625, 0.812]'}
* Discovery metrics: {'density': 0.6428571428571429, 'coverage': 0.6923076923076923, 'population_prevalence': 0.047619047619047616, 'lift': 0.5952380952380953, 'population_size': 273.0, 'total_targets': 13.0, 'samples_in_box': 14.0, 'targets_in_box': 9.0}
* Held-out metrics: {'density': 0.6666666666666666, 'coverage': 0.6666666666666666, 'population_prevalence': 0.05128205128205128, 'lift': 0.6153846153846153, 'population_size': 117.0, 'total_targets': 6.0, 'samples_in_box': 6.0, 'targets_in_box': 4.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    200
True      73
Name: count, dtype: int64
Total instances: (273, 4)
Running PRIM ... rhodium
6 possible boxes
* Key Rules: {'Client Selector Criteria': '{(not selected)}', 'Alpha Dirichlet Mean': '[0.625, 0.688]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.6712328767123288, 'population_prevalence': 0.2673992673992674, 'lift': 0.7326007326007327, 'population_size': 273.0, 'total_targets': 73.0, 'samples_in_box': 49.0, 'targets_in_box': 49.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.6774193548387096, 'population_prevalence': 0.26495726495726496, 'lift': 0.7350427350427351, 'population_size': 117.0, 'total_targets': 31.0, 'samples_in_box': 21.0, 'targets_in
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  6      6              4   
1   PRIM    S-M     117                 31     21             21   
2   PRIM    M-S     117                 18      9              9   
3   PRIM    M-M     117                 62     33             33   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.051          0.667            0.615                0.595   
1          0.265          1.000            0.735                0.733   
2          0.154          1.000            0.846                0.846   
3          0.530          1.000            0.470                0.469   

   test_recall_coverage  
0                 0.667  
1                 0.677  
2                 0.500  
3                 0.532  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 62     33             33   
1   CART    S-M     117                 31     21             21   
2   CART    M-S     117                 18      9              9   
3   CART    S-S     117                  6      6              4
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-c8-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-c8-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-c8-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-c8-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-c8-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-c8-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-c8-image.md); [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__all-configurations__clients-8__environment-all.png).
