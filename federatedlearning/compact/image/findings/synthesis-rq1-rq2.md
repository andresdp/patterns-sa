# Cross-case synthesis — Image task — RQ1 and RQ2

This synthesis crosschecks the seven individual case reports for the compact all-environment campaign. It addresses the task’s cases independently; it does not pool image and text outcomes. Case analyses: [baseline](analysis-fl-rq-baseline-image-findings.md), [c4](analysis-fl-rq-c4-image-findings.md), [c8](analysis-fl-rq-c8-image-findings.md), [c10](analysis-fl-rq-c10-image-findings.md), [client_selector](analysis-fl-rq-client_selector-image-findings.md), [hdh](analysis-fl-rq-hdh-image-findings.md), [message_compressor](analysis-fl-rq-message_compressor-image-findings.md).

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

### Recurring findings

- In the three client-count-specific all-configuration slices, M-M is the largest held-out region (c4: 79/117; c8/c10: 62/117 each). M-S is more prominent at c4 (30/117) than c8 (18/117) or c10 (16/117); S-M is substantial at c8/c10 (31 and 33 runs). This is a shift in the observed distribution across separate slices, not evidence that client count alone explains it.
- Alpha Dirichlet Mean and delay recur near the top of importance rankings at c4/c8/c10. Their repeated predictive relevance makes them sensible first variables for tradeoff exploration; their ranks do not imply that changing either variable will move outcomes in a specified direction.
- Pattern Types Active summaries are not a stable dose-response: M-S share rises across groups at c4, but the c8/c10 patterns are mixed. The three-active-type group has only 30 runs versus 60/170/130 in the 0/1/2 groups, and groups mix different complete configurations and operating conditions.

### Configuration-profile findings

- The OFF/OFF/OFF, selector-only, HDH-only, and compressor-only notebooks are distinct all-client-count profiles. They are not randomized or matched comparisons of activating a pattern. For example, the image HDH-only test slice contains only S-M/M-M; compressor-only is 47/63 M-M. These differences motivate follow-up comparisons but do not isolate pattern effects.
- Among those single-policy profiles, the outcome distributions suggest candidate contexts for further evaluation: HDH-only concentrates on medium-time outcomes; compressor-only on M-M. Baseline includes S-M/M-S/M-M. None establishes an inherent feasibility boundary.

### Conclusion for RQ1

The compact campaign shows populated tradeoff regions and repeated association of Alpha Dirichlet Mean and delay with outcomes. Which regions dominate varies by client-count slice and fixed configuration profile. Designers can use these variables to structure exploration, while researchers should treat pattern count and client count as strata requiring controlled or repeated comparison, not causal explanations.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

### Recurring findings

- Across c4/c8/c10, held-out rules repeatedly use alpha, delay, and sometimes selector state to identify common tradeoffs. A low-delay envelope (about ≤12.5%) recurs for M-S in baseline, c4, and c10, and for M-S at c8 with additional joint alpha/JSD bounds. M-M rules generally combine higher alpha with longer delay, with additional selector/CPU restrictions varying by slice.
- The what-if tables show useful concentration with materially different coverage. At c8, CART boxes retain 21/117 S-M runs with 100% precision and 21/31 target coverage; M-S retains 13/117 with 13/18 coverage; M-M retains 33/117 with 33/62 coverage. At c4, the M-M box also reaches 100% precision but captures only 6/79 targets (7.6%). A perfect precision number alone hides this severe coverage loss.
- The compressor-only profile has the strongest broad held-out concentration: PRIM and CART capture 45/47 M-M, 9/9 M-S, and 6/7 S-M, each at 100% precision. The evidence is still conditional on that profile and its 63-run test set.

### Scope-specific findings and evidence gaps

- c4’s S-S/S-M targets and single-pattern S-S boxes are sparse; several boxes retain just 1–6 runs. Treat high precision as fragile. In HDH-only, S-M starts at 55.6% prevalence and the box raises it to 95% with 76% coverage; M-M box quality differs between PRIM and CART.
- Architectural explanations add parent policy context (e.g., selector OFF when criteria are not selected) and separate design prescription from the operating envelope. Their syntax makes a joint rule understandable; it does not establish causal mechanism.
- The Section 11 matrix should be read with coverage and retained count: a zero can mean no supported observations in that cell, while `None` indicates no box. Neither means a measured zero-risk or impossible region. The table compares filtered membership within held-out data, not a system rerun or lower continuous-outcome variance.

### Conclusion for RQ2

ADEPT can expose compact, interpretable operating envelopes that enrich tradeoff purity, but the useful design depends on the purity–coverage balance. For common image-task regions, start with delay and alpha and preserve selector conditions as joint context. Require a minimum retained count and target coverage before recommending any box; sparse quadrants need more runs and repeated partitions.

## Cross-cutting interpretation

- “All-environment” includes all available environmental conditions, not a shared/fixed environment. Fixed client-count cases and all-client-count policy profiles have different scopes and denominators.
- Box restrictions filter held-out runs. They do not rerun FL under prescribed conditions, change actual system inputs, prove causality, or establish reduced variance of continuous accuracy/time. Report baseline rate, precision, lift in percentage points, retained count, and target coverage together.
- The compact representation averages client attributes; within-client and round variation remain hidden. Findings apply to the measured run-level data and current campaign.
