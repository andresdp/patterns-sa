# Baseline — all patterns OFF

**Notebook:** [analysis-fl-baseline.ipynb](../../federatedlearning/analysis-fl-baseline.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** The baseline retains high-bin accuracy on every text run, while image runs occupy medium- or low-accuracy regions.

## Observed outcomes by task

| Task/model | Runs | Mean accuracy | Mean round time | Observed regions |
|---|---:|---:|---:|---|
| AG_NEWS/MLP | 180 | 88.88% | 11.286 s | `L-M` 150/180, `L-S` 30/180 |
| CIFAR-10/CNN 16k | 180 | 50.85% | 11.668 s | `M-M` 106/180, `S-M` 44/180, `M-S` 30/180 |

These means describe this configuration’s own sampled environments. Region counts use the overview’s fixed edges. Comparisons between separate single-configuration notebook means have unequal environment support.

## Conditions associated with tradeoffs

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `S-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {CIFAR-10}; `non_iid_percentage`: [50.000, 75.000] | 12/12 | 92.3% |
| `M-S` | `Dataset`: {CIFAR-10}; `non_iid_percentage`: [25.000, 50.000]; `delay_percentage`: [0.000, 12.500] | 9/9 | 100.0% |
| `L-S` | `Dataset`: {AG_NEWS}; `non_iid_percentage`: [25.000, 50.000]; `delay_percentage`: [0.000, 12.500] | 9/9 | 100.0% |
| `L-M` | `Dataset`: {AG_NEWS}; `delay_percentage`: [12.500, 100.000] | 45/45 | 100.0% |

Low delay distinguishes the faster regions for both tasks. High non-IID share with 8 or 10 image clients is associated with lower accuracy: the `S-M` rule contains 12/12 successful test cases. The baseline is therefore a credible reference, but its attainable tradeoff depends on task and environment.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 95.5%; `non_iid_percentage` 3.1%; `Total Clients` 1.3% | 0.990 | 1.293 pp |
| Round time | `delay_percentage` 94.1%; `Total Clients` 5.2%; `Dataset` 0.5% | 0.973 | 0.362 s |

With all patterns OFF, their parameters are constant and cannot explain within-baseline differences. Task/model dominates accuracy (95.5%) and delay dominates time (94.1%). The held-out fits are strong in this sampled space, supporting the recurring task/delay envelopes without implying a pattern effect.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 4 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `Total Clients`, `non_iid_percentage`.

The [cross-notebook feature audit](../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | `000` | `M-S` | 8.3% → 100.0% | +91.7 | 9/108 (8.3%) |
| PRIM/CART | `000` | `L-S` | 8.3% → 100.0% | +91.7 | 9/108 (8.3%) |
| PRIM/CART | `000` | `L-M` | 41.7% → 100.0% | +58.3 | 45/108 (41.7%) |

Both methods find restrictions under which the all-OFF system reaches these targets in every retained test case. The fast targets retain only 9/108 scenarios each; the text/middle-time envelope retains 45/108. This is robustness improvement through operating-condition restriction without adding a pattern. It does not imply that the baseline attains the fast target outside that envelope.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication and RQs

Retain baseline when its observed quality/time region meets the requirement. Compare a pattern against it on shared conditions before accepting additional behavior. This notebook contains no ON/OFF decision variation, so it cannot attribute an improvement to a pattern.

**RQ1:** Establishes this complete configuration’s outcome distribution. **RQ2:** Gives conditional rules, their support, and before/inside-box robustness. **RQ3:** Supplies the all-OFF reference. **RQ4:** Variability includes different partitions and runtime conditions; these pooled means do not measure stability at one fixed setting.
