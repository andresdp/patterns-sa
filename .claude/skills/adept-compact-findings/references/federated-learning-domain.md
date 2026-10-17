# Federated-learning domain context

## System and pattern context

Federated learning trains a shared model across distributed clients while keeping their training data local. In a typical round, a server sends model parameters, participating clients train locally and return updates, and the server aggregates those updates. This preserves data locality, while making model quality and execution time sensitive to client resources, communication, participation, and local-data heterogeneity. Accuracy and round time can trade off; do not assume an architectural pattern is uniformly beneficial.

The compact campaign studies three patterns:

| Pattern | Role in the FL architecture | Interpretation cue |
|:--|:--|:--|
| Client Selector (CS) | Selects participating clients using configured criteria. | A selected-client population and the selector policy are related, but distinct. |
| Message Compressor (MC) | Compresses messages exchanged between clients and server. | Less communication can come with added computation; net behavior is context-dependent. |
| Heterogeneous Data Handler (HDH) | In the cited AP4FED implementation, generates synthetic examples to address class imbalance in non-IID client datasets. | Non-IID conditions do not themselves imply that HDH must be ON. Use the specification and observed rule. |

These mechanisms provide domain context for crosschecking feature ranks and boxes, not assumed explanations. Treat each as an expert expectation: findings can be consistent, mixed, not observed, or not assessable. A rule consistent with a mechanism can motivate a causal hypothesis for later validation, but does not demonstrate that the mechanism caused the observed outcome. A condition on a compact client average describes the recorded run-level summary, not every client or round.

The box architecture explanation is syntactic: use only directed relationships declared in the system JSON and the conceptual decision/policy model to connect conditions to their parent decisions and related settings. This adds explanatory context without asserting a causal pathway.

### Theory-informed expectations to test against the findings

- **Client Selector:** selection changes which clients participate and may change the resource mix; its relationship with time and model quality can depend on those selected clients and the sampled environment.
- **Message Compressor:** compression may reduce communication demand while adding computation for compression/decompression. The net relationship with total time and accuracy may vary with workload and environment.
- **Heterogeneous Data Handler:** in the studied AP4FED implementation, HDH generates synthetic examples to address class imbalance in non-IID client datasets. Non-IID conditions alone do not mean HDH is enabled or beneficial in every run.
- **Client count and environment:** client count, delay, resource capacity, and non-IID conditions may change the observed relationship between a pattern policy and the outcomes. Because the campaign is observational and groups may have different environment mixes, describe this as context-dependent association unless a controlled design supports more.

Use the expectations to interpret a discovered conjunction after checking its metrics and support. Do not use theory to override a rule's weak held-out precision/recall or sparse support.

## Scope of this campaign

The [compact README](../../../../federatedlearning/compact/README.md), [notebook stratification guide](../../../../federatedlearning/compact/NOTEBOOK_STRATIFICATION.md), and executed notebooks define the actual study and current slices. The campaign covers eight ON/OFF combinations of CS, MC, and HDH; CIFAR-10/CNN 16k and AG_NEWS/MLP as paired task/model contexts; client counts 4, 8, and 10; focal-pattern stress slices; and combined-pattern slices at shared stress levels. Follow the selected run's scope guide and notebook filters for the cases actually analyzed; do not infer coverage from an old plan or filename alone.

“All-environment” means all sampled conditions, not one controlled environment. Policy groups may have different mixes of delay, low-spec, and non-IID conditions. Pattern-count groups also mix full configurations and instance counts; describe them as observed strata, not randomized pattern doses. The compact numeric client features are aggregated averages, hiding individual-client imbalance and round behavior; detailed client/round analysis is deferred.

## Outcome semantics and target regions

In the current compact campaign, `final_val_accuracy` measures validation accuracy and higher is preferred. `avg_total_time` is the campaign's average total round-time measure and lower is preferred; consult the README for its measurement definition and units. The shared S/M/L labels are numeric bins, not quality rankings. With accuracy first and time second, `L-S` is the strict semantically preferred cell (high accuracy, low time).

Select the preferred or acceptable target region(s) from metric semantics and any stated stakeholder goal before inspecting a notebook's occupancy. Then report which cells actually contain runs in that slice. If `L-S` is empty, keep it as the preferred but unobserved target and report that a box cannot be trained for it in that slice. Do not choose a different occupied cell solely because it has support. Add a secondary acceptable target only with an explicit FL or stakeholder rationale and label it as secondary. Confirm each notebook's axis order, bin edges, and region counts before interpreting labels.

RQ1 describes the observed objective-space map and allocation to complete configurations. Counts and within-configuration proportions come first; contingency measures can supplement them when support is sufficient. RQ2 carries the selected target forward and asks whether a joint rule predicts its membership on held-out runs, with precision and recall read together with baseline prevalence and retained support.

For practitioners, separate a **design prescription** (policy and its related settings) from an **operating envelope** (sampled conditions or observed execution descriptors). Identify what can be configured before a run and what can only be monitored or observed afterward. The baseline and single-pattern notebooks are separate observational profiles, not randomized or matched estimates of pattern effects. State support and target coverage before treating any discovered rule as useful guidance.

When a rule has reasonably strong held-out precision and recall, interpret it as predictive architectural guidance within the tested campaign: the joint constraints identify a substantial and reasonably concentrated share of the target cases. This can support a candidate design prescription and motivate causal follow-up. It does not prove that enforcing the rule will cause the target. Continuous-outcome variance reduction can only be claimed when variance or dispersion is directly measured, not from discrete tradeoff membership alone.

## Sources

- Compagnucci, Pinciroli, and Trubiani, [“Experimenting Architectural Patterns in Federated Learning Systems,” *Journal of Systems and Software* 232 (2026), 112655](../../../../papers/jss-federated-learning-1-s2.0-S0164121225003243-main.pdf), [DOI](https://doi.org/10.1016/j.jss.2025.112655). Describes the broader AP4FED pattern implementation and evaluation context.
- Compagnucci, Pinciroli, and Trubiani, [“Performance Analysis of Architectural Patterns for Federated Learning Systems” (ICSA 2025)](../../../../papers/2025-ICSA-Architectural-Patterns-Federated-Learning.pdf). Provides background on FL rounds, client selection, and message compression; current campaign details come from its own artifacts.
