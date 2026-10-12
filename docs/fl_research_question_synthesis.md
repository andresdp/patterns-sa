# ADEPT–FL: decision associations and conclusions by research question

This synthesis links pattern choices and environmental conditions to **observed accuracy/time tradeoffs and run consistency**. It consolidates the [14 notebook findings](fl_notebook_findings/README.md), rechecked against the compact records and saved notebook outputs in `perfmodels`.

The evidence supports conditional associations. Seed matching makes the comparisons more specific, but hosts and scheduling remain unmatched, so causal effects are not identified. Possible mechanisms are discussed separately from measured differences. Accuracy changes are in **percentage points (pp)**; a negative time difference means faster rounds.

**Resolution of these conclusions:** The present phase uses compact run-level outcomes and across-client summaries. Numeric features such as CPU/RAM/JSD means describe the recorded client population within a run; they do not retain individual-client distributions or joint conditions. Equal averages can therefore mask different bottlenecks and client imbalance. Some usage averages cover participants only, which can change with CS. RQ1/RQ3 compare aggregate outcomes; RQ2's rules constrain summaries rather than every client; RQ4 measures variation across runs rather than among clients or rounds. These findings support an initial design shortlist and operating-envelope assessment. Explaining individual-client mechanisms with the detailed records is deferred until the compact space is understood; existing detailed-log HDH activity counts are a limited supporting measurement.

## RQ1 — Which decisions and configurations are associated with feasible tradeoffs?

**Conclusion: complete configurations offer different accuracy/time compromises, and the useful alternatives depend on task and client count. More enabled patterns do not consistently improve both outcomes.**

The strongest comparable design-space view is the common environment point: 25% low-spec, 25% non-IID, and 25% delayed clients. Each of six task/client slices contains all eight configurations and ten partition seeds per configuration. Configuration codes are `(CS, MC, HDH)`, with `1` meaning ON and `000` the baseline.

| Task | Clients | Highest observed mean accuracy: configuration; accuracy / time | Lowest observed mean time: configuration; accuracy / time | Configurations on the mean frontier |
|---|---:|---|---|---|
| Image | 4 | `001`; 58.35% / 12.842 s | `101`; 57.07% / 10.030 s | `001`, `011`, `101`, `111` |
| Image | 8 | `000`; 52.80% / 11.898 s | `111`; 51.08% / 10.887 s | `000`, `010`, `110`, `111` |
| Image | 10 | `110`; 51.80% / 11.524 s | `101`; 50.64% / 11.224 s | `100`, `101`, `110` |
| Text | 4 | `000`; 91.27% / 12.369 s | `101`; 90.46% / 9.617 s | `000`, `001`, `101`, `110` |
| Text | 8 | `010`; 90.16% / 12.002 s | `100`; 89.55% / 10.818 s | `000`, `010`, `100` |
| Text | 10 | `000`; 90.42% / 11.381 s | `101`; 89.10% / 11.127 s | `000`, `100`, `101` |

The **mean frontier** retains configurations for which no other alternative has both at least as high mean accuracy and at most as low mean time, with one strict advantage. This is a numerical shortlist calculated from the records, not an uncertainty-adjusted ranking. Tiny gaps can put alternatives on the frontier without establishing a meaningful advantage.

For example, at four text clients, baseline averages **91.27% / 12.369 s**, whereas CS-only averages **90.46% / 9.694 s**. CS therefore shifts the observed tradeoff toward speed at an accuracy cost. At ten image clients, CS+MC averages **51.80% / 11.524 s**, compared with baseline **51.52% / 11.638 s**: this composition has a better observed mean on both objectives, although its gaps are small and do not establish dominance on every run.

Feasibility must be evaluated against a requirement on individual outcomes. As an **illustrative** requirement, at least 90% text accuracy and at most 11 s total round time is met in **0/10 baseline runs and 3/10 CS-only runs** at four clients. None of the eight configurations meets the stricter 91%/11 s requirement in these ten runs. An attractive mean is therefore not evidence of stable requirement satisfaction.

