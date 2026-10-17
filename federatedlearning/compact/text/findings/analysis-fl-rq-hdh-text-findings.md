# Findings — analysis-fl-rq-hdh-text

## Scope and support

ADEPT compact FL HDH-only analysis: AG_NEWS/MLP, all client counts

This notebook analyzes the all-environment single-pattern configuration (`OFF,OFF,ON`) for the text task across all sampled client counts (4, 8 and 10). It follows the established ADEPT analysis sequence and uses the fixed campaign-wide tradeoff grid. No baseline or other pattern configuration is included.

- **RQ1 — Single-pattern tradeoff behavior:** Which accuracy–time regions occur with HDH enabled as the only pattern, and how do their observed frequencies and outcome distributions vary across client counts and sampled environments?
- **RQ2 — Single-pattern operating envelopes:** Which joint design and environmental conditions are associated with each observed region, and how do PRIM/CART box restrictions change held-out target rates, coverage and stability?

This is a profile of one deployable pattern configuration, not a comparison against baseline or other patterns. Dataset and model are treated as one paired task context. Results are observational associations. Environmental coverage is uneven, so observed relationships may reflect the sampled environment mix.. # Set project root in path so we can import 'adept' package import sys sys.path.append("../../..") sys.path.append("../..") import contextlib import io import itertools import json import pandas as pd import matplotlib.pyplot as plt from adept import PatternAnalysis from adept.utils.linter import SystemLinter from adept.utils.spec_summary import summarize_system import fl_slices from box_reports import write_box_report # The spec declares how the per-client columns ("Client <N> <field>") are aggregated # into system-level parameters and objectives (dataspace.aggregations, see # adept/utils/aggregation.py); fl_slices.slice_filter only adds the pattern-stress # columns and filters the runs.

The case has **150 runs**: 105 discovery/training and 45 held-out/test. The grouping unit is run-level `partition_seed`; the split is a grouped holdout by `partition_seed` (3 of 10 seed groups held out), with no rare-class fallback reported. The notebook reports a stratification score of `0.000622.`. Client attributes are run-level aggregates. See [split diagnostics](<../../../../federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#cell-18>).

The fixed campaign grid has 9 cells. `L-S` means high validation accuracy and low average total round time; this is the semantic preference (maximize `final_val_accuracy`, minimize `avg_total_time`), set before checking occupancy. It is occupied by 0 / 150 rows overall. Empty cells are unobserved in this slice, not infeasible.

| Partition | N | S-S | S-M | S-L | M-S | M-M | M-L | L-S | L-M | L-L |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 105 | 0 | 0 | 0 | 0 | 3 | 0 | 0 | 96 | 6 |
| Test | 45 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 42 | 3 |


## RQ1 — Tradeoffs and design allocation

Across the observed rows, the occupied regions are `M-M` (3), `L-M` (138), `L-L` (9); the remaining cells have zero support. The complete-configuration contingency table and within-group shares are in [Section 5](<../../../../federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#cell-30>). Read those counts as observed allocation within this case: configuration groups and environments are not randomized or fully crossed, and pooled dimensions can change composition. Marginal pattern-count summaries are not substitutes for complete configuration comparisons.

For this slice, the strict target is preferred but unobserved; no box can be fit for it in this case. The objective-space plot corroborates the cell occupancy and bin boundaries: [quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).

## RQ2 — Joint conditions for the preferred target

The model-relative weighted ranking begins ['non_iid_percentage', 'Alpha Dirichlet Mean', 'JSD Mean', 'Total Clients', 'delay_percentage', 'CPU Mean', 'low_spec_percentage']. It screens candidates; it does not indicate direction or causal influence. The notebook’s actual key-parameter subset and importance output are in [Section 8](<../../../../federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb#cell-52>); fixed or scope-aliased variables are excluded as shown there.

No PRIM or CART rule was learned for the preferred `L-S` target because it is absent from this slice. Training and held-out target support are both zero, so target precision/recall and held-out validation are unavailable. No alternate target is substituted. The held-out unrestricted `L-S` rate is 0; a boxed precision and target coverage cannot be calculated because the target is absent. Boxes for other occupied regions are documented in the [box report](../boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md).

The held-out partition has no target examples; held-out recall is unavailable, not zero, so validation of the target rule is not possible in this split. The conditions are consistent with an operating-envelope interpretation in federated learning, but no association here demonstrates a causal effect or deployment guarantee. Policy matrices are conditional on their displayed policy groups; zeros may mean no support.

## Implications and limits

- **For practitioners:** treat the `L-S` rule as a candidate condition set for a controlled follow-up in the stated task/slice; preserve the listed operating range and measure accuracy and time directly before adopting it.
- **For researchers:** repeat the grouped holdout across seeds or collect a new campaign, report the complete configuration-by-region counts, and test policy/context interactions under a design that separates them.
- **Case limits:** observations are run-level, context mixes are uneven, and stress/instance summaries may be derived. The box predicts membership in this campaign; it neither establishes an intervention effect nor demonstrates reduced continuous-outcome variance.

## Evidence

- Notebook and inline outputs: [analysis notebook](../../../../federatedlearning/compact/text/analysis-fl-rq-hdh-text.ipynb) (split cell 18; allocation Section 5; feature ranking Section 8; discovery Section 9; held-out matrices Section 11).
- Box metrics and architectural interpretation: [box report](../boxes/boxes__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.md).
- Saved plots: [quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__hdh-only_OFF_OFF_ON__clients-all__environment-all.png).
