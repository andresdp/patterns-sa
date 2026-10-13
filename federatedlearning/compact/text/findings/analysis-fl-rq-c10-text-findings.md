# Findings — Text task — C10

## Scope and evidence

- **Slice:** All pattern configurations; exactly 10 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: M-M 1 (.9%), L-S 24 (20.5%), L-M 92 (78.6%); M-S and remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c10-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__all-configurations__clients-10__environment-all.md), [quality-space chart](../plots/quality-space__task-text__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__all-configurations__clients-10__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M dominates. L-S share is about 17% with no active pattern types and 33% with three; 3-type stratum n=30. Since configuration and environment mix across groups, this association does not isolate pattern count.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, Client Selector Criteria, JSD Mean, Pattern Instances, CPU Mean, HDH Instances** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART agrees on delay ≤12.5% for L-S and delay ≥12.5% plus CPU 10.25–11 for L-M. M-M is a single held-out target and its PRIM box is low precision.

**Architectural reading:** the L-S/L-M rules are operating-envelope screens over delay and CPU, with no supported policy change implied. M-M is too rare for a usable prescription.

**Held-out what-if comparison (Section 11):** Held out: L-S CART retains 15/117, all target (15/24 = 62.5% coverage; baseline 20.5%); L-M retains 66, all target (66/92 = 71.7%; baseline 78.6%). M-M PRIM retains 9 with 1 target (11.1% precision; target support 1). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** For common L-S/L-M outcomes, screen by delay, then assess CPU in the longer-delay envelope. Do not use the M-M rule operationally yet.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

M-M one target; perfect precision for common targets applies only to selected boxes in this held-out sample. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
