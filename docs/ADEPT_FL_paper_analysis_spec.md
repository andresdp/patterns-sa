# ADEPT–FL Paper Analysis and Implementation Spec

## Purpose and scope

This document is a handoff for the coding agent working on the current ADEPT–FL paper. It aligns the analysis with the conceptual extension and the paper draft while keeping implementation small enough for the current paper.

The paper studies how three federated-learning architectural pattern decisions relate to accuracy and round time, both individually and in combination. The current campaign contains all eight ON/OFF configurations, three client counts, two tasks, and environmental variation that is not fully crossed across configurations. The analysis should describe comparisons supported by those executed runs.

The paper may present **matched descriptive contrasts** and ADEPT scenario-discovery results. It should not claim causal effects or describe the contrasts as interventions. Causal estimands and intervention semantics are out of scope for this paper.

The current phase uses compact run-level data and ADEPT's across-client summaries: numeric client fields are averaged over recorded values, and categorical fields use distinct-value counts. Detailed client/round behavior is deferred until these compact results are understood. Interpret rules and feature scores at the aggregate-run level; equal means can hide different client distributions, joint conditions, or bottlenecks. Resource-usage averages can cover participants only, whereas resource-allocation averages can cover all recorded clients. Existing detailed-log HDH activity counts are supporting measurements, not a completed detailed analysis. See the formalization's Section 2.1 for the aggregation model.

## Background and formalization

Let the system configuration be

\[
c=(p_{\mathrm{CS}},p_{\mathrm{MC}},p_{\mathrm{HDH}})\in\{0,1\}^3,
\]

where each policy is encoded as 0 (OFF) or 1 (ON). `000` is the all-patterns-off baseline. The eight possible values of `c` are the eight system configurations represented in the combined campaign. A decision is a design question; a policy is one alternative; a configuration assigns one policy to every decision. Additional selectable settings are levers, with fixed ON settings treated as policy bindings.

Let `S = (Task, N)` be context, where `Task` is the image or text task and `N` is the number of clients. Let `U = (low-spec share, non-IID share, delay share)` be the recorded environmental conditions. Let `Y = (accuracy, total round time)` be the primary continuous outcomes. ADEPT's discretized tradeoff label is `T = q(Y)` and remains useful for contingency, robustness, PRIM, and CART analyses.

The observational object is the outcome distribution for the configurations and conditions actually run:

\[
Y\mid C=c,S,U.
\]

The campaign is not a complete crossing of every configuration with every environmental point. Therefore, contrasts are computed only on shared support. A missing configuration-condition cell is reported as unavailable, not inferred.

The simplified definitions and hypothetical influence model are in [paper_adept_formal_extension.md](paper_adept_formal_extension.md). The diagram expresses mechanism hypotheses only; the analysis remains observational. Realized participation, augmentation work, and pattern-instance counts are execution descriptors rather than external uncertainties. Rules on these quantities need a prospective-observability and controllability check before they can be used as design prescriptions. The number of enabled pattern types is a configuration summary, not an independent lever.

### Matched one-factor contrast

For a selected pattern decision `j`, compare two configurations that differ only in `j`, holding the other two pattern decisions fixed. Within each shared setting `s,u,z`, calculate:

\[
\Delta_j(s,u,z)=\overline{Y}_{j=1,s,u,z}-\overline{Y}_{j=0,s,u,z},
\]

where `z` is the recorded partition seed and the companion policies remain fixed in each comparison.

The summary gives the equal-weight mean, minimum, maximum, share of settings with a positive raw difference, and run counts. For accuracy, a positive difference favors ON; for round time, a negative difference favors ON. Report raw differences and support; do not collapse both outcomes into an unlabeled “improvement” sign.

Here “matched” means that the two configurations share values of the selected columns. The compact CSVs contain `partition_seed` and `repeat` (1–10); within each task, client-count, environment, and configuration cell, `partition_seed` values 1–10 occur once each, so the compact campaign supports matching by data-partition seed. `run_id` is unique per run and does not identify corresponding configurations; hostnames vary. Include `partition_seed` in `MATCH_ON` to make the contrast seed-matched, and describe it as matched by partition seed rather than as an unqualified paired-run estimate. This controls the recorded partition seed only; it does not match host, scheduling, or other run conditions.

## Research questions and analysis sequence

The current draft proposes RQ1–RQ4. Keep the questions, but align their answers to the available evidence and avoid overstating what the design supports.

