# Exploring Federated-Learning Architectural Tradeoffs with ADEPT

> **Working manuscript draft.** This version follows the current compact-campaign scope: two research questions, six task/client-count slices, and no matched-pair study. Results are a synthesis of the executed notebooks and remain observational. Author verification items are listed at the end.

## Abstract

Architects of federated-learning systems must choose among architectural patterns while accounting for client resources, data heterogeneity, and communication conditions. This paper applies ADEPT, a data-driven method for architectural design-space analysis, to a compact campaign of 2,340 AP4FED runs. The campaign combines three pattern policies—the Client Selector, Message Compressor, and Heterogeneous Data Handler—across eight configurations, two paired task/model settings, and client counts of 4, 8, and 10. We ask which accuracy–round-time tradeoffs occur and how they relate to design choices, then whether joint conditions discovered by PRIM and CART concentrate target tradeoffs on held-out runs. Each scenario is analyzed at a shared environment point and across all available environments, using a campaign-wide fixed objective grid. The common-environment view often has limited outcome variation, while all-environment feature rankings repeatedly elevate delay and resource/data-distribution descriptors. Several held-out boxes associate delay at or below 12.5% with fast-round targets; some reach 100% target frequency while retaining only a fraction of the scenario, so coverage and retained design space matter alongside precision. ADEPT adds a syntactic architectural explanation that traces box conditions through relationships declared in the system specification, grouping policy settings and operating conditions without asserting causation. The results help architects shortlist configurations and operating envelopes for further evaluation, and help researchers identify where the campaign supports conclusions and where new crossed experiments are needed.

**Keywords—** Software architecture, federated learning, architectural patterns, design-space exploration, scenario discovery, robustness.

## I. Introduction

Federated learning (FL) trains a shared model using data held by multiple clients. Each round distributes a global model, performs local training, returns client updates, and aggregates them. The resulting model quality and round duration depend on architectural choices as well as client resources, data distributions, and communication conditions. A software architect therefore faces a space of alternatives: a policy may improve one objective under some conditions while making another objective or operating constraint harder to satisfy.

Architectural patterns offer reusable ways to address recurring FL concerns. The Client Selector (CS) determines client participation; the Heterogeneous Data Handler (HDH) addresses non-IID data in the AP4FED implementation; and the Message Compressor (MC) compresses exchanged model parameters. Their mechanisms motivate questions about accuracy and execution time, but their observed relationships in a campaign depend on configuration, operating conditions, and measurement. A designer needs to know which complete alternatives occupy useful regions of the quality space and under what conditions those regions were observed.

ADEPT supports architecture-aware exploration by linking a system specification to execution data, characterizing tradeoffs, and discovering conditions associated with selected outcomes. For composed FL systems, a useful explanation must preserve the fact that policies and their settings are related. A statistical box may include a low-level setting whose meaning depends on an enabled policy, together with conditions on the operating environment. ADEPT can use relationships declared in the system JSON to place those predicates in context. This is a syntactic interpretation layer: it organizes related conditions and does not establish causal influence.

We study the AP4FED compact campaign using accuracy and average total round time as joint outcomes. Dataset and model occur as two fixed pairs—CIFAR-10/CNN 16k for image classification and AG_NEWS/MLP for text classification—so they are treated as task context, not independently varied factors. Each task is examined at client counts 4, 8, and 10. For each of these six slices, we compare a common-environment view with an all-environment view.

The study asks:

- **RQ1. Which tradeoffs occur, and how do design choices relate to them?**
- **RQ2. Which joint conditions identify a target tradeoff, and what changes inside the box?**

RQ1 maps the observed objective space by task, client count, and complete CS/MC/HDH configuration. RQ2 uses feature ranking to screen predictors and PRIM/CART to find conjunctions associated with non-empty tradeoff regions, then compares target frequency before and after applying each box to held-out observations. This what-if comparison makes explicit the trade between concentration, target coverage, and retained design space. Neither analysis is a causal estimate.

