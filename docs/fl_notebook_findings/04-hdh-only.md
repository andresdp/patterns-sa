# HDH only

**Notebook:** [analysis-fl-hdh.ipynb](../../federatedlearning/analysis-fl-hdh.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** HDH-configured runs include substantial low-accuracy image support; the matched comparison gives no general accuracy advantage.

## Observed outcomes by task

| Task/model | Runs | Mean accuracy | Mean round time | Observed regions |
|---|---:|---:|---:|---|
| AG_NEWS/MLP | 150 | 84.18% | 14.000 s | `L-M` 138/150, `L-L` 9/150, `M-M` 3/150 |
| CIFAR-10/CNN 16k | 150 | 46.78% | 11.560 s | `S-M` 82/150, `M-M` 65/150, `S-S` 2/150, `M-S` 1/150 |

These means describe this configuration’s own sampled environments. Region counts use the overview’s fixed edges. Comparisons between separate single-configuration notebook means have unequal environment support.

## Conditions associated with tradeoffs

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `S-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {CIFAR-10}; `JSD Mean`: [0.027, 0.087] | 21/21 | 77.8% |
| `M-M` | `Total Clients`: [4.000, 6.000]; `Dataset`: {CIFAR-10}; `JSD Mean`: [0.003, 0.055] | 10/11 | 47.6% |
| `L-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {AG_NEWS} | 27/27 | 69.2% |
| `L-L` | `Total Clients`: [4.000, 9.000]; `Dataset`: {AG_NEWS}; `delay_percentage`: [50.000, 75.000] | 2/7 | 66.7% |

The image `S-M` box combines 8–10 clients with JSD 0.027–0.087 and succeeds in 21/21 test cases, capturing 77.8% of that target. In this grid, that means accuracy at most 47.74%, not successful recovery of accuracy under heterogeneity. The slow/high-accuracy `L-L` box has only 2/7 successful test cases.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 94.1%; `JSD Mean` 3.8%; `non_iid_percentage` 1.2% | 0.980 | 1.985 pp |
| Round time | `HDH Instances` 62.3%; `Total Clients` 10.7%; `delay_percentage` 10.4% | 0.699 | 0.786 s |

`HDH Instances` leads timing (62.3%) and is supported by held-out shuffling, but it is an activity measure derived from the execution, not a directly chosen design input. JSD is observed in every run of this HDH-only slice, so its accuracy score reflects numerical variation rather than ON/OFF missingness here. Task/model still receives 94.1% of accuracy importance.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 5 parameters under the score >3% gate: `Dataset`, `HDH Instances`, `JSD Mean`, `Total Clients`, `delay_percentage`.

The [cross-notebook feature audit](../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | `001` | `M-M` | 23.3% → 90.9% | +67.6 | 11/90 (12.2%) |
| CART | `001` | `M-M` | 23.3% → 84.6% | +61.3 | 13/90 (14.4%) |
| PRIM/CART | `001` | `L-M` | 43.3% → 100.0% | +56.7 | 27/90 (30.0%) |

The `L-M` envelope gives 100% attainment for 27/90 HDH-only test cases, compared with 43.3% before restriction. For `M-M`, PRIM achieves higher conditional attainment on a smaller retained subset than CART. This is evidence that operating/design-space restrictions can stabilize a chosen region even when the standalone pattern comparison shows no general accuracy benefit.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication and RQs

Verify applied augmentation before using these results to assess HDH’s mechanism. Across all HDH-ON configurations, logged activity occurs in only 42/480 image runs, compared with 466/480 text runs. The matched result is −1.45 pp accuracy; time has both positive and negative differences. Treat HDH as a task-specific alternative to evaluate, not an established remedy for non-IID data.

**RQ1:** Establishes this complete configuration’s outcome distribution. **RQ2:** Gives conditional rules, their support, and before/inside-box robustness. **RQ3:** Use the companion `vs-baseline` notebook for an isolated decision comparison. **RQ4:** Variability includes different partitions and runtime conditions; these pooled means do not measure stability at one fixed setting.
