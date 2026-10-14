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

Before interpreting results, obtain two run inputs from the user: (1) the exact notebook paths or glob patterns to cover, and (2) a scope/stratification guide that maps each selected notebook to its slice and explains how the slices relate (for example, whether they overlap or partition the data). The selected notebook list defines the case count; never assume a fixed number, filename scheme, or stratification design. If either input is missing or ambiguous, ask for it before analysis. Consult [ADEPT framework context](references/adept-framework.md) and [FL domain context](references/federated-learning-domain.md) for interpretation. The current campaign's [notebook stratification and scope guide](../../../federatedlearning/compact/NOTEBOOK_STRATIFICATION.md) is an example/default only; use the run-supplied guide as authority for the current analysis. Use the current notebooks, box reports, plots, and campaign README as the authority for data and results.

## Run

1. From the repository root, build or refresh the input manifest using the notebook set and scope guide supplied for this run. For example, to include every image notebook matching a naming pattern:

   ```sh
   conda run -n perfmodels python .claude/skills/adept-compact-findings/scripts/inventory_inputs.py --task image --scope-guide federatedlearning/compact/NOTEBOOK_STRATIFICATION.md --notebook 'federatedlearning/compact/image/analysis-fl-rq-*-image.ipynb'
   ```

   Supply one or more exact paths or glob patterns with `--notebook`; the resolved set is the complete set of cases for this run. Supply the stratification/scope document with `--scope-guide`. Use `--task image`, `--task text`, or `--task both`; for `both`, the patterns must select notebooks in both task folders. The inventory validates every selected notebook, its two saved plots, and matching box report, and records SHA-256 fingerprints plus the scope-guide fingerprint in each task's `findings/evidence-manifest.json`. Confirm the manifest's notebook list and count match the intended coverage. If any selected input is missing, unexecuted, or failed, stop analysis for the affected task and report the issue. Do not silently use stale or partial evidence.

2. For a refresh, treat any existing findings and synthesis files as stale outputs, not evidence. Do not read, quote, summarize, or use them to guide the new analysis. Read each task's manifest and every selected notebook, its matching box report, and the plots listed by the manifest. Notebook outputs are the primary source for numeric results; box reports supply box-level architectural explanations and metrics; plots corroborate visual patterns. Inspect notebook inline outputs where a result is not represented by a saved PNG. Do not infer precise values from chart pixels when a table or notebook output has the value.

   For RQ2, inspect Section 11's held-out box summary **and** the policy-specific before/boxed/gain and target-coverage matrices. These answer related but different questions: the box summary describes tradeoff membership for the target box, while the matrices describe tradeoff membership within a policy group after filtering. Report the unrestricted test rate, boxed rate, absolute change in percentage points, retained run count/fraction, and target coverage where available. Explain the direction of each comparison in plain language.

3. Recompute one case finding for every selected notebook and a synthesis for each selected task, based on the current source artifacts and supplied stratification guide. Crosscheck each synthesis against the newly derived case findings and primary artifacts, never against a prior synthesis. Analyze image and text independently; do not create a pooled cross-task conclusion unless the user asks for one. Prepare the complete replacement set before overwriting existing outputs, so an interrupted refresh leaves the previous complete set intact. The number of case reports is exactly the number of selected notebooks for that task.

4. Crosscheck every material factual statement against the source artifacts. Cite evidence inline with repository-relative Markdown links, preferably to the notebook section and cell, box report, or plot. Keep recommendations traceable to the observed evidence and name the task/configuration/client-count scope they apply to.

## Output contract

Write only generated analysis artifacts in:

- `federatedlearning/compact/image/findings/`
- `federatedlearning/compact/text/findings/`

For each selected notebook, write `<notebook-stem>-findings.md`. Include:

- Case scope and data support: task, configuration slice, client count scope, environment scope, train/test support, populated/empty target regions.
- Report the total, training, and held-out row counts, plus the tradeoff-region counts (including zeros) in **each** partition. State the grouping unit and whether stratification succeeded or a fallback was used. Do not let an overall distribution stand in for the held-out distribution.
- **RQ1 findings:** concrete outcome-space patterns and their observed relationship to design decisions/policies and the dimensions varied or held fixed in that case. Report any relevant subgroup allocations and denominators, following the supplied scope guide; explain overlaps or pooled dimensions where they affect interpretation.
- **RQ2 findings:** feature-importance trends or anomalies, joint PRIM/CART conditions, compact architectural prescription/envelope, and held-out what-if comparison (unrestricted test baseline, box precision, target recall/coverage, lift, retained support). For every box target, distinguish: no discovery box; a box discovered but no held-out target rows (not test-evaluable); and a box evaluated on held-out targets, noting when support is sparse. Report discovery support and held-out target/retained counts so readers can tell what each metric represents.
- Separate concise implications for practitioners and researchers, with actions conditional on the evidence.
- Limitations specific to this case and links to the supporting notebook outputs, box report, and plots.

