---
type: legacy component
title: Legacy replication and case studies
description: Older JMT replication package and plugin-era analysis code retained for comparison, migration evidence, and historical case studies.
tags: [legacy, migration, case-studies]
---

# Legacy replication and case studies

`legacy/` is reference/replication code, not the current ADEPT composition root. Its three case-study families are `patterns/Toy_Example`, `patterns/AWS_Petshop`, and `patterns/Poli_Milano`, with notebooks, images, model/result assets, and scripts. `legacy/README.md` identifies the seven-pattern ICSA replication package, JMT prerequisite, Java requirement, `varEnv.py`, and family-specific simulation conventions.

`legacy/patterns/Toy_Example/analysis.py` is the most complete executable legacy workflow: it creates a `PatternAnalysis`, loads CSV data, adds programmatic tradeoffs when JSON has none, defines schemes, splits data, generates distribution/objective plots, builds contingency views, ranks policy robustness, computes REGRET, and scores features. `etl.py` normalizes source columns to `param1`, `param2`, `latency`, and `availability`; `generate_notebook.py` and extended robustness tests support that demonstration. AWS Petshop and Poli Milano are separate historical data/model families and should not be assumed to use the current `SystemDefinition` schema.

The legacy tests document compatibility boundaries: `test_analysis_session.py` and `test_behavioral_analysis.py` cover old session behavior; `test_parameter_registry.py` covers registry semantics; `test_pattern_migration.py` covers migration from old pattern representations; `test_toy_plugin.py` covers plugin loading. These tests are valuable when changing compatibility aliases or plugin seams but are not proof that current ADEPT notebooks or JMT runners work.

Migration rule: new work belongs under `adept/` and should use `SystemDefinition`, `GenericDataLoader`, and `PatternAnalysis` as currently implemented. Consult legacy code to understand old names, data shapes, and expected user workflows; verify any claimed compatibility against current exports and focused tests. The top-level `legacy/JMT-singlejar-1.2.2.jar` is a binary runtime asset and should not be modified or inspected as source.
