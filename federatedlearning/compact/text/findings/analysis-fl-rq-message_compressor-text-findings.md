# Findings — Text task — MESSAGE COMPRESSOR

## Scope and evidence

- **Slice:** Message Compressor ON; client selector and HDH OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=63: L-S 9 (14.3%), L-M 54 (85.7%); remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-message_compressor-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M dominates the compressor profile. Its two observed outcomes are perfectly split by delay in this test sample, but that does not establish a compressor effect.

Feature ranking in this slice places **delay_percentage, Alpha Dirichlet Mean, non_iid_percentage, Message Compressor Instances, CPU Mean, low_spec_percentage** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM/CART agree on delay ≤about 12.5% for L-S and ≥about 12.5% for L-M; no further pattern policy is required since compressor ON is fixed.

**Architectural reading:** Message Compressor is ON throughout; the box rules principally divide the operating envelope by delay. They do not imply compressor activation is responsible for the observed separation.

**Held-out what-if comparison (Section 11):** Both methods retain 9/63 L-S and 54/63 L-M, all target (100% precision and target coverage). Baseline prevalence is 14.3% and 85.7%; gains +85.7 and +14.3 pp. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Delay is a practical first triage variable within this compressor-enabled profile; validate the threshold before using it as a service-level rule.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only 63 test runs and two populated regions; no evidence about compressor ON versus OFF. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
