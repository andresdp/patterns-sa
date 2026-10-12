# Compact FL notebook findings

The current experiment set addresses two questions for two stakeholder groups: **software architects** comparing design alternatives and assessing deployment conditions, and **researchers** interpreting the evidence and its limits.

- **RQ1 — Tradeoff space:** Which accuracy–round-time regions occur, and how do complete pattern configurations and pattern-count groups relate to them?
- **RQ2 — Operating envelopes:** Which joint design and environmental conditions are associated with target regions, and what robustness/coverage tradeoff follows when a box restricts the evaluated space?

## Execution and findings sequence

Execute the notebooks in this order. Each notebook runs the common-environment view first, followed by the all-environment view.

| Order | Scenario | Notebook | Findings |
|---:|---|---|---|
| 00 | 4 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c4-image.ipynb](../../federatedlearning/analysis-fl-rq-c4-image.ipynb) | [00-c4-image.md](00-c4-image.md) |
| 01 | 4 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c4-text.ipynb](../../federatedlearning/analysis-fl-rq-c4-text.ipynb) | [01-c4-text.md](01-c4-text.md) |
| 02 | 8 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c8-image.ipynb](../../federatedlearning/analysis-fl-rq-c8-image.ipynb) | [02-c8-image.md](02-c8-image.md) |
| 03 | 8 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c8-text.ipynb](../../federatedlearning/analysis-fl-rq-c8-text.ipynb) | [03-c8-text.md](03-c8-text.md) |
| 04 | 10 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c10-image.ipynb](../../federatedlearning/analysis-fl-rq-c10-image.ipynb) | [04-c10-image.md](04-c10-image.md) |
| 05 | 10 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c10-text.ipynb](../../federatedlearning/analysis-fl-rq-c10-text.ipynb) | [05-c10-text.md](05-c10-text.md) |

The six notebooks retain the established ADEPT flow: system/spec review, data splitting, objective distributions and plots, configuration and marginal contingency, robustness, pattern-stress tables and charts, feature importance, PRIM/CART, architectural box interpretation, what-if analysis, box diagnostics, and performance metrics. Matched-pair analysis is outside this paper scope. The previous notebooks are preserved under [`federatedlearning/old-analysis`](../../federatedlearning/old-analysis/README.md).

## Reading the results

- Labels are `<accuracy bin>-<round-time bin>`; `S`, `M`, and `L` mean small, medium, and large values, not quality levels.
- RQ1 contingency and pattern-count percentages are descriptive distributions of observed runs. They do not isolate the causal effect of a pattern.
- A box is a conjunction. Its architectural explanation groups related settings under the policy they imply; operating-envelope conditions describe environmental or workload values observed with the target. Omitted conditions are unrestricted.
- Held-out precision is the target share among retained runs; coverage/recall is the share of target cases captured. The what-if gain is the difference in target rate before and after the restriction. Read it alongside retained run counts and target coverage.
- Common-environment and all-environment views overlap. The common view fixes the shared environmental point; the all-environment view includes the broader sampled mix, which can differ by configuration.
- Compact records average selected client-level numeric values within each run. Findings do not expose client-level imbalance and remain observational; they are not causal estimates or deployment guarantees.

For conclusions crosschecked across all six slices, read the [RQ1/RQ2 synthesis](../fl_research_question_synthesis.md). Earlier findings from the superseded scope are archived in [`old-analysis/`](old-analysis/README.md).
