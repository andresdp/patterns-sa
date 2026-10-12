# Performance-Based Sensitivity Analysis of Architectural Patterns in Federated Learning

> **Working manuscript draft — not submission-ready.** The main sections retain the structure of the original PDF draft: Introduction, Background, Methodology, Experiments, Results, Discussion, Related Work, and Conclusion. Internal subsections use a phase-based approach and organize the evaluation by research question. The compact campaign has now been analyzed; notebook-level findings and RQ mappings are in `docs/fl_notebook_findings/`. The Results section below is a synthesis draft and still needs box-level support reporting, figure selection, and author review. Bracketed notes are not manuscript text.

## Abstract

Architectural patterns in federated learning (FL) relate to model quality and system performance through client resources, local data distributions, and other design choices. We extend ADEPT, a data-driven framework for architectural design-space exploration and scenario discovery, to composed FL systems with multiple pattern decisions, categorical and optional parameters, and replicated client instances. We study the Client Selector (CS), Heterogeneous Data Handler (HDH), and Message Compressor (MC) in AP4FED, focusing on final validation accuracy and average total round time. The evaluation analyzes 2,340 runs across all eight pattern configurations, two tasks, three client counts, and ten partition seeds; environmental conditions are not fully crossed across configurations. In seed-matched standalone comparisons, CS was associated with −0.026 accuracy and −3.590 seconds per round, MC with approximately 0 accuracy and +0.214 seconds, and HDH with −0.015 accuracy and +0.530 seconds on average over shared support. These descriptive contrasts do not establish causal effects, and their ranges show variation across matched seeds. ADEPT’s PRIM/CART analysis identifies candidate operating envelopes whose interpretation depends on the variables constrained and the observed support.

**Keywords—** Data-driven sensitivity analysis, federated learning, architectural patterns, performance tradeoffs, scenario discovery.

## I. Introduction

The adoption of architectural patterns has increasingly been studied in relation to their effects on software quality attributes. In federated learning (FL), these effects depend on the system context: a coordinating server repeatedly exchanges and aggregates model updates from clients whose computational resources and local data distributions may differ. An architectural decision can therefore influence both the quality of the global model and the time required to complete training.

Architectural patterns provide reusable solutions to recurring FL design problems. The Client Selector (CS) determines which clients participate in a training round; the Heterogeneous Data Handler (HDH) aims to mitigate the effects of non-independent and identically distributed (non-IID) client data; and the Message Compressor (MC) reduces the size of exchanged model updates. The performance effect of each pattern depends on the operating conditions. For example, excluding resource-constrained clients may reduce round time but also remove training data, while compression may reduce communication time only when communication is a substantial part of total round time. A data handler may improve model quality under heterogeneous data distributions while increasing local computation. Architects therefore need to understand how pattern decisions relate to performance tradeoffs under specific environmental conditions.

ADEPT was proposed to help software architects understand the performance sensitivity of architectural-pattern configurations and to infer parameter constraints for target performance tradeoffs. Its workflow combines design-space modeling, data exploration, sensitivity assessment, and constraint inference using scenario-discovery algorithms. The original evaluation considered individual microservice patterns and datasets generated from performance models, with primarily numeric parameters and complete outcome records. Applying this workflow to FL raises additional concerns: several pattern decisions may be composed in one system; pattern parameters may be inapplicable when a pattern is disabled; runs contain measurements from multiple client instances; and experimental executions may produce missing outcomes.

In this paper, we extend ADEPT’s analysis to systems composed of FL patterns. We interpret a discovered box as a condition over the system design space, rather than solely as a range of parameters for an individual pattern configuration. A box that constrains design decisions or levers is prescriptive; one that constrains environmental uncertainties defines an operating envelope; and one that constrains both provides a conditional prescription. We evaluate the approach using AP4FED and the CS, HDH, and MC patterns, with the performance tradeoff between final model accuracy and total round time as the primary analysis target.

The study addresses four questions:

- **RQ1:** Which pattern decisions and configurations are associated with the target accuracy–round-time tradeoff?
- **RQ2:** Can ADEPT infer operating envelopes and conditional prescriptions when design decisions and client-environment parameters vary together?
- **RQ3:** How do system-level findings compare with single-pattern, model-stratified, and matched baseline comparisons?
- **RQ4:** What performance variability remains across replicated runs with the same modeled conditions, and what may this variability indicate about unmodeled factors?

