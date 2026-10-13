# Text case findings: C8

## Scope and support

- **Task/configuration/client/environment:** All available configurations; 8 clients fixed; all sampled environments.
- **Rows:** 390 total; 273 training; 117 held out. Split: Grouped holdout: 3/10 partition_seed groups; stratification score 0.000034. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** M-S 4 (1.5%); M-M 1 (0.4%); L-S 53 (19.4%); L-M 215 (78.8%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** M-S 1 (0.9%); M-M 1 (0.9%); L-S 23 (19.7%); L-M 92 (78.6%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Four regions occur; five regions are empty. L-M dominates; M-S and M-M are single-digit targets and unstable for evaluation. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

Across configurations, L-M accounts for 78.8% train and 78.6% test; L-S is 19.4% and 19.7%. The two medium-accuracy regions total only five training and two held-out runs. OFF,OFF,ON is deterministic in L-M; M-M occurs exclusively in one composite configuration but only one training and one test observation, so this is fragile support, not a reliable design rule. Pattern-count groups are broad mixtures; counts by 0 versus 1 versus 2–3 types show L-M dominant throughout. Instance counts include 12/14 outlying observations; interpret as stress/context. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-c8-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Delay has strongest association with time objective in feature ranking; Alpha Dirichlet Mean is strongest for accuracy. This is predictive credit in this eight-client slice. Alpha Dirichlet Mean and delay percentage dominate model-relative importance, followed by Client Selector Criteria and HDH/pattern-instance descriptors. For L-S, the delay ≤12.5% box achieves held-out precision 100% (15/15), captures 15/23 targets (65.2%), +80.3 pp over 23/117 baseline. L-M rule yields 66/66 (100%) and captures 66/92 (71.7%), +21.4 pp. M-S has only one held-out target and one hit/6 retained (precision 16.7%, coverage 100%); M-M also has one test target but its discovered rule retains 6 and captures zero, so test precision is 0% and coverage 0%, signaling poor stability. L-L is unpopulated and has no discovery box. Report box-specific NaN coverage from box report; policy activation summaries show boxes can include OFF states. No rule should imply pattern ON absent an explicit decision binding. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-c8-text.ipynb); [box report](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md); [quality-space plot](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png).
