# Files

- [Decision impact and tradeoff relationships](decision-impact.md) - Contingency and nearest-tradeoff analyzers explain how configuration decisions map to outcome regions.
- [Explanations and visualization](explanations-and-visualization.md) - Pluggable explanation strategies and validated Matplotlib plotting façade for outcome, box, contingency, and robustness views.
- [Feature importance and sensitivity](feature-importance.md) - FeatureImportanceAnalyzer identifies modeled parameters, handles optional NaNs, preprocesses numeric features, and ranks drivers with Random Forests.
- [Robustness metrics and policy impact](robustness.md) - RobustnessAnalyzer quantifies success, distance from target regions, distance to failures, and the uplift of discovered parameter boxes.
- [Scenario discovery and operating boxes](scenario-discovery.md) - PRIM and CART adapters turn parameter/outcome masks into Box constraints, evaluate density and coverage, and feed what-if robustness analysis.
- [Tradeoff definition and discretization](tradeoffs.md) - DataProcessor converts continuous quality outcomes into categorical regions, schemes, Pareto fronts, and reusable row-index maps.
