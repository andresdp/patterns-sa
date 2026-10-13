# Findings — Image task — C4

## Scope and evidence

- **Slice:** All pattern configurations; exactly 4 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: S-S 4 (3.4%), S-M 4 (3.4%), M-S 30 (25.6%), M-M 79 (67.5%); remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c4-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__all-configurations__clients-4__environment-all.md), [quality-space chart](../plots/quality-space__task-image__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__all-configurations__clients-4__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

M-M dominates this slice. Among Pattern Types Active groups, M-S share rises from 17% at 0 active types to 47% at 3, while M-M falls from 77% to 53%; the 3-type group has only 30 runs. This is an association across configurations, not a pattern-count effect.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, Client Selector Criteria, CPU Mean, JSD Mean, Pattern Instances, Pattern Types Active** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART M-S uses delay ≤12.5%; its M-M box includes selector OFF/not-selected, delay ≥37.5%, low JSD, and alpha .688–.875. PRIM and CART both find M-S and M-M boxes, but S-M rules differ and are weak. See architectural descriptions in report.

**Architectural reading:** for the representative M-M CART box, Client Selector is OFF (the selector criteria is not selected); the operating envelope additionally constrains delay, JSD, and alpha. For M-S, the prescription is not a selector change: the key condition is low delay.

**Held-out what-if comparison (Section 11):** For M-S: CART box has 15/117 retained, precision 1.00, coverage 15/30=50%; PRIM retains 6, all 6 target (20%). M-M: each retains 6, all target, but only 6/79=7.6% target coverage. S-S PRIM: 4/6 retained are target (66.7%), coverage 4/4; S-M PRIM precision 16.7%, coverage 1/4. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Treat the fast-delay M-S envelope as a candidate; M-M boxes capture very little of the prevalent target, so do not use them as a broad configuration recipe. Check selector OFF only as part of the joint box.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Several boxes have 1–6 retained test runs; nominally perfect precision is fragile. Sparse S-S/S-M regions. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
