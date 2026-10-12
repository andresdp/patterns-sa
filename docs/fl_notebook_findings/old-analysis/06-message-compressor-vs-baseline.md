# Message Compressor versus baseline

**Notebook:** [analysis-fl-message-compressor-vs-baseline.ipynb](../../../federatedlearning/old-analysis/analysis-fl-message-compressor-vs-baseline.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** MC-ON is associated with nearly unchanged accuracy and longer rounds in 219/300 matched pairs.

**Support:** 780 loaded runs; 300 matched pairs (300 runs per arm used in the contrast). The other two patterns are OFF. Differences compare ON with OFF at the same task, client count, environment shares, and partition seed. Hosts and scheduling remain unmatched. These are observed associations; the campaign does not identify causal effects. Accuracy changes are in **percentage points (pp)**, and negative time changes mean faster rounds.

| Outcome difference: ON − OFF | Mean | Median | Observed min–max |
|---|---:|---:|---:|
| Accuracy (pp) | −0.03 | −0.02 | −2.94 to +3.07 |
| Total round time (s) | +0.214 | +0.183 | −1.072 to +1.819 |

## Conditional target attainment

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-S` | `Dataset`: {CIFAR-10}; `delay_percentage`: [0.000, 12.500] | 18/18 | 100.0% |
| `L-S` | `Dataset`: {AG_NEWS}; `delay_percentage`: [0.000, 12.500] | 18/18 | 100.0% |
| `L-M` | `Dataset`: {AG_NEWS}; `delay_percentage`: [12.500, 100.000] | 99/99 | 100.0% |

The PRIM boxes use all loaded runs of this two-configuration slice, including unmatched environments; they are not evaluated on the matched-pair subset alone. Test successes describe observed target attainment inside a rule. They do not identify an effect of switching the pattern.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 96.0%; `Alpha Dirichlet Mean` 1.3%; `non_iid_percentage` 1.3% | 0.994 | 1.077 pp |
| Round time | `delay_percentage` 94.0%; `Total Clients` 5.3%; `Dataset` 0.3% | 0.979 | 0.316 s |

The selected discovery dimensions are only task, delay, and client count. No explicit MC policy representative passes the 3% gate, so the resulting boxes cannot directly prescribe MC ON versus OFF. Delay receives 94.0% of time importance; the small matched MC time increase remains a separate measured association even though its relative predictive importance is small.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 3 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `Total Clients`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `L-S` | 7.7% → 100.0% | +92.3 | 18/234 (7.7%) |
| PRIM/CART | `000` | `L-S` | 4.9% → 100.0% | +95.1 | 5/102 (4.9%) |
| PRIM/CART | `010` | `L-S` | 9.8% → 100.0% | +90.2 | 13/132 (9.8%) |

The fast/high-accuracy restriction gives 100% attainment in both the baseline and MC-only retained subsets. Because the same target can be made robust in either configuration, this what-if result primarily supports the low-delay task envelope rather than a need to enable compression.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication

For total round time, these comparisons favor retaining MC-OFF unless another measured requirement motivates compression. In all 12 text-task composition comparisons at the common environment point, MC-ON has higher mean time; image-task composition results are mixed. The 138 positive, 157 negative, and 5 zero accuracy differences show why “no average gain” is different from identical runs.

**Possible mechanism:** Compression can reduce transmitted bytes while adding compression/decompression work. The present accuracy/total-time result is compatible with that tradeoff, but it does not measure the byte saving or identify the source of the time increase.

**RQ1/RQ3:** Direct decision/tradeoff association on shared support. **RQ2:** Contextual rules and what-if robustness gains under restriction. **RQ4:** Median, range, and sign counts distinguish average behavior from consistency across matched runs. Whole-campaign ranges also mix different settings; use the fixed stress summaries for within-setting variation.