Pattern stress (the estimated number of deployed pattern instances) is reported under RQ1–RQ2, with its assumptions and measurement limits stated; it is not treated as a separate research question.

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

The extension classifies box dimensions according to their architectural roles. Conditions on design decisions and other architect-controlled levers are **prescriptive**. Conditions on environmental or workload uncertainties define an **operating envelope**. Conditions on both design choices and uncertainties constitute a **conditional prescription**. Conditions on realized execution measurements, such as actual augmentation or participation, are diagnostic and require a prospective-observability and controllability check before they can support an actionable restriction. The discovery algorithms remain unchanged; the extension adapts the data representation and interpretation of their outputs to a mixed, multi-decision system.

A hypothetical influence model links policy choices and operating conditions to participation, data handling, and message handling, and from those mechanisms to accuracy and round time. It guides explanation and identifies useful measurements; its arrows are hypotheses, not relationships established by the observational analysis. The simplified concepts and model are documented in [paper_adept_formal_extension.md](paper_adept_formal_extension.md).

**Table 1 — ADEPT concepts used in this study.** Summarize only the differences needed to follow the contribution: configuration versus decision policy; lever, uncertainty, and pattern setting; numeric, categorical, and optional values; component-instance aggregation; tradeoff and failure label; composite versus marginal grouping and matched contrasts; pattern stress; and the three box readings.

## III. Methodology

ADEPT provides a workflow for moving from a system description and experimental data to tradeoff analysis, sensitivity assessment, and constraint inference. This study retains that progression and extends the representation used in the phases to accommodate composed FL patterns, multiple client instances, and mixed data. **Figure 3** summarizes the methodology.

**Figure 3 — Extended ADEPT workflow.** Adapt the existing ADEPT pipeline: (1) system modeling, (2) data exploration, (3) parameter sensitivity, and (4) constraint inference. Mark configuration grouping, matched contrasts, pattern-stress measures, instance aggregation, mixed-input encoding, and missing-outcome treatment where they enter the pipeline.

### 3.1. Phase 1: System Modeling

The system specification describes one FL system with three design decisions: client selection, message compression, and heterogeneous-data handling. Each decision has ON and OFF policies, and a system configuration identifies one policy for each decision. System-level levers include the model and training setup; uncertainties describe the client environment and data heterogeneity. Pattern-specific parameters are optional because they are inapplicable when the corresponding pattern is OFF.

This representation distinguishes an inapplicable pattern parameter from an ordinary numeric or categorical value. Optionality is preserved during analysis as a “not selected” state rather than imputed with a typical value. The input data also include measurements for multiple client instances. These instance-level values are summarized into run-level parameters or quality measures using declared aggregation functions, such as numeric means or spreads and categorical diversity. Aggregation keeps the design-space representation manageable, but loses information about which client has which combination of properties; interpretations are therefore limited to the summaries actually modeled.

### 3.2. Phase 2: Data Exploration

For the main analysis, the quality objectives are final validation accuracy (maximize) and average total round time (minimize). Training and communication times are secondary performance metrics used to interpret total round time; validation F1 is retained as a secondary metric if it is recorded in the final campaign.

Tradeoff labels must remain consistent across pooled and restricted analyses. Accordingly, the final analysis will document fixed bin boundaries and labels for each comparison population. **[AUTHOR INPUT: Insert final boundaries, labels, and their rationale. If multiple tradeoff-definition strategies are evaluated, identify the primary strategy and treat alternatives as sensitivity analyses.]** Missing outcomes are handled according to their declared meaning. If a missing quality measure denotes an execution failure, the run is assigned a `FAILURE` label rather than omitted from the analysis as though it had succeeded. The final manuscript will specify the treatment used for each quality measure and report the number of affected runs.

### 3.3. Phase 3: Parameter Sensitivity

The analysis examines the relationship between system configurations or decision policies and the target tradeoff. Grouping by system configuration describes complete architectural alternatives. Grouping by one decision pools configurations that share that policy and therefore marginalizes over the other pattern decisions. Because this marginal view can mix effects from different pattern compositions, results are reported with their grouping and are not interpreted as isolated pattern effects unless the experimental design supports that comparison. In particular, a tradeoff reached only by configurations that share two enabled patterns appears exclusive to each of those patterns in the marginal view, although it is associated with their combination; the configuration-level view identifies that combination.

