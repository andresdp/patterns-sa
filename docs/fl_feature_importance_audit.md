# Historical feature-importance audit — superseded experiment scope

> This audit covers the previous 14-notebook analysis, including matched comparisons and the earlier RQ framing. It is preserved for reference and does not describe the active six-notebook RQ1/RQ2 sequence. The current per-slice feature rankings are summarized in the numbered findings linked from `fl_notebook_findings/README.md`.

## Previous-scope feature importance

The audit compares all 14 executed notebooks and distinguishes recurring drivers, changes that follow from the analysis scope, and interpretation or validation flags. Its purpose is to help a software designer understand which dimensions to inspect when choosing alternatives and defining operating envelopes.

## What the notebook scores measure

Each objective has a 50-tree random-forest regressor fitted to the notebook's training rows, with random seed 42. Before fitting, smart correlation selection groups encoded features at absolute Spearman correlation above 0.8 and retains predictive representatives, using a 10-tree regressor and cross-validation. Exact performance ties are resolved alphabetically. Categorical and optional values are encoded; correlated features removed from the fit are put back in the score table with **zero**.

The reported importance is the feature's share of the forest's training impurity reduction. A score of 93.8% is **not** 93.8% of accuracy variance explained, an outcome improvement, a sensitivity slope, or a causal contribution. It has no favorable/adverse direction. That direction comes from outcome distributions and matched comparisons. Scores are normalized separately for each objective and slice, so a larger percentage after slicing does not establish a larger physical effect.

The notebook combines objectives with equal weights to order features, then admits a parameter to scenario discovery if its score is **greater than 3% in either objective**. It does not apply a 3% cutoff to the weighted average. The assertion that all 13 pattern parameters occur in the score table verifies their presence, not that they have positive scores or participate in box discovery.

## Trends across all notebooks

Importance percentages below are the saved notebook scoring results. R² values are additional diagnostics calculated with the same fitted model specification, correlation-pruned feature set, and held-out rows. R² near or below zero indicates weak precise-outcome prediction on that split.

| Analysis | Leading accuracy feature; importance | Leading time feature; importance | Accuracy / time test R² | Train / test runs |
|---|---|---|---:|---:|
| [Overview](fl_notebook_findings/old-analysis/00-overview.md) | `Dataset`; 93.8% | `delay_percentage`; 58.2% | 0.979 / 0.753 | 1638 / 702 |
| [Baseline](fl_notebook_findings/old-analysis/01-baseline.md) | `Dataset`; 95.5% | `delay_percentage`; 94.1% | 0.990 / 0.973 | 252 / 108 |
| [CS only](fl_notebook_findings/old-analysis/02-client-selector-only.md) | `Dataset`; 95.7% | `low_spec_percentage`; 35.5% | 0.945 / 0.179 | 210 / 90 |
| [MC only](fl_notebook_findings/old-analysis/03-message-compressor-only.md) | `Dataset`; 97.0% | `delay_percentage`; 93.7% | 0.993 / 0.989 | 294 / 126 |
| [HDH only](fl_notebook_findings/old-analysis/04-hdh-only.md) | `Dataset`; 94.1% | `HDH Instances`; 62.3% | 0.980 / 0.699 | 210 / 90 |
| [CS vs baseline](fl_notebook_findings/old-analysis/05-client-selector-vs-baseline.md) | `Dataset`; 94.5% | `delay_percentage`; 50.4% | 0.981 / 0.584 | 462 / 198 |
| [MC vs baseline](fl_notebook_findings/old-analysis/06-message-compressor-vs-baseline.md) | `Dataset`; 96.0% | `delay_percentage`; 94.0% | 0.994 / 0.979 | 546 / 234 |
| [HDH vs baseline](fl_notebook_findings/old-analysis/07-hdh-vs-baseline.md) | `Dataset`; 93.6% | `delay_percentage`; 76.6% | 0.988 / 0.899 | 462 / 198 |
| [4-client image](fl_notebook_findings/old-analysis/stress-c4-image.md) | `HDH Batch Size`; 31.8% | `Client Selector Criteria`; 55.1% | 0.042 / -0.026 | 56 / 24 |
| [4-client text](fl_notebook_findings/old-analysis/stress-c4-text.md) | `Client Selector Criteria`; 96.7% | `Client Selector Criteria`; 55.8% | 0.875 / -0.030 | 56 / 24 |
| [8-client image](fl_notebook_findings/old-analysis/stress-c8-image.md) | `JSD Mean`; 67.8% | `Pattern Types Active`; 56.8% | 0.369 / -0.002 | 56 / 24 |
| [8-client text](fl_notebook_findings/old-analysis/stress-c8-text.md) | `JSD Mean`; 54.0% | `Message Compressor Instances`; 31.2% | 0.164 / 0.319 | 56 / 24 |
| [10-client image](fl_notebook_findings/old-analysis/stress-c10-image.md) | `JSD Mean`; 70.8% | `Client Selector Criteria`; 39.3% | 0.193 / -0.060 | 56 / 24 |
| [10-client text](fl_notebook_findings/old-analysis/stress-c10-text.md) | `JSD Mean`; 66.8% | `Message Compressor Alg`; 50.1% | 0.218 / 0.419 | 56 / 24 |

