# Fixed setting — 4 clients, image

**Notebook:** [analysis-fl-stress-c4-image.ipynb](../../../federatedlearning/old-analysis/analysis-fl-stress-c4-image.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS-alone shifts toward faster rounds (−2.637 s) with −0.33 pp accuracy; HDH-alone has the only standalone positive accuracy mean (+0.59 pp).

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.33 | −2.637 | 8/10 | 5/10 |
| MC | −0.22 | −0.033 | 4/10 | 6/10 |
| HDH | +0.59 | −0.545 | 6/10 | 3/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 57.76% | 13.387 | — |
| `001` | HDH | 58.35% | 12.842 | Yes |
| `010` | MC | 57.54% | 13.354 | — |
| `011` | MC+HDH | 57.95% | 12.684 | Yes |
| `100` | CS | 57.44% | 10.750 | — |
| `101` | CS+HDH | 57.07% | 10.030 | Yes |
| `110` | CS+MC | 56.83% | 10.720 | — |
| `111` | CS+MC+HDH | 57.71% | 10.279 | Yes |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

The configuration choices span approximately 57–58% mean accuracy. HDH-alone is the accuracy leader (58.35%, 12.842 s); CS+HDH is the time leader (57.07%, 10.030 s). The all-ON alternative is intermediate (57.71%, 10.279 s). Choose an accuracy floor before comparing those alternatives; apparent HDH differences describe configured use.

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.33 | −2.637 | 8/10 |
| `001` → `101` | −1.28 | −2.812 | 9/10 |
| `010` → `110` | −0.71 | −2.634 | 8/10 |
| `011` → `111` | −0.24 | −2.405 | 8/10 |

For CS-alone, mean time reduction is 2.637 s but median reduction is 0.663 s. Large savings in some runs make the mean substantially more favorable than the middle pair. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-L` | `Client Selector Criteria`: {(not selected)}; `HDH Batch Size`: (not selected) or <= 30.400; `Pattern Types Active`: [0.000, 2.500] | 7/7 | 36.8% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `HDH Batch Size` 31.8%; `Client Selector Criteria` 29.1%; `Pattern Types Active` 25.3% | 0.042 | 0.742 pp |
| Round time | `Client Selector Criteria` 55.1%; `Pattern Types Active` 33.2%; `HDH Batch Size` 6.5% | -0.026 | 2.014 s |

The leading accuracy feature switches between `HDH Batch Size` and the CS representative across forest seeds. Batch size is always 32 when HDH is ON; its importance therefore represents HDH presence, not sensitivity to batch-size tuning. Accuracy R² is only 0.042 and time R² is negative, so this ranking provides weak evidence for identifying a dominant local driver or predicting precise round time.

The saved accuracy leader remains first in only three of five forest seeds; timing’s leader remains first in all five. This is a local ranking-instability flag. Discovery keeps 5 parameters under the score >3% gate: `Client Selector Criteria`, `Pattern Types Active`, `HDH Batch Size`, `Message Compressor Instances`, `Pattern Instances`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `M-L` | 79.2% → 100.0% | +20.8 | 7/24 (29.2%) |

Restricting to the rule raises `M-L` attainment to 100% while retaining 7/24 scenarios. This stabilizes the local medium-accuracy/slow-time target; it is not a prescription for the faster `M-S` region. A positive robustness gain is useful only when the target matches the designer’s requirement.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
