# Paper Plan: Extending ADEPT from Parameter Constraints to Design-Space Conditions

**Status:** Draft plan (2026-09-29)
**Base paper:** Diaz-Pace, Trubiani, Garlan, *ADEPT: A Framework for Automated Data-driven Understanding of Design Decisions in Pattern-based Microservices Architectures* (JSS special issue, extension of ECSA 2025), `papers/sensitivity_design_patterns_SI_JSS26__extension_ECSA25.pdf`
**Running example:** Federated Learning (FL) systems built with AP4FED (Compagnucci, Pinciroli, Trubiani, JSS 232, 2026), `federatedlearning/`
**Companion documents:** [fl_experiment_design.md](fl_experiment_design.md) (the AP4FED experiments this paper needs); [paper_adept_formal_extension.md](paper_adept_formal_extension.md) (extended Table 2, extended Figure 4, formal treatment of mixed and missing data)

---

## 1. Positioning

The base paper states a two-fold goal: (i) **understand** the performance variation of a pattern's design decisions, and (ii) **reduce** it by inferring constraints on pattern parameters. Its evaluation emphasizes (ii), because its five microservice datasets are parameter sweeps of queueing models: within a single decision, uncertain parameters vary and push configurations across tradeoff regions, and PRIM/CART boxes bound them.

Its own limitations point to the next step:
- *External validity:* "we assume one pattern per system and did not analyze systems composed of multiple patterns".
- *Internal validity:* the SD analysis "does not distinguish [the] individual effects" of discrete decisions and numeric parameters.
- *Future work:* federated learning systems [Compagnucci et al.], other quality indicators, textual explanations for the architect.

This extension addresses them with a single conceptual move, instantiated on FL systems where several patterns are composed.

## 2. Conceptual Contribution

### 2.1 From parameter constraints to design-space conditions

In the base paper, a box is a set of **constraints on the parameters of one decision** (a pattern configuration M_D). We generalize it:

> A box is **the condition over the design space under which a tradeoff holds**. Its dimensions can be decisions, levers, and uncertain parameters alike.

The scenario-discovery machinery is unchanged (PRIM, CART, density/coverage/lift on a held-out test set); what changes is which kind of dimension a condition falls on, and therefore **how the architect reads it**:

| The box constrains… | Reading | What it tells the architect | FL instance |
|:---|:---|:---|:---|
| **Decisions and levers** (controlled by the architect) | **Prescriptive** | which choices achieve the tradeoff | "`squeezenet1_1` and client selector ON" → high accuracy, medium time (`L-M`) |
| **Uncertain parameters** (environment, workload) | **Operating envelope** | under which conditions a decision keeps its tradeoff | base paper: short-services-offloaded stays in `<XS,M>` while `N_B` ∈ [2.5, 23]; FL: *to be produced by the new experiments* |
| **Both** | **Conditional prescription** | which choice works in which environment | FL target: "client selector ON keeps accuracy in the top bin as long as ≥ k clients have ≥ 2 CPUs" (hypothesis, §4.3) |

The base paper's "controlling parameter variability" is the operating-envelope reading. "Explaining decisions" is not a new aim: it is the base paper's goal (i), now answered by the same boxes when they fall on decisions.

### 2.2 Why composed patterns require it

With one pattern, analyzing one M_D at a time is natural. With several interacting decisions (FL: client selector × message compressor × heterogeneous data handler), the configuration space is a product, decisions interact, and conditioning on each combination fragments small datasets. Treating decisions as box dimensions lets one discovery run explain the whole composed space. This requires ADEPT to represent:

1. **Configurations vs. decision policies.** A configuration (`ON,OFF,OFF`) is one policy per decision; plain policy names (`ON`/`OFF`) repeat across decisions. Analyses must declare their grouping: per configuration, per decision policy, or per decision.
2. **Optional parameters.** A pattern's settings are empty when the pattern is OFF; "not selected" must be a value a box can include or exclude.
3. **Categorical parameters.** Model architectures, compression algorithms, selection criteria.
4. **Aggregated component instances.** FL has *n* clients per run; per-client settings must be summarized (mean, spread, diversity) into system-level parameters.
5. **Failure outcomes.** Runs that crash or time out must be kept as failures, not silently dropped.