**Task/model dominates mixed-task accuracy.** `Dataset` is the leading accuracy feature in all eight mixed-task analyses, receiving 93.6–97.0% of importance. `Model` is perfectly correlated with dataset and is pruned, so the label `Dataset` represents their coupled task/model contrast. This agrees with global high-accuracy bins being populated only by text runs. It does not isolate the contribution of data versus model, or show that pattern decisions have no accuracy association.

**Delay is the recurring time driver where it varies.** Delay leads six of eight mixed-task timing rankings. It leads both baseline (94.1%) and MC-only (93.7%), supporting the observed low-delay fast-round envelopes without making that result compression-specific. In CS-only, low-spec share leads (35.5%); in HDH-only, logged HDH instance count leads (62.3%). The relevant driver changes when the configuration is fixed because variation available to the model changes.

**Fixed-setting rankings reveal configuration proxies, with unequal predictive support.** At four text clients, the CS representative receives 96.7% of accuracy importance and has test R² 0.875. This agrees with the measured accuracy decrease in all ten standalone CS pairs. At eight and ten clients, JSD leads accuracy for both tasks, but its meaning requires the measurement audit below. For time, all three image stress regressors and the four-client text regressor have test R² at or below zero. Their high-ranked timing features do not provide precise per-run timing predictions. The eight- and ten-client text timing fits are stronger, but remain moderate.

**MC's representative changes with the slice.** Eight-client text uses `Message Compressor Instances` as its timing representative; ten-client text uses `Message Compressor Alg`. The algorithm is always zlib when ON, so neither ranking estimates a comparison among compression algorithms. The underlying compression decision and participating/deployment count can receive credit through different correlated columns. The separate matched evidence supplies the observed adverse timing direction on text workloads.

## Consistency checks and flags

### 1. Zero does not have one meaning

The audit classified each zero using the actual encoded training columns and printed correlation-selection results:

- **Constant:** the feature has one encoded value in the slice and no observed sensitivity can be estimated. Examples are rounds, learning rate, and fixed task/client/environment factors in stress notebooks. A constant feature is not proved unimportant outside that slice.
- **Pruned:** the feature varies but correlation selection removes it. In the overview, `Model` transfers credit to `Dataset` (Spearman −1.000); MC algorithm/instance proxies correlate with total `Pattern Instances` (approximately 0.812/0.895); low-spec share correlates with `CPU Mean` (−0.861). Their zeros do not establish absence of the corresponding design/environment association.
- **Retained but unused:** the forest retains the feature but assigns no training impurity reduction. This is a model result under the available predictors, not proof of causal irrelevance.

All 28 objective-score tables reproduced within the saved numerical precision, their importance sums were one, and no encoded constant received positive importance. The audit found no score-table arithmetic corruption.

### 2. JSD is also a measurement-availability proxy for HDH

Across the campaign, `JSD Mean` is missing in **all 1,380 HDH-OFF runs** and present in **all 960 HDH-ON runs**. Its encoded missing state therefore identifies the configured HDH decision exactly. In each fixed stress slice, all 40 OFF runs are missing and all 40 ON runs have a value. A prominent JSD feature can combine a decision flag with variation in the recorded heterogeneity measurement.

The four-client stress slices have only one distinct nonmissing JSD value per task. There, a fixed HDH parameter such as batch size can stand for the same ON/OFF information. At four image clients, batch size receives 31.8% of accuracy importance even though every HDH-ON run uses batch size 32: this is presence sensitivity, not tuning sensitivity.

At eight and ten clients, numerical JSD values contain information beyond availability. A diagnostic replacement of JSD values with a simple available/not-available flag gives the following accuracy fits, keeping the other predictors fixed:

| Fixed slice | Original JSD test R² | Availability-only test R² |
|---|---:|---:|
| 8-client image | 0.369 | 0.083 |
| 8-client text | 0.164 | -0.315 |
| 10-client image | 0.193 | -0.135 |
| 10-client text | 0.218 | -0.360 |

The loss of predictive performance indicates that JSD's values contribute to these fitted models; it is not purely an ON/OFF flag. Nevertheless, this campaign cannot identify a JSD effect measured independently across all configurations. For a designer, JSD-based prescriptions remain conditional on the measurement/HDH exposure. A stronger interpretation requires recording the same heterogeneity metric when HDH is OFF as well.

