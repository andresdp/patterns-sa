# Overview — decisions, conditions, and tradeoffs

**Notebook:** [analysis-fl.ipynb](../../federatedlearning/analysis-fl.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS is associated with shorter rounds and lower accuracy on shared support. MC has almost unchanged accuracy and slightly longer rounds. HDH has lower accuracy; its time differences have mixed signs.

## Decision comparisons

Differences compare ON with OFF at the same task, client count, environment shares, and partition seed. Hosts and scheduling remain unmatched. These are observed associations; the campaign does not identify causal effects. Accuracy changes are in **percentage points (pp)**, and negative time changes mean faster rounds. Other patterns are OFF in this table.

| Pattern | Matched pairs | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|---:|
| CS | 180 | −2.58 | −3.590 | 162/180 | 143/180 |
| MC | 300 | −0.03 | +0.214 | 81/300 | 157/300 |
| HDH | 180 | −1.45 | +0.530 | 91/180 | 138/180 |

CS’s mean time reduction is 3.590 s, versus a median paired reduction of 2.214 s. For HDH, mean time increases 0.530 s but median difference is −0.013 s: a positive mean conceals mixed signs and large positive differences. These distinctions matter when selecting for repeatable timing.

## Tradeoff space actually observed

The following counts use **all 2,340 rows**, not just the training split.

| Region | Runs | Share |
|---|---:|---:|
| `L-M` | 875 | 37.39% |
| `M-M` | 691 | 29.53% |
| `L-S` | 257 | 10.98% |
| `S-M` | 227 | 9.70% |
| `M-S` | 223 | 9.53% |
| `S-S` | 50 | 2.14% |
| `L-L` | 17 | 0.73% |

The overview thresholds are accuracy 47.74% and 74.73%, and time 9.5065 s and 17.4505 s. Thus `L-S` means accuracy above 74.73% with time at most 9.5065 s. There are 257 such runs (10.98%); `S-L` and `M-L` are absent. These thresholds define this analysis grid, not a designer’s requirements.

All 1,149 `L-*` runs belong to AG_NEWS; none belong to CIFAR-10. The global high-accuracy regions therefore reflect the tasks' different accuracy scales as well as configuration behavior. Assess an image design against an image-task requirement rather than treating absence from `L-*` as evidence of a worse architecture.

## Conditions associated with target regions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `S-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {CIFAR-10}; `Client Selector Criteria`: {(not selected)}; `non_iid_percentage`: [62.500, 75.000] | 41/41 | 60.3% |
| `M-S` | `Dataset`: {CIFAR-10}; `delay_percentage`: [0.000, 12.500] | 41/42 | 61.2% |
| `M-M` | `Dataset`: {CIFAR-10}; `Client Selector Criteria`: {(not selected)}; `non_iid_percentage`: [25.000, 37.500]; `delay_percentage`: [12.500, 100.000] | 102/103 | 49.3% |
| `L-S` | `Dataset`: {AG_NEWS}; `HDH Instances`: [0.000, 2.500]; `delay_percentage`: [0.000, 12.500] | 46/46 | 59.7% |
| `L-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {AG_NEWS}; `Client Selector Criteria`: {(not selected)}; `delay_percentage`: [12.500, 100.000] | 116/116 | 44.1% |

The low-delay image rule succeeds in 41/42 test runs; the low-delay text/low-HDH-activity rule succeeds in 46/46. Neither needs a specific compressor policy. These are environment/task associations, not evidence that compression creates the fast region. The high-non-IID image rule identifies the low-accuracy `S-M` region, so data heterogeneity must be considered alongside the architectural decision.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 93.8%; `non_iid_percentage` 3.6%; `Total Clients` 1.3% | 0.979 | 1.588 pp |
| Round time | `delay_percentage` 58.2%; `Client Selector Criteria` 17.6%; `CPU Mean` 6.0% | 0.753 | 0.997 s |

`Dataset` receives 93.8% of accuracy importance and represents the task/model contrast; `Model` is removed as a perfectly correlated duplicate. For timing, delay (58.2%) and the CS representative (17.6%) agree with the envelope and matched-comparison findings. MC’s zero algorithm score is caused by correlation pruning with `Pattern Instances`, not proof that MC has no timing association. The timing zero for low-spec share similarly transfers credit to correlated `CPU Mean`.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 8 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `Client Selector Criteria`, `non_iid_percentage`, `CPU Mean`, `Total Clients`, `HDH Instances`, `Pattern Instances`.

The [cross-notebook feature audit](../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `M-S` | 9.5% → 97.6% | +88.1 | 42/702 (6.0%) |
| PRIM/CART | All loaded configurations | `L-S` | 11.0% → 100.0% | +89.0 | 46/702 (6.6%) |
| PRIM/CART | `000` | `M-M` | 30.8% → 100.0% | +69.2 | 31/107 (29.0%) |
| PRIM | `100` | `L-M` | 24.7% → unsupported | — | 0/85 (0.0%) |
| CART | `100` | `L-M` | 24.7% → 100.0% | +75.3 | 4/85 (4.7%) |

For the pooled fast/high-accuracy `L-S` target, the rules raise attainment from 11.0% to 100% but retain only 6.6% of test scenarios. The gain is conditional on that narrow envelope. For all-OFF configuration `000`, the `M-M` rule raises attainment from 30.8% to 100% on 31/107 retained cases. PRIM excludes CS-only `100` from its `L-M` rule, while CART retains four CS-only cases and all four attain `L-M`. The methods therefore identify different supported prescriptions/envelopes even when their pooled target densities look similar.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication and RQs

For shorter rounds, investigate CS with an explicit accuracy floor. Use the six fixed task/client stress summaries to choose complete alternatives; they keep environment support comparable. A type-count or instance-count trend does not isolate a decision because configurations and conditions change together.

**RQ1:** Maps observed regions. **RQ2:** Identifies conditions and measured what-if robustness gains. **RQ3:** Quantifies single-pattern associations. **RQ4:** Shows why mean differences need run-level spread. The environment design is incomplete; the six stress slices share only the 25%/25%/25% environment point.