The paper contributes (1) an application of ADEPT to a compact, composed FL design space; (2) an architecture-aware box explanation that adds context through specification-declared relationships; and (3) a two-question analysis that connects observed tradeoffs to joint operating/design conditions and their held-out what-if robustness. The findings are intended to guide architectural shortlisting and follow-up experiments, not to provide deployment guarantees.

## II. Background and Conceptual Framework

### 2.1 Federated-learning patterns and quality objectives

An FL round includes communication with participating clients, local computation, and server aggregation. In AP4FED, CS can exclude clients according to a resource criterion; HDH implements data augmentation for non-IID data; and MC applies zlib compression. These patterns may interact with client resources, data distributions, and communication conditions. We treat these mechanisms as architectural context, while the campaign supplies the evidence about measured outcomes.

The study's quality objectives are final validation accuracy (maximize) and `avg_total_time` (minimize). The compact campaign documentation describes the latter as average total round time including training and communication. The exact instrumentation boundary requires verification from source logs. Other fields, including client CPU/JSD summaries and pattern-instance counts, are treated as observed or derived descriptors, not quality objectives.

### 2.2 ADEPT concepts and variable roles

ADEPT makes the design space and quality space explicit. In this study, the three pattern decisions (CS, MC, HDH) each take an ON/OFF policy. Their joint assignment is a **system configuration**. A policy can have **settings**, such as CS strategy/criterion/value or the MC algorithm; a setting may be inapplicable when its policy is OFF. The dataset/model pair is **chosen task context**. Client count (4, 8, 10) defines the three scale slices. Low-spec, non-IID, and delayed-client shares describe **operating conditions/uncertainties**. Execution summaries describe the realized run. Accuracy and time are **outcomes**, and their discretized pair is a **tradeoff target**.

This vocabulary keeps analysis roles distinct. A predictor used by a fitted model is not necessarily a controllable lever. In particular, pattern-instance counts can depend on the policy, participation, and execution; a box condition on such a count is not automatically a design prescription. Similarly, an operating condition may be monitorable or constrainable in a deployment, but the analysis alone does not show that it can be enforced.

### 2.3 Specification-linked explanation of a box

A PRIM or CART box is a conjunction of predicates. ADEPT preserves those exact predicates and uses only directed relationships implied by the JSON system specification and conceptual decision/policy model to add related context. A condition on a policy setting can be grouped under its parent policy; environmental conditions can be grouped as an operating envelope. Conditions in a box must be read together, especially where a setting is meaningful only under a particular policy.

The explanation does not invent domain influence arrows, expand the set of statistically selected conditions, or claim that a parent policy caused the target. It gives an architect a more legible view of the joint rule while keeping its statistical definition available. “No pattern policy is required by the box conditions” means the fitted conjunction did not select a pattern-policy predicate; it does not show that pattern choice is irrelevant.

## III. Methodology

ADEPT follows an iterative Model & Collect, Prepare, and Analyze & Refine workflow. The study defines its system boundary, decisions, context, uncertainties, and outcomes; links the model to run-level data; validates and filters that data; characterizes the quality space; discovers target-associated conditions; interprets those conditions in the specification; and records limitations and refinements. Any change to filters, target boundaries, or semantic mappings should be versioned and re-analyzed.

### 3.1 RQ1: characterize the observed tradeoff space

For each task/client-count slice and each environment view, RQ1 reports the continuous accuracy/time distributions, objective-versus-pattern-instance plots, tradeoff-region counts and shares, and tables by complete configuration and active pattern count (0, 1, 2–3 pattern types). The complete configuration is the design alternative; marginal pattern or instance summaries are descriptive context. Pattern count does not isolate a policy, and pattern instances may be environment-dependent or assumption-derived.

All notebooks use the same fixed grid, derived from the campaign-wide outcome distribution:

