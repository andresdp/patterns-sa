# Compact FL notebook findings

The revised paper scope uses two research questions: **RQ1** maps observed tradeoffs across design alternatives, and **RQ2** studies joint conditions associated with selected tradeoffs and their what-if robustness. Findings are written for software designers choosing among pattern policies and assessing the operating conditions under which a tradeoff is stable.

## Notebook execution order

Run each client-count/task slice in this order. Every notebook first analyzes the **common-environment** subset, then the **all-environment** subset.

| Order | Scenario | Notebook | Findings |
|---:|---|---|---|
| 1 | 4 clients, image (CIFAR-10/CNN 16k) | [analysis-fl-rq-c4-image.ipynb](../../federatedlearning/analysis-fl-rq-c4-image.ipynb) | [rq-c4-image.md](rq-c4-image.md) |
| 2 | 4 clients, text | [analysis-fl-rq-c4-text.ipynb](../../federatedlearning/analysis-fl-rq-c4-text.ipynb) | Pending prototype review |
| 3 | 8 clients, image | [analysis-fl-rq-c8-image.ipynb](../../federatedlearning/analysis-fl-rq-c8-image.ipynb) | Pending prototype review |
| 4 | 8 clients, text | [analysis-fl-rq-c8-text.ipynb](../../federatedlearning/analysis-fl-rq-c8-text.ipynb) | Pending prototype review |
| 5 | 10 clients, image | [analysis-fl-rq-c10-image.ipynb](../../federatedlearning/analysis-fl-rq-c10-image.ipynb) | Pending prototype review |
| 6 | 10 clients, text | [analysis-fl-rq-c10-text.ipynb](../../federatedlearning/analysis-fl-rq-c10-text.ipynb) | Pending prototype review |

The c4/image notebook is the restored-style prototype for review. It retains the established sequence of model/spec review, data split, objective distributions, design alternatives, contingency and robustness tables, pattern-stress plots, feature ranking, PRIM/CART discovery, architectural explanations, box diagnostics, and performance metrics. Matched-pair analysis was removed; the analysis is organized around RQ1/RQ2. The other five notebooks and cross-scenario synthesis are not yet updated to this prototype style.

## Reading the findings

- A tradeoff label is `<accuracy bin>-<round-time bin>`; `S`, `M`, and `L` denote small, medium, and large values. Read them against each objective’s direction.
- RQ1 contingency percentages show how observed runs for a configuration or pattern-count group distribute across tradeoff regions. These are associations, not effects of enabling a pattern.
- An architectural box is a conjunction. Its explanation groups low-level pattern parameters under the related policy and presents non-pattern conditions as the operating envelope. Variables absent from a box are unrestricted.
- Held-out box precision is target share among retained runs; coverage/recall is the share of target runs retained. What-if robustness compares target share before and after restricting to the box and reports the retained run count. Interpret gains alongside coverage and support.
- The common-environment and all-environment views overlap. The former holds environment shares at the point common to all configurations; the latter includes all sampled environments, whose mix can differ by configuration.
- Compact records average selected client-level numeric fields within each run. They cannot show client-level imbalance or per-round behavior. The findings describe run-level associations and do not support causal claims.

## Previous findings archive

The earlier broad-scope summaries remain in this directory as historical material. They include matched-pair comparisons and the prior RQ framing; they are not the findings for the revised two-question experiment plan. The new sequence above is the active plan.
