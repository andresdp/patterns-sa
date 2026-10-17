# Findings: analysis-fl-rq-baseline-image

## Scope and support

Image, CIFAR-10/CNN 16k; baseline OFF,OFF,OFF; clients 4/8/10 pooled; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-baseline-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000027.
Data split: 126 train, 54 test.

--- Train Set Tradeoff Counts ---
  S,M: 31 (24.60%)
  M,S: 21 (16.67%)
  M,M: 74 (58.73%)

--- Test Set Tradeoff Counts ---
  S,M: 13 (24.07%)
  M,S: 9 (16.67%)
  M,M: 32 (59.26%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
Pattern Instances is constant in these runs: no stress levels to compare.
Pattern Types Active is constant in these runs: no stress levels to compare.
Counts by pattern-count group:
tradeoff             M-M  M-S  S-M
Pattern Count Group               
0                    106   30   44Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x167f01a50>
```

See the [quality-space plot](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Excluded constant parameters from feature scoring (train): ['N Rounds', 'Model', 'Dataset', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'RAM Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['Total Clients', 'CPU Mean', 'Alpha
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    95
True     31
Name: count, dtype: int64
Total instances: (126, 3)
Running PRIM ... rhodium
4 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'Alpha Dirichlet Mean': '[0.600, 0.750]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.9032258064516129, 'population_prevalence': 0.24603174603174602, 'lift': 0.753968253968254, 'population_size': 126.0, 'total_targets': 31.0, 'samples_in_box': 28.0, 'targets_in_box': 28.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.9230769230769231, 'population_prevalence': 0.24074074074074073, 'lift': 0.7592592592592593, 'population_size': 54.0, 'total_targets': 13.0, 'samples_in_box': 12.0, 'targets_in_box': 12.0}
------------------------------
Discovering scenarios for: M-S
Running PRIM discovery for: M-S ...
Instances satisfying property: False    105
True      21
Name: count, dtype: int64
Total instances: (126, 3)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'delay_percentage': '[0.000, 12.500]'}
* Discovery metrics: {'density': 1.0, 'coverage': 1.0, 'population_prevalence': 0.16666666666666666, 'lift': 0.8333333333333334, 'population_size': 126.0, 'total_targets': 21.0, 'samples_in_box': 21.0, 'targets_in_box': 21.0}
* Held-out metrics: {'density': 1.0, 'coverage': 1.0, 'population_prevalence': 0.16666666666666666, 'lift': 0.8333333333333334, 'population_size': 54.0, 'total_targets': 9.0, 'samples_in_box': 9.0, 'targets_in_box': 9.0}
------------------------------
Discovering scenarios for: M-M
Running PRIM discovery for: M-M ...
Instances satisfying property: True
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-M      54                 13     12             12   
1   PRIM    M-S      54                  9      9              9   
2   PRIM    M-M      54                 32     27             27   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.241            1.0            0.759                0.754   
1          0.167            1.0            0.833                0.833   
2          0.593            1.0            0.407                0.413   

   test_recall_coverage  
0                 0.923  
1                 1.000  
2                 0.844  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      54                 32     27             27   
1   CART    S-M      54                 13     12             12   
2   CART    M-S      54                  9      9              9   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.593            1.0            0.407                0.413   
1          0.241            1.0            0.759                0.754   
2          0.167
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-baseline-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-baseline-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-baseline-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-baseline-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-baseline-image.ipynb#cell-68); [box report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png).