Across the full, incompletely crossed campaign, `L-M` contains 875/2,340 runs (37.39%), `M-M` 691 (29.53%), and `L-S` 257 (10.98%). The remaining observed regions are `S-M` 227, `M-S` 223, `S-S` 50, and `L-L` 17. These are whole-campaign counts; earlier reports inadvertently used training-split percentages. The global high-accuracy/fast-time region `L-S` requires accuracy above 74.73% and time at most 9.5065 s. Stress notebooks use their own edges, so their labels cannot rank alternatives across tasks.

All 1,149 global `L-*` runs are text-task runs; the image task has none. This pooled high-accuracy association partly reflects task difficulty and the paired model, rather than a pattern decision. Set task-specific quality requirements before interpreting a region as feasible or desirable.

**Design action:** Specify the accuracy floor and time bound, then use the matching task/client summary to shortlist complete configurations. Check observed target-attainment counts and spread before choosing a mean-frontier alternative.

## RQ2 — Which rules identify target regions, and how does applying them change robustness?

**Conclusion: PRIM and CART identify restrictions under which target tradeoffs are reached more consistently. The robustness gain depends on the configuration, the chosen rule, and how much of the operating/design space the rule retains. Some boxes give no gain or worsen attainment.**

The following PRIM rules come from the overview. “Successes/box runs” measures density on the 702 test rows; coverage is the share of all test runs in the target captured by that rule. Conditions are conjunctive.

| Target and quality meaning | Conditions | Test successes / box runs | Target coverage |
|---|---|---:|---:|
| `M-S`: medium accuracy, fast rounds | CIFAR-10; delay 0–12.5% | 41/42 (97.6%) | 61.2% |
| `L-S`: high accuracy, fast rounds | AG_NEWS; delay 0–12.5%; HDH instances 0–2.5 | 46/46 (100%) | 59.7% |
| `M-M`: medium accuracy/time | CIFAR-10; CS not selected; non-IID 25–37.5%; delay 12.5–100% | 102/103 (99.0%) | 49.3% |
| `S-M`: low accuracy, middle time | CIFAR-10; 8 or 10 clients; CS not selected; non-IID 62.5–75% | 41/41 (100%) | 60.3% |
| `L-M`: high accuracy, middle time | AG_NEWS; 8 or 10 clients; CS not selected; delay 12.5–100% | 116/116 (100%) | 44.1% |
| `L-L`: high accuracy, slow rounds | HDH instances 0.5–8; non-IID 37.5–75% | 5/69 (7.2%) | 100% |

The low-delay rules describe fast regions without selecting a specific compressor decision. Similar rules occur in baseline and MC-only notebooks. This supports a **delay/task association**, not a compression-specific time benefit. The high-non-IID image box identifies a low-accuracy region even with CS OFF; retaining all clients does not guarantee high accuracy under that observed data condition.

The feature-selection gate limits what the boxes can express. In MC versus baseline, only dataset, delay, and client count pass the executed importance threshold; no explicit compression-decision representative enters discovery. Those boxes therefore identify operating envelopes rather than an MC ON/OFF prescription. The [feature audit](fl_feature_importance_audit.md) reports the selected dimensions and the correlation-pruned representatives for every notebook. Their omission from a box should not be interpreted as proof of no pattern association.

Decoded thresholds separate observed factor levels: for example, delay below 12.5% selects the observed 0% level, and delay above 12.5% selects 25–100%. These are not measurements at every intermediate percentage. Task and model are coupled in the campaign, so their separate contributions are not identified.

Small stress boxes cannot justify strong prescriptions: the ten-client text `M-M` box succeeds in **1/1** test case and covers only **7.1%** of that target; the ten-client image `M-M` box succeeds in **1/3** and covers **7.7%**. Conversely, 100% coverage of overview `L-L` is weak screening because 64/69 box runs miss the target. Coverage and density answer different design questions.

