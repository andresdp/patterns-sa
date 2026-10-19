# ADEPT Analysis Guidelines for RQ1 and RQ2

This document records a reusable way to analyze design alternatives and discovered scenario boxes with ADEPT. It separates domain-independent interpretation rules from the domain knowledge used to interpret a particular study. The current examples refer to the compact Federated Learning (FL) campaign, but the ADEPT guidance is intended to transfer to other domains.

## Analysis purpose

The analysis serves software architecture researchers and practitioners. It should help them understand which quality tradeoffs appear in the observed design space, how complete architectural configurations are distributed across those tradeoffs, and whether a joint rule over decisions and operating conditions identifies a useful subset of runs for a target tradeoff.

The analysis is observational, but scenario discovery is predictive: PRIM/CART search for joint constraints associated with a target tradeoff, then the held-out partition checks whether those constraints continue to identify it within the campaign. The resulting architectural rules can guide decisions and motivate causal hypotheses. They do not by themselves identify causal effects or guarantee behavior beyond the studied data.

## Two complementary knowledge layers

### ADEPT-agnostic interpretation

This layer explains how to read objective spaces, feature rankings, and boxes regardless of application domain. It covers outcome preference, occupancy, denominators, feature roles, discovery and held-out evidence, and the limits of a box-based what-if.

### Domain knowledge

This layer defines what each outcome means, which direction is preferred, which variables are decisions or operating conditions, and what mechanisms domain experts expect. Expectations are hypotheses to compare with observed patterns; they are not substitutes for evidence and should not be presented as causal conclusions.

## RQ1 — Describe the observed objective space

RQ1 asks which tradeoffs occur and how architectural decisions relate to them. Its primary evidence is the objective-space plot and the tables that allocate runs to outcome regions and complete configurations.

### 1. Establish outcome semantics and preference

Before inspecting which regions contain points:

1. Name each measured outcome, unit, transformation, and interpretation.
2. Establish its preference direction from the domain semantics or an explicitly stated stakeholder goal. For example, higher predictive accuracy is preferred, while lower latency or response time is preferred.
3. Read the region/bin definitions and axis ordering from the current notebook. Do not infer preference from labels such as `S`, `M`, or `L`; those labels identify numeric ranges and are not quality ratings.
4. Define the semantically preferred region or target set before examining its occupancy. If stakeholders accept more than one tradeoff, state the acceptable set and rationale explicitly.

For the current FL compact campaign, final validation accuracy is maximized and average total round time is minimized. Thus, on the notebook's accuracy-by-time grid, high accuracy paired with low time is the strict semantic preference (labelled `L-S` in the current grid). This preference follows from outcome meaning, not from whether a particular notebook contains `L-S` observations.

### 2. Check the notebook's actual occupied regions

After defining preference, inspect the actual grid and its region-count table for that notebook and scope:

- Report the count and share in every region, including zero-count regions, with the analyzed denominator.
- Distinguish the **preferred target** from the **observed occupied regions**. If the preferred region is empty, report it as desired but unobserved in that sample. Do not relabel another occupied region as the preferred target merely because it has points.
- An empty region means no observations in the selected data; it does not show that the outcome is impossible or infeasible.
- If an alternate target is useful for RQ2, define it as a secondary acceptable tradeoff using domain or stakeholder rationale, and name it explicitly. Do not let observed occupancy alone determine desirability.
- Confirm the current notebook's axis order and label construction. For example, `L-S` means high accuracy and low time only when the first label is accuracy and the second is time.

The preferred target may therefore differ from notebook to notebook in *availability*, but not in semantic meaning when the objective definitions and grid are shared. An unoccupied preferred target is an evidence gap for scenario discovery: a box cannot be learned for a target with no examples in that slice. State this directly rather than treating the absence as a negative finding about the architecture.

### 3. Describe occupancy and configuration allocation

For each notebook:

