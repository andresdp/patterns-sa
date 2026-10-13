# Findings — Image task — MESSAGE COMPRESSOR

## Scope and evidence

- **Slice:** Message Compressor ON; client selector and HDH OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=63: S-M 7 (11.1%), M-S 9 (14.3%), M-M 47 (74.6%); S-S empty.
- **Sources:** [executed notebook](../analysis-fl-rq-message_compressor-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__message_compressor-only_OFF_ON_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

M-M dominates the compressor-only profile, while the observed small-time quadrants are M-S and S-M. This is a profile within available data, not a compressor effect estimate.

Feature ranking in this slice places **delay_percentage, Message Compressor Instances, Alpha Dirichlet Mean, non_iid_percentage, CPU Mean, low_spec_percentage** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Both methods find M-S with delay ≤about 12.5%, M-M with delay ≥about 12.5% and alpha .75–.90, and S-M with higher compressor-instance bounds plus alpha .60–.75 and longer delay.

**Architectural reading:** Message Compressor is ON throughout this profile; boxes add delay/alpha and, for S-M, compressor-instance conditions. They qualify the enabled configuration rather than estimate the compressor’s effect.

**Held-out what-if comparison (Section 11):** Held out n=63: M-S box retains 9/63, precision 1.00, coverage 9/9; M-M retains 45/63, precision 1.00, coverage 45/47=95.7%; S-M retains 6/63, precision 1.00, coverage 6/7=85.7%. Baseline rates are 14.3%, 74.6%, 11.1%; lifts +85.7, +25.4, +88.9 pp. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** For this compressor profile, delay is a useful first screen; for M-M also verify alpha, and for S-M check compressor instance count. Validate the thresholds in a new partition.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

S-S absent in 63 test rows. High box coverage is promising within this specific profile, but remains sample-bound. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
