# Compact Federated Learning Notebook Findings

These summaries follow the analysis sequence in `ADEPT_FL_paper_analysis_spec.md`. Each states a specific observed decision–tradeoff association, the conditions and run counts supporting it, and its design implication. The six stress summaries include complete configuration comparisons and a numerical frontier of mean accuracy/time alternatives. Use continuous outcomes for comparisons between notebooks because the stress-bin edges differ.

For conclusions grouped by paper research question, see the [cross-notebook synthesis](../fl_research_question_synthesis.md).

For recurring drivers, objective-specific rankings, correlated proxies, reproducibility checks, and scoring/selection flags, see the [feature-importance audit](../fl_feature_importance_audit.md). Each notebook summary includes its own top features and the added held-out diagnostic results.

**Observation level for every summary:** This phase analyzes compact run-level results. ADEPT averages selected numeric per-client fields within a run; categorical summaries count distinct observed values. These averages hide client imbalance, combinations of conditions on the same client, and changes over rounds. A box or importance score on a mean describes the run-level summary, not each client. Usage means can cover only participating clients, so the averaging population can change with CS. Configuration outcome means average across runs and are a separate aggregation. General analysis of the detailed client/round records is deferred; the existing HDH activity counts are a limited supporting use of those logs. See [the aggregation explanation](../paper_adept_formal_extension.md#21-observation-level-compact-summaries-first).

| Order | Analysis | Summary | Notebook |
|---:|---|---|---|
| 1 | Overview — all 2,340 runs | [00-overview.md](00-overview.md) | [`analysis-fl.ipynb`](../../federatedlearning/analysis-fl.ipynb) |
| 2 | Baseline — all patterns off | [01-baseline.md](01-baseline.md) | [`analysis-fl-baseline.ipynb`](../../federatedlearning/analysis-fl-baseline.ipynb) |
| 3 | Client Selector only | [02-client-selector-only.md](02-client-selector-only.md) | [`analysis-fl-client-selector.ipynb`](../../federatedlearning/analysis-fl-client-selector.ipynb) |
| 4 | Message Compressor only | [03-message-compressor-only.md](03-message-compressor-only.md) | [`analysis-fl-message-compressor.ipynb`](../../federatedlearning/analysis-fl-message-compressor.ipynb) |
| 5 | HDH only | [04-hdh-only.md](04-hdh-only.md) | [`analysis-fl-hdh.ipynb`](../../federatedlearning/analysis-fl-hdh.ipynb) |
| 6 | Client Selector versus baseline | [05-client-selector-vs-baseline.md](05-client-selector-vs-baseline.md) | [`analysis-fl-client-selector-vs-baseline.ipynb`](../../federatedlearning/analysis-fl-client-selector-vs-baseline.ipynb) |
| 7 | Message Compressor versus baseline | [06-message-compressor-vs-baseline.md](06-message-compressor-vs-baseline.md) | [`analysis-fl-message-compressor-vs-baseline.ipynb`](../../federatedlearning/analysis-fl-message-compressor-vs-baseline.ipynb) |
| 8 | HDH versus baseline | [07-hdh-vs-baseline.md](07-hdh-vs-baseline.md) | [`analysis-fl-hdh-vs-baseline.ipynb`](../../federatedlearning/analysis-fl-hdh-vs-baseline.ipynb) |
| 9 | Pattern stress — 4 clients, image | [stress-c4-image.md](stress-c4-image.md) | [`analysis-fl-stress-c4-image.ipynb`](../../federatedlearning/analysis-fl-stress-c4-image.ipynb) |
| 10 | Pattern stress — 4 clients, text | [stress-c4-text.md](stress-c4-text.md) | [`analysis-fl-stress-c4-text.ipynb`](../../federatedlearning/analysis-fl-stress-c4-text.ipynb) |
| 11 | Pattern stress — 8 clients, image | [stress-c8-image.md](stress-c8-image.md) | [`analysis-fl-stress-c8-image.ipynb`](../../federatedlearning/analysis-fl-stress-c8-image.ipynb) |
| 12 | Pattern stress — 8 clients, text | [stress-c8-text.md](stress-c8-text.md) | [`analysis-fl-stress-c8-text.ipynb`](../../federatedlearning/analysis-fl-stress-c8-text.ipynb) |
| 13 | Pattern stress — 10 clients, image | [stress-c10-image.md](stress-c10-image.md) | [`analysis-fl-stress-c10-image.ipynb`](../../federatedlearning/analysis-fl-stress-c10-image.ipynb) |
| 14 | Pattern stress — 10 clients, text | [stress-c10-text.md](stress-c10-text.md) | [`analysis-fl-stress-c10-text.ipynb`](../../federatedlearning/analysis-fl-stress-c10-text.ipynb) |

## Cross-notebook reading

- The executed campaign has 2,340 runs, but environment support varies by configuration. Full-campaign matched contrasts use only shared task/client/environment/partition-seed support.
- `partition_seed` is matched; host, scheduling, and other unrecorded conditions are not. Treat all differences as descriptive.
- Stress-slice comparisons fix one task, client count, and the common environment point. Each has 10 runs per configuration and uses its own tradeoff bins.
- Pattern-instance stress partly depends on assumptions; see [`compact/README.md`](../../federatedlearning/compact/README.md), especially the HDH configured-versus-applied caveat.
- The campaign supports exploratory associations for RQ1–RQ3. RQ4 is limited to describing variation across the recorded seed-matched runs; this analysis does not estimate a noise floor or attribute variation to specific sources.

## What “one run for each `partition_seed`” means

Within a task × client-count × environment × configuration cell, the data have one execution for each recorded `partition_seed` from 1 through 10. The same ten seed values occur in the corresponding baseline and pattern configurations, so a comparison can pair runs with the same recorded partition seed. For example, the CIFAR-10, 4-client, common-environment baseline run with `partition_seed=1` is paired with the Client Selector run from that same task, client count, environment, and seed value. There are ten such pairs for that one configuration comparison.

This is a *seed-matched* comparison, not a claim that the two rows are the same execution. Each row has its own `run_id`; `partition_seed` denotes the data-partition seed, not a unique run and not proof that training randomness was controlled. Host and scheduling can differ between the paired rows, and any other random seeds are not shown as matched here. `repeat` duplicates the values of `partition_seed` in this campaign, so it is not a second independent replication index. The reported differences are therefore paired descriptions of observed runs, not causal effects or significance tests.

## Detail included in each summary

Accuracy differences are expressed in **percentage points (pp)**: −0.81 pp means, for example, 91.27% to 90.46%. Round-time differences are seconds; negative means ON was faster. The sign-count columns show how many matched runs actually follow that direction, rather than treating a mean as uniform behavior.

The **mean frontier** contains alternatives for which no other observed configuration has at least as high mean accuracy and at most as low mean time, with one strict advantage. It is calculated from unrounded means and considers only those two objectives. It does not establish statistical separation, account for implementation complexity, or imply that every run meets a requirement.

PRIM rules are fitted to training rows and evaluated on held-out rows from the same campaign. **Test successes / box runs** gives density: the fraction inside a rule that meets its target. **Coverage** gives the fraction of all test target cases captured by the rule. In this implementation, **lift is test density minus training target prevalence**, an absolute difference rather than a ratio. A high density supported by one or two rows is weak evidence for a design prescription. A low lift alone does not imply a poor rule when the target is already common. Decoded limits can fall between sampled levels: a client range 6–10 selects the observed 8- and 10-client runs, not an experiment at six clients.

STARR is the sample share of runs in a target tradeoff region. It describes attainment over the sampled conditions; it is distinct from repeatable satisfaction of a designer's accuracy/time requirement in one deployment setting. Pattern-instance plots also combine decisions, participation, and environment; they do not isolate a causal effect of adding an instance.

Each summary now also reports **what-if robustness** from the PRIM/CART tables: the target's unconstrained success rate, success rate inside the box, their difference in percentage points, and the retained test count/fraction. “Baseline” in those comparisons refers to the current configuration before restricting scenarios, not necessarily the all-OFF configuration. Retained scenario fraction measures the operating/design-space restriction; target coverage measures the fraction of successful target cases captured. Higher STARR establishes more consistent target membership, while continuous variance within the target is a separate measurement. A zero with no retained scenarios is unsupported rather than an observed failure rate.

The numerical recheck uses `Final Val Accuracy` and `Avg Total Round Time` from the two compact CSVs. Pairing uses task, client count, environment shares, and partition seed; the other two pattern decisions are fixed. Medians, sign counts, mean frontiers, illustrative target-attainment counts, and within-cell variability were calculated directly from those records in `perfmodels`. PRIM rules and test support come from saved notebook outputs. HDH activity comes from the detailed per-client/per-round records using the notebook's `HDH Time > 0` and participation rule. The recheck did not re-execute the notebooks.

The what-if recheck reconstructed the unrounded PRIM/CART boxes using the saved selected features and executed discovery/split settings in `perfmodels`, then computed retained support with ADEPT's native robustness API. All 14 saved baseline and box-constrained matrices were reproduced. Boundary conversion discrepancies between discovery-time evaluation and reapplication were found in [HDH versus baseline](07-hdh-vs-baseline.md) and [ten-client text](stress-c10-text.md); affected gains are flagged rather than treated as validated improvements. Notebook Section 11 now explains the meaning of the matrices, robustness gains, and both coverage measures.

Whole-campaign region percentages use all 2,340 rows; training/test percentages describe their respective splits. For example, whole-campaign `L-M` is 875/2,340 = 37.39%, whereas its training share is 612/1,638 = 37.36%. The distinction matters when quoting results in the paper.