1. State scope, sample size, denominator, and which regions are populated or empty.
2. Describe the point distribution using counts and proportions, not visual density alone; repeated runs can make a region look dense.
3. Allocate outcomes to **complete architectural configurations** using within-configuration denominators. Keep this distinct from marginal summaries such as the number of enabled pattern types, pattern instances, or one decision considered alone.
4. Identify varying and fixed dimensions, including task/model, client count, stress level, and sampled operating conditions as applicable. Note where groups differ in composition or have sparse support.
5. Describe observed associations. Do not attribute a difference to one policy if the groups also differ in environment, client count, support, or other recorded conditions.

### 4. Optional contingency analysis

Counts and within-group proportions are the baseline evidence. When useful and supported, add contingency measures to characterize how configuration membership and tradeoff regions are associated. Name the measure, its comparison groups, and denominator; inspect sparse and zero cells before interpreting it. These measures can summarize association or concentration, but they do not establish a causal policy effect.

### RQ1 conclusion format

A concise RQ1 conclusion should state:

- the semantically preferred/acceptable region(s) and how they follow from outcome meaning;
- which of those regions are occupied in the notebook, with counts and denominators;
- how complete configurations are allocated across occupied regions;
- which context variables may complicate the comparison; and
- the practical next step or evidence gap, especially when a preferred region is empty or sparsely represented.

## RQ2 — Assess boxes for a selected target tradeoff

RQ2 asks which joint constraints on architectural decisions and operating conditions predict membership in a target tradeoff, and how well those rules identify the target on held-out campaign observations. RQ2 follows the target selection made for RQ1. It must not silently switch targets because another region has more examples.

### 1. Confirm that the target is observable in the slice

For each target region selected from RQ1, report its full-sample, training, and held-out support. If there are no examples in a partition, say that evaluation is unavailable there. A target with zero held-out examples has no held-out recall/coverage estimate; this is not zero recall.

### 2. Use feature importance as candidate screening

Describe feature importance as model-relative predictive credit for the analyzed slice. Check:

- which variables rank highly and whether they recur across relevant notebooks;
- whether expected domain variables are low-ranked, absent, constant, or highly correlated with another variable;
- whether a rank changes when the analysis scope changes; and
- whether the feature is a decision, operating context, outcome-derived field, identifier, or other descriptor according to the system model.

Importance does not give effect direction, a threshold, an independent influence, or a causal explanation. A high-ranked feature is a candidate to inspect in the discovered rules, not a conclusion by itself.

### 3. Read box conditions jointly and in context

For each relevant PRIM/CART box:

- state target region, algorithm, partition, support, and evaluation scope;
- interpret all conditions as one conjunction, not independent effects;
- distinguish architect-controlled decisions/settings from sampled or observed operating conditions;
- use declared system-spec relationships to explain parent decisions and related settings, without inventing causal links;
- preserve units, boundary inclusivity, categories, missing values, and not-selected states; and
- compare rules across algorithms and targets without forcing agreement.

Crosscheck candidate conditions against domain knowledge. A rule may be consistent with a plausible mechanism, inconsistent with an expectation, or not informative about it. Record that comparison as interpretation, not causal validation.

### 4. Evaluate each rule's target identification and design-space coverage

For discovery and held-out partitions separately, report where available:

- unrestricted target prevalence;
- box precision or target share among retained runs;
- target recall/coverage;
- lift relative to the same partition's unrestricted prevalence;
- retained count and fraction; and
- the target count available for evaluation.

Read these together as measures of predictive usefulness and design-space coverage. Precision describes how often the rule's selected runs belong to the target; recall/coverage describes how much of the target population the rule identifies. A rule with reasonably strong precision and recall offers both target concentration and broad target capture within the evaluated sample. High precision with low coverage identifies a narrow candidate prescription; high recall with low precision admits many non-target runs. A rule that performs well in discovery but weakly on held-out data has limited predictive stability. A high held-out precision based on very few retained rows is narrow evidence.

### 5. Interpret the rule as predictive architectural guidance

Applying a box rule to held-out observations tests whether the joint decision/context constraints continue to identify the target tradeoff among runs not used to discover the rule. This supports a predictive interpretation within the campaign: an architect can inspect the rule as a candidate prescription and operating envelope associated with the target, together with its precision, recall, and coverage cost. The held-out comparison is stronger evidence than a discovery-only fit, while remaining internal validation on the same campaign.