### 2.3 A diagnostic by-product: unexplained variability

When runs of the *same* decisions and parameter values fall into different tradeoff regions, no box can separate them, and ADEPT reports a low-density box. In the current FL data this happens: the five `squeezenet1_1` baseline runs, identical in every modeled factor, spread over `M-M` (2), `L-M` (2) and `L-L` (1), and neither PRIM nor CART finds a box for that cell (§4.2). The reading is actionable: **the specification misses a factor** (here, most likely training randomness), and the architect should either model it or treat it as noise. Replicated runs make this measurable: the current data already has 5 runs per model and configuration (2 for `squeezenet1_1` + HDH), without a seed column; the new campaign records seeds explicitly.

### 2.4 Storyline: a three-layer conceptual model

The paper's narrative follows the three layers of ADEPT's conceptual model ([paper_adept_formal_extension.md](paper_adept_formal_extension.md) §1.1). Each layer answers one question, and every extension of the paper belongs to exactly one layer. This gives a reader a single map from the base paper to the extension:

| Layer | Question it answers | Base paper | What the extension adds | Where FL needs it |
|:---|:---|:---|:---|:---|
| **1. Design space** (specified by the architect) | *What can be decided, and what varies?* | one pattern, one decision, numeric parameters | systems of several patterns; configurations vs. decision policies; parameter roles (lever / uncertainty / pattern setting), categorical domains, optional settings | three ON/OFF patterns in one component; `Model` categorical; pattern settings absent when OFF |
| **2. Data** (produced by experiments) | *What was observed?* | complete, simulated runs of a queueing model | real runs, some failing or unmeasured (missing-outcome treatments); replicated components summarized by aggregation; replicates and seeds | AP4FED training runs; per-client columns; the experiment campaign |
| **3. Analysis** (derived by ADEPT) | *What explains the tradeoffs?* | boxes constraining parameters of one decision | encoding and decoding of mixed data; `FAILURE` tradeoffs; boxes as conditions over the design space, with three readings; grouping by configuration or decision; ablations | prescriptive map (current data); envelopes and conditional prescriptions (new data) |

How the layers structure the paper:
- **Approach section.** Introduce the conceptual model as a figure with its three layers. Then walk through the layers in order, each one closing with what changes with respect to the base paper. The extended Table 2 is organized by the same layers.
- **The pipeline follows the layers.** Figure 4's phases map onto them: modeling = layer 1; data exploration = the step from layer 2 to layer 3 (tradeoffs); sensitivity and constraint inference = layer 3. The ★ components of the extended Figure 4 sit where a new layer-1 or layer-2 feature (categorical, optional, missing, replicated) reaches the analysis.
- **The main claim crosses the layers.** A box (layer 3) restricts parameters (layer 1), and when those are pattern settings, it restricts the decisions that bind them. "Boxes explain decisions" is therefore a statement about the link between layers 1 and 3, and the FL instance diagram (formal doc §1.2) shows this path explicitly.
- **Threats to validity follow the layers.**
  - Layer 1: specification completeness (the unexplained-variability diagnostic).
  - Layer 2: data sufficiency and noise (campaign size, replication, failures).
  - Layer 3: method validity (encoding, discretization, dominant factors, ablations).
- **Running example.** The FL instance of the model is introduced once, then revisited layer by layer: the spec (layer 1), the AP4FED runs and client aggregation (layer 2), and the boxes and their readings (layer 3).
- **One tradeoff throughout: model accuracy × total round time** (§4.1). It is the classic FL tradeoff, so the paper needs no motivation for it. It is introduced with the quality objectives (layer 1), measured in the runs (layer 2), and every box, hypothesis and ablation is stated in its terms (layer 3). Every pattern is characterized by how it moves a configuration in this plane.

