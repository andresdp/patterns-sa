# Findings — Image task — C10

## Scope and evidence

- **Slice:** All pattern configurations; exactly 10 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: S-S 6 (5.1%), S-M 33 (28.2%), M-S 16 (13.7%), M-M 62 (53.0%); remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c10-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__all-configurations__clients-10__environment-all.md), [quality-space chart](../plots/quality-space__task-image__all-configurations__clients-10__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__all-configurations__clients-10__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

M-M and S-M are common, while M-S is less frequent than at c4. Pattern-type stratification is mixed: M-S rises from 17% (0 types) to 33% (3), but S-M and M-M also shift; the 3-type group is n=30.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, CPU Mean, Client Selector Criteria, JSD Mean, Pattern Instances, Pattern Types Active** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART: M-S pairs delay ≤12.5% with alpha .825–.90; S-M pairs alpha .60–.825 with selector OFF; M-M pairs delay ≥12.5%, alpha .825–.90 and CPU 10.25–11. Report provides full policy context.

**Architectural reading:** the S-M CART box prescribes Client Selector OFF with alpha bounds. The M-M box adds an operating envelope over delay, alpha, and CPU; it does not prescribe changing those observed conditions.

**Held-out what-if comparison (Section 11):** Held out: M-S baseline 16/117, box 15, all target (93.8% coverage); S-M baseline 33, box 27, all target (81.8%); M-M baseline 62, box 45, all target (72.6%). For S-S, CART retains 3 with only 1 target (33.3% precision, 16.7% coverage); PRIM retains 6 with 3 target (50%, 50%). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** For common regions, screen by the observed alpha/delay combination and verify selector/CPU conditions before considering a configuration. Keep S-S exploratory.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Rare S-S box is not precise; box conditions and measured input envelope are observational. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