Describe what the rule predicts and how well it identifies the target, rather than presenting the exercise as a generic data-filtering result. This can inform robustness-oriented architecture decisions: the rule identifies combinations of decisions and operating conditions under which the target tradeoff is repeatedly observed in the available evidence. If the notebook also measures dispersion or variance of continuous outcomes inside and outside the rule, report that comparison with its sample support; discrete precision/recall alone do not establish reduced continuous-outcome variance. The rule can suggest a causal explanation or intervention to test, but does not prove that imposing its conditions causes the target or guarantees future behavior.

### RQ2 conclusion format

A concise RQ2 conclusion should state:

- whether a box was discovered and whether the target had enough held-out support to evaluate it;
- the joint architectural prescription and operating envelope;
- how feature-ranking evidence and domain expectations relate to the rule;
- how reliably the rule predicts the target on held-out data, including precision, recall, baseline prevalence, and retained support; and
- the candidate architectural guidance or causal hypothesis it motivates, plus the next validation needed and its evidence limits.

## Federated Learning domain reference for this campaign

The following information is campaign-specific and should not be generalized to ADEPT analyses in other domains.

### Outcomes and preferred directions

- `final_val_accuracy`: model validation accuracy; higher is preferred.
- `avg_total_time`: the campaign's average total round-time measure; lower is preferred. Use the campaign documentation for its precise measurement boundary and units.

The current shared grid bins each outcome as `S/M/L`. These are numeric low/medium/high bins, not ratings. Since accuracy is maximized and time minimized, `L-S` is the strict preferred accuracy-time region when labels are ordered accuracy first, time second. It may be empty in an individual notebook. Preserve it as the semantic target and report its lack of observations; only add other target regions when they are explicitly justified as acceptable tradeoffs.

### Decisions, context, and outcomes

- **Architectural decisions/policies:** ON/OFF state of Client Selector (CS), Message Compressor (MC), and Heterogeneous Data Handler (HDH), together with their declared settings.
- **Policy stress:** parsed stress percentages associated with the patterns. Stress is distinct from client count.
- **Run context/uncertainties:** client count and sampled resource, non-IID, delay, and other environmental values. Check the notebook's actual features and system specification to determine which values were set, sampled, or derived.
- **Outcomes:** final validation accuracy and average total round time.

In the compact dataset, client-level attributes are averaged into run-level values. These summaries do not expose the distribution among clients or variation across rounds. The notebooks are observational; configurations and environmental samples may be imbalanced or overlapping across views.

### Theory-informed expectations to check

Use these as domain expectations supplied by the FL architecture and prior knowledge, not as assumed findings:

- CS changes the participating-client selection and may change the resource mix, with possible consequences for both time and model quality.
- MC can reduce communication demand while adding compression/decompression work; its net relationship with time and accuracy may depend on workload and environment.
- In the studied AP4FED implementation, HDH generates synthetic examples to address class imbalance in non-IID client datasets. Non-IID conditions alone do not imply that HDH is active or beneficial in every run.
- Client count and sampled delay, resource, and non-IID conditions may alter the observed relationship between a policy and the two outcomes.

For each expectation, classify the evidence as **consistent**, **mixed**, **not observed**, or **not assessable**, and cite the relevant support. “Consistent with” describes agreement between an expected mechanism and observed association; it is not proof of causation.

## Reporting principles

- Analyze each notebook according to its documented scope; first establish whether notebook subsets overlap or partition the campaign.
- Keep train/discovery metrics separate from held-out/test metrics and include denominators.
- Treat empty regions, unsupported configurations, and missing target support as limits of observed evidence, not proof of impossibility.
- Give practitioner recommendations conditionally, with the applicable configuration/context, retained support, coverage cost, and validation need.
- Give researchers enough detail to reproduce interpretation: region boundaries, filters, support, splits, box metrics, and the limitations of the observational design.

