# Findings — analysis-fl-rq-combined-patterns-stress-75-text

## Scope and support

ADEPT compact FL combined-pattern analysis: AG_NEWS/MLP — 75% stress, all client counts

This notebook compares every supported non-empty combination of the three pattern decisions at one shared stress level, pooling the available client counts (4, 8, and 10). Every enabled pattern must have the selected stress value; disabled patterns remain OFF. Baseline is outside this analysis. The support table lists all seven possible non-empty combinations and marks absent combinations as unavailable.

- **RQ1 — Configuration tradeoffs:** Which accuracy–time regions occur for each supported pattern combination at 75% stress across the available client counts?
- **RQ2 — Joint operating envelopes:** Which additional conditions describe each observed region, and how do PRIM/CART restrictions change held-out target rates, coverage and stability?

The source campaign has rows for all three single-pattern combinations and all three pairwise combinations at this level. The three-pattern combination is included only when the campaign has matching rows; its support is reported explicitly. Client count and sampled environment vary in this pooled view, so observed differences describe the available campaign envelope and are not isolated causal effects.. # Set project root in path so we can import 'adept' package import sys sys.path.append("../../..") sys.path.append("../..") import contextlib import io import itertools import json import pandas as pd import matplotlib.pyplot as plt from adept import PatternAnalysis from adept.utils.linter import SystemLinter from adept.utils.spec_summary import summarize_system import fl_slices from box_reports import write_box_report # The spec declares how the per-client columns ("Client <N> <field>") are aggregated # into system-level parameters and objectives (dataspace.aggregations, see # adept/utils/aggregation.py); fl_slices.slice_filter only adds the pattern-stress # columns and filters the runs.

The case has **360 runs**: 252 discovery/training and 108 held-out/test. The grouping unit is run-level `partition_seed`; the split is a grouped holdout by `partition_seed` (3 of 10 seed groups held out), with no rare-class fallback reported. The notebook reports a stratification score of `0.000328.`. Client attributes are run-level aggregates. See [split diagnostics](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-18>).

The fixed campaign grid has 9 cells. `L-S` means high validation accuracy and low average total round time; this is the semantic preference (maximize `final_val_accuracy`, minimize `avg_total_time`), set before checking occupancy. It is occupied by 74 / 360 rows overall. Empty cells are unobserved in this slice, not infeasible.

| Partition | N | S-S | S-M | S-L | M-S | M-M | M-L | L-S | L-M | L-L |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Train | 252 | 0 | 0 | 0 | 6 | 8 | 0 | 51 | 176 | 11 |
| Test | 108 | 0 | 0 | 0 | 3 | 1 | 0 | 23 | 76 | 5 |


## RQ1 — Tradeoffs and design allocation

Across the observed rows, the occupied regions are `M-S` (9), `M-M` (9), `L-S` (74), `L-M` (252), `L-L` (16); the remaining cells have zero support. The complete-configuration contingency table and within-group shares are in [Section 5](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-30>). Read those counts as observed allocation within this case: configuration groups and environments are not randomized or fully crossed, and pooled dimensions can change composition. Marginal pattern-count summaries are not substitutes for complete configuration comparisons.

For this slice, the strict target is observed in both partitions and has adequate split support for discovery and an internal held-out check. The objective-space plot corroborates the cell occupancy and bin boundaries: [quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png).

## RQ2 — Joint conditions for the preferred target

The model-relative weighted ranking begins ['Client Selector Criteria', 'non_iid_percentage', 'JSD Mean', 'Pattern Instances', 'delay_percentage', 'Total Clients', 'HDH Instances', 'Pattern Types Active', 'low_spec_percentage', 'CPU Mean', 'Alpha Dirichlet Mean', 'Message Compressor Instances', 'Message Compressor Alg']. It screens candidates; it does not indicate direction or causal influence. The notebook’s actual key-parameter subset and importance output are in [Section 8](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-52>); fixed or scope-aliased variables are excluded as shown there.

For `L-S`, PRIM’s conjunction is **`Client Selector Criteria` {CPU}; `Pattern Instances` [1.000, 1.500]; `delay_percentage` [25.000, 50.000]**. This rule states an operating envelope over recorded context; verify the activation mix in the [box report](../boxes/boxes__task-text__combined-patterns__clients-all__stress-75__environment-all.md). Discovery support: precision 0.8085, target coverage 0.7451, baseline target prevalence 0.2024, lift 0.6061; 51 target runs among 252 training rows, with 38/47 target/retained inside the box. Held-out support: Unrestricted held-out `L-S` rate 0.2130; boxed rate 0.7222; absolute change +50.9 percentage points. The rule retains 18/108 test runs (16.7%) and captures 13/23 targets (coverage 0.5652). Absolute lift over prevalence is 0.5093. Full PRIM/CART conditions are in the [box report](../boxes/boxes__task-text__combined-patterns__clients-all__stress-75__environment-all.md); the policy-specific baseline/boxed/gain matrices and target-coverage matrix are in [notebook Section 11](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-68>) ([PRIM matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-69>), [PRIM coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-70>), [CART matrices](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-72>), [CART coverage](<../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb#cell-73>)).

This target has held-out support; the fixed rule is predictive within this grouped split, with coverage and retained support stated above. The conditions are consistent with an operating-envelope interpretation in federated learning, but no association here demonstrates a causal effect or deployment guarantee. Policy matrices are conditional on their displayed policy groups; zeros may mean no support.

## Implications and limits

- **For practitioners:** treat the `L-S` rule as a candidate condition set for a controlled follow-up in the stated task/slice; preserve the listed operating range and measure accuracy and time directly before adopting it.
- **For researchers:** repeat the grouped holdout across seeds or collect a new campaign, report the complete configuration-by-region counts, and test policy/context interactions under a design that separates them.
- **Case limits:** observations are run-level, context mixes are uneven, and stress/instance summaries may be derived. The box predicts membership in this campaign; it neither establishes an intervention effect nor demonstrates reduced continuous-outcome variance.

## Evidence

- Notebook and inline outputs: [analysis notebook](../../../../federatedlearning/compact/text/analysis-fl-rq-combined-patterns-stress-75-text.ipynb) (split cell 18; allocation Section 5; feature ranking Section 8; discovery Section 9; held-out matrices Section 11).
- Box metrics and architectural interpretation: [box report](../boxes/boxes__task-text__combined-patterns__clients-all__stress-75__environment-all.md).
- Saved plots: [quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png](../../../../federatedlearning/compact/text/plots/quality-space__task-text__combined-patterns__clients-all__stress-75__environment-all__final_val_accuracy-vs-avg_total_time.png); [feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png](../../../../federatedlearning/compact/text/plots/feature-importance__task-text__combined-patterns__clients-all__stress-75__environment-all.png).
