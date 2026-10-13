# Text case findings: C10

## Scope and support

- **Task/configuration/client/environment:** All available configurations; 10 clients fixed; all sampled environments.
- **Rows:** 390 total; 273 training; 117 held out. Split: Rare-class warning disables row-label stratification; grouped holdout still keeps partition_seed groups intact (3/10 held out), chosen for best region match; stratification score 0.000032. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** M-S 1 (0.4%); M-M 2 (0.7%); L-S 57 (20.9%); L-M 213 (78.0%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** M-S 0 (0%); M-M 1 (0.9%); L-S 24 (20.5%); L-M 92 (78.6%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Four regions occur; five are empty. M-S is absent from held-out data and cannot be evaluated; M-M has one held-out run. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M dominates (78.0% train; 78.6% test), with L-S near 21%. Rare medium-accuracy regions provide little evidence. This is the fixed 10-client comparison across configurations, not a contrast with pooled configuration profiles. Stress groups summarize mixed configurations and deployment contexts; pattern type count and instance count are different grouping units. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-c10-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Delay percentage is a major predictor in the saved heatmap; model ranking is relative to this 10-client slice. Constant pattern settings cannot support within-slice effects. L-S box: held-out 15/15 precision 100%, baseline 24/117 (20.5%), +79.5 pp, coverage 15/24 (62.5%). L-M: 66/66 precision, baseline 92/117 (78.6%), +21.4 pp, coverage 66/92 (71.7%). Rules are consistent with low delay for L-S and higher delay for L-M. The single M-M held-out target is captured (1/1) by its box; this remains very weak evidence. M-S was discovered in training, but no held-out targets exist, so test metrics are unavailable. No evidence supports the empty regions. Interpret not-selected parameter states only where explicitly encoded by the box; see report. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__all-configurations__clients-10__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__all-configurations__clients-10__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-c10-text.ipynb); [box report](../boxes/boxes__task-text__all-configurations__clients-10__environment-all.md); [quality-space plot](../plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__all-configurations__clients-10__environment-all.png).