In this codebase, `lift = test density − training target prevalence`: it is an **absolute difference**, not a ratio or causal improvement. The box tables above provide the more direct evidence for design decisions.

### What-if: restricting the space to improve target robustness

The notebook's Section 11 asks: **if a designer admits only settings satisfying a discovered box, how consistently does each configuration reach the target?** For configuration $d$, target tradeoff $T$, and box $B$, compare unconstrained robustness $R_0=P(T\mid d)$ with constrained robustness $R_B=P(T\mid d,B)$. The gain is $R_B-R_0$. Both are STARR success rates on the same test split; the restricted sample is a subset of the original sample. This “baseline” is the unconstrained rate for the configuration being evaluated, not necessarily the all-patterns-OFF configuration.

The overview provides substantial conditional gains:

| Method | Configuration scope | Target | Before → inside box | Gain (pp) | Retained test scenarios |
|---|---|---|---:|---:|---:|
| PRIM and CART | All configurations | `M-S` | 9.5% → 97.6% | +88.1 | 42/702 (6.0%) |
| PRIM and CART | All configurations | `L-S` | 11.0% → 100.0% | +89.0 | 46/702 (6.6%) |
| PRIM and CART | All configurations | `M-M` | 29.5% → 99.0% | +69.5 | 103/702 (14.7%) |
| PRIM | All configurations | `L-M` | 37.5% → 100.0% | +62.5 | 116/702 (16.5%) |
| CART | All configurations | `L-M` | 37.5% → 100.0% | +62.5 | 120/702 (17.1%) |
| PRIM and CART | All-OFF `000` | `M-M` | 30.8% → 100.0% | +69.2 | 31/107 (29.0%) |
| PRIM and CART | All-OFF `000` | `L-S` | 6.5% → 100.0% | +93.5 | 7/107 (6.5%) |
| PRIM | CS-only `100` | `L-M` | 24.7% → unsupported | — | 0/85 |
| CART | CS-only `100` | `L-M` | 24.7% → 100.0% | +75.3 | 4/85 (4.7%) |

These are robustness gains from **restricting admissible scenarios**, rather than gains from changing a pattern alone. For example, a designer can obtain a more consistent `M-M` region with all patterns OFF by adopting the image-task, lower-non-IID, higher-delay envelope, but that restriction retains only 31/107 of that configuration's test scenarios. The global `L-S` result is stronger target consistency over a much narrower envelope. A fixed task/environment deployment must be checked against the rule; changing a configuration does not enforce a low-delay environment.

PRIM and CART can expose different compromises. In the eight-client image slice, PRIM raises `M-M` attainment from **45.8% to 52.4% (+6.5 pp)** while retaining **21/24** scenarios. CART raises it to **66.7% (+20.8 pp)** while retaining only **3/24**. The designer trades a broader admissible space for a higher conditional success rate. In contrast, the ten-client image PRIM box lowers `M-M` attainment from **54.2% to 33.3% (−20.8 pp)** on three retained cases. That box does not support a robustness-improving prescription. At ten text clients, PRIM's `M-M` gain is based on one retained case, while CART's rule gives a negative gain on two: neither is sufficient evidence of a reliable prescription.

**Retained scenario fraction** $P(B\mid d)$ measures the operating/design freedom left by the restriction; **target coverage** $P(B\mid T,d)$ measures how much of the successful target region it captures. Neither should be omitted when judging a what-if gain. The matrices contain constrained success rates, so gains must be calculated against the matching unconstrained rows. A zero may mean no retained scenarios, and a missing box is unsupported; neither is evidence of observed failure under an implemented rule.

Higher STARR means the retained outcomes fall in the target region more consistently. It demonstrates robustness of **tradeoff membership**; a reduction in continuous accuracy/time variance within that region would require a separate distribution calculation. For designer-controlled levers, the box gives a candidate configuration restriction. For uncertainties, it defines the operating envelope within which the result is supported.

