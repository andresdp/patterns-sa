# Compact FL notebook findings

The active notebook set follows the revised paper scope: **RQ1** describes observed tradeoffs across design alternatives, and **RQ2** studies joint design/operating conditions associated with selected tradeoffs and their what-if robustness. Findings are written for software designers comparing policies and assessing deployment envelopes.

## Notebook execution order

Run these in order. Each notebook executes the **common-environment** analysis first, then the **all-environment** analysis.

| Order | Scenario | Notebook | Findings |
|---:|---|---|---|
| 1 | 4 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c4-image.ipynb](../../federatedlearning/analysis-fl-rq-c4-image.ipynb) | [rq-c4-image.md](rq-c4-image.md) |
| 2 | 4 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c4-text.ipynb](../../federatedlearning/analysis-fl-rq-c4-text.ipynb) | [rq-c4-text.md](rq-c4-text.md) |
| 3 | 8 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c8-image.ipynb](../../federatedlearning/analysis-fl-rq-c8-image.ipynb) | [rq-c8-image.md](rq-c8-image.md) |
| 4 | 8 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c8-text.ipynb](../../federatedlearning/analysis-fl-rq-c8-text.ipynb) | [rq-c8-text.md](rq-c8-text.md) |
| 5 | 10 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c10-image.ipynb](../../federatedlearning/analysis-fl-rq-c10-image.ipynb) | [rq-c10-image.md](rq-c10-image.md) |
| 6 | 10 clients, text (AG_NEWS/MLP) | [analysis-fl-rq-c10-text.ipynb](../../federatedlearning/analysis-fl-rq-c10-text.ipynb) | [rq-c10-text.md](rq-c10-text.md) |

All six notebooks retain the established ADEPT analysis sequence: model/spec review, data splitting, objective distributions and plots, configuration/marginal contingency and robustness, pattern-stress tables and charts, feature ranking, PRIM/CART discovery, architectural box explanations, what-if analysis, box diagnostics, and performance metrics. Matched-pair sections are out of scope. The original 14 notebooks are retained in [`federatedlearning/old-analysis`](../../federatedlearning/old-analysis/README.md).

## Reading the findings

- Tradeoff labels are `<accuracy bin>-<round-time bin>`; `S`, `M`, and `L` denote small, medium, and large values, not good/bad.
- RQ1 tables report how observed runs within a configuration or pattern-count group distribute across regions. They describe associations, not the effect of enabling a pattern.
- A box is a conjunction. Its architectural explanation groups related settings under policy decisions and describes non-pattern limits as an operating envelope. Conditions omitted from the box are unrestricted.
- Held-out precision is the target share among retained runs; coverage/recall is the share of target cases captured. What-if robustness compares target rate before and after restricting to the box. Read gains alongside retained support and coverage.
- Common-environment and all-environment views overlap. The first holds environment shares at a point shared across configurations; the latter contains all sampled environments, whose mix may differ by configuration.
- Compact data average selected client-level numeric values within a run. Per-client imbalance and round-level variation are not visible. Findings are observational and do not establish causality.

For conclusions across all six scenarios, see the [RQ1/RQ2 synthesis](../fl_research_question_synthesis.md).
