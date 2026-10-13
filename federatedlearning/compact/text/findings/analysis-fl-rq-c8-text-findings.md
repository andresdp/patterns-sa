# Findings — Text task — C8

## Scope and evidence

- **Slice:** All pattern configurations; exactly 8 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: M-S 1 (.9%), M-M 1 (.9%), L-S 23 (19.7%), L-M 92 (78.6%); others empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c8-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__all-configurations__clients-8__environment-all.md), [quality-space chart](../plots/quality-space__task-text__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__all-configurations__clients-8__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M is the dominant outcome. Pattern type groups show L-S share rising from 17% with no active types to 33% with three; L-M falls 83%→67%, but the three-type group is only 30 runs and mixtures differ.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, Client Selector Criteria, HDH Instances, Pattern Instances, CPU Mean, Pattern Types Active** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART L-S uses delay ≤12.5%; L-M combines delay ≥12.5% and CPU 10.125–10.75. M-S PRIM box is weak and target is a single held-out run.

**Architectural reading:** the common L-S/L-M rules do not add a pattern prescription; they narrow the environment using delay and, for L-M, CPU. The rare M-S box has too little support to guide design.

**Held-out what-if comparison (Section 11):** Held out: L-S CART retains 15, all target (65.2% coverage; baseline 23/117); L-M retains 66, all target (71.7% coverage; baseline 92/117). M-S PRIM retains 6 with 1 target (16.7% precision; target support 1). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Use delay as a candidate L-S/L-M divider, but do not derive a separate M-S rule from one target.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Rare M-S/M-M target regions (one run each); empty quadrants mean unobserved in this sample. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
