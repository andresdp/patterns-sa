# Performance-Based Sensitivity Analysis of Architectural Patterns in Federated Learning

> **Working manuscript draft — not submission-ready.** The main sections retain the structure of the original PDF draft: Introduction, Background, Methodology, Experiments, Results, Discussion, Related Work, and Conclusion. Internal subsections use a phase-based approach and organize the evaluation by research question, informed by the existing ADEPT journal paper. Wording is original and does not reproduce the source paper. Results from the small exploratory dataset are omitted in favor of placeholders for the replacement campaign. Bracketed author notes are not manuscript text. The target venue’s page limit and current instructions remain to be confirmed.

## Abstract

Architectural patterns in federated learning (FL) affect model quality and system performance through their interaction with client resources, local data distributions, and other design choices. We extend the application of ADEPT, a data-driven framework for exploring architectural design spaces and analyzing performance sensitivity through scenario discovery, from individual patterns with numeric parameters to composed FL systems with multiple design decisions, categorical and optional parameters, and replicated client instances. The approach relates design-space conditions to performance tradeoffs using interpretable boxes. We study three patterns—the Client Selector (CS), Heterogeneous Data Handler (HDH), and Message Compressor (MC)—in an AP4FED system, focusing on final model accuracy and total round time. Depending on the parameter roles constrained by a box, the resulting rules provide prescriptive guidance, operating envelopes, or conditional prescriptions. **[AUTHOR INPUT: Add verified final campaign size, primary findings, and their implication after completing the replacement analysis.]** The evaluation examines configuration-level tradeoffs, environmental conditions, and variability across replicated runs.

**Keywords—** Data-driven sensitivity analysis, federated learning, architectural patterns, performance tradeoffs, scenario discovery.

## I. Introduction

The adoption of architectural patterns has increasingly been studied in relation to their effects on software quality attributes. In federated learning (FL), these effects depend on the system context: a coordinating server repeatedly exchanges and aggregates model updates from clients whose computational resources and local data distributions may differ. An architectural decision can therefore influence both the quality of the global model and the time required to complete training.

Architectural patterns provide reusable solutions to recurring FL design problems. The Client Selector (CS) determines which clients participate in a training round; the Heterogeneous Data Handler (HDH) aims to mitigate the effects of non-independent and identically distributed (non-IID) client data; and the Message Compressor (MC) reduces the size of exchanged model updates. The performance effect of each pattern depends on the operating conditions. For example, excluding resource-constrained clients may reduce round time but also remove training data, while compression may reduce communication time only when communication is a substantial part of total round time. A data handler may improve model quality under heterogeneous data distributions while increasing local computation. Architects therefore need to understand how pattern decisions relate to performance tradeoffs under specific environmental conditions.

ADEPT was proposed to help software architects understand the performance sensitivity of architectural-pattern configurations and to infer parameter constraints for target performance tradeoffs. Its workflow combines design-space modeling, data exploration, sensitivity assessment, and constraint inference using scenario-discovery algorithms. The original evaluation considered individual microservice patterns and datasets generated from performance models, with primarily numeric parameters and complete outcome records. Applying this workflow to FL raises additional concerns: several pattern decisions may be composed in one system; pattern parameters may be inapplicable when a pattern is disabled; runs contain measurements from multiple client instances; and experimental executions may produce missing outcomes.

In this paper, we extend ADEPT’s analysis to systems composed of FL patterns. We interpret a discovered box as a condition over the system design space, rather than solely as a range of parameters for an individual pattern configuration. A box that constrains design decisions or levers is prescriptive; one that constrains environmental uncertainties defines an operating envelope; and one that constrains both provides a conditional prescription. We evaluate the approach using AP4FED and the CS, HDH, and MC patterns, with the performance tradeoff between final model accuracy and total round time as the primary analysis target.

The study addresses four questions:

- **RQ1:** Which pattern decisions and configurations are associated with the target accuracy–round-time tradeoff?
- **RQ2:** Can ADEPT infer operating envelopes and conditional prescriptions when design decisions and client-environment parameters vary together?
- **RQ3:** How do system-level findings compare with single-pattern, model-stratified, and baseline-normalized analyses?
- **RQ4:** What performance variability remains across replicated runs with the same modeled conditions, and what may this variability indicate about unmodeled factors?