| Metric | Bin edges | Direction |
|---|---|---|
| Final validation accuracy | 0.2075, 0.4774, 0.7473, 1.0172 | Maximize |
| Average total round time | 1.5625, 9.5065, 17.4505, 25.3945 | Minimize |

Tradeoff labels combine the low/medium/high numeric bins for each measure. `S/M/L` name numeric ranges, not better or worse quality. A fixed grid lets the same label retain the same numeric meaning across slices. Empty cells are reported as unobserved in this campaign.

### 3.2 RQ2: discover joint conditions and compare what-if restrictions

For each populated tradeoff region, the notebook's existing feature-ranking method screens candidate predictors, after which PRIM and CART infer training-set boxes. Feature importance is a model-based screening score; it does not give effect direction or causal importance. Recurrent rankings are compared across slices and between common/all-environment views, with attention to feature correlation, availability, proxy variables, and ranking instability.

The notebooks hold out three of the ten `partition_seed` groups and keep each seed group together. A candidate grouped holdout is selected to approximate the full slice's tradeoff-label distribution. The resulting partitions contain 56 training and 24 test runs in each common-environment view, and 273 training and 117 test runs in each all-environment view. This is internal validation within the same campaign, not independent replication.

For each objective, feature ranking fits a random-forest regressor on training rows with optional pattern parameters included. Smart correlation selection removes redundant encoded features and restores them with zero in the score table. Scores are normalized shares of training impurity reduction. Equal objective weights order features; discovery retains a parameter when its score exceeds 0.03 for either objective. A zero can mean a constant feature, a correlated feature pruned before fitting, or a feature unused by the forest. Importance is a screening score, not direction, causal importance, or percentage of outcome variance.

For the training box, ADEPT reports support, precision/density, coverage/recall, and lift, where lift is box training precision minus training target prevalence. The box is then applied to held-out runs. The what-if reports baseline target frequency in all held-out runs, target frequency among box-matching runs, their absolute percentage-point difference, retained run count/fraction, and held-out target coverage/recall. The last two prevent a high in-box rate from hiding a very narrow rule that misses many target cases. No non-empty box is reported as no discovered rule for that target/view. A box restriction re-filters recorded observations; it does not simulate an intervention.

The architecture explanation adds JSON-linked context to the box predicates and groups them into a design prescription and operating envelope when the predicates support those categories. Exact numeric conditions remain visible, and the original statistical predicates remain authoritative.

## IV. Experimental Setup

### 4.1 Campaign and analysis units

The AP4FED compact data comprises 2,340 runs: 1,380 baseline/single-pattern runs and 960 composed-pattern runs. It covers two paired task/model contexts, three client counts (4, 8, 10), all eight ON/OFF combinations of CS, MC, and HDH, and ten `partition_seed` values in each of 234 observed configuration-condition cells. Each seed is present once per such cell. The environmental design is not fully crossed. The only environment point shared by every configuration is 25% low-spec, 25% non-IID, and 25% delayed clients.

Each of the six notebooks selects one task and client count and runs two views:

| View | Inclusion | Interpretation |
|---|---|---|
| Common environment | Shared environment point across all configurations | Comparison at one common sampled condition; limited environmental variation |
| All environments | All available records in the selected task/client-count slice | Broader operating-condition coverage, with uneven configuration/environment support |

These views overlap in records and are not independent replications. The image task is CIFAR-10 with CNN 16k; the text task is AG_NEWS with MLP. Dataset and model are paired and cannot be separated in this campaign.

The records show 20 rounds, `Epochs = 1`, learning rate 0.001, and batch size 64. The meaning of `Epochs` needs AP4FED-source confirmation before calling it local epochs. There are 39 hostnames; complete hardware and resource-isolation details are not included in the compact CSVs. Compact numeric client fields are averaged within each run, concealing client-level variation and imbalance.

### 4.2 Analysis protocol and reporting

