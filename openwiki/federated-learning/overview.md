---
type: integration guide
title: Federated-learning experiment data

description: Standalone federated-learning preprocessing and ADEPT system-definition variants for policy/configuration analysis with semantic missing values.
tags: [federated-learning, preprocessing, data]
---

# Federated-learning experiment data

`federatedlearning/` is a data-preparation and diagnostic area that reuses ADEPT models but is not a separate ADEPT package. `FLsystem.json` describes a single source layout; `FLsystem_split.json` describes a split/normalized layout. Their CSVs (`FLwithAP_MLdata*.csv`) contain experiment/outcome data and may include missing optional pattern values.

`preprocess_csv.split_ap_list(input_csv, output_csv=None)` assumes semicolon-delimited input and searches for a column containing `AP List`. It converts decimal commas in object columns, removes braces, splits exactly three comma-separated values, and creates `client_selector_pattern`, `message_compressor_pattern`, `hdh_pattern`, and `config_id` by joining those values. It drops the original AP List column and writes comma-delimited output; with no output path it overwrites the input. Malformed/missing AP List or fewer than three parts are not normalized into a safe fallback and can fail, so inspect the input first.

The generated `config_id` is the configuration-identification column used by `GenericDataLoader` to map JSON `SystemConfiguration`/pattern-policy bindings and inject parameter values. The split JSON is designed to make these pattern columns explicit and to preserve NaN/optional behavior for the session audit. Outcome NaNs remain subject to `QualityObjective.nan_policy`; experiment parameter NaNs can be filled or sentinel-transformed according to metadata.

`test_json_validation.py` is a diagnostic script that validates `FLsystem.json`, but it contains hard-coded host paths and should be run only after adapting paths. `test_split_json.py` loads `FLsystem_split.json` through `PatternAnalysis`, prints NaN and pattern/configuration distributions, and is a manual workflow rather than a pure pytest fixture. `test_manual_simple.py` is another end-to-end diagnostic; it references older session method names and a hard-coded working directory, so current `adept/core/session.py` is authoritative.

Safe recipe: copy source CSV, run `python federatedlearning/preprocess_csv.py input.csv output.csv`, inspect generated columns and IDs, validate the selected JSON with `SystemDefinition.model_validate`, then use `PatternAnalysis` from the federated-learning directory. Avoid committing overwritten raw data or machine-specific path edits.
