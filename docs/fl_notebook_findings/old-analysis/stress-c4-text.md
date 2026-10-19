# Fixed setting — 4 clients, text

**Notebook:** [analysis-fl-stress-c4-text.ipynb](../../../federatedlearning/old-analysis/analysis-fl-stress-c4-text.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS-alone is faster in 9/10 seed matches and lower in accuracy in all 10; MC-alone is slower on average.

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.81 | −2.676 | 9/10 | 10/10 |
| MC | −0.06 | +0.282 | 3/10 | 7/10 |
| HDH | −0.06 | −0.034 | 6/10 | 7/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 91.27% | 12.369 | Yes |
| `001` | HDH | 91.21% | 12.335 | Yes |
| `010` | MC | 91.21% | 12.652 | — |
| `011` | MC+HDH | 91.27% | 12.513 | — |
| `100` | CS | 90.46% | 9.694 | — |
| `101` | CS+HDH | 90.46% | 9.617 | Yes |
| `110` | CS+MC | 90.47% | 10.103 | Yes |
| `111` | CS+MC+HDH | 90.45% | 10.169 | — |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

Baseline averages 91.27% accuracy at 12.369 s; CS-alone averages 90.46% at 9.694 s. This is a concrete accuracy/time choice. Under an illustrative requirement of at least 90% accuracy and at most 11 s, baseline meets both in 0/10 runs and CS-alone in only 3/10. None of the eight configurations meets a stricter 91%/11 s requirement in these ten runs.

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.81 | −2.676 | 9/10 |
| `001` → `101` | −0.75 | −2.719 | 8/10 |
| `010` → `110` | −0.74 | −2.549 | 6/10 |
| `011` → `111` | −0.81 | −2.344 | 8/10 |

CS-alone mean time is 9.694 s but median is 11.611 s. Its paired time saving averages 2.676 s but has a median of 0.724 s. The mean is insufficient evidence of an 11-second timing bound. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-L` | `Client Selector Criteria`: {(not selected)} | 13/13 | 65.0% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Client Selector Criteria` 96.7%; `Pattern Types Active` 1.6%; `HDH Instances` 0.9% | 0.875 | 0.119 pp |
| Round time | `Client Selector Criteria` 55.8%; `Pattern Types Active` 30.0%; `Message Compressor Instances` 8.2% | -0.030 | 1.952 s |

The CS representative receives 96.7% of accuracy importance, agrees with the leading held-out shuffle diagnostic, and predicts accuracy well (R² 0.875). The matched result supplies the direction: CS lowers accuracy in all ten standalone pairs. CS also leads time importance, but timing R² is negative; its average speed association does not yield a reliable per-run time prediction.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 4 parameters under the score >3% gate: `Client Selector Criteria`, `Pattern Types Active`, `Message Compressor Instances`, `HDH Batch Size`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `M-L` | 83.3% → 100.0% | +16.7 | 13/24 (54.2%) |

The CS-not-selected rule makes the local `M-L` target certain in the 13 retained test cases. It describes a consistent slower-round operating/design subset. The gain therefore answers how to stabilize that specific tradeoff, while the matched CS comparison answers how to exchange some accuracy for speed; those are different design questions.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
