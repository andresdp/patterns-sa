# Client Selector versus baseline

**Notebook:** [analysis-fl-client-selector-vs-baseline.ipynb](../../../federatedlearning/old-analysis/analysis-fl-client-selector-vs-baseline.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** CS-ON is associated with shorter rounds in 162/180 matched pairs and lower accuracy in 143/180.

**Support:** 660 loaded runs; 180 matched pairs (180 runs per arm used in the contrast). The other two patterns are OFF. Differences compare ON with OFF at the same task, client count, environment shares, and partition seed. Hosts and scheduling remain unmatched. These are observed associations; the campaign does not identify causal effects. Accuracy changes are in **percentage points (pp)**, and negative time changes mean faster rounds.

| Outcome difference: ON − OFF | Mean | Median | Observed min–max |
|---|---:|---:|---:|
| Accuracy (pp) | −2.58 | −1.67 | −34.08 to +7.87 |
| Total round time (s) | −3.590 | −2.214 | −12.848 to +0.602 |

## Conditional target attainment

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-M` | `Dataset`: {CIFAR-10}; `Client Selector Criteria`: {(not selected)}; `non_iid_percentage`: [25.000, 50.000]; `delay_percentage`: [12.500, 100.000] | 27/27 | 50.0% |
| `L-S` | `Dataset`: {AG_NEWS}; `delay_percentage`: [0.000, 50.000] | 26/67 | 89.7% |

The PRIM boxes use all loaded runs of this two-configuration slice, including unmatched environments; they are not evaluated on the matched-pair subset alone. Test successes describe observed target attainment inside a rule. They do not identify an effect of switching the pattern.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 94.5%; `non_iid_percentage` 3.2%; `Total Clients` 1.3% | 0.981 | 1.738 pp |
| Round time | `delay_percentage` 50.4%; `Client Selector Criteria` 25.7%; `CPU Mean` 12.3% | 0.584 | 1.521 s |

Delay (50.4%) and the CS representative (25.7%) dominate timing. This is consistent with the observed speed/accuracy exchange, while importance alone supplies no sign or causal effect. Task/model dominance (94.5%) masks much of the smaller accuracy difference associated with CS; the matched comparison remains the direct evidence for that choice.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 6 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `Client Selector Criteria`, `CPU Mean`, `Total Clients`, `non_iid_percentage`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM | All loaded configurations | `L-S` | 14.6% → 38.8% | +24.2 | 67/198 (33.8%) |
| CART | All loaded configurations | `L-S` | 14.6% → 100.0% | +85.4 | 9/198 (4.5%) |
| PRIM | `100` | `L-S` | 23.0% → 47.2% | +24.2 | 36/87 (41.4%) |
| CART | `100` | `L-S` | 23.0% → unsupported | — | 0/87 (0.0%) |

PRIM’s broader `L-S` envelope retains 67/198 scenarios and raises attainment to 38.8%; CART reaches 100% but retains only 9/198, all baseline cases. For CS-only, PRIM raises attainment from 23.0% to 47.2% on 36/87 cases; CART retains none. Thus the strong pooled CART gain cannot be presented as a supported what-if improvement for CS-only.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication

CS is the clearest candidate for shifting the tradeoff toward time. Its mean accuracy difference is −2.58 pp, so whether it is useful depends on the accuracy floor. At the common environment point, all 24 CS comparisons across six task/client slices and four other-pattern compositions have lower mean time; the individual-run time sign still varies.

**Possible mechanism:** Excluding slower clients is a plausible explanation for shorter rounds, and changing the participating data can plausibly alter accuracy. The aggregate outcomes do not verify that mechanism or remove host/runtime differences.

**RQ1/RQ3:** Direct decision/tradeoff association on shared support. **RQ2:** Contextual rules and what-if robustness gains under restriction. **RQ4:** Median, range, and sign counts distinguish average behavior from consistency across matched runs. Whole-campaign ranges also mix different settings; use the fixed stress summaries for within-setting variation.