The contributions are threefold: (1) we extend ADEPT’s design-space representation to systems with composed pattern decisions and mixed, optional parameters; (2) we define prescriptive, operating-envelope, and conditional interpretations of scenario-discovery boxes; and (3) we evaluate the approach on an FL system that composes three architectural patterns. The remainder of the paper presents the background and concepts, the approach, the experimental setup, the evaluation, threats to validity, related work, and conclusions.

## II. Background

### 2.1. Federated Learning and Architectural Patterns

An FL round distributes global model parameters to participating clients, performs local training, returns client updates, and aggregates those updates at the server. Repeating this process produces successive global models. Total round time depends on computation and communication across participating clients; model quality may also depend on the distribution of local data.

We study three architectural patterns from the FL pattern catalog. The **Client Selector (CS)** profiles clients and selects a subset for participation; the configuration considered here uses a resource-based CPU criterion. The **Heterogeneous Data Handler (HDH)** addresses non-IID data using the data-augmentation implementation in AP4FED. The **Message Compressor (MC)** compresses model parameters exchanged between clients and the server; the configuration considered here uses zlib. These mechanisms motivate the factors in the evaluation, but their performance effects are measured rather than assumed. [2], [7], [8]

**Figure 1 — FL operation.** Retain or redraw the draft’s server–client overview, showing model broadcast, local training, update return, and aggregation. Verify figure provenance and reuse permissions.

**Figure 2 — Patterns considered.** Adapt the draft’s pattern diagram to indicate where CS, HDH, and MC intervene in an FL round. Present performance directions, if retained, as hypotheses rather than guaranteed effects.

### 2.2. Design Spaces and ADEPT

A system design space comprises feasible architectural configurations and the parameter values under which those configurations are evaluated. The corresponding quality space contains the measured values of quality attributes, such as model accuracy and round time. A performance tradeoff is a region of the quality space representing values of interest to the architect. ADEPT analyzes the correspondence between these spaces to identify design-space conditions associated with a target tradeoff.

In the original ADEPT setting, a pattern configuration combines design decisions and numeric parameters. In this study, a **system configuration** is a joint assignment of policies across the CS, MC, and HDH decisions (for example, CS ON, MC OFF, HDH ON). A **decision policy** is an alternative associated with one decision. This distinction is necessary because ON and OFF occur for multiple patterns; analyses must specify whether results are grouped by system configuration or by the policy of an individual decision.

ADEPT uses scenario-discovery algorithms, including PRIM and CART, to infer interpretable boxes associated with a target tradeoff. **Density** is the proportion of runs within a box that satisfy the target tradeoff; **coverage** is the proportion of all runs in the target tradeoff captured by the box. These measures characterize the evaluated data and should be interpreted together with their support counts, not as guarantees for unseen deployments. [9]

The extension classifies box dimensions according to their architectural roles. Conditions on design decisions and other architect-controlled levers are **prescriptive**. Conditions on environmental or workload uncertainties define an **operating envelope**. Conditions on both design choices and uncertainties constitute a **conditional prescription**. The discovery algorithms remain unchanged; the extension adapts the data representation and interpretation of their outputs to a mixed, multi-decision system.

**Table 1 — ADEPT concepts used in this study.** Summarize only the differences needed to follow the contribution: configuration versus decision policy; lever, uncertainty, and pattern setting; numeric, categorical, and optional values; component-instance aggregation; tradeoff and failure label; and the three box readings.

## III. Methodology

ADEPT provides a workflow for moving from a system description and experimental data to tradeoff analysis, sensitivity assessment, and constraint inference. This study retains that progression and extends the representation used in the phases to accommodate composed FL patterns, multiple client instances, and mixed data. **Figure 3** summarizes the methodology.

**Figure 3 — Extended ADEPT workflow.** Adapt the existing ADEPT pipeline: (1) system modeling, (2) data exploration, (3) parameter sensitivity, and (4) constraint inference. Mark configuration grouping, instance aggregation, mixed-input encoding, and missing-outcome treatment where they enter the pipeline.

### 3.1. Phase 1: System Modeling

The system specification describes one FL system with three design decisions: client selection, message compression, and heterogeneous-data handling. Each decision has ON and OFF policies, and a system configuration identifies one policy for each decision. System-level levers include the model and training setup; uncertainties describe the client environment and data heterogeneity. Pattern-specific parameters are optional because they are inapplicable when the corresponding pattern is OFF.

