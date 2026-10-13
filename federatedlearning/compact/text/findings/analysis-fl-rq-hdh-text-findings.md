# Findings — Text task — HDH

## Scope and evidence

- **Slice:** HDH ON; client selector and compressor OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=45: L-M 42 (93.3%), L-L 3 (6.7%); remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-hdh-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The sample is overwhelmingly L-M. This high starting prevalence limits the practical value of a box that only isolates the same common outcome.

Feature ranking in this slice places **non_iid_percentage, Alpha Dirichlet Mean, JSD Mean, Total Clients, delay_percentage, CPU Mean, low_spec_percentage** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM/CART L-M rule reduces to clients ≥6; L-L uses a narrow delay/client/JSD envelope and is weak. HDH is ON throughout, so these are conditional associations.

**Architectural reading:** HDH is ON throughout. The L-M rule adds only a client-count bound; the L-L rule adds delay, client-count, and JSD conditions, but rests on three targets.

**Held-out what-if comparison (Section 11):** L-M: box retains 30/45, all target, 30/42=71.4% coverage; baseline already 93.3%, so absolute prevalence gain is only 6.7 pp. L-L retains 3 with 1 target (33.3% precision, 33.3% coverage; baseline 3/45). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Do not add a complex control for L-M based on a small +6.7 pp concentration gain. The L-L condition is exploratory only.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only three L-L targets; high base prevalence makes precision alone misleading. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
