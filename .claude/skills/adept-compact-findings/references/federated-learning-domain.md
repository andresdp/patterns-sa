# Federated-learning domain context

## System and pattern context

Federated learning trains a shared model across distributed clients while keeping their training data local. In a typical round, a server sends model parameters, participating clients train locally and return updates, and the server aggregates those updates. This preserves data locality, while making model quality and execution time sensitive to client resources, communication, participation, and local-data heterogeneity. Accuracy and round time can trade off; do not assume an architectural pattern is uniformly beneficial.

The compact campaign studies three patterns:

| Pattern | Role in the FL architecture | Interpretation cue |
|:--|:--|:--|
| Client Selector (CS) | Selects participating clients using configured criteria. | A selected-client population and the selector policy are related, but distinct. |
| Message Compressor (MC) | Compresses messages exchanged between clients and server. | Less communication can come with added computation; net behavior is context-dependent. |
| Heterogeneous Data Handler (HDH) | In the cited AP4FED implementation, generates synthetic examples to address class imbalance in non-IID client datasets. | Non-IID conditions do not themselves imply that HDH must be ON. Use the specification and observed rule. |

These mechanisms provide domain context, not causal explanations for a feature rank or box. A condition on a compact client average describes the recorded run-level summary, not every client or round.

## Scope of this campaign

The [compact README](../../../../federatedlearning/compact/README.md) and executed notebooks define the actual study: eight ON/OFF combinations of CS, MC, and HDH; CIFAR-10/CNN 16k and AG_NEWS/MLP as paired task/model contexts; client counts 4, 8, and 10; and final validation accuracy plus average total round time. Baseline and single-pattern notebooks profile all three client counts; c4/c8/c10 notebooks fix a count and include available pattern configurations.

“All-environment” means all sampled conditions, not one controlled environment. Policy groups may have different mixes of delay, low-spec, and non-IID conditions. Pattern-count groups also mix full configurations and instance counts; describe them as observed strata, not randomized pattern doses. The compact numeric client features are aggregated averages, hiding individual-client imbalance and round behavior; detailed client/round analysis is deferred.

For practitioners, separate a **design prescription** (policy and its related settings) from an **operating envelope** (sampled conditions or observed execution descriptors). Identify what can be configured before a run and what can only be monitored or observed afterward. The baseline and single-pattern notebooks are separate observational profiles, not randomized or matched estimates of pattern effects. State support and target coverage before treating any discovered rule as useful guidance.

## Sources

- Compagnucci, Pinciroli, and Trubiani, [“Experimenting Architectural Patterns in Federated Learning Systems,” *Journal of Systems and Software* 232 (2026), 112655](../../../../papers/jss-federated-learning-1-s2.0-S0164121225003243-main.pdf), [DOI](https://doi.org/10.1016/j.jss.2025.112655). Describes the broader AP4FED pattern implementation and evaluation context.
- Compagnucci, Pinciroli, and Trubiani, [“Performance Analysis of Architectural Patterns for Federated Learning Systems” (ICSA 2025)](../../../../papers/2025-ICSA-Architectural-Patterns-Federated-Learning.pdf). Provides background on FL rounds, client selection, and message compression; current campaign details come from its own artifacts.
