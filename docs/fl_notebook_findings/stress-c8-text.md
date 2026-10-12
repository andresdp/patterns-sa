# Fixed setting — 8 clients, text

**Notebook:** [analysis-fl-stress-c8-text.ipynb](../../federatedlearning/analysis-fl-stress-c8-text.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS-alone exchanges −0.55 pp accuracy for −0.664 s time; MC and HDH alone have higher mean time.

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.55 | −0.664 | 7/10 | 9/10 |
| MC | +0.07 | +0.520 | 1/10 | 4/10 |
| HDH | −1.29 | +0.347 | 3/10 | 10/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 90.09% | 11.482 | Yes |
| `001` | HDH | 88.81% | 11.829 | — |
| `010` | MC | 90.16% | 12.002 | Yes |
| `011` | MC+HDH | 88.95% | 12.396 | — |
| `100` | CS | 89.55% | 10.818 | Yes |
| `101` | CS+HDH | 87.85% | 11.404 | — |
| `110` | CS+MC | 89.54% | 11.377 | — |
| `111` | CS+MC+HDH | 87.99% | 11.933 | — |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

MC-alone has the highest mean accuracy (90.16%) but takes 12.002 s, compared with baseline at 90.09%/11.482 s. CS-alone is fastest at 89.55%/10.818 s. The 0.07 pp compressor difference is numerically small; it does not establish a reproducible accuracy advantage. HDH-alone is lower in accuracy in all ten seed pairs and slower in seven.

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.55 | −0.664 | 7/10 |
| `001` → `101` | −0.96 | −0.425 | 6/10 |
| `010` → `110` | −0.62 | −0.625 | 5/10 |
| `011` → `111` | −0.95 | −0.463 | 7/10 |

MC-alone is slower in 9/10 pairs, with mean and median time increases both approximately 0.52 s. This is a more consistent adverse timing association than a positive mean driven by a few outliers. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `L-M` | `Client Selector Criteria`: {(not selected)}; `HDH Batch Size`: (not selected) or <= 30.400; `Pattern Types Active`: [0.500, 3.000] | 1/2 | 16.7% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `JSD Mean` 54.0%; `Pattern Types Active` 31.4%; `Message Compressor Instances` 9.3% | 0.164 | 2.231 pp |
| Round time | `Message Compressor Instances` 31.2%; `Client Selector Criteria` 30.2%; `Pattern Types Active` 21.1% | 0.319 | 0.497 s |

JSD leads accuracy (54.0%); replacing it with an availability flag lowers accuracy R² from 0.164 to −0.315. Its values contain information conditional on being recorded, while the overall fit remains weak. MC instance count (31.2%) and the CS representative (30.2%) are close timing leaders; held-out shuffling ranks CS above MC instances. Read these as candidate predictive groups, not a precise ranking of causal pattern effects.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 5 parameters under the score >3% gate: `JSD Mean`, `Pattern Types Active`, `Message Compressor Instances`, `Client Selector Criteria`, `HDH Batch Size`.

The [cross-notebook feature audit](../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `L-M` | 25.0% → 50.0% | +25.0 | 2/24 (8.3%) |
| CART | All loaded configurations | `M-M` | 33.3% → 33.3% | +0.0 | 3/24 (12.5%) |

The `L-M` restriction increases attainment but still succeeds in only one of two retained cases. The CART `M-M` rule gives no gain. These tables do not support a strong robustness prescription in this fixed setting.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
