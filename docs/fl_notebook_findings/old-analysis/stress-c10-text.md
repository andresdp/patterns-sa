# Fixed setting — 10 clients, text

**Notebook:** [analysis-fl-stress-c10-text.ipynb](../../../federatedlearning/old-analysis/analysis-fl-stress-c10-text.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS-alone has a modest speed/accuracy exchange; HDH-alone sacrifices 1.04 pp accuracy for only 0.054 s lower mean time.

**Conditions held in the comparison:** one task/client count, 25% low-spec, 25% non-IID, and 25% delayed clients; eight configurations × ten partition seeds = 80 runs. Accuracy differences below are pp; time differences are seconds. Hosts and scheduling are not matched.

## One pattern at a time, other patterns OFF

| Pattern | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|
| CS | −0.17 | −0.250 | 6/10 | 9/10 |
| MC | −0.04 | +0.193 | 3/10 | 6/10 |
| HDH | −1.04 | −0.054 | 7/10 | 8/10 |

## Complete alternatives and feasible tradeoffs

| Configuration (CS, MC, HDH) | Patterns ON | Mean accuracy | Mean round time (s) | Mean frontier |
|---|---|---:|---:|---|
| `000` | Baseline | 90.42% | 11.381 | Yes |
| `001` | HDH | 89.38% | 11.327 | — |
| `010` | MC | 90.39% | 11.574 | — |
| `011` | MC+HDH | 89.38% | 11.858 | — |
| `100` | CS | 90.26% | 11.131 | Yes |
| `101` | CS+HDH | 89.10% | 11.127 | Yes |
| `110` | CS+MC | 90.23% | 11.378 | — |
| `111` | CS+MC+HDH | 89.13% | 11.659 | — |

Each configuration has ten runs. “Mean frontier” means no other observed configuration has both at least as high mean accuracy and at most as low mean time, with one strict advantage. It uses unrounded means and does not account for uncertainty; near ties can disappear under rounding. This is a shortlist of observed tradeoff alternatives.

Baseline is the accuracy leader (90.42%, 11.381 s). CS-alone moves to 90.26%/11.131 s. Adding HDH to CS saves only another 0.004 s on the mean while moving accuracy to 89.10%; a tiny numerical time advantage does not make it a compelling alternative. MC-alone is slightly lower in accuracy (−0.04 pp) and slower (+0.193 s).

## Composition and stability

| Add CS while holding MC/HDH fixed | Mean accuracy change (pp) | Mean time change (s) | CS faster |
|---|---:|---:|---:|
| `000` → `100` | −0.17 | −0.250 | 6/10 |
| `001` → `101` | −0.28 | −0.200 | 7/10 |
| `010` → `110` | −0.16 | −0.196 | 7/10 |
| `011` → `111` | −0.25 | −0.199 | 6/10 |

CS-alone is faster in 6/10 pairs, while HDH-alone is faster in 7/10 with one tie. Frequency and magnitude differ: HDH’s more frequent small reductions do not offset its much larger accuracy decrement. These are seed-matched associations, not causal effects or formal interaction tests.

## Discovered conditions

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-S` | `Client Selector Criteria`: {CPU}; `Message Compressor Alg`: {(not selected)}; `JSD Mean`: (not selected) or <= 0.009; `HDH Instances`: [0.000, 1.000] | 1/3 | 33.3% |
| `M-M` | `Client Selector Criteria`: {(not selected)}; `Message Compressor Alg`: {(not selected)}; `Pattern Types Active`: [0.500, 1.500] | 1/1 | 7.1% |
| `M-L` | `Client Selector Criteria`: {CPU}; `Message Compressor Alg`: {zlib}; `JSD Mean`: [-0.001, 0.018] | 1/3 | 14.3% |

These rules use the notebook’s local bin edges and a 24-row test split. Use successful/test counts and coverage to assess them; a 100% density from one or two cases is weak evidence of stability. The environment is fixed, so these boxes cannot describe how changing delay or non-IID share alters the tradeoff.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `JSD Mean` 66.8%; `Pattern Types Active` 18.6%; `Message Compressor Alg` 8.7% | 0.218 | 1.266 pp |
| Round time | `Message Compressor Alg` 50.1%; `Client Selector Criteria` 22.6%; `HDH Instances` 15.4% | 0.419 | 0.256 s |

JSD leads accuracy (66.8%) with only modest held-out prediction; replacing it with an availability flag gives R² −0.360 instead of 0.218. MC’s algorithm flag leads timing (50.1%), consistent with MC’s positive time differences on the text task; direction comes from those matched differences. The timing fit is moderate (R² 0.419), not a deployment guarantee.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 5 parameters under the score >3% gate: `JSD Mean`, `Message Compressor Alg`, `Pattern Types Active`, `Client Selector Criteria`, `HDH Instances`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | All loaded configurations | `M-M` | 58.3% → 100.0% | +41.7 | 1/24 (4.2%) |
| CART | All loaded configurations | `M-M` | 58.3% → 50.0% | −8.3 | 2/24 (8.3%) |
| PRIM/CART | All loaded configurations | `M-L` | 29.2% → 33.3% | +4.2 | 3/24 (12.5%) |

PRIM’s large `M-M` gain is based on one retained case; CART’s different `M-M` rule lowers attainment. The `M-L` gain is small and based on three cases. These results are insufficient for a reliable robustness prescription.

**Numerical audit:** For PRIM `M-S`, discovery reports three test cases but reapplication in the what-if path retains four. Its inferred boundaries must be reconciled before reporting a validated gain; it is excluded from this table.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

**RQ1:** Complete-alternative tradeoffs. **RQ2:** Local rules and their what-if gain-versus-retention tradeoffs. **RQ3:** Composition-dependent decision differences. **RQ4:** Run consistency in a fixed macro setting. Use continuous outcomes to compare with other notebooks because stress-bin edges differ.
