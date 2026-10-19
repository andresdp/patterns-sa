# Findings — analysis-fl-rq-baseline-text

## Scope and support

ADEPT compact FL baseline analysis: AG_NEWS/MLP, all client counts

This notebook analyzes the all-environment baseline (`OFF,OFF,OFF`) for the text task across all sampled client counts (4, 8 and 10). It follows the established ADEPT analysis sequence and uses the fixed campaign-wide tradeoff grid.

- **RQ1 — Baseline tradeoff behavior:** Which accuracy–time regions occur with no pattern enabled, and how do their observed frequencies and outcome distributions vary across client counts and sampled environments?
- **RQ2 — Baseline operating envelopes:** Which joint environmental and run-context conditions are associated with each observed region, and how do PRIM/CART box restrictions change held-out target rates, coverage and stability?

This is a reference behavior profile for the no-pattern configuration; it cannot compare pattern policies. Dataset and model are treated as one paired task context. Results are observational associations. Environmental coverage is uneven, so observed relationships may reflect the sampled environment mix.. # Set project root in path so we can import 'adept' package import sys sys.path.append("../../..") sys.path.append("../..") import contextlib import io import itertools import json import pandas as pd import matplotlib.pyplot as plt from adept import PatternAnalysis from adept.utils.linter import SystemLinter from adept.utils.spec_summary import summarize_system import fl_slices from box_reports import write_box_report # The spec declares how the per-client columns ("Client <N> <field>") are aggregated # into system-level parameters and objectives (dataspace.aggregations, see # adept/utils/aggregation.py); fl_slices.slice_filter only adds the pattern-stress # columns and filters the runs.

The case has **180 runs**: 126 discovery/training and 54 held-out/test. The grouping unit is run-level `partition_seed`; the split is a grouped holdout by `partition_seed` (3 of 10 seed groups held out), with no rare-class fallback reported. The notebook reports a stratification score of `0.000000.`. Client attributes are run-level aggregates. See [split diagnostics](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-18>).

The fixed campaign grid has 9 cells. `L-S` means high validation accuracy and low average total round time; this is the semantic preference (maximize `final_val_accuracy`, minimize `avg_total_time`), set before checking occupancy. It is occupied by 30 / 180 rows overall. Empty cells are unobserved in this slice, not infeasible.

| Partition | N | S-S | S-M | S-L | M-S | M-M | M-L | L-S | L-M | L-L |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 126 | 0 | 0 | 0 | 0 | 0 | 0 | 21 | 105 | 0 |
| Test | 54 | 0 | 0 | 0 | 0 | 0 | 0 | 9 | 45 | 0 |


## RQ1 — Tradeoffs and design allocation

Across the observed rows, the occupied regions are `L-S` (30), `L-M` (150); the remaining cells have zero support. The complete-configuration contingency table and within-group shares are in [Section 5](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-30>). Read those counts as observed allocation within this case: configuration groups and environments are not randomized or fully crossed, and pooled dimensions can change composition. Marginal pattern-count summaries are not substitutes for complete configuration comparisons.

For this slice, the strict target is observed in both partitions and has adequate split support for discovery and an internal held-out check. The objective-space plot corroborates the cell occupancy and bin boundaries: [quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png).

## RQ2 — Joint conditions for the preferred target

The model-relative weighted ranking begins ['delay_percentage', 'non_iid_percentage', 'Total Clients', 'low_spec_percentage', 'CPU Mean', 'Alpha Dirichlet Mean']. It screens candidates; it does not indicate direction or causal influence. The notebook’s actual key-parameter subset and importance output are in [Section 8](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-52>); fixed or scope-aliased variables are excluded as shown there.

For `L-S`, PRIM’s conjunction is **`non_iid_percentage` [25.000, 50.000]; `delay_percentage` [0.000, 12.500]**. This rule states an operating envelope over recorded context; verify the activation mix in the [box report](../boxes/analysis-fl-rq-baseline-text.md). Discovery support: precision 1, target coverage 1, baseline target prevalence 0.1667, lift 0.8333; 21 target runs among 126 training rows, with 21/21 target/retained inside the box. Held-out support: Unrestricted held-out `L-S` rate 0.1667; boxed rate 1; absolute change +83.3 percentage points. The rule retains 9/54 test runs (16.7%) and captures 9/9 targets (coverage 1). Absolute lift over prevalence is 0.8333. Full PRIM/CART conditions are in the [box report](../boxes/analysis-fl-rq-baseline-text.md); the policy-specific baseline/boxed/gain matrices and target-coverage matrix are in [notebook Section 11](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-68>) ([PRIM matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-69>), [PRIM coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-70>), [CART matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-72>), [CART coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb#cell-73>)).

This target has held-out support; the fixed rule is predictive within this grouped split, with coverage and retained support stated above. The conditions are consistent with an operating-envelope interpretation in federated learning, but no association here demonstrates a causal effect or deployment guarantee. Policy matrices are conditional on their displayed policy groups; zeros may mean no support.

## Implications and limits

- **For practitioners:** treat the `L-S` rule as a candidate condition set for a controlled follow-up in the stated task/slice; preserve the listed operating range and measure accuracy and time directly before adopting it.
- **For researchers:** repeat the grouped holdout across seeds or collect a new campaign, report the complete configuration-by-region counts, and test policy/context interactions under a design that separates them.
- **Case limits:** observations are run-level, context mixes are uneven, and stress/instance summaries may be derived. The box predicts membership in this campaign; it neither establishes an intervention effect nor demonstrates reduced continuous-outcome variance.

## Evidence

- Notebook and inline outputs: [analysis notebook](../../../../federatedlearning/compact/text/analysis-fl-rq-baseline-text.ipynb) (split cell 18; allocation Section 5; feature ranking Section 8; discovery Section 9; held-out matrices Section 11).
- Box metrics and architectural interpretation: [box report](../boxes/analysis-fl-rq-baseline-text.md).
- Saved plots: [quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__baseline_OFF_OFF_OFF__clients-all__environment-all.png).