This representation distinguishes an inapplicable pattern parameter from an ordinary numeric or categorical value. Optionality is preserved during analysis as a “not selected” state rather than imputed with a typical value. The input data also include measurements for multiple client instances. These instance-level values are summarized into run-level parameters or quality measures using declared aggregation functions, such as numeric means or spreads and categorical diversity. Aggregation keeps the design-space representation manageable, but loses information about which client has which combination of properties; interpretations are therefore limited to the summaries actually modeled.

### 3.2. Phase 2: Data Exploration

For the main analysis, the quality objectives are final validation accuracy (maximize) and average total round time (minimize). Training and communication times are secondary performance metrics used to interpret total round time; validation F1 is retained as a secondary metric if it is recorded in the final campaign.

Tradeoff labels must remain consistent across pooled and restricted analyses. Accordingly, the final analysis will document fixed bin boundaries and labels for each comparison population. **[AUTHOR INPUT: Insert final boundaries, labels, and their rationale. If multiple tradeoff-definition strategies are evaluated, identify the primary strategy and treat alternatives as sensitivity analyses.]** Missing outcomes are handled according to their declared meaning. If a missing quality measure denotes an execution failure, the run is assigned a `FAILURE` label rather than omitted from the analysis as though it had succeeded. The final manuscript will specify the treatment used for each quality measure and report the number of affected runs.

### 3.3. Phase 3: Parameter Sensitivity

The analysis examines the relationship between system configurations or decision policies and the target tradeoff. Grouping by system configuration describes complete architectural alternatives. Grouping by one decision pools configurations that share that policy and therefore marginalizes over the other pattern decisions. Because this marginal view can mix effects from different pattern compositions, results are reported with their grouping and are not interpreted as isolated pattern effects unless the experimental design supports that comparison.

### 3.4. Phase 4: Constraint Inference

Before scenario discovery, categorical and optional parameters are encoded for the learning algorithms. The encoder is fitted on the training set and reused unchanged on the test set. After PRIM or CART produces parameter constraints, ADEPT decodes them into the original categories, numeric ranges, and optional “not selected” states. Feature-selection and scenario-discovery settings will be reported as executed in the final analysis; they will not be inferred from the original ADEPT paper where the implementation differs.

The inferred constraints are evaluated on the test set using density and coverage, together with the number of runs supporting each estimate. Where the experimental design permits, uncertainty will be assessed using a method that respects the replication structure. Ordinal encoding can constrain which subsets of nominal categories are expressible as intervals, particularly for parameters with three or more categories; this limitation is considered when interpreting the inferred constraints.

## IV. Experiments

We evaluate the approach using the AP4FED FL system and the three patterns described in Section 2.1. The experimental design varies system configurations and client-environment parameters to support analysis of both prescriptive conditions and environment-dependent performance sensitivity. The final setup and all factor levels must reflect the campaign actually executed.

**Table 2 — executed experimental design.** Report task/model, client count, pattern configuration, pattern-specific stress factors, number of rounds, local epochs, repetitions/seeds, and hardware allocation. Include only factors needed to understand the RQs; place exhaustive combinations in supplementary material if permitted by the venue.

> **Protocol reconciliation required:** The attached manuscript PDF describes 2,340 runs across AG NEWS/MLP and CIFAR-10/CNN 16k, with 20 rounds, five local epochs, three client counts, ten partition seeds, and all eight pattern configurations. The repository’s `docs/fl_experiment_design.md` specifies a different proposed campaign. The text below must be finalized from the executed campaign record; do not combine these plans.

### 4.1. Subject System and Factors

The AP4FED system is represented in ADEPT as a composition of the CS, MC, and HDH patterns. Their ON/OFF policies define system configurations. Client resources, client count, and data heterogeneity characterize the operating environment; model and training choices are levers when varied and controlled factors when held fixed. **[AUTHOR INPUT: Replace this paragraph with the verified factor levels and implementation settings from the executed campaign.]**

### 4.2. Measures and Data Collection

The primary performance metrics are final validation accuracy and average total round time. Report whether time is measured per round or over the complete training run, and define the timing boundary. Training and communication times are explanatory metrics; final or best validation F1 is secondary only if recorded in the final dataset. Record all attempted runs, including failures, and retain identifiers for system configuration, environment point, repetition, and seed.

