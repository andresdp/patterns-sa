# ADEPT Methodological Framework and Compact FL Experimental Plan

## 1. Purpose and scope

This document aligns ADEPT's conceptual framework with the completed compact federated-learning (FL) campaign and the paper's two research questions. ADEPT connects architectural choices and their declared relationships to observed executions and quality outcomes. Its analyses characterize the sampled design space and discover joint conditions associated with target tradeoffs. They are observational: feature importance and PRIM/CART boxes do not estimate causal effects.

The empirical scope is the compact campaign. The detailed client/round records are outside this analysis and may be used in later work. Numeric client-level fields in the compact records are summarized by means, so client-level imbalance and within-run trajectories are not visible.

## 2. ADEPT as an iterative method

ADEPT links an explicit model of an architecture and its context to execution data, then uses analysis and interpretation to refine the model and study. Its three phases and eight activities are:

| Phase | Step | Activity | Result |
|---|---:|---|---|
| **Model & Collect** | 1 | Define purpose, system boundary, quality concerns, and research questions. | Study scope and outcome definitions |
| | 2 | Describe decisions/policies, settings, context, uncertainties, observations, and outcomes. | Semantic model tied to the system specification |
| | 3 | Execute configurations and retain measurements and provenance. | Run-level observations |
| **Prepare** | 4 | Validate, join, summarize, encode, filter, and document data; derive targets and analysis subsets. | Reproducible analysis data |
| **Analyze & Refine** | 5 | Characterize outcomes and discover conditions for target outcomes. | Descriptive and scenario-discovery results |
| | 6 | Interpret results in architectural terms and assess support and limitations. | Architecture-aware findings |
| | 7 | Refine the model, data, or analysis where evidence warrants it. | Versioned refinement |
| | 8 | Consolidate findings, decisions, provenance, and limitations. | Reproducible report |

The main feedback loop is Steps 4–7: analysis and interpretation may reveal a data or model issue; any resulting change is versioned, re-prepared, and re-analyzed. The compact FL study follows this structure through six scenario notebooks and a cross-scenario synthesis.

## 3. Conceptual model for ADEPT and this study

The model distinguishes what the designer configures, what describes the study context, what varies as operating conditions, what is observed during execution, and what is evaluated as quality. A *configuration* is the joint assignment of policies and their settings; a *scenario* is a filtered analysis population, not a new kind of variable.

| ADEPT concept | Compact FL examples | Role in this study |
|---|---|---|
| **Decision / policy** | Client Selector (CS), Message Compressor (MC), Heterogeneous Data Handler (HDH), each ON or OFF | Architectural alternatives; together they define one of eight configurations |
| **Policy setting** | CS strategy/criteria/value; MC algorithm; HDH settings | Parameters associated with an enabled policy; some are inapplicable when the policy is OFF |
| **Other design settings** | Learning rate, batch size, epochs, rounds | Fixed in the analyzed campaign; not estimated as effects |
| **Chosen context** | Dataset paired with model: CIFAR-10/CNN 16k or AG_NEWS/MLP | Defines the image or text task; dataset and model do not vary independently |
| **Scale/context** | Client count: 4, 8, or 10 | Defines the three client-count slices; these are the study's stress levels |
| **Uncertainties / operating conditions** | Low-spec-client share, non-IID-client share, delayed-client share; related client/resource summaries | Conditions under which a configuration was observed, not architectural prescriptions by default |
| **Execution observations** | Average client CPU/JSD summaries, participation, pattern-instance summaries, measured timing | Describe recorded executions. Derived or post-execution fields are not automatically controllable inputs |
| **Outcomes** | Final validation accuracy (maximize), average total round time (minimize) | Continuous quality measures |
| **Derived target** | Fixed-grid accuracy/time label such as `M-S` | Tradeoff region used for distributions and scenario discovery |

### 3.1 Syntactic relationship model and box explanation

ADEPT's extended box explanation uses only directed relationships declared by the JSON system specification and the conceptual decision/policy model. It traces a low-level box condition to its declared policy or setting context when that relationship exists. It does not add domain-hypothesized influence arrows or claim that a traced “parent” caused the outcome. The relationship graph is explanatory metadata: it supplies context around the statistical conjunction while preserving every original predicate.

For example, if a box contains an enabled CS criterion, the explanation can group the declared strategy, criterion, and value beneath the CS policy, and show environmental predicates as an operating envelope:

```text
Architectural interpretation
• Design prescription:
  • Client Selector = ON
    • Strategy = Resource-Based
    • Criteria = CPU
    • Value = [declared value, subject to metadata validation]
  • Message Compressor = ON
    • Algorithm = zlib
• Operating envelope:
  • non-IID > 25%
  • delay < 50%
```

