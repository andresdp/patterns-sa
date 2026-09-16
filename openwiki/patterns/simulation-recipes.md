---
type: operational recipe
title: Pattern simulation recipes
description: How pattern runners generate JMT models, execute Java simulations in parallel, collect metrics, and feed ADEPT analysis assets.
tags: [patterns, jmt, simulation]
---

# Pattern simulation recipes

The representative runners in `patterns/*/runSim.py` use the same sequence: enumerate parameter products, replace `VAL###` placeholders in a `model.placeholder.jsimg`, invoke `java -cp <jmtpath> jmt.commandline.Jmt sim ...`, parse the generated `.jsim` XML, and append measure means/bounds plus simulation time to a CSV. `multiprocessing.Pool` runs jobs concurrently and a shared `Lock` protects append operations. Temporary model/result files are removed with shell `rm`.

`Gateway_Offloading/runSim.py` derives complementary population/service parameters (for example `nB = N_TOT - nA` and inverse rates) before simulation. `CQRS/separated_HW/runSim.py` and `separated_SW/runSim.py` differ in their parameter grids and output data for the two implementation choices. The Pipes and Filters `joint` and `separated` runners follow the same generated-model contract. Other families expose the same pattern but may rely on `legacy/varEnv.py`-style environment setup.

Prerequisites are Java/OpenJDK, JMT `JMT-singlejar-1.2.2.jar`, a configured `jmtpath`/`NUM_SIM_THREADS`, the family’s placeholder model, and writable working directories. Runners write family-local CSV headers with parameter and measurement names and may overwrite the output CSV at startup. Run from the family directory so placeholder paths and relative imports resolve. Do not run broad parameter products accidentally: inspect ranges and expected row counts first.

The output CSV is then referenced by a family JSON `DataSpace.source_file` or per-configuration `source_file`; notebooks such as `Gateway_Offloading/analysis-go.ipynb` demonstrate loading, discretization, contingency, discovery, robustness, and plots. Generated `model*.jsimg`, `*-result.jsim`, CSVs, PNGs, and `*_boxes*.json` have different ownership and should not be confused with declarative definitions.

Validation is manual: first run a small parameter grid and inspect the CSV header/row count, then load it with `PatternAnalysis` and run focused ADEPT tests. No repository test automatically launches Java, multiprocessing simulation, or notebook execution.
