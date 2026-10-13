# Text case findings: HDH

## Scope and support

- **Task/configuration/client/environment:** HDH only (OFF,OFF,ON); all client counts (4, 8, 10); all sampled environments.
- **Rows:** 150 total; 105 training; 45 held out. Split: Grouped holdout: 3/10 partition_seed groups; stratification score 0.000622. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** M-M 3 (2.9%); L-M 96 (91.4%); L-L 6 (5.7%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** M-M 0 (0%); L-M 42 (93.3%); L-L 3 (6.7%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Three regions populated; six empty. M-M is absent from test and not evaluable. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M dominates both partitions (91.4% train; 93.3% test); L-L is a small tail. The only-pattern profile cannot establish the effect of enabling HDH compared with other configurations. No test target exists for M-M. Pattern Types Active is fixed at one, but HDH instance count varies with client count/context; it remains a stress descriptor. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-hdh-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

HDH instances and non-IID/client summary features are slice-relevant; with HDH fixed ON, this does not compare the HDH decision. Importance is predictive credit only. The L-M rule has held-out precision 100% (30/30), baseline 42/45 (93.3%), +6.7 pp, and coverage 30/42 (71.4%). L-L target is rare: 1/3 retained gives 33.3% precision, +26.7 pp over baseline 3/45 (6.7%), coverage 1/3 (33.3%). The report’s box conditions include operating/run context; use as a candidate validation envelope only. M-M was found in training but has no test targets, so held-out precision/recall are unavailable. Not-selected values for HDH settings are structurally absent under HDH ON and cannot be generalized to HDH OFF. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-hdh-text.ipynb); [box report](../boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).
