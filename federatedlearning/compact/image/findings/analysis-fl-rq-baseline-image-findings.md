# Findings — Image task — BASELINE

## Scope and evidence

- **Slice:** OFF/OFF/OFF only; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=54: S-M 13 (24.1%), M-S 9 (16.7%), M-M 32 (59.3%); other quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-baseline-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__baseline_OFF_OFF_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

With patterns disabled, M-M is the most common observed outcome. This is a single-policy profile across client counts, not a comparison against enabled patterns.

Feature ranking in this slice places **delay_percentage, Alpha Dirichlet Mean, Total Clients, CPU Mean** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM and CART converge on delay ≤12.5% for M-S; alpha .75–.90 plus delay ≥12.5% for M-M; S-M uses alpha .60–.75, with PRIM also requiring 6–10 clients. Rules contain no enabled-pattern prescription.

**Architectural reading:** the OFF/OFF/OFF case requires no pattern prescription. The box adds an operating envelope over delay and alpha (and, for S-M, client count); it does not propose enabling a pattern.

**Held-out what-if comparison (Section 11):** Held out (n=54): for each target, PRIM/CART precision=1.00. M-S: baseline 9/54, box 9, coverage 9/9; S-M: 13/54, box 12, coverage 12/13; M-M: 32/54, box 27, coverage 27/32. Gains over prevalence are +83.3, +75.9, +40.7 percentage points. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Use delay bands as a candidate operating-envelope screen for this baseline only; alpha adds a useful M-M/S-M distinction. Validate beyond this held-out split before setting operating limits.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only 54 test runs, and the observed complete partition by rules is not a deterministic guarantee. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