Rules involving realized participation, HDH work, or pattern-instance counts also require care: these measurements depend on the choices and execution, so they are diagnostic conditions rather than external uncertainties. Before adopting such a rule prospectively, establish how its conditions can be assessed or satisfied before the outcome is known. The [simplified formalization and hypothetical influence model](paper_adept_formal_extension.md) make this distinction explicit; filtering the observed runs does not estimate the effect of enforcing the rule in deployment.

**Numerical audit:** Recomputing exact box constraints and support reproduced all 14 notebooks' saved PRIM/CART matrices. However, some HDH-versus-baseline boxes disagree between discovery evaluation and subsequent what-if application: floating-point boundary conversion can exclude records at an intended boundary, such as 25%. The ten-client text PRIM `M-S` box also has different support across those paths. The affected gains are flagged in their notebook summaries and excluded from the validated examples above; their boundary handling needs reconciliation before a final paper claim.

**Design action:** Choose the target, then compare the configuration's before/inside-box success rate, gain, retained scenario count, and target coverage. Prefer a useful gain with credible support and an operating envelope the deployment can satisfy. A large gain on a tiny retained subset is a prompt for targeted validation. This is the practical what-if contribution of scenario discovery, alongside its explanatory rules.

## RQ3 — How do individual decisions and pattern composition change the observed tradeoff?

**Conclusion: CS has the most consistent association with shorter mean time; MC has no timing advantage on the text task; HDH has no general observed accuracy advantage. The accuracy/time exchange changes with surrounding patterns.**

The campaign-wide comparisons below hold the other patterns OFF and match task, client count, environment shares, and partition seed. Their shared settings differ in number across patterns.

| Pattern ON versus OFF | Matched pairs | Mean accuracy change (pp) | Mean time change (s) | ON faster | ON lower accuracy |
|---|---:|---:|---:|---:|---:|
| CS | 180 | −2.58 | −3.590 | 162/180 | 143/180 |
| MC | 300 | −0.03 | +0.214 | 81/300 | 157/300 |
| HDH | 180 | −1.45 | +0.530 | 91/180 | 138/180 |

The fixed common-environment slices clarify the associations:

- **CS:** All **24** composition-specific comparisons (six task/client slices × four settings of MC/HDH) have lower mean round time with CS ON. Accuracy is lower in **23/24**. The exception is ten image clients with MC ON and HDH OFF: adding CS changes accuracy by **+0.21 pp** and time by **−0.170 s**, compared with **−0.30 pp / −0.357 s** when adding CS to baseline in that same slice. These comparisons reuse the same 80 runs within each slice; they are not 24 independent replications.
- **MC:** All **12** text composition comparisons have higher mean time, from **+0.178 to +0.567 s**. Image results are mixed: 7/12 are faster on the mean. MC-only’s high pooled accuracy mean is therefore insufficient evidence of an accuracy benefit or a total-time benefit from choosing MC.
- **HDH:** Standalone mean accuracy is lower in five of six fixed slices; the exception is four image clients (**+0.59 pp**). Time differences vary in direction. However, per-round logs record any HDH work in only **42/480 HDH-ON image runs**, compared with **466/480 text runs**. “HDH enabled” and “augmentation applied” are substantially different exposures in this campaign.

**Possible mechanisms, to be verified:** CS changes participation, potentially removing slow clients and some training data; compression may exchange fewer bytes at a computation cost; HDH may alter training data and computation when actually applied. The outcome associations are compatible with these mechanisms, but neither matched totals nor discovered boxes verify them. Training/communication timing and participation/activity logs are needed to connect a mechanism to the observed change.

**Design action:** Consider CS when a speed/accuracy exchange is acceptable, and compare it in the intended composition rather than assuming its standalone result transfers. For text workloads, retain MC only for a separately demonstrated requirement such as message size or network cost. Validate HDH on actual augmentation activity and expected data heterogeneity before selecting it for accuracy.