## 3. Framework Extensions (implementation status)

| Extension | Paper concept | Implementation | Status |
|:---|:---|:---|:---|
| Policy grouping for multi-decision systems | configuration vs. decision policy; `by=` grouping | `docs/robustness_policy_grouping.md` | ✅ |
| Numeric encoding of categorical and optional parameters | "not selected" as a box value; category sets in boxes | `FeatureEncoder`, `Box.readable_limits()`, `docs/nan_strategy.md` | ✅ |
| Outcome failure semantics | missing-outcome treatments (failure / drop / fixed value); `FAILURE` category and failure tradeoffs ("when do runs fail?") | `DataProcessor.define_tradeoffs`; formal doc §3.6 | ✅ for label-based phases; **to do** for components reading continuous outcomes: feature importance fails on NaN, regret counts a failure as zero (formal doc T8, T9; needed before the new campaign) |
| Declarative aggregation of component instances | aggregated parameters and objectives | `dataspace.aggregations`, `docs/instance_aggregation.md` | ✅ (mean/std/min/max/median, diversity) |
| Spec linting and summary | policy-combination coverage, low variance, NaN semantics | `SystemLinter`, `summarize_system` | ✅ |
| Deterministic key-parameter selection | reproducible smart correlation | tie-breaking in `FeatureImportanceAnalyzer` | ✅ |
| Design-space report (textual explanation) | bridging SD output to the architect's vocabulary; can instantiate the conceptual model (formal doc §1.1-1.2) for any spec | `docs/plans/2026-09-18-1723-feat-design-space-report-plan.md` (R8 proposed) | Planned |
| Categorical proportion statistic for aggregation | e.g. share of non-IID clients | extend `adept/utils/aggregation.py` | To do (needed by the new FL data) |
| Per-decision / per-stratum discovery | the base paper's M_D-conditioned boxes; per-model views | option on `discover_scenarios` | To do (see §6) |
| Restricting a session to a slice, keeping pooled tradeoff labels (A1, A2-fix) | slice = condition on configurations and/or levers | For FL: `federatedlearning/fl_slices.py` (row filter as loader `preprocessor`), and `make_slice_notebooks.py`, which writes the full dataset's detected edges into each focused notebook's `TRADEOFF_EDGES`, which generates `analysis-fl-{baseline,client-selector,message-compressor,hdh}.ipynb` (optionally `--include-baseline`). First-class option (e.g. `session.restrict(where=...)`) plus evaluating a box on another slice (transfer check) | Workaround ✅; API to do |
| Static tradeoff grid (§4.5): explicit frozen edges, open-ended outer bins, no padding, reusable across sessions | comparable tradeoff labels across slices and data additions | Bins are detected from the data by default; `create_tradeoffs(method='discretization', labels=..., edges={objective: [e0, ..., en]})` fixes them instead (labels required, no padding added); runs outside the edges are reported and left unlabelled. In FL, the base notebook detects the edges, and `make_slice_notebooks.py` fixes the edges detected on the full dataset in every focused notebook | ✅ explicit edges; open-ended outer bins to do |
| Encoding choices for discovery: native categorical PRIM, one-hot/target-ordered codes for CART, declared category order, encoding-related lint, permutation importance | valid and complete search over nominal categories (formal doc §4.1) | [paper_adept_formal_extension.md](paper_adept_formal_extension.md) §6, T2-T7 | To do (not needed for current FL data; T4 recommended before the new campaign) |
| Outcomes relative to a reference configuration (A2-normalize) | relative outcome: gain/ratio over the baseline at the same model and environment point | Possible today as derived columns in the `preprocessor`, declared as objectives; a declarative option in the spec | Workaround ✅; declarative to do |

## 4. Instantiation on Federated Learning

### 4.1 System under analysis

