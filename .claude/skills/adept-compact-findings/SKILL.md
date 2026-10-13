---
name: adept-compact-findings
description: Analyze already-executed ADEPT compact federated-learning notebooks, box reports, and plots to produce per-notebook RQ1/RQ2 findings plus image and text syntheses.
---

# ADEPT compact findings analysis

Use this skill when the user asks to refresh or crosscheck research findings from the compact FL campaign. The notebooks are assumed to have already been executed and their plots and box reports generated. Do not rerun notebooks or regenerate source artifacts as part of this analysis.

The analysis serves **software architecture researchers and software architecture practitioners who know federated learning**. Use domain terms such as non-IID share, client selector, participation, and round time without introductory tutorials. Explain ADEPT-specific terms when they affect a conclusion. For practitioners, translate observed patterns into design or operating-envelope guidance. For researchers, state evidence, support, cross-case consistency, and limits to transfer. Address both audiences without repeating the same conclusion twice.

## Research questions

Use the current notebook wording and analyze both questions in every case:

- **RQ1 — Which tradeoffs occur, and how do design choices relate to them?** Describe populated and empty accuracy–time regions, outcomes across complete pattern configurations, relevant contingency/robustness evidence, and pattern-stress summaries. Distinguish a configuration choice from a pattern-count or instance-count grouping.
- **RQ2 — Which joint conditions identify a target tradeoff, and what changes inside the box?** Synthesize feature rankings, PRIM/CART rules, their architectural interpretations, NaN/not-selected coverage, and box-restricted held-out what-if results. State where no box was found or evaluation support is weak.

These are observational questions. A box is a joint association over design and operating conditions; its architectural interpretation supplies specification context, not a causal explanation. Avoid causal wording such as “causes,” “improves because,” or “effect of a pattern.”

Before interpreting notebook results, consult [ADEPT framework context](references/adept-framework.md) and [FL domain context](references/federated-learning-domain.md). The ADEPT reference contains domain-agnostic diagnostic guidance for the two primary evidence artefacts: objective-space allocations and scenario-discovery boxes. Apply that guidance even when the current campaign uses FL-specific names. Use the FL note to explain this study's setting; use current notebooks, box reports, and campaign README as the authority for the actual experiment, data, and results.

## Run

1. From the repository root, build or refresh the input manifest for the requested task(s):

   ```sh
   conda run -n perfmodels python .claude/skills/adept-compact-findings/scripts/inventory_inputs.py --task both
   ```

   Use `--task image` or `--task text` for a single task. The inventory checks the seven expected executed notebooks, their two saved plots, and their matching box reports; it records SHA-256 fingerprints and writes `evidence-manifest.json` in each task's `findings/` folder. If it reports missing, unexecuted, or failed inputs, stop analysis for the affected task and report the issue. Do not silently use stale or partial evidence.

2. Read each task's manifest, all seven notebooks, seven box reports, and the plots listed by the manifest. Notebook outputs are the primary source for numeric results; box reports supply box-level architectural explanations and metrics; plots corroborate visual patterns. Inspect notebook inline outputs where a result is not represented by a saved PNG. Do not infer precise values from chart pixels when a table or notebook output has the value.

   For RQ2, inspect Section 11's held-out box summary **and** the policy-specific before/boxed/gain and target-coverage matrices. These answer related but different questions: the box summary describes tradeoff membership for the target box, while the matrices describe tradeoff membership within a policy group after filtering. Report the unrestricted test rate, boxed rate, absolute change in percentage points, retained run count/fraction, and target coverage where available. Explain the direction of each comparison in plain language.

3. Write one findings file per notebook and one synthesis per task using the output contract below. Analyze image and text independently; do not create a pooled cross-task conclusion unless the user asks for one.

4. Crosscheck every material factual statement against the source artifacts. Cite evidence inline with repository-relative Markdown links, preferably to the notebook section and cell, box report, or plot. Keep recommendations traceable to the observed evidence and name the task/configuration/client-count scope they apply to.

## Output contract

Write only generated analysis artifacts in:

- `federatedlearning/compact/image/findings/`
- `federatedlearning/compact/text/findings/`

