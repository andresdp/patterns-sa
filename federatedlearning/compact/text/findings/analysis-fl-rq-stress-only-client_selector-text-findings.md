# Findings — analysis-fl-rq-stress-only-client_selector-text

## Scope and support

ADEPT compact FL Client Selector stress-only analysis: AG_NEWS/MLP, all client counts

This notebook analyzes the all-environment image runs with **Client Selector ON and both other patterns OFF**. Client counts (4, 8, and 10) are pooled. Objective-space colors identify the focal pattern-stress percentages, in increasing severity order.

- **RQ1 — Stress-conditioned tradeoffs:** Which accuracy–time regions occur at each observed Client Selector stress level, and how do their run and tradeoff distributions compare?
- **RQ2 — Stress-aware operating envelopes:** Which joint architectural and environmental conditions, including Client Selector stress, are associated with each observed region? How do PRIM/CART restrictions change held-out target rates, coverage, and stability?

The focal pattern's stress percentage equals its matching environment percentage in these runs. Feature ranking and box discovery use the pattern-specific feature and exclude that duplicate environment column. These are observational associations, not causal effects.. # Set project root in path so we can import 'adept' package import sys sys.path.append("../../..") sys.path.append("../..") import contextlib import io import itertools import json import pandas as pd import matplotlib.pyplot as plt from adept import PatternAnalysis from adept.utils.linter import SystemLinter from adept.utils.spec_summary import summarize_system import fl_slices from box_reports import write_box_report # The spec declares how the per-client columns ("Client <N> <field>") are aggregated # into system-level parameters and objectives (dataspace.aggregations, see # adept/utils/aggregation.py); fl_slices.slice_filter only adds the pattern-stress # columns and filters the runs.

The case has **150 runs**: 105 discovery/training and 45 held-out/test. The grouping unit is run-level `partition_seed`; the split is a grouped holdout by `partition_seed` (3 of 10 seed groups held out), with no rare-class fallback reported. The notebook reports a stratification score of `0.000277.`. Client attributes are run-level aggregates. See [split diagnostics](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-18>).

The fixed campaign grid has 9 cells. `L-S` means high validation accuracy and low average total round time; this is the semantic preference (maximize `final_val_accuracy`, minimize `avg_total_time`), set before checking occupancy. It is occupied by 68 / 150 rows overall. Empty cells are unobserved in this slice, not infeasible.

| Partition | N | S-S | S-M | S-L | M-S | M-M | M-L | L-S | L-M | L-L |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 105 | 0 | 0 | 0 | 3 | 0 | 0 | 48 | 54 | 0 |
| Test | 45 | 0 | 0 | 0 | 1 | 0 | 0 | 20 | 24 | 0 |


## RQ1 — Tradeoffs and design allocation

Across the observed rows, the occupied regions are `M-S` (4), `L-S` (68), `L-M` (78); the remaining cells have zero support. The complete-configuration contingency table and within-group shares are in [Section 5](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-30>). Read those counts as observed allocation within this case: configuration groups and environments are not randomized or fully crossed, and pooled dimensions can change composition. Marginal pattern-count summaries are not substitutes for complete configuration comparisons.

For this slice, the strict target is observed in both partitions and has adequate split support for discovery and an internal held-out check. The objective-space plot corroborates the cell occupancy and bin boundaries: [quality-space__task-text__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__stress-ONLY-client_selector__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__stress-ONLY-client_selector__clients-all__environment-all.png).

## RQ2 — Joint conditions for the preferred target

The model-relative weighted ranking begins ['Client Selector Stress Percentage', 'Alpha Dirichlet Mean', 'CPU Mean', 'non_iid_percentage', 'Total Clients', 'delay_percentage']. It screens candidates; it does not indicate direction or causal influence. The notebook’s actual key-parameter subset and importance output are in [Section 8](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-52>); fixed or scope-aliased variables are excluded as shown there.

For `L-S`, PRIM’s conjunction is **`CPU Mean` [8.000, 8.875]; `non_iid_percentage` [25.000, 50.000]; `delay_percentage` [25.000, 50.000]**. This rule states an operating envelope over recorded context; verify the activation mix in the [box report](../boxes/boxes__task-text__stress-ONLY-client_selector__clients-all__environment-all.md). Discovery support: precision 0.8571, target coverage 0.3750, baseline target prevalence 0.4571, lift 0.4000; 48 target runs among 105 training rows, with 18/21 target/retained inside the box. Held-out support: Unrestricted held-out `L-S` rate 0.4444; boxed rate 0.7778; absolute change +33.3 percentage points. The rule retains 9/45 test runs (20.0%) and captures 7/20 targets (coverage 0.3500). Absolute lift over prevalence is 0.3333. Full PRIM/CART conditions are in the [box report](../boxes/boxes__task-text__stress-ONLY-client_selector__clients-all__environment-all.md); the policy-specific baseline/boxed/gain matrices and target-coverage matrix are in [notebook Section 11](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-68>) ([PRIM matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-69>), [PRIM coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-70>), [CART matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-72>), [CART coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb#cell-73>)).

This target has held-out support; the fixed rule is predictive within this grouped split, with coverage and retained support stated above. The conditions are consistent with an operating-envelope interpretation in federated learning, but no association here demonstrates a causal effect or deployment guarantee. Policy matrices are conditional on their displayed policy groups; zeros may mean no support.

## Implications and limits

- **For practitioners:** treat the `L-S` rule as a candidate condition set for a controlled follow-up in the stated task/slice; preserve the listed operating range and measure accuracy and time directly before adopting it.
- **For researchers:** repeat the grouped holdout across seeds or collect a new campaign, report the complete configuration-by-region counts, and test policy/context interactions under a design that separates them.
- **Case limits:** observations are run-level, context mixes are uneven, and stress/instance summaries may be derived. The box predicts membership in this campaign; it neither establishes an intervention effect nor demonstrates reduced continuous-outcome variance.

## Evidence

- Notebook and inline outputs: [analysis notebook](../../../../federatedlearning/compact/text/analysis-fl-rq-stress-only-client_selector-text.ipynb) (split cell 18; allocation Section 5; feature ranking Section 8; discovery Section 9; held-out matrices Section 11).
- Box metrics and architectural interpretation: [box report](../boxes/boxes__task-text__stress-ONLY-client_selector__clients-all__environment-all.md).
- Saved plots: [quality-space__task-text__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__stress-ONLY-client_selector__clients-all__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__stress-ONLY-client_selector__clients-all__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__stress-ONLY-client_selector__clients-all__environment-all.png).