**[AUTHOR INPUT: Confirm dataset partitioning and preprocessing, software versions, hardware/container configuration, resource isolation, timing instrumentation, failed-run handling, and data/code availability. The PDF reports a Leonardo supercomputer setup; retain those details only if they describe the final campaign.]**

### 4.3. Analysis Protocol

Use matched data-partition seeds across compared system configurations where available. Report how requested percentages of clients are converted to integer counts and provide the realized counts. State the train/test split, random seeds, feature-selection procedure, PRIM/CART settings, tradeoff boundaries, and uncertainty-estimation method. Also report deviations from the planned protocol. **[AUTHOR INPUT: Insert the executed settings and analysis decisions.]**

### 4.4. Analysis Views

The pooled analysis includes the evaluated models and system configurations under a common tradeoff definition. To examine potential masking and composition effects, compare it with (i) analyses restricted to one pattern at a time, (ii) model-stratified analyses, and (iii) baseline-normalized outcomes when runs are matched by model and environment. Evaluate constraints inferred from a single-pattern subset on composed-pattern runs only when the latter have sufficient support. A change in density indicates that the inferred constraints transfer differently to the observed subset; it does not, by itself, establish a causal interaction.

## V. Results

> **Evaluation placeholders:** This section is reserved for analyses on the larger replacement dataset. The 32-run exploratory results are not presented as confirmatory findings. For every reported box or comparison, include the applicable denominator, support count, uncertainty, and tradeoff definition.

### 5.1. RQ1: Role of Pattern Decisions in Accuracy–Time Tradeoffs

This question examines how system configurations and individual pattern decisions are distributed across the quality space, and whether the observed performance variability is explained by the modeled design decisions alone.

**[INSERT FINAL EVIDENCE: Summarize the distribution of system configurations across quality-space tradeoffs and report configuration-level or decision-policy densities. Identify feasible and sparsely supported tradeoff regions. Include one compact figure or table, then interpret the architectural alternatives without causal overstatement.]**

### 5.2. RQ2: Scenario Discovery for Conditional Behavior

This question examines whether PRIM and CART infer parameter constraints under which a target accuracy–time tradeoff is achieved. Report prescriptive constraints on design choices, operating envelopes over environmental parameters, and conditional constraints that combine choices with environmental conditions. Organize findings around the hypotheses retained in the final analysis: CS effects under resource variation; HDH effects under data heterogeneity; MC effects under communication-relevant conditions; and total-round-time envelopes under changes in client count and resources.

**[INSERT FINAL EVIDENCE: For each retained box, report the decoded parameter constraints, algorithm, target tradeoff, training- and test-set support, density, coverage, uncertainty, and target prevalence. Report tradeoffs for which no constraints were inferred, and identify unsupported or inconclusive analyses.]**

### 5.3. RQ3: Ablation and Model-Stratified Analyses

This question compares pooled results with analyses restricted to individual patterns and analyses that control for or normalize model differences. Single-pattern subsets characterize performance when one pattern is active; model-stratified analyses reduce confounding by model scale; baseline-normalized outcomes express changes relative to matched reference runs where available.

**[INSERT FINAL EVIDENCE: State which ablation analyses were performed and compare results only when tradeoff labels and denominators are compatible. Include transfer analyses only for adequately supported subsets. Distinguish exploratory analyses from planned tests.]**

### 5.4. RQ4: Replication and Unexplained Variability

Replicated runs permit comparison of between-condition and within-condition performance variability. This question examines whether runs with the same modeled inputs nevertheless fall into different quality-space regions, and whether low-density constraints may indicate stochastic variation or omitted factors.

**[INSERT FINAL EVIDENCE: Report replicate-level performance variability and the estimation method. Discuss whether the data distinguish training stochasticity from unmodeled environmental effects; do not attribute residual variability to a single source without evidence.]**

## VI. Discussion

The results will be interpreted in terms of the three readings of the inferred constraints. Prescriptive constraints identify design choices associated with a target performance tradeoff; operating envelopes characterize environmental conditions under which the tradeoff is observed; conditional constraints relate design choices to those conditions. These interpretations are specific to the evaluated AP4FED configurations and sampled operating conditions.

**[AUTHOR INPUT: After completing Results, add a concise synthesis of what the findings mean for software architects and ADEPT. Distinguish empirical findings from implications and avoid presenting associations as causal effects.]**