For each of the seven notebooks in a task, write `<notebook-stem>-findings.md`. Include:

- Case scope and data support: task, configuration slice, client count scope, environment scope, train/test support, populated/empty target regions.
- **RQ1 findings:** concrete outcome-space patterns and their observed relationship to configuration, decisions/policies, client count, or pattern-stress groups. Report denominators when using percentages.
- **RQ2 findings:** feature-importance trends or anomalies, joint PRIM/CART conditions, compact architectural prescription/envelope, and held-out what-if comparison (unrestricted test baseline, box precision, target recall/coverage, lift, retained support).
- Separate concise implications for practitioners and researchers, with actions conditional on the evidence.
- Limitations specific to this case and links to the supporting notebook outputs, box report, and plots.

For each task, write `synthesis-rq1-rq2.md`. Crosscheck that task's seven per-notebook reports. Organize the synthesis under RQ1 and RQ2, and for each RQ distinguish recurring findings, configuration/client-count-specific findings, and evidence gaps. State what can be concluded for this task, where conclusions do not transfer across its cases, and the strongest practitioner and researcher implications. Do not simply concatenate case summaries.

The inventory script owns `evidence-manifest.json`; the analysis owns the findings and synthesis Markdown. On a refresh, replace only those generated files in the selected task's `findings/` directory. Preserve other files and any findings outside those directories. Do not modify notebooks, plots, box reports, the paper draft, or older synthesis documents.

## Interpretation rules

- Compare like scopes. The `c4`, `c8`, and `c10` notebooks isolate one client count and include all configurations. Baseline and single-pattern notebooks retain all client counts; treat those as configuration profiles, not as direct substitutes for a client-count-specific comparison.
- Keep complete configurations distinct from marginal pattern summaries. `Pattern Types Active` is a configuration-level count; `Pattern Instances` also varies with run context and is a stress descriptor, not a directly assigned policy.
- Respect the campaign's shared discretization grid. Empty quadrants mean no observed runs in this sample, not impossible outcomes.
- **Discovery metrics are training metrics.** They describe the training partition used for parameter ranking and box fitting. **Held-out metrics are test metrics.** The test partition is separated by `partition_seed` and evaluates the fixed rule on runs not used to discover it. Compare both; high train performance with weaker test performance suggests limited out-of-sample stability.
- Precision is the fraction of box-retained runs in the target; recall/coverage is the fraction of target runs captured by the box. Absolute lift is box precision minus target prevalence in the same partition. Report held-out baseline rate, precision, recall/coverage, lift, and retained/test support together when available.
- In Section 11 policy matrices, a zero in a boxed or gain cell can represent an unsupported cell or no runs retained; it is not evidence of zero risk or an impossible outcome. Check the accompanying target-coverage and retained-count matrices before interpreting it. `None` means no box was found for that target. Do not describe the “test set” matrix as the baseline policy robustness unless it is explicitly the same policy group; the all-patterns-OFF policy is a separate configuration.
- Box filtering is a what-if restriction over already observed held-out runs. Do not claim that it changed the system, reduced variance of continuous outcomes, or guarantees robustness. STARR-style membership stability concerns discrete tradeoff membership only.
- A 100% precision on a small number of runs is narrow evidence. Qualify small support, missing target cases, or unavailable test targets. Do not treat missing metrics as zero.
- Read architectural conditions jointly. Use the box report's design prescription and operating envelope; conditions are not independent effects. Explicitly state whether a box includes NaN/not-selected states when relevant.
- Compact numeric client attributes are aggregated within each run. Conclusions concern this run-level representation and can hide client-level imbalance and round-level variation.
- Feature importance is relative predictive credit in the fitted slice/model. Check recurring ranks and glitches (constant variables, zeroed correlated proxies, omitted parameters, or rank changes); do not describe importance as direction, sensitivity slope, or causal influence.
- State the available support behind every what-if result. A high boxed rate with low retained support or low target coverage is a narrow rule, not broad robustness. When a target is rare or absent in held-out data, say that evaluation is weak or unavailable rather than extrapolating from discovery metrics.