`fl_system` composes three ON/OFF pattern decisions: **client selector** (resource-based: only clients meeting a CPU criterion train), **message compressor** (zlib), and **heterogeneous data handler (HDH)** (DCGAN data augmentation for non-IID clients). Levers: model architecture and training hyperparameters. Uncertainties: per-client resources and data heterogeneity, aggregated over the clients. Objectives: predictive quality (F1, accuracy) and system cost (round, training and communication time; CPU/RAM usage).

**Target tradeoff: model accuracy × total round time.** The paper focuses on one tradeoff, the classic one in federated learning: how accurate the global model gets versus how long training takes (wall-clock time per round, often summarized as *time-to-accuracy*).

| Objective | Column (spec name) | Direction | Why this choice |
|:---|:---|:---|:---|
| **Model accuracy** | `Final Val Accuracy` (`final_val_accuracy`) | maximize | The standard FL quality measure (CIFAR-10 is class-balanced, so accuracy is not misleading). The **final** round's value is what the trained model delivers. The *best* value over rounds (used so far, `best_val_f1`) selects a round on the validation set, which is optimistic. |
| **Total round time** | `Avg Total Round Time` (`avg_total_time`) | minimize | The wall-clock cost of a round: local training plus communication, including waiting for the slowest client. With `num_Rounds` fixed at 10, total training time is 10 × this value, so the ranking is the same. |

Why this tradeoff carries the storyline:
- **Every pattern moves the system in this one plane, through different mechanisms.** This makes the patterns' effects directly comparable, in the architect's terms:
  - the **client selector** acts on *both* axes: it removes stragglers (time) and weak or skewed clients (accuracy);
  - the **message compressor** acts on the *communication share* of time;
  - **HDH** trades *training time* for *accuracy under non-IID data*.