### Threats to Validity

**Internal validity.** Total round time may depend on host load, scheduling, container behavior, and client assignment, in addition to the modeled architectural factors. Matched seeds and resource controls can reduce some confounding but do not eliminate it. PRIM and CART are heuristic algorithms, and their inferred constraints depend on the data split, feature-selection procedure, and tradeoff definition. Report the controls used and avoid causal claims unsupported by the experimental design.

**Construct validity.** Accuracy, F1, and total round time measure different aspects of FL quality and system performance and are not interchangeable. Discretized tradeoffs depend on the selected quality measures and bin boundaries; report these choices and assess important conclusions under reasonable alternative tradeoff definitions when feasible. Define measurement boundaries and missing-outcome semantics explicitly.

**Method validity.** Aggregating client-level measurements makes populations with different numbers of clients analyzable, but removes client identities and joint client-level structure. Ordinal encoding may restrict the parameter constraints expressible for nominal parameters with several categories. Density and coverage are estimated from finite samples and should be reported with support and uncertainty; inferred constraints do not guarantee behavior outside the sampled design space.

**External validity.** Findings are bounded by the AP4FED implementation, selected architectural patterns, datasets, models, resource conditions, and hardware used in the campaign. They do not establish that the same performance effects hold for other FL algorithms, model families, deployment environments, or pattern implementations. **[AUTHOR INPUT: Update this subsection to match actual campaign coverage and limitations.]**

## VII. Related Work

Research on FL has described the training process, surveyed FL systems, and proposed architectural patterns for client management, model management, and training. AP4FED studies the performance behavior of selected FL patterns under controlled experimental conditions. The present work builds on this line by applying performance sensitivity analysis and scenario discovery to relate composed pattern decisions and environmental parameters to observed performance tradeoffs. [1]–[8]

ADEPT was developed to analyze how architectural-pattern decisions and parameters relate to quality-attribute tradeoffs, using PRIM and CART to infer interpretable parameter constraints. Its evaluation focused on microservice patterns and datasets generated from performance models. This study extends the approach to a system composed of multiple FL patterns and interprets inferred constraints over design decisions, levers, and environmental uncertainties. Research on adaptive pattern toggling and architectural design-space exploration provides additional context for pattern selection and system performance variability. [9], [11], [12]

**[AUTHOR INPUT: Check that each cited work directly supports the comparison; verify the full metadata and add only closely relevant studies. Resolve the duplicate pattern-catalog entry and incomplete [12] in the references.]**

## VIII. Conclusion

This paper applies ADEPT to performance sensitivity analysis of architectural patterns in federated learning. The approach extends the original single-pattern analysis by interpreting scenario-discovery boxes as conditions over composed design decisions, system levers, and environmental uncertainties. It also specifies how optional pattern parameters, categorical inputs, aggregated client measurements, and missing outcomes are represented in the analysis workflow. In this formulation, inferred constraints provide prescriptive guidance, operating envelopes, or conditional prescriptions for target performance tradeoffs.

**[AUTHOR INPUT: Replace with a concise synthesis of the strongest verified results from the larger campaign and their architectural implication. State the principal limitation.]**

Future work may examine additional FL patterns, systems, datasets, and quality attributes, and investigate how inferred constraints transfer across implementations and deployment environments. **[AUTHOR INPUT: Retain only directions supported by the completed study and the team’s actual plans.]**

## References

> Entries are provisional transcriptions from the attached draft, not fully verified references. Verify metadata against publisher or repository records, remove duplicates, and resolve incomplete entries before submission.

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-Efficient Learning of Deep Networks from Decentralized Data,” in *International Conference on Artificial Intelligence and Statistics (AISTATS)*, vol. 54, 2017, pp. 1273–1282.

[2] S. K. Lo, Q. Lu, L. Zhu, H.-Y. Paik, X. Xu, and C. Wang, “Architectural Patterns for the Design of Federated Learning Systems,” *Journal of Systems and Software*, vol. 191, p. 111357, 2022.

[3] C. Zhang, Y. Xie, H. Bai, B. Yu, W. Li, and Y. Gao, “A Survey on Federated Learning,” *Knowledge-Based Systems*, vol. 216, p. 106775, 2021.

[4] P. Kairouz et al., “Advances and Open Problems in Federated Learning,” *Foundations and Trends in Machine Learning*, vol. 14, nos. 1–2, pp. 1–210, 2021.