For RQ1, plots and tables show continuous outcomes as well as the fixed-grid regions. For RQ2, feature ranking precedes PRIM/CART discovery. The held-out seed-group split described in Section 3.2 is applied per slice/view. Report the exact box conjunction, its specification-aware architectural explanation, algorithm, target, held-out denominator, target counts, precision, lift/gain, coverage, and retained fraction. Percentages without counts are insufficient for small cells.

The analysis is observational with respect to joint pattern configurations and operating conditions. Although all eight pattern configurations are represented, environmental coverage differs across configurations, and hosts/scheduling are not matched. Interpret common-environment results as descriptions at the shared point and all-environment results as descriptions of the available, unevenly sampled envelope.

## V. Results

The results below synthesize the six executed notebook analyses. Detailed scenario results are in [the notebook findings index](fl_notebook_findings/README.md); the cross-scenario evidence is in [the RQ synthesis](fl_research_question_synthesis.md).

### 5.1 RQ1 — Which tradeoffs occur, and how do design choices relate to them?

The common-environment view is informative as a shared-point comparison but has limited outcome diversity in several slices. Three of six common views contain only one populated tradeoff region: 8-client text is entirely `L-M`, 10-client image entirely `M-M`, and 10-client text entirely `L-M`. In 8-client image, the test set is entirely `M-M`, with only two other training observations outside that region. These slices cannot support useful discovery for absent regions and offer little basis for ranking configurations on those targets.

The observed map differs across paired task/client-count slices. Common-environment image runs center on `M-M` at 8 and 10 clients, while 4-client image also contains `M-S`. Text runs center on `L-M`, with a visible `L-S` subset at 4 clients. Because dataset and model are paired and the tradeoff labels summarize fixed numeric bins, this does not identify a standalone dataset or client-count effect. A designer should compare continuous outcomes and the complete configuration in the matching task and client-count scenario before transferring a choice.

Pattern-count groups show local associations, not a universal gradient. In common 4-client text, `L-S` rises from 0% among zero-instance runs to 22.5% among runs with 2–3 instances; common 4-client image shows a similar movement toward `M-S`. Across all environments, text `L-S` is 16.7% to 21.9% from zero to 2–3 instances at 8 clients, and 16.7% to 25.0% at 10 clients. Image behavior is different: 8-client image remains mostly `M-M`, and 10-client image shows only a slight `M-M` rise with no consistent movement in faster regions. These groups mix different configurations, environment conditions, participation levels, and derived instance counts. They do not support a general recommendation to add pattern instances.

For an architect, the useful unit is therefore the complete CS/MC/HDH configuration under an explicit task, client count, and operating envelope. Use the common view to understand alternatives at the shared point, then the all-environment view to see the wider observed condition mix. Treat empty quadrants as a guide to where more experiments are needed, not as proof those outcomes cannot occur.

### 5.2 RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?

Feature rankings shift with the analysis view. In all-environment analyses, Alpha Dirichlet Mean and delay percentage appear at or near the top across all six slices; CPU Mean and JSD Mean also recur. Common-environment rankings more often emphasize configuration-linked variables such as CS criteria, pattern types/instances, compressor algorithm, or HDH settings. These rankings show which fields help fitted models organize the observed outcomes. They do not identify causal drivers, and correlated or derived variables may act as proxies.

The clearest recurring operating-envelope association is low delay for fast-round targets. CART/PRIM boxes repeatedly include delay at or below 12.5% for `L-S` in 8- and 10-client text and fast-round image targets in 4-, 8-, and 10-client image. Several reported held-out boxes have 100% target frequency, but their coverage differs: the 8-client text `L-S` example captures 15 of 23 held-out target cases (65.2%); the 10-client image `M-S` example captures 15 of 16 (93.8%); and the 4-client image CART `M-S` example captures 15 of 30 (50%). A designer considering low delay as an operating condition should choose a box based on both the retained population and the share of desired cases it covers.

