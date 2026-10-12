# Message Compressor only

**Notebook:** [analysis-fl-message-compressor.ipynb](../../federatedlearning/analysis-fl-message-compressor.ipynb)  
**Saved execution:** perfmodels; 51 code cells; no notebook cell errors.

**Main association:** Fast-round regions are associated with low delay; the matched evidence does not show a total-round-time advantage from enabling MC.

## Observed outcomes by task

| Task/model | Runs | Mean accuracy | Mean round time | Observed regions |
|---|---:|---:|---:|---|
| AG_NEWS/MLP | 210 | 89.87% | 12.023 s | `L-M` 180/210, `L-S` 30/210 |
| CIFAR-10/CNN 16k | 210 | 52.58% | 12.065 s | `M-M` 158/210, `M-S` 30/210, `S-M` 22/210 |

These means describe this configuration’s own sampled environments. Region counts use the overview’s fixed edges. Comparisons between separate single-configuration notebook means have unequal environment support.

## Conditions associated with tradeoffs

| Target | Conditions in the saved PRIM rule | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-S` | `Dataset`: {CIFAR-10}; `delay_percentage`: [0.000, 12.500] | 9/9 | 100.0% |
| `M-M` | `Dataset`: {CIFAR-10}; `Message Compressor Instances`: [4.000, 6.000]; `delay_percentage`: [12.500, 100.000] | 18/19 | 38.3% |
| `L-S` | `Dataset`: {AG_NEWS}; `delay_percentage`: [0.000, 12.500] | 9/9 | 100.0% |
| `L-M` | `Dataset`: {AG_NEWS}; `delay_percentage`: [12.500, 100.000] | 54/54 | 100.0% |

At delay below 12.5%, the image `M-S` and text `L-S` boxes each succeed in 9/9 test runs. The higher-delay text `L-M` rule succeeds in 54/54. The same delay split also appears in baseline, so it is not specific to compression.

## Feature importance: drivers and consistency

Scores below are shares of the fitted forest’s training impurity reduction, not percentage changes in outcomes or variance explained. The added held-out checks use the same training/test split and retained features as the notebook.

| Objective | Top three scored features | Held-out R² | Held-out mean absolute error |
|---|---|---:|---:|
| Accuracy | `Dataset` 97.0%; `Message Compressor Instances` 1.1%; `Alpha Dirichlet Mean` 1.0% | 0.993 | 1.170 pp |
| Round time | `delay_percentage` 93.7%; `Message Compressor Instances` 5.7%; `Dataset` 0.4% | 0.989 | 0.253 s |

Delay dominates timing (93.7%). `Message Compressor Instances` stands for deployment/client-count variation in this always-ON slice; `Total Clients` is a redundant proxy and its zero is not evidence of no client-count sensitivity. The fitted timing model predicts held-out rows well, but no compression-algorithm or ON/OFF tuning is estimated here.

The leading feature is unchanged over five forest seeds for both objectives, with training rows and correlation pruning held fixed. This checks model randomness, not stability across new partitions or deployments. Discovery keeps 3 parameters under the score >3% gate: `Dataset`, `delay_percentage`, `Message Compressor Instances`.

The [cross-notebook feature audit](../fl_feature_importance_audit.md) distinguishes constant and pruned zeros, measurement proxies, threshold sensitivity, and held-out prediction limits.

## What-if: robustness after applying box rules

“Before” is target attainment over that configuration’s unconstrained test scenarios; “inside box” uses only scenarios satisfying the inferred rule. Gain is the difference in percentage points. Retained/test counts show the operating/design-space restriction required. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON.

| Method | Configuration | Target | Before → inside box | Gain (pp) | Retained test runs |
|---|---|---|---:|---:|---:|
| PRIM/CART | `010` | `L-S` | 7.1% → 100.0% | +92.9 | 9/126 (7.1%) |
| PRIM | `010` | `M-M` | 37.3% → 94.7% | +57.4 | 19/126 (15.1%) |
| CART | `010` | `M-M` | 37.3% → 100.0% | +62.7 | 18/126 (14.3%) |
| PRIM/CART | `010` | `L-M` | 42.9% → 100.0% | +57.1 | 54/126 (42.9%) |

For MC-only, both methods raise `L-S` attainment from 7.1% to 100% within the low-delay text envelope, retaining nine test cases. On `M-M`, CART gives a higher conditional rate while retaining one fewer case than PRIM. These results support rule-based robustness assessment of the compressor configuration; they do not establish that compression itself caused the gain.

This is conditional tradeoff robustness (STARR), evaluated by restricting observed scenarios. It measures consistency of target-region membership, rather than the continuous accuracy/time standard deviation. Environment constraints are operating-envelope conditions the designer must assess; a pattern choice alone does not enforce them.

## Design implication and RQs

MC’s matched accuracy change is −0.03 pp and time change +0.214 s; 219/300 pairs take longer. The high raw accuracy mean in this notebook reflects its sampled workload/environment mix. A bandwidth-related reason to retain compression needs message-size or communication-cost evidence beyond this accuracy/total-time tradeoff.

**RQ1:** Establishes this complete configuration’s outcome distribution. **RQ2:** Gives conditional rules, their support, and before/inside-box robustness. **RQ3:** Use the companion `vs-baseline` notebook for an isolated decision comparison. **RQ4:** Variability includes different partitions and runtime conditions; these pooled means do not measure stability at one fixed setting.
