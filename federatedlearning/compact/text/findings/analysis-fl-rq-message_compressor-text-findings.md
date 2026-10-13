# Text case findings: MESSAGE COMPRESSOR

## Scope and support

- **Task/configuration/client/environment:** Message Compressor only (OFF,ON,OFF); all client counts (4, 8, 10); all sampled environments.
- **Rows:** 210 total; 147 training; 63 held out. Split: Grouped holdout: 3/10 partition_seed groups; stratification score 0.000000. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** L-S 21 (14.3%); L-M 126 (85.7%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** L-S 9 (14.3%); L-M 54 (85.7%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Only two regions populated; seven empty. L-M is the majority. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The profile is 85.7% L-M and 14.3% L-S in both partitions. This describes Message Compressor ON across the sampled client counts and contexts; no OFF comparison is present, so it is not a pattern effect estimate. Pattern Types Active is one throughout; Message Compressor Instances varies across client counts and context and should not be treated as assigned pattern dose. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-message_compressor-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Delay is the main differentiator for these regions; Alpha Dirichlet Mean and client/resource descriptors also appear in feature ranking. Compressor policy and algorithm are fixed, so their scores cannot establish effects. PRIM and CART partition on delay: L-S at 0–12.5% delay and L-M at 12.5–100%. Each held-out box is pure and complete: L-S 9/9 precision, baseline 9/63 (14.3%), +85.7 pp, 9/9 coverage; L-M 54/54, baseline 54/63 (85.7%), +14.3 pp, 54/54 coverage. Agreement is strong within this slice but the held-out set repeats the same broad split and covers only the observed seed groups. No box should be read as requiring compression: it is fixed ON by sample selection; architecture explanation reports no policy inference from the environmental rule. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-message_compressor-text.ipynb); [box report](../boxes/boxes__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.png).
