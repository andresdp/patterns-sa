# HDH versus baseline

**Notebook:** [analysis-fl-hdh-vs-baseline.ipynb](../../../federatedlearning/old-analysis/analysis-fl-hdh-vs-baseline.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** HDH-ON is associated with lower accuracy in 138/180 pairs; its round-time differences have mixed signs.

**Support:** 660 loaded runs; 180 matched pairs (180 runs per arm used in the contrast). The other two patterns are OFF. Differences compare ON with OFF at the same task, client count, environment shares, and partition seed. Hosts and scheduling remain unmatched. These are observed associations; the campaign does not identify causal effects. Accuracy changes are in **percentage points (pp)**, and negative time changes mean faster rounds.

| Outcome difference: ON − OFF | Mean | Median | Observed min–max |
|---|---:|---:|---:|
| Accuracy (pp) | −1.45 | −1.34 | −7.02 to +2.50 |
| Total round time (s) | +0.530 | −0.013 | −3.591 to +9.650 |

## Conditional target attainment

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `S-M` | `Total Clients`: [6.000, 10.000]; `Dataset`: {CIFAR-10}; `non_iid_percentage`: [62.500, 75.000] | 31/31 | 81.6% |
| `L-L` | `Total Clients`: [4.000, 6.000]; `HDH Instances`: [1.500, 8.000] | 3/12 | 100.0% |

The PRIM boxes use all loaded runs of this two-configuration slice, including unmatched environments; they are not evaluated on the matched-pair subset alone. Test successes describe observed target attainment inside a rule. They do not identify an effect of switching the pattern.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 93.6%; `non_iid_percentage` 4.1%; `Total Clients` 1.6% | 0.988 | 1.399 pp |
| Round time | `delay_percentage` 76.6%; `HDH Instances` 10.2%; `Total Clients` 7.0% | 0.899 | 0.561 s |

Timing is associated mainly with delay (76.6%) and HDH activity count (10.2%). JSD is missing in all 360 HDH-OFF runs and present in all 300 HDH-ON runs, so it combines data-heterogeneity information with the configured decision’s measurement availability. Interpret any JSD rule conditionally, and retain the separate numerical-boundary audit for the what-if matrices.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 6 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `HDH Instances`, `Total Clients`, `JSD Mean`, `non_iid_percentage`.

The [cross-notebook feature audit](../../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | All loaded configurations | `L-M` | 43.4% → 100.0% | +56.6 | 63/198 (31.8%) |
| PRIM | All loaded configurations | `L-L` | 1.5% → 25.0% | +23.5 | 12/198 (6.1%) |
| CART | All loaded configurations | `L-L` | 1.5% → 100.0% | +98.5 | 1/198 (0.5%) |

For `L-M`, both methods retain 63/198 scenarios and raise target attainment from 43.4% to 100%. For rare `L-L`, CART’s apparent 100% is based on one retained case; PRIM retains twelve cases but only three attain the target. The latter illustrates the gain-versus-support tradeoff rather than a strong slow-region prescription.

**Numerical audit:** The saved PRIM `M-S`, `M-M`, and `L-S` what-if matrices retain zero cases despite nonzero support in their discovery metrics; CART has the same discrepancy for `M-S` and `M-M`. A checked `L-S` box contains a lower non-IID limit of `25.000000000000004` and an upper missing-value sentinel just below the encoded value, so strict reapplication excludes boundary records. Those cells require boundary-handling reconciliation before a robustness conclusion. The supported `L-M`/`L-L` rows above agree across the evaluation paths.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication

There is no general observed accuracy gain from choosing HDH in this setup. The median time change is approximately zero despite a +0.530 s mean: 91 pairs are faster, 88 slower, and one tied. Timing therefore needs a distribution-based decision, not a claim that HDH is uniformly slower.

**Possible mechanism:** Augmentation may change both training data and computation, but the activity logs show different exposure across tasks: only 42/480 HDH-ON image runs record HDH work, versus 466/480 text runs. These comparisons characterize the configured decision; they cannot establish augmentation efficacy when little work was actually recorded.

**RQ1/RQ3:** Direct decision/tradeoff association on shared support. **RQ2:** Contextual rules and what-if robustness gains under restriction. **RQ4:** Median, range, and sign counts distinguish average behavior from consistency across matched runs. Whole-campaign ranges also mix different settings; use the fixed stress summaries for within-setting variation.
