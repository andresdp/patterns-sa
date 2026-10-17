# Findings: analysis-fl-rq-c4-image

## Scope and support

Image, CIFAR-10/CNN 16k; all eight configurations, fixed client count 4; all environments. Complete run/configuration rows are the observational unit; compact client attributes are run-level aggregates. ADEPT groups by `partition_seed`, fits feature rankings and boxes on training groups, and evaluates fixed rules on held-out groups.

### Split and tradeoff support

Notebook [Section 4, split diagnostics](../analysis-fl-rq-c4-image.ipynb#cell-18), cell 18:

```text
Grouped split by partition_seed: 3 of 10 groups held out; stratification score=0.000088.
Data split: 273 train, 117 test.

--- Train Set Tradeoff Counts ---
  S,S: 8 (2.93%)
  S,M: 10 (3.66%)
  M,S: 68 (24.91%)
  M,M: 187 (68.50%)

--- Test Set Tradeoff Counts ---
  S,S: 4 (3.42%)
  S,M: 4 (3.42%)
  M,S: 30 (25.64%)
  M,M: 79 (67.52%)
```

### RQ1 — Tradeoffs and design allocation

Accuracy is preferred higher and total time lower. The semantic ideal is `L-S` under the fixed bins; retain this target even if empty. The common discretization edges are accuracy 0.2075/0.4774/0.7473/1.0172 and time 1.5625/9.5065/17.4505/25.3945. Empty cells mean unobserved in this sample, not infeasible. Complete configurations differ from marginal pattern/instance counts.

The notebook objective-space chart/table is Section 4; allocation output from cell 43 / Section 5:

```text
S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                              
Pattern Instances=0  0.02  0.06  0.0  0.11  0.80  0.0  0.0  0.0  0.0
Pattern Instances=1  0.11  0.03  0.0  0.40  0.46  0.0  0.0  0.0  0.0
Pattern Instances=2  0.00  0.07  0.0  0.14  0.79  0.0  0.0  0.0  0.0
Pattern Instances=3  0.00  0.00  0.0  0.20  0.80  0.0  0.0  0.0  0.0
Pattern Instances=4  0.00  0.01  0.0  0.28  0.71  0.0  0.0  0.0  0.0
Pattern Instances=5  0.00  0.18  0.0  0.00  0.82  0.0  0.0  0.0  0.0
Pattern Instances=6  0.00  0.00  0.0  0.00  1.00  0.0  0.0  0.0  0.0<Figure size 800x445 with 2 Axes>                         S-S   S-M  S-L   M-S   M-M  M-L  L-S  L-M  L-L
policy                                                                 
Pattern Types Active=0  0.00  0.07  0.0  0.17  0.77  0.0  0.0  0.0  0.0
Pattern Types Active=1  0.04  0.04  0.0  0.20  0.72  0.0  0.0  0.0  0.0
Pattern Types Active=2  0.04  0.02  0.0  0.31  0.63  0.0  0.0  0.0  0.0
Pattern Types Active=3  0.00  0.00  0.0  0.47  0.53  0.0  0.0  0.0  0.0<Figure size 800x340 with 2 Axes>Counts by pattern-count group:
tradeoff             M-M  M-S  S-M  S-S
Pattern Count Group                    
0                     46   10    4    0
1                    122   34    7    7
2-3                   98   54    3    5Within-group tradeoff shares:
<pandas.io.formats.style.Styler at 0x168547610>
```

See the [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook leaves overlap; compare configurations only within the stated scope.

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
Instances satisfying property: False    265
True       8
Name: count, dtype: int64
Total instances: (273, 4)
Running PRIM ... rhodium
3 possible boxes
* Key Rules: {'Alpha Dirichlet Mean': '[0.625, 0.688]', 'Client Selector Stress Percentage': '[35.000, 75.000]'}
* Discovery metrics: {'density': 0.42857142857142855, 'coverage': 0.75, 'population_prevalence': 0.029304029304029304, 'lift': 0.39926739926739924, 'population_size': 273.0, 'total_targets': 8.0, 'samples_in_box': 14.0, 'targets_in_box': 6.0}
* Held-out metrics: {'density': 0.6666666666666666, 'coverage': 1.0, 'population_prevalence': 0.03418803418803419, 'lift': 0.6324786324786325, 'population_size': 117.0, 'total_targets': 4.0, 'samples_in_box': 6.0, 'targets_in_box': 4.0}
------------------------------
Discovering scenarios for: S-M
Running PRIM discovery for: S-M ...
Instances satisfying property: False    263
True      10
Name: count, dtype: int64
Total instances: (273, 4)
Running PRIM ... rhodium
4 possible boxes
* Key Rules: {'Alpha Dirichlet Mean': '[0.625, 0.688]', 'JSD Mean': '(not selected) or <= 0.027', 'delay_percentage': '[0.000, 50.000]', 'Client Selector Stress Percentage': '(not selected) or <= 47.500'}
* Discovery metrics: {'density': 0.23529411764705882, 'coverage': 0.4, 'population_prevalence': 0.03663003663003663, 'lift': 0.19866408101702218, 'population_size': 273.0, 'total_targets': 10.0, 'samples_in_box': 17.0, 'targets_in_box': 4.0}
* Held-out metrics: {'density': 0.3333333333333333, 'coverage': 0.25, 'population_prevalence': 0.03418803418803419, 'lift': 0.29914529914529914, 'population_size'
```

Held-out PRIM/CART performance (Section 13, cell 66):

```text
PRIM: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   PRIM    S-S     117                  4      6              4   
1   PRIM    S-M     117                  4      3              1   
2   PRIM    M-S     117                 30     15             15   
3   PRIM    M-M     117                 79     22             22   

   baseline_rate  box_precision  test_delta_rate  train_lift_absolute  \
0          0.034          0.667            0.632                0.399   
1          0.034          0.333            0.299                0.199   
2          0.256          1.000            0.744                0.751   
3          0.675          1.000            0.325                0.315   

   test_recall_coverage  
0                 1.000  
1                 0.250  
2                 0.500  
3                 0.278  CART: held-out support, precision, lift and target coverage
  method target  test_n  baseline_target_n  box_n  target_in_box  \
0   CART    M-M     117                 79     24             24   
1   CART    M-S     117                 30     15             15   
2   CART    S-M     117                  4      0              0   
3   CART    S-S     117                  4      0              0
```

Policy-specific before/boxed/gain and target-coverage matrices (Section 11, cell 68), which differ from the target-box summary:

```text
Policy-specific matrices are in notebook Section 11
```

Read conditions jointly as candidate prescriptions and operating envelopes; see the [box report](../boxes/analysis-fl-rq-c4-image.md). Small retained support is narrow evidence. If a held-out target is absent, evaluation is unavailable rather than zero precision/recall. These predictive associations can guide a conditional experiment, but do not establish that imposing a rule causes the outcome.

### Implications and limits

**Practitioners:** use the conditions only as candidate envelopes for this image-task slice; preserve the configuration, stress, client, and environment context, then validate on new seeds.

**Researchers:** report train and held-out region counts, target prevalence, precision, lift, coverage, retained rows and target support together. Controlled comparisons are needed to separate design choices from sampled context. Findings are observational and specific to CIFAR-10/CNN 16k and run-level aggregates.

**Artifacts:** notebook [cell 18](../analysis-fl-rq-c4-image.ipynb#cell-18), [cell 48](../analysis-fl-rq-c4-image.ipynb#cell-48), [cell 55](../analysis-fl-rq-c4-image.ipynb#cell-55), [cell 66](../analysis-fl-rq-c4-image.ipynb#cell-66), [cell 68](../analysis-fl-rq-c4-image.ipynb#cell-68); [box report](../boxes/analysis-fl-rq-c4-image.md); [quality-space plot](../plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-image__all-configurations__clients-4__environment-all.png).
