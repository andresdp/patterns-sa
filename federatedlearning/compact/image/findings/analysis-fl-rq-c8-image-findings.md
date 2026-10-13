# Findings — Image task — C8

## Scope and evidence

- **Slice:** All pattern configurations; exactly 8 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: S-S 6 (5.1%), S-M 31 (26.5%), M-S 18 (15.4%), M-M 62 (53.0%); remaining quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c8-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__all-configurations__clients-8__environment-all.md), [quality-space chart](../plots/quality-space__task-image__all-configurations__clients-8__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__all-configurations__clients-8__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

M-M remains the largest region, with S-M now a substantial second region. Pattern-type groups vary non-monotonically, so the aggregate active-type count does not support a simple “more patterns, better/worse” rule.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, JSD Mean, CPU Mean, Client Selector Criteria, Pattern Instances, Pattern Types Active** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART boxes pair S-M with alpha .625–.688 and selector OFF; M-S with alpha .813–.875, delay ≤12.5%, and low/not-selected JSD; M-M with alpha .813–.875, selector OFF, and delay ≥12.5%. Architectural report shows the joint context.

**Architectural reading:** the S-M CART box prescribes Client Selector OFF, with alpha in a narrow band. The M-S box also includes low delay and low/not-selected JSD; read these as a joint environment envelope.

**Held-out what-if comparison (Section 11):** Held out: S-M baseline 31/117, CART retains 21, all target (67.7% coverage); M-S baseline 18/117, CART retains 13, all target (72.2%); M-M baseline 62/117, CART retains 33, all target (53.2%). PRIM M-S retains 9/117 (50% target coverage). CART S-S has 1 retained/1 target, only 1/6 target coverage. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Use alpha as a first segmentation variable, then test delay and selector state jointly; these screens keep moderate coverage for common regions in this slice.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Small S-S support; perfect box precision applies to one test run for CART S-S. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