For each selected task, write `synthesis-rq1-rq2.md`. Crosscheck all newly derived case reports for that task and the primary artifacts. Organize the synthesis under RQ1 and RQ2. Derive the comparison themes from the supplied stratification guide: describe recurring findings, findings specific to the guide's strata, and evidence gaps without assuming particular branches such as client-count or focal-pattern slices. State what can be concluded for this task, where conclusions do not transfer across cases, and the strongest practitioner and researcher implications. Do not simply concatenate case summaries.

The inventory script owns `evidence-manifest.json`; the analysis owns the findings and synthesis Markdown. Do not delete prior findings before analysis: ignore them as evidence, prepare the complete refreshed set, and then overwrite only the selected case reports and synthesis in the selected task's `findings/` directory. Preserve the manifest, other files, and findings for cases outside the current selection. Do not modify notebooks, plots, box reports, the paper draft, or older synthesis documents.

## Interpretation rules

- Derive each case's fixed, pooled, and varying dimensions from the supplied stratification/scope guide and confirm them against the notebook's actual filters and row counts. Do not infer scope from filename patterns alone.
- Compare like scopes as defined by the guide. Determine whether cases form disjoint partitions, overlapping views, or a mixture before aggregating counts or claiming consistency. Never assume the notebooks partition the full dataset.
- Keep complete configuration/policy groupings distinct from marginal summaries or derived descriptors. Treat a variable as a design decision, uncertainty, outcome, or derived measure according to the system specification and notebook processing, not its label alone.
- Report each case's actual feature set, exclusions, and split diagnostics after reruns. If scope-dependent aliases, missing values, or constant variables affect ranking/discovery, explain their effect using the current notebook evidence.
- Respect the campaign's shared discretization grid. Empty quadrants mean no observed runs in this sample, not impossible outcomes.
- **Discovery metrics are training metrics.** They describe the training partition used for parameter ranking and box fitting. **Held-out metrics are test metrics.** The test partition is separated by `partition_seed` and evaluates the fixed rule on runs not used to discover it. Compare both; high train performance with weaker test performance suggests limited out-of-sample stability.
- Use the notebook's split diagnostics as evidence: report the full region distribution on each side, identify held-out regions with zero target rows as unavailable for evaluation, and never present undefined test precision/recall as zero. A target absent from test can still have a valid discovered box; it simply has no held-out target support for validating that box.
- In this campaign, a rare-class warning disables row-label stratification. When `group_column='partition_seed'` is supplied, the implementation still keeps seeds wholly in one partition and selects among grouped holdouts to best match the region distribution. Describe this as a grouped holdout with a stratification fallback; do not call it a row-random split. Report the notebook's actual split diagnostics rather than inferring the method from the warning text alone.
- Precision is the fraction of box-retained runs in the target; recall/coverage is the fraction of target runs captured by the box. Absolute lift is box precision minus target prevalence in the same partition. Report held-out baseline rate, precision, recall/coverage, lift, and retained/test support together when available.
- In Section 11 policy matrices, a zero in a boxed or gain cell can represent an unsupported cell or no runs retained; it is not evidence of zero risk or an impossible outcome. Check the accompanying target-coverage and retained-count matrices before interpreting it. `None` means no box was found for that target. Do not describe the “test set” matrix as the baseline policy robustness unless it is explicitly the same policy group; the all-patterns-OFF policy is a separate configuration.
- Box filtering is a what-if restriction over already observed held-out runs. Do not claim that it changed the system, reduced variance of continuous outcomes, or guarantees robustness. STARR-style membership stability concerns discrete tradeoff membership only.
- A 100% precision on a small number of runs is narrow evidence. Qualify small support, missing target cases, or unavailable test targets. Do not treat missing metrics as zero.
- Read architectural conditions jointly. Use the box report's design prescription and operating envelope; conditions are not independent effects. Explicitly state whether a box includes NaN/not-selected states when relevant.
- Compact numeric client attributes are aggregated within each run. Conclusions concern this run-level representation and can hide client-level imbalance and round-level variation.
- Feature importance is relative predictive credit in the fitted slice/model. Check recurring ranks and glitches (constant variables, zeroed correlated proxies, omitted parameters, or rank changes); do not describe importance as direction, sensitivity slope, or causal influence.
- State the available support behind every what-if result. A high boxed rate with low retained support or low target coverage is a narrow rule, not broad robustness. When a target is rare or absent in held-out data, say that evaluation is weak or unavailable rather than extrapolating from discovery metrics.