Each box remains a conjunction. Its listed conditions must be read together; a policy may require particular settings, and the operating conditions qualify the observed association. “No pattern policy is required by the box conditions” means the fitted conjunction contains no such predicate; it does not mean the policy is irrelevant.

There is an unresolved metadata mismatch: compact records with CS ON show `Client Selector Value = 7.0`, while the compact JSON specification binds the ON policy to `2.0`. Until reconciled, reports must preserve the data value for statistical descriptions, flag the discrepancy in architecture explanations, and avoid presenting 2.0 as the executed value. More generally, a JSON relationship can organize an explanation but cannot repair an inconsistent run record.

## 4. Data, scenario, and comparison units

An **execution record** is one compact run with configuration, task, client count, environment fields, outcome metrics, and identifiers/provenance. A **dataset** is the versioned set of those records and its schema and collection metadata. A **subset** is a deterministic filtered set. A **scenario** here is one task/model pair at one client count, viewed in two overlapping ways:

1. **Common-environment:** only the environment point shared by all eight configurations (25% low-spec, 25% non-IID, 25% delayed clients). This supports comparisons at a shared sampled condition.
2. **All-environment:** every available environment record for that task/client-count slice. Configuration coverage is uneven, so design differences may also reflect environment composition.

The two views contain shared runs and are complementary analyses, not independent replications. There are six task/client-count slices: two tasks × three client counts (4, 8, 10). Each notebook analyzes one slice in common-environment then all-environment order.

The campaign contains 2,340 runs: 1,380 baseline/single-pattern and 960 composed-pattern runs. It covers eight ON/OFF configurations and ten `partition_seed` values in each of 234 observed configuration-condition cells. `partition_seed` is used to keep all rows from a seed group together in train/test splitting; the study does not conduct matched-pair contrasts. The campaign has incomplete environmental crossing. The compact representation averages selected numeric client fields and can hide unequal client behavior.

## 5. Experimental methodology

### 5.1 Research questions

**RQ1 — Tradeoff space:** *Which tradeoffs occur, and how do design choices relate to them?*

**RQ2 — Scenario discovery and what-if robustness:** *Which joint conditions identify a target tradeoff, and what changes inside the box?*

RQ1 gives the architect a map of observed quality alternatives and their configuration context. RQ2 asks whether a joint restriction on design and operating conditions yields a higher held-out target frequency, and what design-space coverage that restriction gives up. Neither question asks for a causal effect.

### 5.2 Shared outcome representation

Use final validation accuracy and `avg_total_time` (documented in the campaign as average total round time, training plus communication). Accuracy is maximized; time is minimized. All six notebooks use the same campaign-wide bin edges:

| Objective | Fixed edges | Direction |
|---|---|---|
| Accuracy | 0.2075, 0.4774, 0.7473, 1.0172 | Higher is better |
| Average total round time | 1.5625, 9.5065, 17.4505, 25.3945 | Lower is better |

Labels use `S/M/L` for the low/medium/high numeric bins for each objective; they are not quality ratings. Combined labels (for example, `M-S`) identify a cell in accuracy × time space. The fixed grid supports comparison across scenarios. A quadrant with no observations is empty within the analyzed sample, not an impossible outcome.

### 5.3 RQ1 analysis

For each of six slices and both views, report continuous objective distributions and objective-space plots, tradeoff counts/shares, and configuration-level contingency tables. Show pattern-type count (0, 1, or 2–3 active pattern types) and pattern-instance plots as secondary summaries. Pattern instances depend on configuration and environment, and some are derived or assumed; instance count is not an independently assigned design lever. Identify the complete CS/MC/HDH configuration whenever interpreting a pattern-count association.

RQ1 is descriptive. It uses no feature-importance ranking, PRIM, or CART to support its conclusions. Its purpose is to show what the compact campaign observed, where tradeoffs were populated, and how observed distributions vary with full configurations, task/model context, client count, and environment view. Percentages must be accompanied by counts and interpreted in light of uneven support.

### 5.4 RQ2 analysis

For each non-empty target region in each view, the notebooks use the current ADEPT feature-ranking procedure to screen candidate predictors, then fit PRIM and CART on the training partition. For each objective, a random-forest regressor is fit on training rows with optional pattern parameters included; smart correlation selection removes redundant encoded features, which are restored in the displayed score table with zero. Scores are normalized shares of training impurity reduction. Equal objective weights order the ranking, and a parameter is selected if its score is greater than 0.03 for either objective. Thus a zero may mean constant, pruned as a correlated duplicate, or retained but unused; a feature omitted from discovery may also be below the gate. Importance scores are screening diagnostics, not causal importance or effect direction. Compare trends across task/client-count slices and views, including possible proxies, correlated variables, missingness/availability effects, and unstable rankings.