Box restrictions can make a target more frequent in the retained observations, with a tradeoff against design-space coverage. In 8-client text, `L-S` rises from 19.7% in the held-out scenario to 100% in a box retaining 15/117 runs and 65.2% of target cases. In 10-client image, `M-S` rises from 13.7% to 100%, retaining 15/117 and 93.8% of target cases. Conversely, common 8-client image already has 100% `M-M`; its PRIM/CART restrictions reduce retained rows without increasing target frequency. This is an actionable no-restriction result for that measured view: extra conditions were unnecessary to retain the observed target rate.

Architecture explanations help turn a conjunction into a reviewable design question. They group policy settings under their declared decision and show environmental predicates as the operating envelope. However, a literal CS setting requires care: all CS-ON records contain value 7.0, while the JSON binding declares 2.0. The discrepancy must be resolved before the paper presents the declared value as the executed prescription. Until then, explain the CS policy and criterion only with an explicit metadata caveat.

For architects, a high precision rule is a candidate for follow-up configuration testing only when its coverage and retained count fit the intended use. For researchers, no-box results, empty targets, and low-support boxes define evidence boundaries. The common and all-environment views overlap and share the same campaign, so their results must not be counted as independent confirmation.

## VI. Discussion

The compact study illustrates two kinds of guidance ADEPT can provide to software designers. RQ1 maps which accuracy/time regions appeared for complete pattern configurations in each task/client-count context. RQ2 identifies joint observed conditions under which a target region was more frequent in held-out runs, and quantifies how much of the scenario and how many target cases a restriction retains. The architecture explanation makes those joint conditions easier to reason about by tracing declared policy-setting relationships and separating them from operating conditions.

The most direct design implication is procedural: select a target accuracy/time region, identify configurations that reached it in the relevant task and client-count slice, and inspect the associated box's complete prescription, operating envelope, precision, coverage, and retained fraction. Low delay recurs in several fast-round boxes, making it a useful condition to test in subsequent deployments or experiments. It is not a guarantee that enforcing a delay threshold will cause the target. Pattern-count trends are less suitable as prescriptions because count groups combine different policies and context; compare named configurations instead.

For researchers, the results show where the campaign is informative and where it is not. Common-environment slices provide a controlled descriptive point but often have too little target diversity for discovery. All-environment slices offer wider conditions but are unevenly crossed. The repeated low-delay association merits a follow-up experiment that independently varies delay and architecture configuration. Policy-specific conclusions need adequate support at matched operating conditions, and the CS setting discrepancy must be reconciled. Detailed client/round analyses could test whether run-level means hide relevant client-level behavior.

### Threats to validity

**Internal validity.** The analyses are observational. Configuration/environment crossing is incomplete, and the available records do not establish that hosts, scheduling, or all execution conditions were controlled. Box what-if results re-filter a held-out sample; they do not represent interventions. Grouping by partition seed prevents group leakage between train and test but does not control unrecorded variation or provide external validation.

**Construct validity.** Accuracy and average total round time represent the two selected objectives, but target labels depend on fixed bin boundaries. The labels `S/M/L` denote numeric ranges, not quality judgments. The precise `avg_total_time` instrumentation boundary and the meaning of `Epochs` need source confirmation. Numeric per-client fields are averaged, which can mask imbalance and tails. Pattern-instance measures partly rely on assumptions and should not be treated as clean intervention variables.

**Method validity.** Feature-importance scores depend on the fitted model, feature correlation, and feature availability; they are screening results, not effect sizes. PRIM/CART boxes depend on the grouped split and algorithm settings. High precision from few rows can be unstable, so every rate must be reported with counts, coverage, and retained fraction. The six scenarios use a shared grid, but common and all-environment views overlap and are not replications.

**External validity.** Evidence comes from one FL system, two paired dataset/model tasks, client counts 4/8/10, and the sampled compact campaign. Results should not be generalized to other models, workloads, hardware, or client populations without further evaluation. The more useful next step is a deliberately crossed campaign for promising configuration/envelope combinations, followed by detailed client-level analysis where the design question requires it.