## RQ4 — How stable are the tradeoffs under the same modeled macro conditions?

**Conclusion: identical configuration/task/client/environment shares do not imply identical outcomes. Some mean-feasible choices fail the target on most observed runs.**

Each of the 234 observed cells has ten different partition seeds. The following statistics summarize variability across those seeds and associated runtime conditions. They do not isolate repeated-execution noise with all inputs held fixed.

| Within-cell statistic across ten runs | Accuracy | Total round time |
|---|---:|---:|
| Median cell standard deviation | 1.53 pp | 0.501 s |
| 10th–90th percentiles of cell standard deviations | 0.28–3.72 pp | 0.158–3.511 s |
| Median cell max-minus-min range | 4.42 pp | 1.596 s |
| Largest cell max-minus-min range | 34.83 pp | 13.317 s |

The four-client text CS-only example shows why this matters: its mean time is **9.694 s**, but median time is **11.611 s**, and only **3/10** runs meet the illustrative 90%/11 s target. The observed timing distribution does not support designing to the favorable mean alone.

The direction of a paired change can also be less stable than its mean suggests. Across the campaign, HDH has mean time change **+0.530 s** but median **−0.013 s**, with 91 faster pairs, 88 slower, and one tie. That supports a mixed timing association, not a uniformly slower HDH configuration. Whole-campaign paired ranges also combine between-setting differences and should not be labeled within-condition noise.

**Design action:** Rank alternatives by target-attainment rate and spread in the intended setting, alongside mean accuracy/time. Where ten runs show inconsistent satisfaction of a hard requirement, collect more runs on the target runtime before committing. Recorded partition variation, host/load differences, and other randomness remain combined; this campaign does not identify their separate causes or a guaranteed deployment bound.

## Implications for the paper and traceability

The [cross-notebook feature-importance audit](fl_feature_importance_audit.md) supplies a further consistency check. Dataset/task-model is the leading accuracy feature in all eight mixed-task analyses (93.6–97.0% of normalized forest importance), and delay leads six of their timing rankings. The importance percentages quantify training predictive credit, not physical effect size or variance explained. Within fixed settings, the four-client text CS accuracy signal has a strong held-out fit (R² 0.875), agreeing with its measured accuracy loss; timing fits are weak in all three image slices and four-client text. These weak regressions limit precise timing explanations even where a broad tradeoff box has good measured STARR.

The audit also found that JSD is missing in every HDH-OFF run and observed in every HDH-ON run, so a high JSD score combines measurement availability with actual heterogeneity values. Numeric values do add predictive information in the eight-/ten-client stress fits, but a separate uncertainty effect across policies is not identified. Importance leaders persist over five forest seeds in 27/28 objective fits; that reproducibility holds training rows and pruning fixed and is not evidence of deployment stability. Finally, recorded CS thresholds are 7 in all CS-ON runs while the declarative ON binding says 2; that policy metadata needs reconciliation before reporting the setup.

The empirical contribution is a design-space explanation: **which alternatives move toward faster rounds, what accuracy is exchanged, which operating conditions support the target, how box restrictions improve conditional tradeoff robustness, and whether run variability undermines feasibility**. CS’s timing association, MC’s text timing penalty, and the HDH activity distinction are specific decision findings. Delay and non-IID rules locate conditions where targets are observed; the PRIM/CART what-if comparison measures the robustness gain and operating-space restriction associated with adopting those conditions.

All configuration means, paired means/medians/sign counts, numerical mean frontiers, illustrative target counts, and variability statistics were re-aggregated from the two compact CSVs. PRIM constraints and box metrics come from saved execution output, evaluated on held-out rows from the same campaign. What-if gains and retained support were recomputed through ADEPT's native analysis API with the executed discovery settings and checked against the saved matrices. See the [findings index](fl_notebook_findings/README.md) for metric definitions and links to every notebook. The per-notebook summaries retain the local comparisons, what-if gains, support, and numerical audit notes.
