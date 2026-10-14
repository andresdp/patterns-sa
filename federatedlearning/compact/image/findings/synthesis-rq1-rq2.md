# Image task synthesis: RQ1 and RQ2

**Scope:** 10 executed image notebooks covering CIFAR-10/CNN 16k: three all-configuration client-count strata (4, 8, 10), three focal-pattern-ON stress views, and four fixed-policy profiles. The three client-count cases are comparable slices; fixed-policy profiles are descriptive single-policy views, not pairwise comparisons. Focal-pattern views overlap because co-enabled runs recur. Do not sum case counts as unique campaign runs. [Scope guide](../../NOTEBOOK_STRATIFICATION.md).

## RQ1 — Which tradeoffs occur, and how do design choices relate to them?

Across all-configuration client-count cases, observed outcomes occupy low/medium accuracy and low/medium time regions; high accuracy regions are unpopulated in these slices under the shared grid. At c4, the dominant held-out region is M-M (79/117), with M-S 30/117 and S-S/S-M 4 each. At c8, M-M is 62/117, S-M 31/117, M-S 18/117, S-S 6/117. At c10, M-M is 62/117, S-M 33/117, M-S 16/117, S-S 6/117. Thus c8/c10 held-out distributions are similar, while c4 has a larger M-M and M-S share; these are descriptive contrasts between client-count slices.

The baseline profile has S-M 13/54, M-S 9/54, M-M 32/54 held out. Message Compressor only has S-M 7/63, M-S 9/63, M-M 47/63. Client Selector only and HDH only show all four of S-S, S-M, M-S, M-M in training, but HDH-only has no held-out S-S or M-S runs. These single-policy profiles give outcome-space context, not evidence of policy superiority. Complete-configuration contingency tables should guide policy interpretation; marginal pattern status and pattern-count groupings pool distinct designs.

The stress analyses condition on the named pattern being ON and pool client counts plus other decisions. Their held-out region distributions differ (Client Selector stress: M-M 81/144 and M-S 37/144; compressor stress: M-M 120/180 and M-S 39/180; HDH stress: M-M 71/144 and S-M 41/144). Since these views overlap and mix policy/environment composition, this does not identify a stress effect. In every case, empty regions mean unobserved outcomes under the sampled scope, not impossible outcomes.

**Practitioner implication:** select candidate policies against the desired accuracy/time band and verify them under the intended client count and environment mix. The current evidence does not support a universal best pattern or a guaranteed feasibility boundary. **Research implication:** c8/c10 show similar held-out distributions, but box and policy-level evidence must be checked per case; the c4 contrast and profile gaps argue for scope-specific reporting.

## RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

PRIM and CART discover different joint rules by slice. Their conditions combine pattern decisions, stress or environment measures, and run-level context, with feature candidates changing by scope: client count is fixed/excluded in c4/c8/c10; pooled in profiles and stress views; the focal stress feature is retained while its paired environment alias is excluded in focal views; pattern-stress aliases and invariant predictors are excluded in profiles. Read the box reports jointly for design prescriptions, operating envelopes, observed pattern activation, and whether NaN/not-selected values are included. Feature rankings are model-relative and do not establish direction or influence.

Held-out evaluation is strongest for common regions and varies by slice. The c8/c10 all-configuration boxes frequently achieve 100% precision for M-S/M-M and useful but incomplete target coverage; c4's PRIM M-S/M-M boxes are 100% precise but retain 15 and 22 of 117 test runs and cover 50% and 28% of those targets, while its CART rules for rare S-S/S-M retain no held-out runs. Client Selector-only boxes have limited support and weak coverage for multiple targets. HDH-only S-S/M-S targets are absent from test, so these boxes are not test-evaluable there. The pooled stress views generally show high precision for M-S/M-M but incomplete coverage; compressor-stress S-S is especially unsupported (one held-out target and low box precision). Consult each case report's exact baseline, retained support, precision, change, and coverage table.

The all-run held-out summaries and policy-specific Section 11 matrices answer different questions: the former evaluate the fixed rule on all held-out rows; the latter show post-filter tradeoff membership within each policy group. A zero matrix cell can be unsupported or contain no retained runs. Box filtering is a what-if restriction over observed held-out runs, not a system intervention.

**Practitioner implication:** treat boxes as candidate joint envelopes, and prioritize those with meaningful retained support, target coverage, and stable performance across relevant scopes. **Research implication:** report grouped holdout support and coverage alongside precision; replicate rules across seeds, client counts, and workloads before transferring them. Conclusions apply to this image task's compact run-level sample and do not transfer to the text task or to client-level/round-level behavior.

## Case evidence

Each refreshed case report links its notebook, box report, and plots. The refreshed manifest records fingerprints and confirms all 10 selected notebooks, plots, and box reports are present and executed.

- [analysis-fl-rq-baseline-image findings](analysis-fl-rq-baseline-image-findings.md) — [analysis-fl-rq-baseline-image.ipynb](../analysis-fl-rq-baseline-image.ipynb)
- [analysis-fl-rq-c10-image findings](analysis-fl-rq-c10-image-findings.md) — [analysis-fl-rq-c10-image.ipynb](../analysis-fl-rq-c10-image.ipynb)
- [analysis-fl-rq-c4-image findings](analysis-fl-rq-c4-image-findings.md) — [analysis-fl-rq-c4-image.ipynb](../analysis-fl-rq-c4-image.ipynb)
- [analysis-fl-rq-c8-image findings](analysis-fl-rq-c8-image-findings.md) — [analysis-fl-rq-c8-image.ipynb](../analysis-fl-rq-c8-image.ipynb)
- [analysis-fl-rq-client_selector-image findings](analysis-fl-rq-client_selector-image-findings.md) — [analysis-fl-rq-client_selector-image.ipynb](../analysis-fl-rq-client_selector-image.ipynb)
- [analysis-fl-rq-hdh-image findings](analysis-fl-rq-hdh-image-findings.md) — [analysis-fl-rq-hdh-image.ipynb](../analysis-fl-rq-hdh-image.ipynb)
- [analysis-fl-rq-message_compressor-image findings](analysis-fl-rq-message_compressor-image-findings.md) — [analysis-fl-rq-message_compressor-image.ipynb](../analysis-fl-rq-message_compressor-image.ipynb)
- [analysis-fl-rq-stress-client_selector-image findings](analysis-fl-rq-stress-client_selector-image-findings.md) — [analysis-fl-rq-stress-client_selector-image.ipynb](../analysis-fl-rq-stress-client_selector-image.ipynb)
- [analysis-fl-rq-stress-hdh-image findings](analysis-fl-rq-stress-hdh-image-findings.md) — [analysis-fl-rq-stress-hdh-image.ipynb](../analysis-fl-rq-stress-hdh-image.ipynb)
- [analysis-fl-rq-stress-message_compressor-image findings](analysis-fl-rq-stress-message_compressor-image-findings.md) — [analysis-fl-rq-stress-message_compressor-image.ipynb](../analysis-fl-rq-stress-message_compressor-image.ipynb)
