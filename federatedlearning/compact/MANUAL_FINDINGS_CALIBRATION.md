# Manual Notebook Findings Calibration Guide

This guide records a repeatable way to manually analyze related compact-campaign notebooks before changing the `adept-compact-findings` skill. The goal is to establish concrete examples of useful findings for Federated Learning (FL) practitioners and software architecture researchers. The analysis should be grounded in the executed notebooks, generated plots, box reports, and the scopes recorded in [`NOTEBOOK_STRATIFICATION.md`](NOTEBOOK_STRATIFICATION.md).

## Purpose

Use manual analysis to establish what a clear, data-driven finding looks like for each research question (RQ), how notebook evidence supports it, and what practical or research action follows. These reviewed examples become calibration cases for improving the analysis skill. Do not begin by rewriting all generated findings; first establish the method on a few related notebook groups, including cases where evidence is weak or conflicting.

## Analyze notebook families as comparisons

Use the stratification tree to select a related family, then document what varies and what remains fixed across its notebooks. Current families include:

- all configurations at each client count;
- isolated stress levels for one pattern;
- combined pattern configurations at a shared stress level; and
- individual configuration profiles.

Treat a notebook as a filtered observational view, not as an independent experiment by default. Before comparing cases, verify their filters, overlap, outcome definitions, partitions, and support. Draw conclusions only at the scope supported by those cases.

## Evidence-to-insight workflow

For every candidate finding, keep these five parts distinct:

1. **Observation:** State the directly reported evidence: counts and denominators, quadrant allocation, objective ranges, feature ranks, box conditions, or box metrics. Cite the notebook section or generated artifact.
2. **Comparison:** Name the comparator and verify it is meaningful for the claim. Prefer comparisons within the same notebook family and scope. State when client count, environment, policy composition, or sample support also differs.
3. **Interpretation:** Explain what the observed association suggests about the behavior of the architectural alternatives. Do not turn feature rank or a box condition into an independent effect.
4. **Evidence limit:** Record sparse support, empty regions, train/held-out differences, missing values, overlap, or other constraints that could change the interpretation.
5. **Action:** State a concrete practitioner or researcher next step that follows from the evidence, such as a configuration to evaluate, operating condition to monitor, comparison to run, or causal hypothesis to test.

Avoid standalone domain advice. Each action should be traceable to the observation and comparison that motivate it.

## Keep RQ1 and RQ2 distinct

### RQ1: observed objective-space behavior

1. Establish the semantic preference for each outcome from its meaning and units before interpreting quadrant occupancy. For example, higher validation accuracy and lower response time are preferred in the current FL campaign.
2. Check the notebook's actual quadrant definitions and occupancy. Report the preferred quadrant even when it is empty; an empty quadrant means no observed rows in that filtered sample, not impossibility.
3. Describe how complete configurations are allocated across occupied quadrants using counts and within-configuration denominators. Distinguish these allocations from feature-importance results or marginal summaries.
4. Compare patterns, stress levels, or client counts only within a suitable family and report relevant differences in environment and support.
5. Conclude with the observed tradeoff, its scope, and the next comparison or experiment that would resolve an evidence gap.

### RQ2: predictive value of joint box rules

1. Start from a target quadrant justified by RQ1 and check its full, discovery, and held-out support.
2. Use feature importance to identify candidates for inspection. Check whether highly ranked features recur across related notebooks and whether expected FL variables are low-ranked, absent, constant, aliased, or unstable across scopes.
3. Interpret each box as a conjunction of architectural decisions/settings and operating conditions. Use its architectural explanation to recover pattern activation and related context; do not read conditions independently.
4. Report discovery and held-out metrics with denominators, including target prevalence, precision, recall/coverage, lift, and retained support when available. Explain what changes under the box relative to the unrestricted partition. A missing held-out target means validation is unavailable, not that recall is zero.
5. Translate useful rules into candidate design guidance or an experiment to run. Phrase them as observed predictive associations. They can motivate causal hypotheses but do not establish that imposing a rule causes the target or reduces continuous outcome variance.

## Cross-case consistency labels

When synthesizing a family, assign each proposed claim one of these labels:

- **Repeated across cases:** the same relationship appears in multiple comparable notebooks with meaningful support.
- **Scope-dependent:** the relationship appears only under stated filters or its strength/direction varies across comparable scopes.
- **Contradicted:** comparable cases show materially different or opposite evidence.
- **Not assessable:** support, missing data, or unavailable evaluation prevents a conclusion.

Do not call a finding repeated merely because notebooks share a feature name or visual pattern. Check the actual counts, conditions, metrics, and denominators in each case.

## Calibration worksheet

For each manually reviewed notebook family, record:

| Field | What to capture |
|:---|:---|
| Family and scope | Notebook paths, filters, overlap, and fixed/varying dimensions |
| RQ1 evidence | Preferred target, occupied quadrants, counts/shares, configuration allocation |
| RQ2 evidence | Target support; feature-rank candidates; selected boxes and joint conditions; discovery and held-out metrics |
| Strongest finding | One or two claims, each tied to a specific observation and comparator |
| Consistency label | Repeated, scope-dependent, contradicted, or not assessable, with supporting cases |
| Evidence limit | The specific support, split, confounding, or scope issue that bounds the claim |
| Action | A practitioner decision to evaluate or a researcher follow-up experiment/hypothesis |
| Wording to reuse or avoid | A short example showing what is crisp and evidence-led, or what became vague |

Keep at least one calibration case with inconclusive or conflicting evidence. The skill must learn when to qualify or withhold a conclusion, not only how to write positive results.

## Criteria for a useful finding

A finding is ready to reuse as a calibration example when a reader can answer:

- What exactly was observed, in which notebook scope, and with what denominator?
- Compared with what?
- What does the evidence suggest about the behavior of the design alternatives?
- What could make that interpretation unreliable or narrower than it sounds?
- What should a practitioner or researcher do next because of this result?

If any answer is missing, improve the evidence record before polishing the prose. After several reviewed families provide examples for both RQs, use those examples to revise and test the analysis skill.