To describe how one pattern decision relates to outcomes, we use **matched one-factor contrasts**. A contrast compares two configurations that differ only in that decision, for example CS ON with the other patterns OFF against the all-OFF baseline. The compact campaign records `partition_seed` values 1–10 for each executed configuration-condition cell. We therefore match the two arms within task, client count, environment parameters, and partition seed, then calculate the treatment-minus-reference outcome difference for each shared seed. Summaries give the equal-weight mean and range of seed-matched differences, the share that are positive, and run support. Repeating the contrast at each combination of the other patterns describes how the observed contrast varies by composition. These are descriptive seed-matched comparisons; partition-seed matching does not control host, scheduling, or other unrecorded run conditions and does not make the contrasts causal estimates.

We also characterize the amount of patterning in each run, its **pattern stress**. The primary measure is the number of deployed pattern instances: one client selector, one message compressor per participating client, and one HDH instance per participating client on which data augmentation was performed. This is a derived execution descriptor: it depends on the client environment and on the decisions themselves, including CS participation and actual HDH work. It is therefore distinguished from external uncertainties and is not used as an ordinary pre-execution matching factor. The number of enabled pattern types (0–3) is a secondary configuration summary; selecting a count alone does not specify which policies are ON. **[AUTHOR INPUT: Confirm the instance-counting rules with the AP4FED implementation; the current counts for CS and MC are inferred, and HDH instances are measured from per-round logs.]**

### 3.4. Phase 4: Constraint Inference

Before scenario discovery, categorical and optional parameters are encoded for the learning algorithms. The encoder is fitted on the training set and reused unchanged on the test set. After PRIM or CART produces parameter constraints, ADEPT decodes them into the original categories, numeric ranges, and optional “not selected” states. Feature-selection and scenario-discovery settings will be reported as executed in the final analysis; they will not be inferred from the original ADEPT paper where the implementation differs.

The inferred constraints are evaluated on the test set using density and coverage, together with the number of runs supporting each estimate. Where the experimental design permits, uncertainty will be assessed using a method that respects the replication structure. Ordinal encoding can constrain which subsets of nominal categories are expressible as intervals, particularly for parameters with three or more categories; this limitation is considered when interpreting the inferred constraints.

The executed feature-ranking stage uses a 50-tree random-forest regressor per objective (random seed 42), after smart correlation selection with absolute Spearman threshold 0.8 and model-performance selection using a 10-tree regressor. Scores are normalized shares of training impurity reduction. Removed correlated features are displayed with zero, alongside genuinely constant or unused features. Features are ordered with equal objective weights, and admitted to discovery when their importance exceeds 0.03 in either objective. Consequently, a dimension absent from a box may have been pruned or excluded by this gate; absence is not evidence of no architectural association. Additional held-out and model-seed diagnostics are reported separately from the executed notebook scores.

## IV. Experiments

We evaluate the approach using the AP4FED FL system and the three patterns described in Section 2.1. The experimental design varies system configurations and client-environment parameters to support analysis of both prescriptive conditions and environment-dependent performance sensitivity. The final setup and all factor levels must reflect the campaign actually executed.

**Table 2 — executed experimental design.** Report task/model, client count, pattern configuration, pattern-specific stress factors, number of rounds, local epochs, repetitions/seeds, and hardware allocation. Include only factors needed to understand the RQs; place exhaustive combinations in supplementary material if permitted by the venue.

> **Executed compact campaign:** The versioned compact CSVs contain 2,340 runs (1,380 baseline/single-pattern runs and 960 composed-pattern runs), covering AG_NEWS/MLP and CIFAR-10/CNN 16k; 4, 8, and 10 clients; all eight ON/OFF configurations; and 10 partition seeds per executed configuration-condition cell. Each task has 1,170 runs. The 234 present configuration-condition cells each contain one run at each seed 1–10. Environment coverage varies by configuration: the design is not fully crossed, and the one environment point shared by all configurations is 25% low-spec, 25% non-IID, and 25% delayed clients. The records show 20 rounds, `Epochs = 1`, learning rate 0.001, and batch size 64; confirm the AP4FED meaning of `Epochs` before describing it as local epochs. `avg_total_time` is documented as average total round time (training plus communication); the precise timing instrumentation is not in the compact CSV. The separate `docs/fl_experiment_design.md` is a proposed protocol and is not evidence that that campaign was executed. Hostnames vary across 39 hosts; detailed hardware/resource-isolation specifications need experiment-log confirmation.

