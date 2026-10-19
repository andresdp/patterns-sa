# Findings: analysis-fl-rq-stress-only-message_compressor-image

## Scope and support

Image, CIFAR-10/CNN 16k; exactly message compressor ON with other patterns OFF; stress levels pooled across clients 4/8/10; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000081.
Data split: 147 train, 63 test.

--- Train Set Tradeoff Counts ---
  S,M: 15 (10.20%)
  M,S: 21 (14.29%)
  M,M: 111 (75.51%)

--- Test Set Tradeoff Counts ---
  S,M: 7 (11.11%)
  M,S: 9 (14.29%)
  M,M: 47 (74.60%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=4   0.0  0.03  0.0  0.14  0.83  0.0  0.0  0.0  0.0
Pattern Instances=8   0.0  0.14  0.0  0.14  0.71  0.0  0.0  0.0  0.0
Pattern Instances=10  0.0  0.14  0.0  0.14  0.71  0.0  0.0  0.0  0.0Pattern Types Active is constant in these runs: no stress levels to compare.
Runs and objective means by Message Compressor Stress Percentage:
                                      runs  final_val_accuracy (mean)  \
Message Compressor Stress Percentage                                    
0.0                                     30                      0.541   
25.0                                    30                      0.538   
50.0                                    30                      0.539   
75.0                                    90                      0.507   
100.0                                   30                      0.542   

                                      avg_total_time (mean)  
Message Compressor Stress Percentage                         
0.0                                                   4.490  
25.0                                                 12.292  
50.0                                                 13.215  
75.0                                                 13.543  
100.0                                                13.828  Tradeoff counts by stress level:
tradeoff                              M-M  M-S  S-M
Message Compressor Stress Percentage               
0                                       0   30    0
25                                     30    0    0
50                                     30    0    0
75                                     68    0   22
100
```

See the [quality-space plot](../plots/quality-space__task-image__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'low_spec_percentage', 'non_iid_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Features selected: ['N Rounds', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selec
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    132
True      15
Name: count, dtype: int64
Total instances: (147, 4)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'Message Compressor Instances': '[6.000, 10.000]', 'non_iid_percentage': '[50.000, 75.000]'}
* Discovery metrics: {'density': 1.0, 'coverage': 0.9333333333333333, 'population_prevalence': 0.10204081632653061, 'lift': 0.8979591836734694, 'population_size': 147.0, 'total_targets': 15.0, 'samples_in_box': 14.0, 'targets_in_box': 14.0}
* Held-out metrics: {'density': 1.0, 'coverage': 0.8571428571428571, 'population_prevalence': 0.1111111111111111, 'lift': 0.8888888888888888, 'population_size': 63.0, 'total_targets': 7.0, 'samples_in_box': 6.0, 'targets_in_box': 6.0}
------------------------------
Discovering scenarios for: M-S
Running PRIM discovery for: M-S ...
Instances satisfying property: False    126
True      21
Name: count, dtype: int64
Total instances: (147, 4)
Running PRIM ... rhodium
2 possible boxes
* Key Rules: {'Alpha Dirichlet Mean': '[0.750, 0.900]', 'Message Compressor Stress Percentage': '[0.000, 12.500]'}
* Discovery metrics: {'density': 1.0, 'coverage': 1.0, 'population_prevalence': 0.14285714285714285, 'lift': 0.8571428571428572, 'population_size': 147.0, 'total_targets': 21.0, 'samples_in_box': 21.0, 'targets_in_box': 21.0}
* Held-out metrics: {'density': 1.0, 'coverage': 1.0, 'population_prevalence': 0.14285714285714285, 'lift': 0.8571428571428572, 'population_size': 63.0, 'total_targets': 9.0, 'samples_in_box': 9.0, 'targets_in_box': 9.0}
------------------------------
Discovering scenarios for:
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-M      63                  7      6              6   
1   PRIM    M-S      63                  9      9              9   
2   PRIM    M-M      63                 47     45             45   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.111            1.0            0.889                0.898   
1          0.143            1.0            0.857                0.857   
2          0.746            1.0            0.254                0.245   

   test_recall_coverage  
0                 0.857  
1                 1.000  
2                 0.957  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      63                 47     45             45   
1   CART    M-S      63                  9      9              9   
2   CART    S-M      63                  7      6              6   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.746            1.0            0.254                0.245   
1          0.143            1.0            0.857                0.857   
2          0.111
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-stress-only-message_compressor-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-stress-only-message_compressor-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-stress-only-message_compressor-image.md); [quality-space plot](../plots/quality-space__task-image__stress-ONLY-message_compressor__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__stress-ONLY-message_compressor__clients-all__environment-all.png).