1. **RQ1 — Configuration and tradeoff:** Which complete pattern configurations are associated with the accuracy–round-time tradeoff? Use the all-configurations overview and the six controlled stress slices. Report configuration-level outcome and tradeoff distributions.
2. **RQ2 — Operating conditions, boxes, and what-if robustness:** Which design-space conditions are associated with target tradeoffs, and how does restricting the space to their inferred rules change target robustness? Use the existing PRIM/CART workflow and interpret boxes as prescriptions, operating envelopes, or conditional prescriptions according to the variables they contain. Compare each configuration's unconstrained and box-constrained test-set STARR, report the gain in percentage points, retained scenario fraction/count, and target coverage. The matrices report constrained success rates rather than gains themselves; exclude unsupported cells from improvement claims. Higher target attainment is robustness of tradeoff membership, not by itself a reduction in continuous-outcome variance. Do not frame box constraints as causal effects.
3. **RQ3 — Single-pattern comparisons:** How do individual patterns compare with baseline, and does a pattern's observed difference vary with the other patterns? Use baseline/individual-pattern `vs-baseline` notebooks where there is shared support, plus `others='all'` contrasts in the full-factorial stress slices.
4. **RQ4 — Variability:** What variability remains among runs under the same modeled conditions? Use within-cell run distributions and report run counts. Do not add a new noise-floor model unless the final data has stable replicate/seed identifiers and the paper needs that analysis.

Recommended notebook sequence:

1. `analysis-fl.ipynb`: full-campaign coverage, ADEPT overview, and exploratory results.
2. Baseline and three individual-pattern notebooks: describe the baseline and standalone patterns. Use the `vs-baseline` variants for direct configuration contrasts, restricted to shared task, client count, and environment conditions.
3. Six `stress-c{4,8,10}-{image,text}` notebooks: primary controlled configuration comparisons and pattern-composition contrasts at the common environment point.
4. `allenv` stress notebooks, if retained: describe how observed comparisons vary across environments, after displaying configuration-condition coverage. These support a limited uncertainty-response description, not a fully crossed response-surface claim.

The notebook families can remain generated from the shared analysis notebook. Do not create separate bespoke analysis implementations for each slice.

## Assessment of the attached C4/text notebook

The implementation in `analysis-fl-stress-c4-text.ipynb` is aligned with the formal extension and is conceptually correct as a **matched-condition descriptive contrast**:

- `MATCH_ON` includes Dataset, Total Clients, the three environment-share columns, and `partition_seed` so corresponding data partitions are matched.
- `others='reference'` compares each pattern alone against the all-OFF baseline.
- `others='all'` compares ON and OFF for a pattern at each combination of the other two decisions. This is the right view for asking whether observed differences depend on pattern composition.
- It reports per-setting mean differences, min/max, positive-difference share, and run counts.
- The notebook marks the analysis as descriptive rather than causal.

For this stress notebook, task, client count, and environment are fixed. With `partition_seed` in `MATCH_ON`, `others='reference'` has 10 matched seed-settings per decision, one run per arm at each seed. The `others='all'` analysis has four other-pattern contexts per decision, each with 10 matched seeds. The min/max and positive-difference share therefore describe variation across these 10 seeds within this one task/client/environment point; they are not evidence of consistency across many contexts or environments.

Two interpretation constraints should be retained in the notebook and manuscript:

1. The selected matching columns define comparability. The compact CSV provides `partition_seed`, and the notebook includes it so each contrast compares runs using the same recorded data partition. This does not match host, scheduling, or any unrecorded run conditions.
2. A sign change across the `others='all'` rows is a descriptive indication that the observed contrast differs by composition. Do not label interactions solely from a sign flip, especially when differences are small; show the raw contrasts and support counts.

For a fixed task/client-count/common-environment stress slice, each configuration has 10 runs and the shared partition seeds permit 10 seed-matched contrasts per configuration pair. In `others='reference'`, each pattern-alone contrast is against the baseline; in `others='all'`, each decision has four other-pattern contexts. The equal-weight summary gives each matched seed within a context equal influence. The sign summaries still describe observed seed-matched contrasts and do not establish causality.

## Actionable implementation plan

### Keep and verify the existing ADEPT method

`PatternAnalysis.get_decision_contrasts` already implements the core method in `adept/core/session.py`. Do not build a second contrast engine. Keep the contrast API as the single implementation and adjust the notebook presentation or method documentation only where needed.

For each decision and objective:

1. Identify the two policy arms and the context of the other pattern decisions.
2. Group runs by `MATCH_ON` columns.
3. Retain only groups containing both arms.
4. Calculate arm means, raw treatment-minus-reference differences, and per-arm run counts.
5. Summarize differences equally across matched settings, within each other-pattern context.
6. Present the per-setting results or a compact plot alongside the summary.