- **The two objectives are in real tension** (Spearman ρ = 0.62 between accuracy and round time on the current data, driven by the model). So the tradeoff regions are not trivially ordered, and "better accuracy at no time cost" (the selector's `M-S`/`L-M` boxes) is a meaningful finding.
- **The other metrics become explanatory, not targets.** Training and communication time decompose round time and explain *why* a box holds (e.g. H3 on communication). F1 is a robustness check. CPU/RAM usage stays out of scope for the tradeoffs.

**Relation to the earlier analysis.** The notebook first used `best_val_f1` × `avg_total_time`. It now uses `final_val_accuracy` × `avg_total_time` and was re-run (2026-09-30). Accuracy and F1 rank the runs almost identically (Spearman ρ = 0.985), so the main findings are unchanged. The re-run also shows two differences, both instructive (§4.2).

### 4.2 What the current dataset shows (prescriptive reading)

The published AP4FED dataset used so far (32 runs, `federatedlearning/FLwithAP_MLdata_split.csv`) covers 4 of 8 decision combinations (baseline plus each pattern alone), two models, and a **constant client environment** (4 clients with 3 CPUs, 1 client with 1 CPU; 2 of 5 clients non-IID). With the tradeoff `final_val_accuracy` × `avg_total_time` (3 bins each), PRIM and CART agree on a prescriptive map in which three of the four model × selector cells have a region of their own:

| | client selector OFF | client selector ON |
|:---|:---|:---|
| `CNN 16k` | `S-S` (fast, low accuracy; PRIM and CART, lift 0.45) | `M-S` (same speed, accuracy +0.013 at the edge of the next bin; lift 0.41, test density 0.5) |
| `squeezenet1_1` | no region: the baseline's 5 runs spread over `M-M` (2), `L-M` (2) and `L-L` (1) | `L-M` (top accuracy in every run, ~18% shorter rounds; lift 0.86, test density 1.0) |

PRIM adds a fifth box, **HDH ON → `M-L`**: on `squeezenet1_1`, HDH lowers accuracy (-0.016) and slows rounds by 58%, so its runs alone form the medium-accuracy, slow region.

Architectural reading: model capacity trades accuracy for compute; resource-based client selection removes the 1-CPU, non-IID straggler (it records no activity in selector runs), gaining accuracy at no cost; HDH adds generator training time, and on the large model it lowers accuracy in this environment; compression has little to save (communication ≈ 2 s per round). Details: `federatedlearning/analysis-fl.ipynb`, Sections 3, 8 and 9.

**Differences with the F1-based analysis, and what they teach:**
- **Bin-edge sensitivity.** With F1, the `squeezenet1_1` baseline was a clean `M-M` cell (CART lift 0.36). With accuracy, its runs (0.447-0.465) straddle the `M`/`L` edge at 0.460, so identical configurations land in three regions and no box can describe them. Two metrics that rank runs almost identically can still produce different boxes when an equal-width edge cuts through a cluster. This is a concrete argument for the static grid with meaningful edges (§4.5), and an instance of the unexplained-variability diagnostic (§2.3).
- **HDH becomes visible.** With F1, HDH's accuracy drop on the large model did not change bins. With accuracy it does, and PRIM describes it by a condition on the pattern alone. This strengthens the "HDH is a cost in this environment" reading.

**Limits:** no envelope or conditional boxes are possible, because no uncertain parameter varies; pattern interactions are unobserved (4 of 8 combinations); 2-4 test runs per box.

### 4.3 What the new experiments must show (envelope and conditional readings)

[fl_experiment_design.md](fl_experiment_design.md) specifies an AP4FED campaign that varies the client environment, completes the 8 decision combinations, and replicates runs. It is built to test hypotheses of the three kinds:

| ID | Hypothesis | Reading it would illustrate |
|:---|:---|:---|
| H1 | The client selector's accuracy gain grows with the share of low-resource clients, and vanishes when all clients are capable. | conditional prescription |
| H2 | HDH improves accuracy only when data heterogeneity is high (low Dirichlet α, many non-IID clients); otherwise it only adds training time. | conditional prescription |
| H3 | The message compressor pays off only when communication is a significant share of the round (more clients, larger models). | conditional prescription |
| H4 | For a fixed configuration, round time stays in the fast tier while the number of clients and the resource spread stay below identifiable bounds. | operating envelope |
| H5 | Some pattern combinations interact (e.g. selector + HDH: excluding non-IID clients removes the data HDH would repair). | prescriptive, on combinations |

### 4.4 Ablation studies

The pooled analysis (all configurations, both models) answers RQ1, but it hides two things: the behavior of each pattern on its own, and every effect smaller than the model's. Two ablations restrict or transform the dataset to expose them. Neither changes the ADEPT pipeline; each runs it on a different view of the same data. The formal treatment is in [paper_adept_formal_extension.md](paper_adept_formal_extension.md) §3.9.

#### A1. Single-pattern ablation: one pattern at a time

**Idea.** Fix the decisions, so the only things left to vary are the pattern's settings and the environment. This reproduces the base paper's analysis of Gateway Offloading (one M_D at a time), now on an FL pattern.

| Variant | Runs kept | What varies | Box reading | Question answered |
|:---|:---|:---|:---|:---|
| **A1-alone** | pattern *p* ON, the other two OFF (e.g. `ON,OFF,OFF`) | *p*'s settings (selector threshold), environment (U1-U5) | **operating envelope** of *p* | Under which environments does *p* keep a given tradeoff? Which parameters matter for *p* (key parameters of *p*)? |
| **A1-vs-baseline** | *p*-only runs ∪ baseline (`OFF,OFF,OFF`) | *p* ON/OFF, its settings, environment | **conditional prescription** for *p* | When is enabling *p* better than not enabling anything? (H1-H3 one pattern at a time) |
| **A1-fixed** | *p* ON, the other two free (4 configurations) | the other two decisions, *p*'s settings, environment | prescriptive + envelope | Does *p*'s envelope depend on which patterns it is composed with? |

**Protocol.**
- **Tradeoff labels are those of the pooled analysis**: the static grid of §4.5, frozen on the full dataset, then the runs are restricted. This keeps `S`/`M`/`L` meaning the same thing in every slice, so densities are comparable across slices and with the pooled boxes. Per-slice bins would answer a different question: which tradeoffs exist *within* the slice.
- Per slice, repeat Phases 3 and 4: density of each tradeoff (the base paper's density(M_D, T)), feature importance and key parameters, and PRIM/CART boxes.
- Settings of the patterns fixed to OFF are constant ⊥ in the slice; the linter's low-variance check flags them and they are left out.
- **Transfer check.** Evaluate each A1-alone box on the runs where *p* is ON together with other patterns. If density drops, *p*'s envelope does not survive composition: this is direct evidence of an interaction (H5), obtained without fitting interaction terms.

**Expected results.**
- On the current data, every A1 slice has a constant environment and 5 replicates per model. Only the model and the replication noise vary, so there is nothing for the boxes to explain. This is a useful negative control: it shows why the new data is needed.
- On the new data, A1-alone for the client selector should yield an envelope on the share of low-resource clients and the threshold (H1). A1-alone for HDH should yield one on α and the share of non-IID clients (H2).

#### A2. Model ablation: removing the dominant lever

**Motivation.** On the current data `Model` takes about 0.98 (accuracy) and 0.89 (time) of the feature importance. The key-parameter threshold had to be lowered to 0.03 for any pattern to be selected, and the time bins mostly separate the two models. Pattern and environment effects are real, but they are an order of magnitude smaller: `Model` **shadows** them. There are three ways to take the model out, and they are not equivalent:

| Variant | How | Tradeoff labels | What it shows |
|:---|:---|:---|:---|
| **A2-fix** (stratify) | Analyze each model separately (`Model` = `CNN 16k`, then `squeezenet1_1`) | **Static per model** (§4.5): with the all-model grid every `CNN 16k` run falls in the fast bin, leaving nothing to explain. Tradeoffs are then relative to the model's tier. | Key parameters and boxes of the patterns and the environment for a given model; whether they differ between models (e.g. the selector speeds up `squeezenet1_1` rounds by 18% but slows `CNN 16k` rounds by 6%) |
| **A2-normalize** (relative outcomes) | Replace each outcome by its value relative to the baseline configuration **of the same model at the same environment point**: accuracy gain (difference), time ratio (quotient). Pool both models; `Model` is removed from the features. | Pooled bins on the relative outcomes, e.g. "accuracy gain ≥ 0.02 at ≤ 10% extra time" | Pattern effects in a model-independent unit ("what does enabling the pattern buy, and at what cost?"). **Validity check:** `Model` should score ≈ 0 when scored on the relative outcomes. If it does not, the pattern effects depend on the model, which is itself a finding. |
| **A2-drop** (naive) | Leave `Model` out of the features, keep raw outcomes | Pooled bins | A **control**, not an analysis: the model's effect turns into variability the boxes cannot explain (low-density boxes). This is the RQ4 diagnostic "a factor is missing from the spec", with a known answer. |

**Protocol.**
- Run A2-fix and A2-normalize with the **standard** key-parameter threshold (the base paper's setting) instead of 0.03, and compare the key-parameter sets and rankings with the pooled analysis.
- Report A2-drop only to demonstrate the diagnostic.
- A1 × A2-fix (one pattern, one model, environment varying) is exactly the base paper's setting, and the cleanest analysis for the operating-envelope reading.

**Data requirement.** A2-normalize needs the baseline configuration run at **every** environment point **for each model** (a paired design). [fl_experiment_design.md](fl_experiment_design.md) §3 provides it.

### 4.5 A static tradeoff grid for all comparisons

The ablations compare boxes and densities across slices, so a tradeoff label must mean the same thing in every slice. ADEPT's default discretization does not guarantee this: it recomputes equal-width bins from the minimum and maximum of whatever data the session holds. A `CNN 16k` slice would then redefine `S`/`M`/`L` for itself. The base paper's Table 3 classifies fixed bins as *static*, but they are static per dataset, not across datasets.

**Protocol.**
1. When the campaign is complete, compute each objective's absolute minimum and maximum over the **comparison population**, and freeze the bin edges as explicit numbers (in the notebook and in the paper).
2. Reuse the frozen edges, unchanged, in the pooled analysis and every slice, and in any later data addition (e.g. Tier 3).
3. Make the outer bins open-ended (`(-∞, e₁]`, `(e₂, +∞)`), so a run outside the frozen range is still labelled with the extreme bin instead of being left out.
4. Drop the ±0.1 padding for frozen edges. It is added in objective units, so on F1 it widens the range by 0.2, for data spanning 0.16. On the current data the padded edges are 0.136 / 0.255 / 0.374 / 0.493, which gives an `S` bin that effectively starts at the lowest observed F1 (0.236) and is much narrower in practice than `M`.
5. Once frozen, edges may be rounded to values meaningful to the architect (e.g. accuracy 0.35 / 0.40 / 0.45, or round times of 60 s / 300 s), which turns the grid into a documented requirement rather than a statistical artifact.

**One grid is not enough when a factor spans an order of magnitude.** Round time goes from 17-51 s (`CNN 16k`) to 182-552 s (`squeezenet1_1`) in the current data. With 3 static bins over the whole range (linear edges ~196 s and ~374 s, or log-scaled ~55 s and ~174 s), **every** `CNN 16k` run falls in the first time bin. The within-model effects (e.g. HDH's +32% on `CNN 16k`) are then invisible. The comparison population therefore determines the grid:

| Comparison | Comparison population (defines the frozen edges) |
|:---|:---|
| Pooled analysis, A1 (patterns within the composed system), A2-drop | all runs |
| A2-fix, and A1 × A2-fix (the base paper's setting) | all runs **of that model** (one frozen grid per model) |
| A2-normalize | all runs, on the **relative** outcomes (accuracy gain, time ratio). Model-independent, so one grid covers both models, and edges have a direct reading (e.g. ratio 1.0 / 1.1 / 1.25). |

Within each family the grid is static, so densities and boxes are comparable across all slices of that family. Across families, compare the key parameters and the box conditions, not the densities.

## 5. Research Questions for the Extension

- **RQ1 (composed decisions).** Can ADEPT explain which decisions, and combinations of decisions, of a composed-pattern system achieve a given tradeoff? *(prescriptive boxes; current and new FL data)*
- **RQ2 (conditions).** Can ADEPT infer operating envelopes and conditional prescriptions when decisions and uncertain parameters vary together? *(new FL data; H1-H4)*
- **RQ3 (confounding and shadowing).** How do pooled boxes compare with the ablations: boxes for one pattern at a time (A1) and boxes with the dominant lever fixed or normalized away (A2)? What do the differences reveal about pattern interactions and shadowed effects, and how does this address the base paper's confounding threat? *(§4.4; the current data serves as a negative control, the new data for the analysis)*
- **RQ4 (unexplained variability).** How much of the tradeoff variability is explained by modeled factors versus replication noise, and can low-density boxes flag missing factors? *(replicated runs)*

## 6. Alignment Items Between the Base Paper and the Code

To resolve before, or as part of, the extension (either update the text or the code):

1. **Smart correlation.** Paper: Pearson correlation, keep the feature with the highest variance. Code: Spearman (threshold 0.8), keep the best single-feature Random Forest; exact ties broken alphabetically.
2. **Per-decision discovery.** Paper: PRIM per (tradeoff, decision), CART per decision. Code: `discover_scenarios` pools decisions; per-decision runs are not an API option. Add it (also serves RQ3), or document how the paper's tables were produced.
3. **Split and outliers.** Paper: 70/30 stratified, z-score outlier removal (z = 3). Gateway Offloading notebook: 60/40 with outlier removal; FL: 70/30, random fallback, no outlier removal.
4. **Bin padding.** Equal-width bins are computed over the observed range padded by 0.1 in objective units; significant for 0-1 metrics (utilization, F1). Resolved for the extension by the static grid of §4.5 (no padding for frozen edges); for the re-run of the microservice patterns, use proportional padding or mention it under validity.
5. **Concept table (base paper Table 2).** "Parameter: numeric, predefined range, affected by uncertainty" must be generalized: roles (lever, constraint, uncertainty), types (numeric, categorical), optionality, aggregated instances; plus outcome failure semantics.

## 7. Threats to Validity to Address

- **Small samples.** Boxes validated on 1-4 test runs (current FL data). Mitigation: the new campaign's size and replicated runs; report confidence intervals or bootstrap densities.
- **Dominant factors.** `Model` explains ~90% of feature importance; pattern effects only surface with a low key-parameter threshold. Mitigation: the model ablation A2 (§4.4), reported next to the pooled analysis (RQ3).
- **Encoded categorical parameters.** PRIM and CART run on ordinal codes. The boxes and their metrics are valid under any fixed encoding, but for nominal parameters with three or more values the search is restricted to contiguous code ranges and depends on the code order. This is lossless for FL: every categorical dimension has at most two encoded values, or an intrinsic order. Argument and mitigations in the formal doc §4.1.
- **Small slices.** Ablations analyze subsets: a single-pattern slice for one model has 36 runs in Tier 1 of the experiment design. Mitigation: the extra replicates proposed there for the baseline and single-pattern cells; bootstrap intervals for box density and coverage.
- **Tradeoff definition.** Equal-width bins cut through clusters (the accuracy edges at 0.336 and 0.460 cut through the `CNN 16k` cluster and the `squeezenet1_1` baseline runs; with F1 the boxes differed, §4.2). Mitigation: repeat with threshold- and Pareto-based tradeoffs, as in the base paper's RQ3.
- **Real vs. simulated data.** FL runs are real training executions (with noise), unlike the base paper's queueing models; replication makes the noise explicit.
- **Host resources.** AP4FED runs share one host; resource contention can confound time metrics. Mitigation: the campaign caps allocated cores (see the experiment design).

## 8. Work Plan

| Step | Content | Depends on | Status |
|:---|:---|:---|:---|
| P1 | Conceptual framing (§2), three-layer storyline (§2.4), generalized concept table and conceptual-model figure | - | Draft (this document; formal doc §1) |
| P2 | Resolve alignment items (§6) | - | To do |
| P3 | FL analysis on current data (prescriptive reading, RQ1, RQ3 partial) | ADEPT extensions (§3) | Done in `analysis-fl.ipynb`, switched to and re-run with `final_val_accuracy` × `avg_total_time` (2026-09-30, §4.2); to be condensed for the paper |
| P4 | Run the AP4FED campaign | [fl_experiment_design.md](fl_experiment_design.md) | To do (AP4FED operators) |
| P5 | Ingest new data: spec update, aggregation statistics, notebook | P4, §3 "to do" rows | To do |
| P6 | RQ2 and RQ4 analyses; H1-H5 | P5 | To do |
| P6b | Ablations A1 (single pattern) and A2 (model): slice/normalize views, then RQ3 comparison with the pooled analysis. A1 on the current data as negative control can start now. | P5; slice and relative-outcome support (§3) | To do |
| P7 | Re-run the five microservice patterns with the aligned pipeline, to keep the base results comparable | P2 | To do |
| P8 | Design-space report as the textual-explanation contribution (optional) | report plan | Planned |
| P9 | Writing | P1-P7 | To do |

## 9. Open Questions

- Should the extension keep the five microservice patterns as a baseline section, or focus on FL with the microservices results summarized?
- ~~Which FL tradeoffs matter most to the architect?~~ Resolved (2026-09-30): model accuracy × total round time (§4.1); communication and training time as explanatory metrics, CPU/RAM out of scope. Open: add *time-to-accuracy* (rounds or seconds to reach a target accuracy) as a second view? It needs per-round accuracy logging (experiment design §5).
- Are the client cluster and multi-task model trainer patterns in scope (AP4FED supports them), or only the three analyzed so far?
- Is the design-space report (P8) part of this paper's contribution or a separate tool paper?
