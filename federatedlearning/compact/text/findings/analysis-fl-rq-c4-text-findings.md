# Findings — Text task — C4

## Scope and evidence

- **Slice:** All pattern configurations; exactly 4 clients; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=117: M-S 2 (1.7%), M-M 0, L-S 31 (26.5%), L-M 79 (67.5%), L-L 5 (4.3%); S-S/S-M/S-L/M-L empty.
- **Sources:** [executed notebook](../analysis-fl-rq-c4-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__all-configurations__clients-4__environment-all.md), [quality-space chart](../plots/quality-space__task-text__all-configurations__clients-4__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__all-configurations__clients-4__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M dominates. In Pattern Types Active groups, L-S share increases from 17% (zero active types) to 43% (three active); L-M declines 83%→57%; three-type stratum has only 30 runs. This mixes configurations and is not a dose-response result.

Feature ranking in this slice places **Alpha Dirichlet Mean, delay_percentage, Client Selector Criteria, HDH Instances, CPU Mean, Pattern Instances, Pattern Types Active** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

CART L-S uses delay ≤12.5%; L-M combines longer delay, Client Selector OFF/not-selected, low pattern instances and low HDH instances. L-L boxes are sparse and PRIM/CART rules differ.

**Architectural reading:** the representative L-M CART box includes Client Selector OFF/not-selected plus delay and low pattern/HDH-instance bounds. L-S is identified mainly by its lower-delay operating envelope.

**Held-out what-if comparison (Section 11):** Held out: L-S CART 15 retained, all target (48.4% target coverage; baseline 31/117). L-M CART 45, all target (57.0%; baseline 79/117). PRIM L-L covers all five targets but only 5/12 retained are target (41.7% precision); CART has 3/3 target but captures 3/5 (60%). M-S PRIM: 1/8 precision, 1/2 target coverage. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Use delay for L-S screening and the joint OFF/operating conditions for L-M as hypotheses; do not operationalize L-L/M-S rules without more data.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

L-L and M-S have only 5 and 2 target test observations, so apparent high coverage or precision is unstable. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
