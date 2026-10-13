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

Follow the canonical workflow's evidence checks, scope rules, output contract, and observational interpretation limits. Analyze `image` and `text` independently. Use the current notebooks, box reports, plots, and campaign README as the authority for results.

Run Python commands in the `perfmodels` conda environment, for example:

```sh
conda run -n perfmodels python .claude/skills/adept-compact-findings/scripts/inventory_inputs.py --task image
```

Use `--task text` for the text campaign or `--task both` when refreshing both. If the inventory reports missing, unexecuted, or failed inputs, stop analysis for the affected task and report the issue. Write analysis only to the selected task's `findings/` directory, preserving unrelated files.