## VII. Related Work

The study builds on work in federated learning, architectural patterns for distributed systems, and data-driven sensitivity analysis. FL research has developed communication-efficient learning and methods for heterogeneous client data [1], [2]. Architectural pattern catalogs organize recurring design solutions for FL systems [3], [4]. ADEPT contributes a workflow for relating architectural design spaces to quality outcomes and for deriving interpretable parameter constraints through scenario discovery [5]. The present study applies that perspective to composed pattern policies and adds a specification-linked explanation of joint box conditions. References and venue formatting require final author verification.

## VIII. Conclusion

This paper applies ADEPT to a compact FL campaign and asks which accuracy–round-time tradeoffs occur and which joint conditions identify them. The six-slice analysis finds that outcome regions vary by paired task/model and client count; pattern-instance groups show local associations but no universal monotonic tradeoff. In scenario discovery, low delay recurs in several fast-round boxes, and held-out what-if comparisons show that higher target concentration can come with substantial loss of scenario coverage. In one common view, further box restrictions add no concentration because the target is already universal in the observed sample.

ADEPT's syntactic box explanation adds architectural context by tracing statistical predicates through declared policy-setting relationships, while preserving the conjunction and avoiding causal claims. For software architects, the results support a disciplined shortlist of configurations and operating envelopes for further testing. For researchers, they expose support gaps and specify which policy/environment combinations need better crossed evidence. Independent validation, resolution of the CS metadata discrepancy, and a fuller account of execution measurement are needed before making stronger recommendations.

## References

> Provisional references transcribed from the earlier draft. Verify bibliographic metadata and citation relevance before submission.

[1] B. McMahan, E. Moore, D. Ramage, S. Hampson, and B. A. y Arcas, “Communication-Efficient Learning of Deep Networks from Decentralized Data,” in *International Conference on Artificial Intelligence and Statistics (AISTATS)*, vol. 54, 2017, pp. 1273–1282.

[2] S. K. Lo, Q. Lu, L. Zhu, H.-Y. Paik, X. Xu, and C. Wang, “Architectural Patterns for the Design of Federated Learning Systems,” *Journal of Systems and Software*, vol. 191, p. 111357, 2022.

[3] I. Compagnucci, R. Pinciroli, and C. Trubiani, “Performance Analysis of Architectural Patterns for Federated Learning Systems,” in *International Conference on Software Architecture (ICSA)*, IEEE, 2025, pp. 289–300.

[4] I. Compagnucci, R. Pinciroli, and C. Trubiani, “Experimenting Architectural Patterns in Federated Learning Systems,” *Journal of Systems and Software*, vol. 232, p. 112655, 2026.

[5] J. A. Diaz-Pace, C. Trubiani, and D. Garlan, “ADEPT: A Framework for Automated Data-Driven Understanding of Design Decisions in Pattern-Based Microservices Architectures,” *Journal of Systems and Software*, vol. 241, p. 113006, 2026.

## Author verification before submission

- Reconcile CS `Client Selector Value` (7.0 in all CS-ON records; 2.0 in the compact JSON binding) and regenerate explanations if the specification changes.
- Verify the `avg_total_time` measurement boundary and the AP4FED meaning of `Epochs = 1`.
- Add verified host/hardware, scheduling/resource-isolation, failure-handling, software-version, and data/code availability details from campaign records.
- Select representative plots and exact box tables from the six notebook findings; ensure all counts, denominators, and architectural explanations agree with the executed outputs.
- Verify and complete bibliographic details and venue formatting for references [1]–[5].

## Analysis sources

- [Notebook execution order and per-slice findings](fl_notebook_findings/README.md)
- [Cross-scenario RQ1/RQ2 synthesis](fl_research_question_synthesis.md)
- [Compact campaign data, specs, and notebook guide](../federatedlearning/compact/README.md)
- [ADEPT methodological framework and experimental plan](adept_methodology_and_experimental_plan.md)