### 4.1. Subject System and Factors

The AP4FED system is represented in ADEPT as a composition of the CS, MC, and HDH patterns. Their ON/OFF policies define system configurations. Client resources, client count, and data heterogeneity characterize the operating environment; model and training choices are levers when varied and controlled factors when held fixed. **[AUTHOR INPUT: Replace this paragraph with the verified factor levels and implementation settings from the executed campaign.]**

**[AUTHOR INPUT: Reconcile the CS policy metadata. All 960 CS-ON compact records use `Client Selector Value = 7.0`, whereas the compact system specification binds the ON policy to 2.0. Feature scores and outcome comparisons use the recorded values; report the executed setting rather than the uncorrected binding.]**

### 4.2. Measures and Data Collection

The primary performance metrics are final validation accuracy and average total round time. Report whether time is measured per round or over the complete training run, and define the timing boundary. Training and communication times are explanatory metrics; final or best validation F1 is secondary only if recorded in the final dataset. Record all attempted runs, including failures, and retain identifiers for system configuration, environment point, repetition, and seed.

**[AUTHOR INPUT: Confirm dataset partitioning and preprocessing, software versions, hardware/container configuration, resource isolation, timing instrumentation, failed-run handling, and data/code availability. The PDF reports a Leonardo supercomputer setup; retain those details only if they describe the final campaign.]**

### 4.3. Analysis Protocol

The compact records contain `partition_seed` and `repeat` values 1–10, with each seed represented once in each configuration-condition cell. Contrasts therefore match by partition seed as well as task, client count, and environment. The available CSVs do not make host conditions identical across matched runs. State the train/test split, analysis random seeds, feature-selection procedure, PRIM/CART settings, tradeoff boundaries, and uncertainty-estimation method used in the executed notebooks. Report client-count realization and timing/round details from the source logs where verified; do not import the separate proposed protocol's details.

### 4.4. Analysis Views

The pooled analysis includes the evaluated tasks and system configurations under a common tradeoff definition. To examine masking and composition, compare it with (i) analyses restricted to one pattern at a time, (ii) task-stratified analyses, and (iii) seed-matched one-factor contrasts of each pattern against the all-OFF baseline, within shared task, client-count, environment, and partition-seed values (Section 3.3). Evaluate constraints inferred from a single-pattern subset on composed-pattern runs only when the latter have sufficient support. A change in density indicates that the inferred constraints transfer differently to the observed subset; it does not, by itself, establish a causal interaction.

## V. Results

The results below summarize the executed compact campaign. Notebook-specific findings, matched contrasts, and RQ mappings are indexed in `docs/fl_notebook_findings/`. Tradeoff percentages use the overview notebook’s fixed bins; each stress notebook detects its own bins. Report box support and coverage with each rule. The seed-matched contrasts are descriptive, and no significance tests or noise-floor estimates are reported.

### 5.1. RQ1: Role of Pattern Decisions in Accuracy–Time Tradeoffs

This question examines how system configurations and individual pattern decisions are distributed across the quality space, and whether the observed performance variability is explained by the modeled design decisions alone.

Across all 2,340 runs, the most frequent regions under the overview’s fixed grid are `L-M` (875 runs; 37.39%) and `M-M` (691; 29.53%), followed by `L-S` (257; 10.98%), `S-M` (227; 9.70%), `M-S` (223; 9.53%), `S-S` (50; 2.14%), and `L-L` (17; 0.73%). No observations fall in `S-L` or `M-L`. These pooled proportions describe a campaign with unequal environmental support across configurations. The overview’s pattern-stress summaries also show that pattern-type levels combine different configurations and environments; the fixed task/client-count stress slices are more appropriate for controlled configuration descriptions.

### 5.2. RQ2: Scenario Discovery for Conditional Behavior

This question examines whether PRIM and CART infer parameter constraints under which a target accuracy–time tradeoff is achieved. Report prescriptive constraints on design choices, operating envelopes over environmental parameters, and conditional constraints that combine choices with environmental conditions. Organize findings around the hypotheses retained in the final analysis: CS effects under resource variation; HDH effects under data heterogeneity; MC effects under communication-relevant conditions; and total-round-time envelopes under changes in client count and resources.

