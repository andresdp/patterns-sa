# Cross-case synthesis — Text task — RQ1 and RQ2

This synthesis crosschecks the seven individual case reports for the compact all-environment campaign. It addresses the task’s cases independently; it does not pool image and text outcomes. Case analyses: [baseline](analysis-fl-rq-baseline-text-findings.md), [c4](analysis-fl-rq-c4-text-findings.md), [c8](analysis-fl-rq-c8-text-findings.md), [c10](analysis-fl-rq-c10-text-findings.md), [client_selector](analysis-fl-rq-client_selector-text-findings.md), [hdh](analysis-fl-rq-hdh-text-findings.md), [message_compressor](analysis-fl-rq-message_compressor-text-findings.md).

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

### Recurring findings

- L-M dominates each c4/c8/c10 held-out slice (79, 92, and 92 of 117 runs); L-S is the consistent second region (31, 23, and 24). Other regions are rare or empty: c8 has one M-S and one M-M run, c10 has one M-M and no M-S. Baseline and compressor-only are similarly L-M-heavy (45/54 and 54/63).
- Delay and Alpha Dirichlet Mean recur in feature rankings. At fixed client count, Client Selector Criteria and HDH Instances also recur among leading parameters. In single-policy profiles, environmental features such as non-IID share and low-spec share rise in rank. Rankings are model-relative associations, not directions or causal levers.
- Pattern Types Active groups show L-S share increasing from about 17% in the zero-type group to 33% at c8/c10 and 43% at c4, with a corresponding L-M decline. The three-type group has only 30 runs and groups differ in complete configurations and operating conditions. This is a descriptive lead, not a pattern-count effect.

### Configuration-profile findings

- Baseline, selector-only, HDH-only, and compressor-only are different all-client-count profiles. HDH-only has 42/45 L-M while compressor-only has 54/63 L-M; neither comparison isolates what enabling that pattern does.
- In HDH-only, the 93.3% L-M starting prevalence means its box contributes only 6.7 percentage points of additional concentration. A high precision should not be mistaken for a valuable restriction when the target is already nearly universal.

### Conclusion for RQ1

For the text task, the compact evidence is dominated by L-M, with delay separating L-S from L-M across several slices. Other quadrants lack enough observations for stable conclusions. Designers can use the observed delay division to organize exploration, while researchers should prioritize data that populates rare regions and separates pattern configurations under comparable operating conditions.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

### Recurring findings

- In baseline, compressor-only, and c8/c10 all-configuration cases, PRIM and CART repeatedly recover the approximate delay boundary of 12.5%: lower delay identifies L-S, and higher delay identifies L-M. In c8/c10, the longer-delay L-M boxes also use CPU bounds. At c4, L-M rules include client selector OFF and low pattern/HDH instances, showing that the same tradeoff can require additional joint context in a different slice.
- Held-out concentration is strong for common outcomes: c8 CART retains 15/117 L-S runs (15/23 target coverage) and 66/117 L-M runs (66/92); c10 yields 15/24 and 66/92. In baseline and compressor-only, both boxes match all held-out runs in their respective target classes. These supports range from 9 to 66 and should remain visible beside precision.
- Rare-region boxes are much weaker: c8 M-S has only one target run and PRIM precision 1/6; c10 M-M has one target and PRIM precision 1/9; c4 M-S has two targets and PRIM precision 1/8. These are not actionable rules.

### Scope-specific findings and evidence gaps

- Selector-only boxes retain only 3–9 cases and capture 15–35% of target runs; the conditions are multi-variable. Use them as candidate filters for data collection or review, not deployment prescriptions.
- HDH-only illustrates why baseline prevalence matters: L-M is already 42/45 and the box retains 30, all target. Precision rises to 100%, but the rate rises only 6.7 points and coverage is 71.4%. L-L has three target runs and one is captured.
- The architectural explanation correctly converts “criteria not selected” into Client Selector OFF when supported by the system specification. Read this as context for joint box conditions, not independent feature effects. Section 11 support counts are essential; unsupported zeros/`None` do not represent proven robustness or infeasibility.

### Conclusion for RQ2

The repeated delay split is the clearest actionable result for common text-task tradeoffs. Treat it as a screening boundary for the compact campaign and validate it on new partitions. Avoid operational guidance for M-* and L-L regions until test support grows; report precision with baseline prevalence, retained count, and target coverage.

## Cross-cutting interpretation

- “All-environment” includes all available environmental conditions, not a shared/fixed environment. Fixed client-count cases and all-client-count policy profiles have different scopes and denominators.
- Box restrictions filter held-out runs. They do not rerun FL under prescribed conditions, change actual system inputs, prove causality, or establish reduced variance of continuous accuracy/time. Report baseline rate, precision, lift in percentage points, retained count, and target coverage together.
- The compact representation averages client attributes; within-client and round variation remain hidden. Findings apply to the measured run-level data and current campaign.
