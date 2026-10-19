---
name: adept-compact-findings
description: Analyze already-executed ADEPT compact federated-learning notebooks, box reports, and plots; create per-notebook RQ1/RQ2 findings and task syntheses.
---

# ADEPT compact findings analysis

Use this skill to refresh or crosscheck findings from the repository's compact FL campaign. The notebooks are expected to have been executed and their plots and box reports generated already. Do not rerun notebooks or regenerate source artifacts as part of the analysis.

The detailed, maintained workflow and interpretation rules are shared with the Claude Code skill. Read these files before analyzing results:

- [Canonical analysis workflow](../../../.claude/skills/adept-compact-findings/SKILL.md)
- [ADEPT framework and artefact interpretation guidance](../../../.claude/skills/adept-compact-findings/references/adept-framework.md)
- [Federated Learning campaign context](../../../.claude/skills/adept-compact-findings/references/federated-learning-domain.md)
- [Recorded RQ1/RQ2 analysis guidelines](../../../docs/adept_analysis_guidelines.md)
- [Notebook stratification and scope tree](../../../federatedlearning/compact/NOTEBOOK_STRATIFICATION.md)

Follow the canonical workflow's evidence checks, scope rules, output contract, and interpretation limits. For RQ1, set preferred regions from metric semantics before checking each notebook's occupied cells. For RQ2, carry those targets forward and treat boxes as predictive architectural rules evaluated with held-out support, crosschecked against FL knowledge. These rules can motivate causal hypotheses but do not prove causation. At each run, provide the exact notebook paths or glob patterns to cover and the Markdown guide that describes the current stratification and each notebook's scope. The supplied notebook set determines the number of case reports; do not assume a fixed count or strategy. Analyze `image` and `text` independently unless the user requests a different grouping. Use the current notebooks, box reports, plots, and campaign README as the authority for results.

Run Python commands in the `perfmodels` conda environment, for example:

```sh
conda run -n perfmodels python .claude/skills/adept-compact-findings/scripts/inventory_inputs.py --task image --scope-guide federatedlearning/compact/NOTEBOOK_STRATIFICATION.md --notebook 'federatedlearning/compact/image/analysis-fl-rq-*-image.ipynb'
```

For example, pass the case inventory and scope guide explicitly:

```sh
conda run -n perfmodels python .claude/skills/adept-compact-findings/scripts/inventory_inputs.py --task image --scope-guide federatedlearning/compact/NOTEBOOK_STRATIFICATION.md --notebook 'federatedlearning/compact/image/analysis-fl-rq-*-image.ipynb'
```

Use `--task text` for the text campaign or `--task both` when supplied notebook patterns cover both. If the inventory reports missing, unexecuted, or failed inputs, stop analysis for the affected task and report the issue. Write analysis only to the selected task's `findings/` directory, preserving unrelated files.
