# Fixed setting — 10 clients, image

**Notebook:** [analysis-fl-stress-c10-image.ipynb](../../../federatedlearning/old-analysis/analysis-fl-stress-c10-image.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS’s accuracy association changes with composition: −0.30 pp against baseline, but +0.21 pp when MC is already ON and HDH OFF.

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.30 | −0.357 | 6/10 | 7/10 |
| MC | +0.07 | +0.056 | 4/10 | 4/10 |
| HDH | −0.73 | +0.028 | 5/10 | 7/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 51.52% | 11.638 | — |
| `001` | HDH | 50.79% | 11.666 | — |
| `010` | MC | 51.59% | 11.694 | — |
| `011` | MC+HDH | 50.80% | 11.582 | — |
| `100` | CS | 51.23% | 11.281 | Yes |
| `101` | CS+HDH | 50.64% | 11.224 | Yes |
| `110` | CS+MC | 51.80% | 11.524 | Yes |
| `111` | CS+MC+HDH | 50.65% | 11.339 | — |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

CS+MC has the highest mean accuracy (51.80%) at 11.524 s, versus baseline 51.52%/11.638 s. CS+HDH is fastest (50.64%, 11.224 s). CS-alone provides an intermediate point (51.23%, 11.281 s). These are numerical mean frontiers; the small gaps require distribution checks before selection.

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.30 | −0.357 | 6/10 |
| `001` → `101` | −0.15 | −0.442 | 7/10 |
| `010` → `110` | +0.21 | −0.170 | 6/10 |
| `011` → `111` | −0.15 | −0.243 | 5/10 |

CS-alone is faster in 6/10 pairs; MC-alone is slower in 6/10. The mean time differences are small relative to their observed ranges. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-M` | `Client Selector Criteria`: {(not selected)}; `Message Compressor Alg`: {(not selected)}; `JSD Mean`: [0.001, 0.007] | 1/3 | 7.7% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `JSD Mean` 70.8%; `Pattern Types Active` 16.9%; `Message Compressor Alg` 7.1% | 0.193 | 1.138 pp |
| Round time | `Client Selector Criteria` 39.3%; `Pattern Types Active` 30.6%; `Message Compressor Alg` 15.9% | -0.060 | 0.337 s |

JSD receives 70.8% of accuracy importance, but the model’s accuracy R² is only 0.193; an availability-only replacement gives −0.135. Its prominence combines measurement availability and observed value differences. CS leads time importance, yet time R² is negative. Use the measured composition contrasts for the accuracy sign change and test distributions for timing feasibility.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 5 parameters under the score >3% gate: `JSD Mean`, `Pattern Types Active`, `Client Selector Criteria`, `Message Compressor Alg`, `HDH Batch Size`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | All loaded configurations | `M-M` | 54.2% → 33.3% | −20.8 | 3/24 (12.5%) |

The PRIM restriction reduces target attainment by 20.8 pp rather than improving it. CART has no non-empty box for this slice. The what-if result therefore rejects this PRIM box as a robustness-improving prescription on the test data.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
