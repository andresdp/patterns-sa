# Client Selector only

**Notebook:** [analysis-fl-client-selector.ipynb](../../../federatedlearning/old-analysis/analysis-fl-client-selector.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** Selector-only runs often occupy faster time bins, but fast rounds also occur with low accuracy.

## Observed outcomes by task

| Task/model | Runs | Mean accuracy | Mean round time | Observed regions |
|---|---:|---:|---:|---|
| AG_NEWS/MLP | 150 | 86.37% | 7.799 s | `L-M` 78/150, `L-S` 68/150, `M-S` 4/150 |
| CIFAR-10/CNN 16k | 150 | 50.09% | 8.794 s | `M-M` 75/150, `M-S` 36/150, `S-M` 21/150, `S-S` 18/150 |

These means describe this configuration’s own sampled environments. Region counts use the overview’s fixed edges. Comparisons between separate single-configuration notebook means have unequal environment support.

## Conditions associated with tradeoffs

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `S-S` | `Total Clients`: [4.000, 9.000]; `Dataset`: {CIFAR-10}; `non_iid_percentage`: [50.000, 75.000] | 2/4 | 40.0% |
| `M-S` | `Total Clients`: [4.000, 6.000]; `Dataset`: {CIFAR-10}; `Alpha Dirichlet Mean`: [0.750, 0.887]; `low_spec_percentage`: [37.500, 75.000]; `delay_percentage`: [25.000, 50.000] | 3/6 | 25.0% |
| `M-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {CIFAR-10}; `low_spec_percentage`: [25.000, 37.500]; `non_iid_percentage`: [25.000, 50.000] | 4/4 | 17.4% |
| `L-S` | `Dataset`: {AG_NEWS}; `non_iid_percentage`: [50.000, 75.000] | 6/12 | 28.6% |

The `M-M` rule succeeds in 4/4 test runs but captures only 17.4% of that target, while the image `M-S` rule succeeds in 3/6. These small boxes locate candidate operating conditions; they do not establish stable target attainment.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 95.7%; `Alpha Dirichlet Mean` 1.3%; `Total Clients` 1.0% | 0.945 | 2.372 pp |
| Round time | `low_spec_percentage` 35.5%; `delay_percentage` 22.3%; `Dataset` 12.8% | 0.179 | 2.574 s |

CS policy parameters are constant because CS is always ON. Low-spec share becomes the leading timing feature (35.5%), followed by delay (22.3%); this is resource/environment variation within selector-only runs. Timing prediction is weak on held-out rows (R² 0.179), so the ranking does not establish a dependable time bound.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 6 parameters under the score >3% gate: `Dataset`, `low_spec_percentage`, `delay_percentage`, `Total Clients`, `Alpha Dirichlet Mean`, `non_iid_percentage`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | `100` | `L-S` | 23.3% → 50.0% | +26.7 | 12/90 (13.3%) |
| CART | `100` | `L-S` | 23.3% → 100.0% | +76.7 | 2/90 (2.2%) |
| PRIM | `100` | `L-M` | 25.6% → 50.0% | +24.4 | 6/90 (6.7%) |
| CART | `100` | `L-M` | 25.6% → 100.0% | +74.4 | 9/90 (10.0%) |

CART’s `L-S` restriction is more selective: 100% target attainment on only two retained cases, versus PRIM’s 50% on twelve. For `L-M`, CART retains nine cases with 100% attainment, while PRIM retains six with 50%. A designer should compare both gain and retained support; the two-case fast-region result is too small to establish stable deployment behavior.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication and RQs

For a time constraint, CS is a candidate with an accuracy cost: the companion matched comparison is −2.58 pp accuracy and −3.590 s time. The raw configuration means here combine different environments and should not be used as the savings estimate.

**RQ1:** Establishes this complete configuration’s outcome distribution. **RQ2:** Gives conditional rules, their support, and before/inside-box robustness. **RQ3:** Use the companion `vs-baseline` notebook for an isolated decision comparison. **RQ4:** Variability includes different partitions and runtime conditions; these pooled means do not measure stability at one fixed setting.
