# ADEPT framework context

## What ADEPT does

ADEPT is a data-driven framework that connects an explicit architecture/system model to execution data and quality outcomes. Its workflow characterizes a design space, identifies parameters useful for understanding outcome variation, and uses scenario discovery—such as PRIM and CART—to find joint conditions associated with a target tradeoff. The resulting boxes can help architects inspect candidate design prescriptions and operating envelopes, including how target concentration changes as part of the evaluated space is restricted.

ADEPT originated in pattern-based performance analysis. The method transfers to the FL campaign, but conclusions must follow the current research design rather than stronger claims in earlier work about sensitivity reduction or ensuring a target.

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
