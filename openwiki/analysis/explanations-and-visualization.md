---
type: analysis component
title: Explanations and visualization
description: Pluggable explanation strategies and validated Matplotlib plotting façade for outcome, box, contingency, and robustness views.
tags: [visualization, explanations, matplotlib]
---

# Explanations and visualization

`ExplanationManager` selects a strategy by name, defaulting or falling back to `TemplateExplainerStrategy`. The template accepts dictionary artifacts, emits a line-oriented summary, and derives an eight-character SHA-1 `explain_id` from stable JSON serialization. `IExplanationStrategy` is the extension seam: implement `explain(artifact, context)` and register the class in the manager's `_strategies` map; `ArchSpaceCore.explain()` is the consumer façade.

`VisualizationManager` validates common DataFrame/scheme inputs and metric names, then delegates to functions in `adept/analysis/visualization.py`. Public routes include tradeoff distributions, quality-objective scatter plots with overlays, stability-radius views, robustness heatmaps/comparisons/uplifts, and box diagnostics. `PatternAnalysis` prepares policy series, tradeoff masks, subset selection, and annotation summaries before calling the manager.

The plotting contract is `matplotlib.figure.Figure`. Empty/non-DataFrame outcomes, empty schemes, or missing x/y metrics become `VisualizationError` at manager boundaries. Visual methods do not own analysis state; they consume already-created schemes, masks, boxes, and matrices. The narrow extension surface is therefore implementation function + manager delegation + coordinator/session method, with the plotting test as the consumer-facing check.

Focused evidence: `tests/test_explanation_manager.py` covers template output and strategy fallback; visualization behavior is exercised indirectly through `tests/test_archspace_core.py` and session tests. Use a non-interactive Matplotlib backend in CI and close figures in new tests. The existing `docs/analysis_journey.md` describes intended user questions but may mention older method names; current signatures in `session.py` are authoritative.
