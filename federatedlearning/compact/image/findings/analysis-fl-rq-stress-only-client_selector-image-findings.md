# Findings: analysis-fl-rq-stress-only-client_selector-image

## Scope and support

Image, CIFAR-10/CNN 16k; exactly client selector ON with other patterns OFF; stress levels pooled across clients 4/8/10; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000267.
Data split: 105 train, 45 test.

--- Train Set Tradeoff Counts ---
  S,S: 13 (12.38%)
  S,M: 15 (14.29%)
  M,S: 25 (23.81%)
  M,M: 52 (49.52%)

--- Test Set Tradeoff Counts ---
  S,S: 5 (11.11%)
  S,M: 6 (13.33%)
  M,S: 11 (24.44%)
  M,M: 23 (51.11%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
Pattern Instances is constant in these runs: no stress levels to compare.
Pattern Types Active is constant in these runs: no stress levels to compare.
Runs and objective means by Client Selector Stress Percentage:
                                   runs  final_val_accuracy (mean)  \
Client Selector Stress Percentage                                    
25.0                                 30                      0.535   
50.0                                 30                      0.529   
75.0                                 90                      0.480   

                                   avg_total_time (mean)  
Client Selector Stress Percentage                         
25.0                                              11.188  
50.0                                               9.250  
75.0                                               7.844  Tradeoff counts by stress level:
tradeoff                           M-M  M-S  S-M  S-S
Client Selector Stress Percentage                    
25                                  27    3    0    0
50                                  20    9    1    0
75                                  28   24   20   18Within-level tradeoff shares (STARR) by Client Selector Stress Percentage:
                                      S-S    S-M  S-L    M-S    M-M  M-L  L-S  \
policy                                                                          
Client Selector Stress Percentage=25  0.0  0.000  0.0  0.100  0.900  0.0  0.0   
Client Selector Stress Percentage=50  0.0  0.033  0.0  0.300  0.667  0.0  0.0   
Client Selector Stress Percentage=75  0.2  0.222  0.0  0.267  0.311  0.0  0.0   

                                      L-M  L-L  
policy                                          
Client Selector Stress Percentage=25  0.0  0.0  
Client Sele
```

See the [quality-space plot](../plots/quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

### RQ2 — Predictive conditions and validation

Feature importance is relative predictive credit in this training slice, not direction or causality. Screened features/ranking output (Section 8, cell 48):

```text
Scoring features for outcome: final_val_accuracy (on subset: train)
Original features (numerically encoded): ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria', 'Client Selector Value', 'Message Compressor Alg', 'HDH Batch Size', 'HDH Beta 1', 'HDH Beta 2', 'HDH Discriminator', 'HDH Epochs', 'HDH Generator', 'HDH Learning Rate', 'HDH Latent Dim', 'HDH Optimizer', 'CPU Mean', 'RAM Mean', 'Alpha Dirichlet Mean', 'JSD Mean', 'Data Distribution Diversity', 'Data Persistence Diversity', 'Pattern Types Active', 'Pattern Instances', 'Client Selector Instances', 'Message Compressor Instances', 'HDH Instances', 'non_iid_percentage', 'delay_percentage', 'Client Selector Stress Percentage', 'Message Compressor Stress Percentage', 'HDH Stress Percentage']
Features selected: ['N Rounds', 'Total Clients', 'Optimizer', 'Learning Rate', 'Batch Size', 'Epochs', 'Client Selector Strategy', 'Client Selector Criteria',
```

PRIM conditions and discovery metrics (Section 9, cell 55):

```text
------------------------------
Discovering scenarios for: S-S
Running PRIM discovery for: S-S ...
Instances satisfying property: False    92
True     13
Name: count, dtype: int64
Total instances: (105, 5)
Running PRIM ... rhodium
5 possible boxes
* Key Rules: {'CPU Mean': '[8.000, 8.125]', 'non_iid_percentage': '[50.000, 75.000]'}
* Discovery metrics: {'density': 0.5714285714285714, 'coverage': 0.3076923076923077, 'population_prevalence': 0.12380952380952381, 'lift': 0.4476190476190476, 'population_size': 105.0, 'total_targets': 13.0, 'samples_in_box': 7.0, 'targets_in_box': 4.0}
* Held-out metrics: {'density': 0.3333333333333333, 'coverage': 0.2, 'population_prevalence': 0.1111111111111111, 'lift': 0.2222222222222222, 'population_size': 45.0, 'total_targets': 5.0, 'samples_in_box': 3.0, 'targets_in_box': 1.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    90
True     15
Name: count, dtype: int64
Total instances: (105, 5)
Running PRIM ... rhodium
6 possible boxes
* Key Rules: {'Total Clients': '[6.000, 10.000]', 'non_iid_percentage': '[50.000, 75.000]'}
* Discovery metrics: {'density': 0.42857142857142855, 'coverage': 0.4, 'population_prevalence': 0.14285714285714285, 'lift': 0.2857142857142857, 'population_size': 105.0, 'total_targets': 15.0, 'samples_in_box': 14.0, 'targets_in_box': 6.0}
* Held-out metrics: {'density': 0.5, 'coverage': 0.5, 'population_prevalence': 0.13333333333333333, 'lift': 0.3666666666666667, 'population_size': 45.0, 'total_targets': 6.0, 'samples_in_box': 6.0, 'targets_in_box': 3.0}
------------------------------
Discovering scenarios for: M-S
Running PRIM di
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S      45                  5      3              1   
1   PRIM    S-M      45                  6      6              3   
2   PRIM    M-S      45                 11      3              2   
3   PRIM    M-M      45                 23      6              6   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.111          0.333            0.222                0.448   
1          0.133          0.500            0.367                0.286   
2          0.244          0.667            0.422                0.762   
3          0.511          1.000            0.489                0.505   

   test_recall_coverage  
0                 0.200  
1                 0.500  
2                 0.182  
3                 0.261  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M      45                 23      6              6   
1   CART    S-M      45                  6      3              0   
2   CART    M-S      45                 11      3              0   
3   CART    S-S      45                  5      3              1
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-stress-only-client_selector-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-stress-only-client_selector-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-stress-only-client_selector-image.md); [quality-space plot](../plots/quality-space__task-image__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__stress-ONLY-client_selector__clients-all__environment-all.png).