### 3. Repeatable ranking is different from predictive stability

With pruning and training rows fixed, five forest seeds (0, 1, 7, 42, 123) preserve the leading feature in 27/28 objective fits. The exception is four-client image accuracy: HDH batch size leads three fits and the CS representative two. Neither is a convincing dominant-driver conclusion given accuracy R² 0.042.

Several other fits have a repeatable leader but weak held-out prediction. For example, four-client text timing consistently ranks CS first but has time R² −0.030 and mean absolute error 1.952 s. Model-seed consistency therefore does not establish that the available features explain run variability. These checks did not resample partition seeds or train/test splits; they should not be presented as confidence intervals or deployment stability estimates.

Held-out permutation checks (ten shuffles per feature) support task/model and delay as leading predictive groups in the overview and baseline. They also support the four-client text CS accuracy signal. At eight text clients, shuffling ranks CS ahead of MC instances for time, reversing their close training-importance order. Shuffling is a diagnostic: it can break dependencies among correlated predictors, and its values are losses in R² rather than importance percentages or causal effects.

### 4. The discovery gate can suppress scientifically relevant dimensions

| Analysis | Keys at >2% | Keys at >3% (executed) | Keys at >5% |
|---|---:|---:|---:|
| Overview | 8 | 8 | 4 |
| Baseline | 4 | 4 | 3 |
| CS only | 6 | 6 | 6 |
| MC only | 3 | 3 | 3 |
| HDH only | 7 | 5 | 5 |
| CS vs baseline | 6 | 6 | 5 |
| MC vs baseline | 3 | 3 | 3 |
| HDH vs baseline | 6 | 6 | 4 |
| 4-client image | 5 | 5 | 5 |
| 4-client text | 4 | 4 | 4 |
| 8-client image | 7 | 7 | 7 |
| 8-client text | 5 | 5 | 5 |
| 10-client image | 5 | 5 | 5 |
| 10-client text | 5 | 5 | 5 |

These are selection changes calculated from the saved scores, not reruns of box discovery. For MC versus baseline, only dataset, delay, and client count pass the executed gate; the resulting boxes cannot explicitly prescribe compression ON/OFF. In the overview, task dominance leaves several decision/heterogeneity proxies below the gate. Absence from a discovered rule can therefore reflect feature selection rather than absence of an association with the target.

For paper claims about a particular decision, retain the matched comparisons and state which decision representatives were available to discovery. A targeted sensitivity check could preserve one explicit representative of each decision and compare resulting box support and what-if gains, or vary the threshold; the current audit does not replace the executed discovery results with such alternatives.

### 5. A verified metadata mismatch affects the meaning of the CS policy

The compact records use `Client Selector Value = 7.0` in **all 960 CS-ON runs**, while `FLsystem_compact_all.json` declares `2.0` in the ON policy binding. The scores were fitted to the recorded values, so the reproduced importance values do not describe an experiment at threshold 2. This mismatch should be reconciled before reporting the policy settings in the paper. It is separate from the already flagged floating-point box-boundary issue.

## Implications for design and the RQs

Use feature importance to identify dimensions worth inspecting, then use matched outcome differences for direction and the box what-if tables for conditional robustness. Task/model and delay are recurrent drivers over the mixed campaign. Fixed-setting analysis can reveal pattern associations that those dominant factors mask, but a high normalized score alone does not identify a strong physical effect or reliable prediction.

For RQ1/RQ3, describe correlated decision proxies as groups and retain the directly measured accuracy/time contrasts. For RQ2, disclose the selected search dimensions: a dimension pruned or below threshold cannot appear directly in a box. For RQ4, poor fixed-setting time prediction flags a limit of the available predictors, without assigning the remaining variation to a particular runtime cause.

Good target STARR and weak continuous-outcome R² can coexist. A broad target region may be consistently attained while exact accuracy or time remains variable. Assess the box's measured before/inside success rate and support independently, then inspect outcome spread and margins within that envelope when the requirement is tight.

## Recheck protocol

All calculations used `perfmodels`. The saved 70/30 notebook splits and correlation-pruned feature sets were reconstructed with the native loader, preprocessing, and split settings. The original 50-tree models at seed 42 reproduced every saved importance table. Additional diagnostics were held-out R²/mean absolute error, ten-repeat held-out permutation checks, five forest seeds with fixed training/pruning, and the JSD availability replacement. The tables in this audit distinguish those added diagnostics from saved notebook scoring outputs. Full notebooks were not re-executed, and their discovery matrices and saved plots were preserved.

Held-out rows come from the same campaign and may share tasks, configurations, operating points, and partition-seed identifiers with training rows. These diagnostics measure interpolation over this campaign, not generalization to an unseen deployment. Inference about independent uncertainty effects, new partitions, or new operating envelopes needs an appropriately grouped follow-up design.
