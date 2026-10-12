# Fixed setting — 8 clients, image

**Notebook:** [analysis-fl-stress-c8-image.ipynb](../../../federatedlearning/old-analysis/analysis-fl-stress-c8-image.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** Every standalone pattern has lower mean accuracy; CS has the largest standalone mean time reduction (−0.365 s).

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.93 | −0.365 | 6/10 | 7/10 |
| MC | −0.46 | −0.070 | 7/10 | 7/10 |
| HDH | −1.27 | −0.208 | 5/10 | 8/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 52.80% | 11.898 | Yes |
| `001` | HDH | 51.53% | 11.690 | — |
| `010` | MC | 52.35% | 11.828 | Yes |
| `011` | MC+HDH | 51.65% | 11.927 | — |
| `100` | CS | 51.88% | 11.533 | — |
| `101` | CS+HDH | 50.91% | 11.216 | — |
| `110` | CS+MC | 52.24% | 11.499 | Yes |
| `111` | CS+MC+HDH | 51.08% | 10.887 | Yes |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

Baseline is the accuracy leader (52.80%, 11.898 s). CS+MC+HDH is fastest on the mean (51.08%, 10.887 s). CS+MC offers an intermediate point (52.24%, 11.499 s). Adding CS to MC-alone costs only 0.11 pp on average, versus 0.93 pp when adding CS to baseline; the surrounding configuration changes the observed tradeoff.

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.93 | −0.365 | 6/10 |
| `001` → `101` | −0.62 | −0.474 | 7/10 |
| `010` → `110` | −0.11 | −0.328 | 8/10 |
| `011` → `111` | −0.56 | −1.040 | 10/10 |

The CS-alone time sign is favorable in only 6/10 pairs. A 0.365 s mean reduction should therefore be checked against the timing requirement and run spread. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-M` | `Pattern Types Active`: [0.500, 3.000]; `Pattern Instances`: [0.000, 8.500] | 11/21 | 100.0% |
| `M-L` | `Client Selector Criteria`: {(not selected)}; `Message Compressor Alg`: {(not selected)}; `Pattern Types Active`: [0.000, 0.500]; `Pattern Instances`: [0.000, 0.500] | 2/2 | 16.7% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `JSD Mean` 67.8%; `Pattern Types Active` 10.9%; `Client Selector Criteria` 10.5% | 0.369 | 0.636 pp |
| Round time | `Pattern Types Active` 56.8%; `Client Selector Criteria` 25.5%; `Pattern Instances` 8.8% | -0.002 | 0.469 s |

JSD leads accuracy (67.8%) but is recorded only for HDH-ON runs. Replacing its values with an availability flag lowers accuracy R² from 0.369 to 0.083, so numerical variation contributes beyond the ON/OFF flag; it is still not an independent heterogeneity effect across all configurations. `Pattern Types Active` leads time importance, but time R² is essentially zero.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 7 parameters under the score >3% gate: `JSD Mean`, `Pattern Types Active`, `Client Selector Criteria`, `Pattern Instances`, `HDH Instances`, `HDH Batch Size`, `Message Compressor Alg`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | All loaded configurations | `M-M` | 45.8% → 52.4% | +6.5 | 21/24 (87.5%) |
| CART | All loaded configurations | `M-M` | 45.8% → 66.7% | +20.8 | 3/24 (12.5%) |
| PRIM/CART | All loaded configurations | `M-L` | 50.0% → 100.0% | +50.0 | 2/24 (8.3%) |

For `M-M`, PRIM gives a small gain while retaining 87.5% of scenarios; CART gives a larger gain while retaining only 12.5%. This is a concrete robustness-versus-operating-freedom choice. The 100% `M-L` result has only two retained cases and is weak support for a design commitment.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
