# Text case findings: CLIENT SELECTOR

## Scope and support

- **Task/configuration/client/environment:** Client Selector only (ON,OFF,OFF); all client counts (4, 8, 10); all sampled environments.
- **Rows:** 150 total; 105 training; 45 held out. Split: Grouped holdout: 3/10 partition_seed groups; stratification score 0.000277. Seeds were kept wholly in one partition.
- **Tradeoff definitions:** final validation accuracy is maximized and average total round time minimized. The shared 3×3 grid uses accuracy edges 0.2075/0.4774/0.7473/1.0172 and time edges 1.5625/9.5065/17.4505/25.3945.
- **Training region counts (all nine regions):** M-S 3 (2.9%); L-S 48 (45.7%); L-M 54 (51.4%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Held-out region counts (all nine regions):** M-S 1 (2.2%); L-S 20 (44.4%); L-M 24 (53.3%); all other cells among S-S, S-M, S-L, M-S, M-M, M-L, L-S, L-M, L-L are zero.
- **Occupancy:** Three regions populated; six empty. No L-L or low-accuracy regions occur in either partition. See notebook Section 4 / cell 18 and Section 3 / cell 14 for exact partition counts and thresholds.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The profile divides roughly evenly between high-accuracy/short-time and high-accuracy/medium-time outcomes. This is a configuration profile pooled across client counts, not a client-count-matched estimate of Client Selector effect. One M-S held-out observation is sparse. All runs have one active pattern type, while Pattern Instances vary with number of clients/deployment; do not equate one active type with one instance. Compare configurations only within the stated client scope; `Pattern Types Active` counts decisions, whereas `Pattern Instances` is a context-dependent deployment/stress descriptor. The accuracy–time plot corroborates occupancy: [quality-space plot](../plots/quality-space__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png). Notebook contingency and robustness outputs: [analysis notebook](../analysis-fl-rq-client_selector-text.ipynb) (Sections 5–7; cells 30–44).

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Client Selector Criteria / client and resource descriptors rank alongside delay and non-IID context; box rules should be read jointly. Policy itself is fixed ON, so its effect is not identifiable here. The three PRIM boxes are context rules, not selector prescriptions: M-S uses Total Clients 4–6 and non-IID 50–75% (0/3 hits; baseline 1/45, coverage 0%); L-S uses CPU Mean 8–8.875, non-IID 25–50%, and delay 25–50% (7/9 precision; baseline 20/45, +33.3 pp; coverage 7/20, 35%); L-M uses Total Clients 6–10 and low-spec 25–37.5% (6/6 precision; baseline 24/45, +46.7 pp; coverage 6/24, 25%). CART reproduces the L-S and L-M held-out rules. These are selective envelopes, not broad coverage. Optional parameter not-selected states are unavailable for the fixed Client Selector ON design where its settings apply. For target coverage and held-out policy matrices, see notebook Section 11 (cells 66–73) and [box report](../boxes/boxes__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md). The feature ranking plot is [feature-importance plot](../plots/feature-importance__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png). A box is a joint observational rule, and filtering is a what-if over already observed held-out rows.

## Implications

- **Practitioners:** Treat the reported rule as a candidate monitoring/selection envelope within this exact task and configuration/client scope. Validate on additional seeds before operational use; sparse targets and retained subsets limit confidence.
- **Researchers:** The fixed-grid occupancy and grouped seed holdout support descriptive within-slice comparisons. Policy attribution is limited by observational coverage, uneven environment composition, run-level aggregates, and rare/empty regions. Importance ranks are model-relative predictive credit, not slopes or causal effects.

## Case limitations and evidence

The compact client/resource/non-IID summaries aggregate at run level and hide client- and round-level variation. Empty grid cells mean unobserved in this sample, not infeasible. All conclusions are conditional on the sampled environments and seeds. Evidence: [analysis notebook](../analysis-fl-rq-client_selector-text.ipynb); [box report](../boxes/boxes__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md); [quality-space plot](../plots/quality-space__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance plot](../plots/feature-importance__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png).
