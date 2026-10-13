# Findings — Image task — HDH

## Scope and evidence

- **Slice:** HDH ON; client selector and compressor OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=45: S-M 25 (55.6%), M-M 20 (44.4%); S-S and M-S empty.
- **Sources:** [executed notebook](../analysis-fl-rq-hdh-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__hdh-only_OFF_OFF_ON__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

Only the two medium-time regions occur in this sample. That is a useful profile boundary, not evidence that HDH makes other outcomes impossible. JSD and delay head the feature ranking.

Feature ranking in this slice places **JSD Mean, delay_percentage, Total Clients, Alpha Dirichlet Mean, HDH Instances, CPU Mean** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Both algorithms identify S-M and M-M boxes using joint JSD/other operating conditions; the policy is already fixed as HDH ON, and boxes add qualification rather than establish an HDH effect.

**Architectural reading:** HDH is ON throughout this profile; the boxes add JSD and other operating-envelope bounds. They qualify HDH-enabled runs, rather than prescribing whether HDH should be enabled.

**Held-out what-if comparison (Section 11):** S-M: both algorithms retain 20/45, precision 19/20=95%, coverage 19/25=76% (baseline 55.6%; +39.4 pp). M-M: PRIM retains 3 with 2 targets (66.7%, 10% coverage); CART retains 8 all target (100%, 40% coverage; baseline 44.4%). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** For the frequent S-M region, evaluate the repeated JSD envelope with HDH enabled. M-M guidance is algorithm-dependent; compare CART and PRIM conditions before operational use.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only 45 test rows; the M-M box is sensitive to algorithm and captures at most 40% of its target. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
