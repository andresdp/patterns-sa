---
type: analysis component
title: Decision impact and tradeoff relationships
description: Contingency and nearest-tradeoff analyzers explain how configuration decisions map to outcome regions.
tags: [contingency, decisions, tradeoffs]
---

# Decision impact and tradeoff relationships

`ContingencyAnalyzer` resolves a configuration-ID column into decision columns named `component:decision`, with policy IDs as values. It accepts dictionary or list configuration representations, preserves the input index, and left-joins the mapping. `compute_contingency()` groups boolean tradeoff-membership columns by one decision key and supports `population` percentages, `row` percentages, or raw `none` counts. A decision key is currently required; the attempted all-decisions stacking path is deliberately rejected.

`PatternAnalysis.get_policy_contingency_matrix()` prepares this map and target masks for all configured tradeoffs, supports all/train/test subsets, and accepts a decision suffix as an approximate match. Higher-level methods return a policy's tradeoff distribution, variable policies (more than one nonzero tradeoff), deterministic policies (one tradeoff above a threshold), and exclusive tradeoffs (one active policy by raw count). `show_policy_contingency()` delegates the resulting matrix to heatmap or Sankey visualization functions.

`TradeoffAnalyzer.get_nearest_tradeoffs()` ordinal-encodes labels using the caller's `all_labels` ordering, fits scikit-learn `NearestNeighbors`, and returns the available comma-separated tradeoff strings nearest to a reference. Its dimensions must match `outputs`, and `k` must be valid for the available set.

<!-- openwiki: mermaid parse failed and this diagram was converted to a text fence so it does not break rendering. Fix the diagram source and restore the mermaid fence. Parser error: Heuristic: an unescaped angle bracket inside a label breaks rendering; rephrase the label. -->
```text
flowchart LR
  Config[configuration ID column] --> Map[component:decision -> policy]
  Map --> Cross[contingency matrix]
  Labels[tradeoff membership masks] --> Cross
  Cross --> Dist[distribution / deterministic / exclusive queries]
  Regions[categorical tradeoff strings] --> KNN[nearest tradeoffs]
```

Focused evidence: `tests/test_contingency.py` verifies configuration expansion and population normalization; `tests/test_tradeoff_analyzer.py` verifies KNN region selection. Session callers additionally depend on tradeoffs already being defined and on aligned subset indices.
