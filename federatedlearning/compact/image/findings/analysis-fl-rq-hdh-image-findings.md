# Findings: analysis-fl-rq-hdh-image

## Scope and support

Image, CIFAR-10/CNN 16k; one fixed configuration profile; clients 4/8/10 pooled; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-hdh-image.ipynb#cell-18), cell 18:

```text
Warning: Some stratification classes have < 2 samples. Falling back to random split.
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000425.
Data split: 105 train, 45 test.

--- Train Set Tradeoff Counts ---
  S,S: 2 (1.90%)
  S,M: 57 (54.29%)
  M,S: 1 (0.95%)
  M,M: 45 (42.86%)

--- Test Set Tradeoff Counts ---
  S,S: 0 (0.00%)
  S,M: 25 (55.56%)
  M,S: 0 (0.00%)
  M,M: 20 (44.44%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0  0.02  0.58  0.0  0.01  0.39  0.0  0.0  0.0  0.0
Pattern Instances=1  0.00  0.29  0.0  0.00  0.71  0.0  0.0  0.0  0.0
Pattern Instances=2  0.00  0.25  0.0  0.00  0.75  0.0  0.0  0.0  0.0Pattern Types Active is constant in these runs: no stress levels to compare.
Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
1                     65    1   82    2Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x1680c1090>
```

See the [quality-space plot](../plots/quality-space__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Excluded constant parameters from feature scoring (train): ['N Rounds', 'Model', 'Dataset', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'RAM Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Client Selector Instances', 'Message Compressor Instances', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage']
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Pattern Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'delay_percentage']
Features selected: ['Total Clients', 'CPU Mean', 'Alpha Dirichlet Mean', 'JSD Me
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-S
Running PRIM discovery for: S-S ...
Instances satisfying property: False    103
True       2
Name: count, dtype: int64
Total instances: (105, 5)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'Total Clients': '[4.000, 6.000]', 'Alpha Dirichlet Mean': '[0.600, 0.688]', 'JSD Mean': '[0.026, 0.066]', 'delay_percentage': '[25.000, 50.000]'}
* Discovery metrics: {'density': 0.3333333333333333, 'coverage': 1.0, 'population_prevalence': 0.01904761904761905, 'lift': 0.3142857142857143, 'population_size': 105.0, 'total_targets': 2.0, 'samples_in_box': 6.0, 'targets_in_box': 2.0}
* Held-out metrics: {'density': 0.0, 'coverage': nan, 'population_prevalence': 0.0, 'lift': 0.0, 'population_size': 45.0, 'total_targets': 0.0, 'samples_in_box': 2.0, 'targets_in_box': 0.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: True     57
False    48
Name: count, dtype: int64
Total instances: (105, 5)
Running PRIM ... rhodium
5 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'Alpha Dirichlet Mean': '[0.600, 0.812]', 'JSD Mean': '[0.019, 0.081]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.9298245614035088, 'population_prevalence': 0.5428571428571428, 'lift': 0.4571428571428572, 'population_size': 105.0, 'total_targets': 57.0, 'samples_in_box': 53.0, 'targets_in_box': 53.0}
* Held-out metrics: {'density': 0.95, 'coverage': 0.76, 'population_prevalence': 0.5555555555555556, 'lift': 0.3944444444444444, 'population_size': 45.0, 'total_targets': 25.0, 'samples_in_box': 20.0, 'targets_in_box': 19.0}
----------------------------
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S      45                  0      2              0   
1   PRIM    S-M      45                 25     20             19   
2   PRIM    M-S      45                  0      3              0   
3   PRIM    M-M      45                 20      3              2   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.000          0.000            0.000                0.314   
1          0.556          0.950            0.394                0.457   
2          0.000          0.000            0.000                0.133   
3          0.444          0.667            0.222                0.571   

   test_recall_coverage  
0                   NaN  
1                  0.76  
2                   NaN  
3                  0.10  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    S-M      45                 25     20             19   
1   CART    M-M      45                 20      8              8   
2   CART    S-S      45                  0      0              0   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/boxes__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-hdh-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-hdh-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-hdh-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-hdh-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-hdh-image.ipynb#cell-68); [box report](../boxes/boxes__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).