For tradeoff labels, the existing optional contrast support may report differences in tradeoff shares. Keep these secondary to continuous accuracy and time differences.

### Minimal notebook changes

1. **Make labels explicit:** call the result “matched-condition contrast” in the notebook guide and output headings. State when matching includes `partition_seed`; do not imply matching on host or other unrecorded factors.
2. **Show the evidence compactly:** retain `settings`, `runs ref`, and `runs treat`; show each matched-setting difference and the partition seed when used. Keep the mean and range. The `>0` summary may remain, but label it “share of matched units with positive raw difference” and explain that positive is not uniformly better across objectives.
3. **Interpret `others='reference'` and `others='all'` separately:** reference is pattern-alone versus baseline. All is the pattern's ON/OFF contrast at each setting of the other decisions. The latter is a composition diagnostic; avoid classifying formal interactions from sign changes alone.
4. **For `allenv` runs:** keep environment variables in `MATCH_ON` and display support counts. Do not silently pool unmatched conditions. If the resulting number of matched settings is too small, report that limitation rather than adding an elaborate model.
5. **Keep the existing ADEPT pipeline:** retain linter, discretized tradeoffs, contingency, robustness, feature ranking, PRIM/CART, and box evaluation. The contrast summary is an additional continuous-outcome view in the sensitivity-analysis phase, before or alongside tradeoff contingency.

6. **Audit feature importance across notebook scopes:** report objective-specific drivers, distinguish constant/pruned/unused zeros, and identify correlated or optional-parameter proxies for decisions. The executed scores are normalized random-forest impurity importance, not causal effects or explained outcome variance. Record which features pass the >0.03-in-either-objective discovery gate. Check consistency under model seeds and held-out predictions before presenting a high-ranked local feature as a reliable driver. Treat JSD availability and logged pattern activity as measurement/exposure issues, and verify policy bindings against the recorded settings. The completed audit is in `docs/fl_feature_importance_audit.md`.

No causal-inference service, intervention abstraction, new scenario-discovery algorithm, or large ADEPT workflow rewrite is required for this paper.

## Alignment with the paper draft and conceptual extension

The approach implements the formal extension's configuration-versus-marginal distinction and its T13 one-factor contrast. It also fits the draft's RQ3 and its Figure 3 addition for matched contrasts. It complements, rather than replaces, the existing ADEPT progression from system modeling to data exploration, sensitivity analysis, and constraint inference.

The paper should describe the contrast layer as an addition within Phase 3 (parameter sensitivity), not as a new causal phase. A compact wording is:

> Because marginal policy groups combine configurations that differ in more than one pattern, we additionally compare configurations that differ in a single pattern decision within shared task, client-count, and environmental settings. We report the mean outcome difference between the two arms within each shared setting, together with support counts, and summarize equally across settings. These are descriptive contrasts over the observed campaign and are not causal effect estimates.

### Required manuscript reconciliation

The draft itself flags that the manuscript's reported 2,340-run campaign and the separate proposed `fl_experiment_design.md` campaign describe different protocols. Before finalizing any results, use the executed campaign records and attached notebooks as the source of truth for run counts, factor levels, seeds, hardware, and analysis claims. Do not combine the proposed future design with the completed campaign. This spec does not assume the proposed campaign was executed.

## Out of scope

- Causal effects, `do()` interventions, potential outcomes, or causal robustness claims.
- A fully crossed environmental response surface or extrapolation to unobserved cells.
- Replacing PRIM/CART, ADEPT tradeoffs, robustness measures, or existing workflow phases.
- A new uncertainty interval or significance-testing framework unless the paper's final analysis requires it and the replication structure is verified.
- Reinterpreting assumed pattern-instance counts as measured quantities; retain the documented assumptions and caveats if pattern stress is reported.

## Completion criteria for the coding handoff

- The coding agent confirms the existing contrast API and its notebook call are the implementation to preserve.
- The notebook clearly distinguishes pattern-alone versus baseline (`others='reference'`) from composition-specific simple contrasts (`others='all'`), and states that matching includes `partition_seed`.
- Each displayed contrast reports the matching columns, number of shared settings, and runs per arm.
- Unsupported configuration-condition comparisons remain absent and are not imputed.
- Text correctly says seed-matched descriptive contrast; it does not claim causal effects or treat partition-seed matching as control for host and other run conditions.
- The paper's reported campaign and notebook analysis agree on executed design details.