The grouped split holds out 3 of the 10 `partition_seed` groups, searching candidate holdout groups for a tradeoff-label distribution close to the full slice. This yields 56 train/24 test rows for common-environment views and 273 train/117 test rows for all-environment views. Grouping prevents runs from the same seed group crossing the split; it does not provide external validation because all rows come from the same campaign.

PRIM and CART boxes are conjunctions of feature predicates. Preserve those predicates and their original bounds. Add a compact architectural explanation by tracing only declared JSON/conceptual relationships, grouping related policy settings beneath their decision and uncertainty predicates under an operating envelope. Treat box rules as joint associations in the sampled population.

For every box, report its training-set support, precision/density, coverage/recall, and ADEPT lift (box training precision minus training target prevalence). Separately report held-out baseline target frequency, in-box target frequency, their absolute percentage-point difference, box count and fraction of the held-out scenario retained, and held-out target coverage/recall. These quantities answer different design questions: target frequency indicates observed concentration; retention indicates how much of the scenario the restriction keeps; coverage indicates how many target cases it captures. The what-if is a re-filtering of held-out observed rows under the box rule, not an intervention or causal improvement. A target with no discovered non-empty box is reported as unsupported in that slice/view, not silently omitted.

### 5.5 Reporting for the two stakeholders

**Software architect/designer:** show the target quality region in business terms, the full configuration, the related settings required by its policy, the operating envelope, and the precision/coverage/retention choice. State what could be configured, what could be monitored or constrained operationally, and what is only an observed execution descriptor. Do not recommend a narrow high-precision box without its retained count and missed-target share.

**Researcher:** report fixed bin thresholds, per-slice population and cell support, empty quadrants, train/test grouping, model/ranking settings, box predicates, and test denominators. Distinguish common from all-environment evidence, and treat their overlap and same-campaign holdout explicitly. Use causal language only if supported by a separate identification strategy.

## 6. Current evidence and interpretation

The active cross-scenario conclusions are maintained in [the RQ synthesis](fl_research_question_synthesis.md), with scenario-level results in [the six notebook findings](fl_notebook_findings/README.md).

For RQ1, the common-environment view has only one populated tradeoff region in three of six slices; the 8-client image test partition is entirely `M-M` with only two other training rows. This view is useful for controlled description but often has too little variation for region discovery. Task/model and client count correspond to different observed outcome maps. Pattern-count summaries show some local gradients, including more fast-round `L-S` observations in the 4-client text and image common views, but no universal monotonic relationship. The full configuration and environment context are the appropriate design alternatives to inspect.

For RQ2, all-environment feature rankings repeatedly elevate delay and alpha/resource descriptors; common-view rankings often emphasize configuration-linked features. Repeated boxes associate delay at or below 12.5% with several fast-round targets, but support and target coverage vary. In examples, held-out target frequency reaches 100% while retaining 15/117 rows; coverage ranges from 65.2% for 8-client text `L-S` to 93.8% for 10-client image `M-S`, and 50% in the cited 4-client image CART box. An already-100% common-view target gains no concentration from further restriction. These are useful what-if tradeoffs only when precision, retained space, and coverage are read together.

The campaign cannot establish that changing delay or a pattern policy causes the observed outcome. Feature importance identifies predictive organization in the fitted data, and box restrictions describe conditional frequencies. The designer can use these results to shortlist configurations and operating envelopes for follow-up evaluation; the researcher should treat them as hypotheses for a more controlled/crossed campaign.

## 7. Known limitations and verification items

1. **Policy metadata:** resolve the CS value mismatch (recorded 7.0 vs JSON binding 2.0) before publishing a literal CS value in an architectural prescription.
2. **Timing construct:** verify the precise instrumentation boundary for `avg_total_time`; the compact data documentation calls it average total round time including training and communication.
3. **Training setting:** verify what `Epochs = 1` means in AP4FED before calling it local epochs.
4. **Execution provenance:** document hardware, scheduling/resource isolation, and failure handling from source logs. Compact CSVs show 39 hostnames but do not fully define those controls.
5. **Aggregation:** compact means conceal client-level imbalance and within-run variation; detailed-log analysis is deferred.
6. **Pattern stress:** instance counts are partly assumption-derived and HDH activity differs sharply by task in detailed logs; do not treat the count as a clean randomized factor.
7. **External validity:** the campaign's environmental design is incomplete and its common view is a single shared point. All-environment patterns may combine configuration and environment-composition differences.
8. **Validation:** grouped seed holdout is internal to this campaign. Independent campaign data are needed to assess transfer.

## 8. Reproducible outputs

The maintained analysis sequence is [00–05 in the findings index](fl_notebook_findings/README.md), one notebook per task/client-count slice. Each notebook includes common and all-environment views. The compact data source and execution instructions are in [`federatedlearning/compact/README.md`](../federatedlearning/compact/README.md). The paper synthesis should cite the notebook findings and report exact box-level counts for any selected example.
