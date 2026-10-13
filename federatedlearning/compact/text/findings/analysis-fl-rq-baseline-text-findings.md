# Text case findings: BASELINE

## Scope and support

- **Task/configuration/client/environment:** OFF,OFF,OFF baseline; clients 4, 8, 10; all sampled environments.
- **Rows:** 180 total; 126 training; 54 held out. Split: Grouped holdout: 3/10 partition_seed groups; stratification score 0.000000. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** L-S 21 (16.7%); L-M 105 (83.3%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** L-S 9 (16.7%); L-M 45 (83.3%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Only L-S and L-M occur; seven of nine grid regions are empty. The L-S box is high accuracy/short time; L-M is high accuracy/medium time. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The all-patterns-OFF baseline allocates 83.3% of both partitions to L-M and 16.7% to L-S. Baseline cannot compare pattern choices. The fixed grid defines high accuracy as 0.7473–1.0172 and short/medium time as 1.5625–9.5065 / 9.5065–17.4505. Context is pooled over unequal client counts and sampled environments. Pattern stress is fixed at zero instances/types in this configuration. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-baseline-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Delay percentage and Alpha Dirichlet Mean lead the fitted ranking; pattern features are constant/not-selected and offer no within-baseline comparison. PRIM and CART identify both observed targets with the same held-out concentration: L-S baseline 9/54 (16.7%), box 9/9 (100%), +83.3 pp, 9/9 target coverage; L-M 45/54 (83.3%), box 45/45, +16.7 pp, 45/45 coverage. Rules partition delay: low delay (0–12.5%) aligns with L-S; delay 12.5–100% with L-M. They are operating-envelope associations; no pattern prescription can be learned in a fixed configuration. All held-out support is modest for L-S (9). No meaningful policy not-selected inference; optional pattern parameters are not selected by design. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-baseline-text.ipynb); [box report](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png).