PRIM and CART produce tradeoff-specific boxes, often separating the image and text tasks and distinguishing low-delay from higher-delay conditions. For example, the overview PRIM rules associate `M-S` with CIFAR-10 and delay below 12.5%, while `L-S` is associated with AG_NEWS, low delay, and a low measured HDH-instance count. These are candidate operating envelopes over observed data. **[AUTHOR INPUT: Select the boxes for the paper and report their exact decoded constraints, algorithm, train/test support, density, coverage, and target prevalence from the notebook outputs. Include unsupported tradeoffs and boxes with weak or negative lift.]**

The what-if analysis assesses the value of applying these rules as design/operating-space restrictions. For each configuration, it compares the test-set fraction attaining a target before restriction with the fraction among scenarios satisfying the inferred box. For the overview's `L-S` target, PRIM and CART raise pooled attainment from 11.0% to 100.0%, retaining 46/702 test scenarios; for the all-OFF configuration's `M-M` target, they raise attainment from 30.8% to 100.0%, retaining 31/107 scenarios. These are conditional robustness gains with explicit restrictions on supported operating space. The eight-client image `M-M` analysis illustrates the gain-versus-retention choice: PRIM improves attainment by 6.5 percentage points while retaining 21/24 scenarios, whereas CART improves it by 20.8 points while retaining 3/24. Some boxes worsen attainment or have too few retained scenarios to justify a prescription.

Improved STARR denotes more consistent membership in the target tradeoff across retained scenarios; it does not by itself establish lower continuous-outcome variance or a causal benefit from changing an input. Environmental limits define an envelope rather than a variable the designer can necessarily enforce. **[AUTHOR INPUT: Reconcile floating-point boundary handling for the affected HDH-versus-baseline and ten-client text boxes before reporting their what-if gains; the discovery metrics and reapplication support differ for those cases. See `docs/fl_research_question_synthesis.md`, RQ2.]**

### 5.3. RQ3: Ablation and Model-Stratified Analyses

This question compares pooled results with analyses restricted to individual patterns and analyses that control for or normalize model differences. Single-pattern subsets characterize performance when one pattern is active; model-stratified analyses reduce confounding by model scale; matched contrasts express each pattern's outcome difference relative to the baseline under the same conditions, and indicate whether that difference changes when other patterns are enabled.

The single-pattern notebooks describe each configuration on its own; task/client-count stress slices and generated `vs-baseline` notebooks provide direct comparisons. Across shared task, client-count, environment, and partition-seed support, CS had 180 matched seed-settings (180 runs per arm), MC had 300 (300 per arm), and HDH had 180 (180 per arm). Their equal-weight mean accuracy / time differences were CS −0.026 / −3.590 s, MC approximately 0 / +0.214 s, and HDH −0.015 / +0.530 s. Differences varied across seeds and settings; for example, CS’s time differences ranged from −12.848 to +0.602 s. On the fixed stress slices, the 10 seed-matched standalone comparisons per task/client-count point show additional variation. These findings describe shared observed support and are not causal estimates.

### 5.4. RQ4: Replication and Unexplained Variability

The cross-notebook feature audit provides a complementary sensitivity check. Task/model is the leading accuracy feature in all eight mixed-task analyses (93.6–97.0% of normalized importance), and delay leads six timing rankings. At four text clients, the CS representative dominates accuracy importance and the reconstructed model has held-out R² 0.875, consistent with the matched accuracy decrease. In contrast, the precise round-time regressors have R² at or below zero in all three image stress slices and four-client text. These limits do not invalidate a directly evaluated target-region success rate, but they qualify claims that the modeled features predict timing stability. JSD is observed only when HDH is ON, so its high scores in some slices combine measurement availability and variation in the recorded values. See `docs/fl_feature_importance_audit.md` for the complete diagnostics and selection flags.

Replicated runs permit comparison of between-condition and within-condition performance variability. This question examines whether runs with the same modeled inputs nevertheless fall into different quality-space regions, and whether low-density constraints may indicate stochastic variation or omitted factors.

The compact records contain ten partition seeds per executed configuration-condition cell. Matching by `partition_seed` allows descriptive comparisons across the same recorded data partitions, but does not match hostname, scheduling, or other unrecorded conditions. The broad ranges of seed-level contrasts—especially for round time—show that mean differences conceal substantial variation in some settings. The current analysis does not separate training stochasticity from host or runtime effects, and does not estimate a noise floor or confidence intervals.

## VI. Discussion

