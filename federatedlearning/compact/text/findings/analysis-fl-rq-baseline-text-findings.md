# Findings — Text task — BASELINE

## Scope and evidence

- **Slice:** OFF/OFF/OFF only; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=54: L-S 9 (16.7%), L-M 45 (83.3%); other quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-baseline-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

For this baseline profile, L-M dominates and L-S is the only other observed outcome. The exact held-out split is a compact-sample result, not a general deterministic boundary.

Feature ranking in this slice places **delay_percentage, non_iid_percentage, Total Clients, low_spec_percentage, Alpha Dirichlet Mean, CPU Mean** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM and CART agree on a simple split: delay ≤about 12.5% for L-S, delay ≥about 12.5% for L-M. No pattern prescription is required.

**Architectural reading:** OFF/OFF/OFF is the fixed design prescription. The learned distinction is an operating envelope split by delay; no pattern activation is required.

**Held-out what-if comparison (Section 11):** Both rules retain exactly the target observations in this test partition: L-S 9/54 and L-M 45/54, 100% precision and 100% target coverage; prevalence/gain are 16.7%/+83.3 pp and 83.3%/+16.7 pp. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Use the delay threshold as an initial triage rule for the baseline configuration, then validate at other client counts and partitions.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only 54 test runs; a perfect split here should not be treated as a deployment guarantee. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
