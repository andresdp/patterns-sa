# Aggregating Per-Instance Columns

**Code:** `adept/utils/aggregation.py` (`aggregate_instance_columns`), applied by `GenericDataLoader`
**Spec:** `dataspace.aggregations` (`InstanceAggregation` in `adept/core/models.py`)
**Tests:** `tests/test_aggregation.py`

## The Problem

Some systems contain several instances of a component, and their datasets record one column per instance and field. The Federated Learning example has 5 clients, each with 9 fields:

```
Client 1 CPU, Client 1 RAM, Client 1 JSD, ..., Client 5 CPU, Client 5 RAM, ...
```

ADEPT's model has a single value per parameter or objective and run, so these columns must be summarized per run before analysis: `CPU Mean`, `JSD Mean`, `Data Distribution Diversity`, and so on.

## Declaring an Aggregation

```json
"dataspace": {
  "aggregations": [
    {
      "pattern": "^Client (\\d+) (.+)$",
      "numeric": ["mean", "std"],
      "categorical": ["nunique"],
      "fields": ["CPU", "RAM", "Data Distribution"]
    }
  ]
}
```

| Key | Meaning | Default |
|:---|:---|:---|
| `pattern` | Regex matching per-instance columns; group 1 = instance id, group 2 = field name | `^Client (\d+) (.+)$` |
| `numeric` | Statistics for numeric fields, across instances, skipping NaN: `mean`, `std`, `min`, `max`, `median` | `["mean"]` |
| `categorical` | Statistics for non-numeric fields: `nunique` (number of distinct values) | `["nunique"]` |
| `fields` | Fields to aggregate | every field matched by `pattern` |

Each statistic produces a `<field> <Statistic>` column: `Mean`, `Std`, `Min`, `Max`, `Median`, and `Diversity` for `nunique`. The original per-instance columns are kept.

**Declaring roles:** the aggregation only computes columns. Whether a summary is a parameter (e.g. `CPU Mean` as an uncertainty) or a quality objective (e.g. `CPU Usage Avg Mean`) is decided the usual way, by declaring it in `system.components.*.parameters` or `dataspace.quality_objectives`. Undeclared summaries stay in `raw_df` but are not analyzed.

## Load Order

`GenericDataLoader` applies, in order: read CSV → `preprocessor` hook → **aggregations** → `column_renames` → policy bindings → lint. Aggregations therefore see the raw column names, and their output can still be renamed.

## Choosing Statistics

`mean` summarizes the typical instance but hides imbalance: clients with CPUs `{1, 1, 1, 1, 9}` and `{2.6, 2.6, 2.6, 2.6, 2.6}` have the same `CPU Mean`. When heterogeneity across instances matters (as in federated learning), add `std`, `min`/`max` or `Diversity` and declare them as parameters. Declaring statistics that are constant across runs only adds low-variance lint warnings.

## Federated Learning Example

`federatedlearning/FLsystem_split.json` declares the aggregation of the 8 client fields it models (6 uncertainties, 2 telemetry objectives), so `session.load()` needs no preprocessor. `federatedlearning/preprocess_fl_clients.py` remains as a thin compatibility wrapper around the same function.
