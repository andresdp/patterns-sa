# Findings — Text task — CLIENT SELECTOR

## Scope and evidence

- **Slice:** Client Selector ON; compressor and HDH OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=45: M-S 1 (2.2%), L-S 20 (44.4%), L-M 24 (53.3%); other quadrants empty.
- **Sources:** [executed notebook](../analysis-fl-rq-client_selector-text.ipynb) (sections 4–11), [box report](../boxes/boxes__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-text__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

L-M and L-S are similarly frequent. As the selector is fixed ON, the results characterize its observed profile and cannot establish the policy’s benefit.

Feature ranking in this slice places **low_spec_percentage, Alpha Dirichlet Mean, CPU Mean, Total Clients, non_iid_percentage, delay_percentage** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Boxes add multi-condition envelopes (e.g. clients, low-spec share, delay, CPU/non-IID and alpha); CART/PRIM differ in complexity. Architectural interpretation ties selector ON to its declared strategy and criteria.

**Architectural reading:** Client Selector is ON throughout (with its declared strategy/criteria/value); discovered conditions narrow clients and operating context around this fixed architecture. They do not imply selector activation is beneficial.

**Held-out what-if comparison (Section 11):** Held out n=45: L-M box retains 6, all target (25% coverage, base 24/45=53.3%). L-S CART retains 3, all target (15% coverage); PRIM retains 9 with 7 targets (77.8% precision, 35% coverage; base 44.4%). Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** The box conditions can be used to shortlist cases for review, but narrow coverage means they are not broad prescriptions. Compare PRIM’s less restrictive L-S envelope with CART.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Small held-out supports (3–9) and low target coverage; rules include several non-controllable conditions. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
