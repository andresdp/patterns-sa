# Findings — Image task — CLIENT SELECTOR

## Scope and evidence

- **Slice:** Client Selector ON; compressor OFF; HDH OFF; client counts 4, 8, 10; all environment; all-environment view. The fixed-policy cases retain client counts 4, 8, and 10; c4/c8/c10 fix that count and include all available pattern configurations.
- **Held-out test distribution:** Test n=45: S-S 5 (11.1%), S-M 6 (13.3%), M-S 11 (24.4%), M-M 23 (51.1%).
- **Sources:** [executed notebook](../analysis-fl-rq-client_selector-image.ipynb) (sections 4–11), [box report](../boxes/boxes__task-image__client_selector-only_ON_OFF_OFF__clients-all__environment-all.md), [quality-space chart](../plots/quality-space__task-image__client_selector-only_ON_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png), and [feature-importance heatmap](../plots/feature-importance__task-image__client_selector-only_ON_OFF_OFF__clients-all__environment-all.png). The notebook contains the numeric tables; the figures provide a visual cross-check.

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

Within this policy profile M-M is most common. Do not compare its percentages directly with other configuration notebooks as if selector activation were randomized or isolated from run composition.

Feature ranking in this slice places **CPU Mean, Alpha Dirichlet Mean, Total Clients, delay_percentage, non_iid_percentage** among the highest relative predictors. This ranking describes predictive credit within the fitted model; it gives neither a direction nor an intervention effect.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

The report’s box rules are conditional on Client Selector ON (including declared strategy/criteria/value); additional CPU, alpha, client-count and delay conditions narrow the operating envelope. The recurrent top features are CPU and alpha.

**Architectural reading:** Client Selector is ON throughout this notebook (the declared resource-based policy and its criteria/value are fixed); box conditions qualify when that architecture co-occurs with an outcome. They do not compare selector ON with OFF.

**Held-out what-if comparison (Section 11):** Held out n=45. CART M-M retains 6/45, precision 1.00, coverage 6/23=26.1% (baseline 51.1%). PRIM M-M same precision/coverage. For S-S, both retain 3; 1 target (33.3% precision, 20% coverage). PRIM S-M: 3/6 targets (50%); M-S 2/3 (66.7%) but 18.2% coverage. Here, box precision is the target share among retained test runs; target coverage is the share of all target test runs retained. “Retained” is the number of all test runs satisfying the rule. Lift is the increase in target share over the unrestricted test prevalence. These are conditional filtering results, not a rerun of the FL system.

**Policy-matrix cross-check (Section 11):** The notebook also reports policy-specific tradeoff shares before and after each target box, the change matrix, target-coverage matrix, and retained counts. Read these as conditional distributions within the named policy. A displayed zero may reflect no retained/supporting observations, and `None` means no box; inspect coverage and count before interpreting either. The unrestricted `test set` rows describe observed policy distributions, not a counterfactual. The OFF/OFF/OFF row is only the baseline configuration.

## Implications

- **For practitioners:** Selector ON alone is not an adequate recipe; treat the reported CPU/alpha and environmental bounds as a joint screening hypothesis. Coverage is low for the common M-M target.
- **For researchers:** Read this as an observational, task- and slice-specific association. Compare discovery with held-out metrics in the linked report, and repeat across partition seeds or campaigns before claiming transfer.

## Limits

Only 45 held-out runs and each box retains at most six; pattern activation is confounded with run-level conditions in this observational slice. Compact client attributes are run-level averages, so within-client heterogeneity and round-level variation are hidden. Empty quadrants mean no observed runs in this slice, not infeasible outcomes. Box conditions must be read jointly; NaN/not-selected states and their parent pattern decisions are documented in the architectural interpretation linked above.
