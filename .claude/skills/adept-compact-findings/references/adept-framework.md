# ADEPT framework context

## What ADEPT does

ADEPT is a data-driven framework that connects an explicit system model to observed configurations, operating conditions, and quality outcomes. It characterizes the observed design space, identifies parameters useful for understanding outcome variation, and uses scenario discovery—such as PRIM and CART—to find joint conditions associated with a target outcome region. The resulting boxes help architects inspect candidate prescriptions and operating envelopes, including how target concentration changes when analysis is restricted to runs matching a rule.

ADEPT originated in pattern-based performance analysis. The method transfers to the FL campaign, but conclusions must follow the current research design rather than stronger claims in earlier work about sensitivity reduction or ensuring a target.

## Diagnose the two primary result artefacts

These guidelines apply across application domains. Translate the generic terms below to the current system model: a **configuration** is a complete assignment of design decisions/policies; **context** is the set of other recorded conditions under which an observation occurred; **outcomes** are measured quality attributes; a **tradeoff/region** is a defined category or area in outcome space; and a **box** is a conjunction of feature conditions selected by a discovery method.

### 1. Objective space, regions, and configuration allocation

Use the objective-space chart together with its underlying tables. The chart shows where observed runs lie in outcome space; region labels or quadrants summarize those outcomes; allocation tables show which configurations and other recorded factors appear in each region.

Interpret in this order:

1. **Confirm what each axis means.** Check the measured outcome, unit, direction of preference, transformations, thresholds, and the exact definition of each region. If an axis is minimized, maximized, or binned, state that before describing a region as desirable. Do not assume that a label such as “high” is preferable without the study's definition.
2. **Describe occupancy before explanation.** Report the sample scope and denominator, which regions contain observations, which are empty, and the distribution of runs across populated regions. Empty means unobserved in this dataset and scope; it does not establish infeasibility. A visually dense region may reflect many repeated runs, so compare counts or proportions rather than point density alone.
3. **Trace allocation at the right level.** Compare complete configurations within the same analysis scope, then describe how observations are allocated among outcome regions. Keep a complete decision assignment distinct from marginal summaries such as the number of active options, individual feature frequencies, or instance counts. Marginal groups can combine different configurations and contexts.
4. **Separate design from context.** A region's allocation may vary with both chosen policies/configurations and non-controlled or sampled context. Describe these as observed associations. If the evidence does not isolate a policy from context, do not attribute the allocation to that policy alone.
5. **Diagnose support and comparability.** Check denominators, rare configurations, missing combinations, sampling/split structure, and whether compared groups share the same outcome definitions and population. Identify when a difference could reflect composition or imbalance. Treat changes across slices as contrasts between observed slices unless the design supports a stronger comparison.
6. **Translate the pattern into a decision-relevant next step.** Say which alternatives or operating contexts deserve further exploration, which region lacks evidence, and what additional observations or controlled comparison would resolve uncertainty. Do not turn descriptive occupancy into a guarantee or feasibility boundary.

An objective-space conclusion should therefore name: (a) the outcome region and how it is defined, (b) its observed count/share and comparison denominator, (c) which complete configurations are represented or over/under-represented, (d) relevant context differences, and (e) the limit on attributing the pattern. When a point-level plot and an allocation table appear inconsistent, check aggregation, filtering, and labels before interpreting either.

### 2. Discovery boxes and roles of relevant features

A discovered box is a joint rule for selecting rows associated with a specified target region. Read all conditions together. A box is not a list of independent effects, a causal model, or a prescription that has been experimentally applied.

Diagnose each box with these checks:

