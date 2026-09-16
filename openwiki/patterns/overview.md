---
type: example catalog
title: Architectural pattern case studies
description: Seven JMT-backed pattern families connect simulation runners and CSV results to ADEPT JSON definitions and notebooks.
tags: [patterns, simulations, case-studies]
---

# Architectural pattern case studies

`patterns/` is an experiment library, not an additional service layer. Each family combines a JMT model/template or generator (`runSim.py`), simulation CSVs, one or more ADEPT JSON definitions, and analysis notebooks. The JSON identifies parameters, configuration policies, and quality objectives; the notebooks consume continuous CSV outcomes through the ADEPT session workflow.

The seven families are:

| Family | Runnable variants/assets | ADEPT/data notes |
|---|---|---|
| `Anti_Corruption_Layer` | `runSim.py`, analysis notebooks, `Anti_Corruption_Layer.json`, PRIM/CART result JSON | ACL queueing model and policy/result analysis |
| `Backends_for_Frontends` | `runSim.py`, notebook, `BackendForFrontend.json` | BFF case study; runner uses legacy simulation support |
| `CQRS` | `separated_HW/runSim.py`, `separated_SW/runSim.py`, `CQRS.json`, notebooks, raw/derived CSVs | hardware/software separation is modeled as two file configurations |
| `Gateway_Aggregation` | `runSim.py`, `Gateway_Aggregation.json`, notebooks, result boxes | aggregation policy/result exploration |
| `Gateway_Offloading` | `runSim.py`, `Gateway_Offloading.json`, notebooks, result boxes | policy column maps three offloading strategies; response time/utilization objectives |
| `Pipes_and_Filters` | `joint/runSim.py`, `separated/runSim.py`, `PipesAndFilters.json`, notebooks | joint/separated implementation variants |
| `Static_Content_Hosting` | `runSim.py`, notebook | older/legacy-style family with less ADEPT JSON coverage |

`cart_boxes-*` and `prim_boxes-*` are generated discovery artifacts, while `results/exp1` and `results/exp2` contain experiment outputs for alternative tradeoff definitions. Keep generated boxes separate from source JSON and raw CSVs; a notebook may consume all three but does not regenerate source models. There is no automated root pytest suite for running Java simulations or validating notebook outputs; treat runners as externally dependent manual workflows. See [simulation recipes](./simulation-recipes.md).

The active ADEPT examples called out by the root README are CQRS, Gateway Aggregation, Gateway Offloading, Anti-Corruption Layer, and Pipes and Filters. `Backends_for_Frontends` and `Static_Content_Hosting` remain inventory items and should not be assumed to have the same current JSON/session maturity.