[5] S. Banabilah, M. Aloqaily, E. Alsayed, N. Malik, and Y. Jararweh, “Federated Learning Review: Fundamentals, Enabling Technologies, and Future Applications,” *Information Processing & Management*, vol. 59, no. 6, p. 103061, 2022.

[6] Duplicate of [2] in the source manuscript; verify and remove if confirmed.

[7] I. Compagnucci, R. Pinciroli, and C. Trubiani, “Performance Analysis of Architectural Patterns for Federated Learning Systems,” in *International Conference on Software Architecture (ICSA)*, IEEE, 2025, pp. 289–300.

[8] I. Compagnucci, R. Pinciroli, and C. Trubiani, “Experimenting Architectural Patterns in Federated Learning Systems,” *Journal of Systems and Software*, vol. 232, p. 112655, 2026.

[9] J. A. Diaz-Pace, C. Trubiani, and D. Garlan, “ADEPT: A Framework for Automated Data-Driven Understanding of Design Decisions in Pattern-Based Microservices Architectures,” *Journal of Systems and Software*, vol. 241, p. 113006, 2026.

[10] C. Briggs, Z. Fan, and P. Andras, “Federated Learning with Hierarchical Clustering of Local Updates to Improve Training on Non-IID Data,” in *International Conference on Neural Network*, 2020, pp. 1–9. **[Verify venue and metadata or remove if not cited.]**

[11] L. Baresi, I. Compagnucci, L. Lestingi, and C. Trubiani, “Adaptive Toggling of Architectural Patterns for Federated Learning,” in *International Conference on Software Engineering for Adaptive and Self-Managing Systems (SEAMS)*, ACM, 2026, pp. 105–116.

[12] C. Medeiros and N. Mendonça, “Exploring the Deployment Design Space of Microservice Applications,” June 2026. **[Incomplete source entry; verify venue, publication status, metadata, and whether cited.]**

[13] T. Kassis, V. Agarwal, Y. He, D. Patel, and A. M. Brueckner, “Scientific Agent Skills: A Library of Procedural Knowledge for Research Agents,” arXiv:2609.00065, 2026. https://doi.org/10.48550/arXiv.2609.00065. **[Tooling provenance only; retain in a software/tooling note or remove from the scientific reference list according to venue disclosure rules.]**

## Author Working Notes — Remove Before Submission

1. **Campaign:** The attached PDF’s 2,340-run protocol conflicts with the separate proposed design in `docs/fl_experiment_design.md`. Confirm the executed campaign and use one consistent factor table and methods description.
2. **Outcomes:** The PDF describes validation F1 as model accuracy; the repository plan selects final validation accuracy and treats F1 as secondary. Use the exact logged measures from the final data.
3. **Methods:** Verify the actual split, encoding, feature selection, tradeoff edges, grouping, discovery settings, and missing-outcome handling. Some failure-aware analyses are identified as incomplete in repository notes.
4. **Evidence and references:** Insert only results recomputed on the replacement dataset; report support, uncertainty, and inconclusive findings. Verify every citation, remove duplicates and uncited entries, and resolve incomplete metadata.
5. **Submission:** Confirm the target venue’s current page limit, reference style, figure rules, and disclosure requirements. This draft was informed by the structure and general stylistic characteristics of the ADEPT journal paper; it does not reuse that paper’s prose.

## Draft Provenance

- Attached draft: `/Users/adiazpace/Documents/_ICSA27____Performance_based_Sensitivity_Analysis_of_Architectural_Patterns_in_Federated_Learning.pdf`.
- ADEPT journal paper: `papers/sensitivity_design_patterns_SI_JSS26__extension_ECSA25.pdf` — used locally to inspect section sequence, phase-based approach, RQ-organized evaluation, validity discussion, and conclusion structure.
- Repository planning and implementation context: `docs/paper_jss_extension_plan.md`, `docs/paper_adept_formal_extension.md`, `docs/fl_experiment_design.md`, `docs/analysis_journey.md`, `docs/instance_aggregation.md`, `docs/nan_strategy.md`, `docs/robustness_policy_grouping.md`, and `federatedlearning/FLsystem_split.json`.
- Scientific-writing workflow reference [13] is listed solely as tooling provenance, not as evidence for scientific claims. Authors should follow the venue’s AI-use disclosure policy.