1. **Identify the target and scope.** State the target outcome region, source population, discovery method, data partition, and sample support. Clarify whether the rule was fitted on one partition and evaluated on another; never label metrics by their most recent evaluation if both partitions matter.
2. **Classify feature roles using the system model.** Separate decision/policy variables (choices an architect can set) from context or operating conditions (conditions that vary around the design), outcome-derived variables, identifiers, and other recorded descriptors. Use declared relationships to explain how a low-level condition relates to its parent decision. This adds syntactic context, not a causal pathway. If a feature's role is ambiguous, say so rather than inferring it from its name.
3. **Explain the whole conjunction.** Translate thresholds and categories faithfully, preserving units, inclusivity, category meaning, missing/not-selected states, and parent-decision implications. Group conditions into design prescription and operating/context envelope when the model supports that distinction. Explicitly note when the box does not constrain a decision or permits multiple decision states.
4. **Explain feature importance separately from box conditions.** Importance ranks indicate predictive credit within a particular fitted model and slice. They do not provide direction, a threshold, a causal effect, or proof that a highly ranked feature belongs in every box. Check consistency across relevant slices and flag instability, correlated proxies, constant or near-constant features, zero importance, and omitted expected parameters.
5. **Assess concentration and coverage together.** For discovery and held-out partitions separately, report target prevalence, box precision, target recall/coverage, lift relative to that partition's prevalence, and rows retained. A selective box may have high precision but low coverage; high coverage may include many non-target rows. A strong discovery result that degrades on held-out rows is evidence of limited stability. Small support makes all rates uncertain.
6. **Interpret restriction as an observational what-if.** Filtering the observed population by box conditions can show how the target share or outcome-region allocation differs among retained rows. Compare with the unrestricted baseline from the same partition and, where useful, with an explicitly named reference configuration. Report retained support and target coverage. This does not simulate changing a policy, reduce continuous-outcome variance by itself, or establish robustness in future settings.
7. **Compare algorithms and targets without forcing agreement.** Similar conditions from different methods or partitions strengthen descriptive consistency; different rules can reflect algorithm objectives, correlated predictors, or limited support. No box for a target means the method did not identify a rule under the chosen setup; it does not mean the target is impossible or has no useful conditions.
8. **End with a conditional action.** Phrase guidance as a candidate to evaluate within the stated scope, including its required context, expected tradeoff, retained support, and evidence gap. Recommend further validation when performance is sparse, unstable, or dependent on a narrow envelope.

For every reported box, make clear **what is a decision**, **what is context**, **which target is being enriched**, and **how much evidence remains after filtering**. Report feature importance as a separate prioritization signal, not as an effect estimate. Across both artefacts, use observational language (“is associated with”, “is over-represented among”, “the box retains”) unless the research design independently supports causal inference.

## Interpretation for this analysis

- A configuration is a joint assignment of policies; a run is one observed execution under that configuration and particular context/conditions.
- Feature importance is model-relative predictive credit, not effect direction or causal influence. A PRIM/CART box is a joint observational association.
- The held-out what-if filters already observed test rows. It does not rerun the FL system, impose the box conditions, estimate an intervention, or guarantee future outcomes. Report the target rate alongside precision/lift, retained count/fraction, and target coverage.
- “Robustness” here concerns membership in a discretized target tradeoff. It does not establish lower variance in continuous accuracy or time.
- This campaign's architecture explanation is syntactic: it uses only directed relationships declared in the JSON specification and conceptual decision/policy model. It adds context to box conditions without adding hypothesized causal links.

For the current study, the repository's concepts are: pattern ON/OFF decisions and settings; paired task/model and client-count context; sampled resource, non-IID, and delay operating conditions; compact execution measurements; and final validation accuracy plus average total round time as outcomes. See the [current campaign README](../../../../federatedlearning/compact/README.md) for definitions and scope.

## Sources

- Diaz-Pace, Trubiani, and Garlan, [“Data-driven Understanding of Design Decisions in Pattern-based Microservices Architecture” (ECSA 2025)](../../../../papers/2025-ECSA-sensitivity-designPatterns-performanceResults.pdf), the earlier PRIM/CART sensitivity-analysis method.
- Diaz-Pace, Trubiani, and Garlan, [“ADEPT: A Framework for Automated Data-driven Understanding of Design Decisions in Pattern-based Microservices Architectures” (working extension PDF)](../../../../papers/sensitivity_design_patterns_SI_JSS26__extension_ECSA25.pdf), the broader ADEPT framework.
- The active [methodological framework and experimental plan](../../../../docs/adept_methodology_and_experimental_plan.md) governs the study-specific adaptation. If older papers or plans differ from current notebooks and README, follow current campaign artifacts and flag the discrepancy.
