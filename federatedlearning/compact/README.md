# Compact FL inputs and notebooks

The [ADEPT-FL guide](../../README.md) explains the research-question mapping, environment setup, and run commands. This directory contains the precomputed FL run data and the corresponding ADEPT system definition.

## Inputs

- `adept_experiments_all_waves.csv`: baseline and single-pattern runs.
- `adept_experiments_all_waves_combinedAP.csv`: combined-pattern runs.
- `FLsystem_compact_all.json`: data schema, parameter definitions, aggregations, and outcomes used by the notebooks.

## Notebooks

Both task directories, `image/` and `text/`, contain the RQ notebooks:

- RQ1: `analysis-fl-rq-stress-only-{client_selector,hdh,message_compressor}-<task>.ipynb`
- RQ2: `analysis-fl-rq-combined-patterns-stress-{25,50,75}-<task>.ipynb`
- RQ3: `analysis-fl-rq-c{4,10}-<task>.ipynb`
- RQ4: `analysis-fl-rq-full-design-<task>.ipynb`

The baseline and c8 notebooks are supplementary analyses. Use `../..` from this directory to reach the repository root, then run the RQ-specific commands shown in the guide.