The results will be interpreted in terms of the three readings of the inferred constraints. Prescriptive constraints identify design choices associated with a target performance tradeoff; operating envelopes characterize environmental conditions under which the tradeoff is observed; conditional constraints relate design choices to those conditions. These interpretations are specific to the evaluated AP4FED configurations and sampled operating conditions.

**[AUTHOR INPUT: After completing Results, add a concise synthesis of what the findings mean for software architects and ADEPT. Distinguish empirical findings from implications and avoid presenting associations as causal effects.]**

### Threats to Validity

**Internal validity.** Total round time may depend on host load, scheduling, container behavior, and client assignment, in addition to the modeled architectural factors. Matched seeds and resource controls can reduce some confounding but do not eliminate it. PRIM and CART are heuristic algorithms, and their inferred constraints depend on the data split, feature-selection procedure, and tradeoff definition. Report the controls used and avoid causal claims unsupported by the experimental design.

**Construct validity.** Accuracy, F1, and total round time measure different aspects of FL quality and system performance and are not interchangeable. Discretized tradeoffs depend on the selected quality measures and bin boundaries; report these choices and assess important conclusions under reasonable alternative tradeoff definitions when feasible. Define measurement boundaries and missing-outcome semantics explicitly. Pattern-instance counts are partly inferred from deployment rules rather than logged; report which counts are measured and which are assumed. **[AUTHOR INPUT: Resolve whether HDH performs augmentation in the image-classification runs; the per-round logs record HDH work on almost no clients there, so HDH results for that task may describe the configured rather than the applied pattern.]**

**Method validity.** Aggregating client-level measurements makes populations with different numbers of clients analyzable, but removes client identities and joint client-level structure. Ordinal encoding may restrict the parameter constraints expressible for nominal parameters with several categories. Density and coverage are estimated from finite samples and should be reported with support and uncertainty; inferred constraints do not guarantee behavior outside the sampled design space. Matched contrasts cover only the settings in which both compared configurations were executed, and equal weighting across settings is a reporting choice rather than a representation of a target population.

The present analysis deliberately uses the compact run-level representation: selected numeric client fields are averaged across recorded client values, while categorical summaries count distinct values. Detailed analysis of individual clients and rounds is deferred until the compact space is understood. Equal means can mask resource imbalance, joint data/resource conditions, or slowest-client behavior; inferred mean constraints do not impose a bound on every client. Resource-usage means may include only participating clients, so their contributing population can depend on CS. Configuration-level outcome means are a separate average across runs. Limited detailed-log counts of actual HDH work support interpretation but do not constitute a general client-level analysis.

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

1. **Protocol details:** The executed compact campaign is reconciled with the CSVs. Confirm the meaning of `Epochs = 1`, exact timing instrumentation, hardware specifications, and resource isolation from experiment logs before finalizing these methods details.
2. **Analysis settings:** Record the executed split seed, encoding, feature selection, PRIM/CART settings, and box-level support/coverage in the final methods and results tables.
3. **Uncertainty:** The current summaries report descriptive seed-matched ranges only. Decide whether the paper needs a replication-aware uncertainty method; do not imply significance from sign shares or ranges.
4. **Evidence and references:** Review the result synthesis, select figures, verify every citation, remove duplicates and uncited entries, and resolve incomplete metadata.
5. **Submission:** Confirm the target venue’s current page limit, reference style, figure rules, and disclosure requirements. This draft was informed by the structure and general stylistic characteristics of the ADEPT journal paper; it does not reuse that paper’s prose.

## Draft Provenance

- Attached draft: `/Users/adiazpace/Documents/_ICSA27____Performance_based_Sensitivity_Analysis_of_Architectural_Patterns_in_Federated_Learning.pdf`.
- ADEPT journal paper: `papers/sensitivity_design_patterns_SI_JSS26__extension_ECSA25.pdf` — used locally to inspect section sequence, phase-based approach, RQ-organized evaluation, validity discussion, and conclusion structure.
- Repository planning and implementation context: `docs/paper_jss_extension_plan.md`, `docs/paper_adept_formal_extension.md`, `docs/fl_experiment_design.md`, `docs/analysis_journey.md`, `docs/instance_aggregation.md`, `docs/nan_strategy.md`, `docs/robustness_policy_grouping.md`, and `federatedlearning/FLsystem_split.json`.
- Scientific-writing workflow reference [13] is listed solely as tooling provenance, not as evidence for scientific claims. Authors should follow the venue’s AI-use disclosure policy.
