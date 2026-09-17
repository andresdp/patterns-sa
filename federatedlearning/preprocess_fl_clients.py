"""Generic per-client column aggregator for federated-learning-style datasets.

This module implements two deliberately separate concerns (per KTD9 in
docs/plans/2026-09-16-1102-feat-federated-learning-adept-support-plan.md):

1. `aggregate_per_client_columns` — a GENERIC mechanism that detects any
   `Client <N> <field>` shaped columns by regex and aggregates them across
   however many client indices are present. It does not know about, or
   hardcode, any specific field name or client count. A different FL-style
   dataset (different client count, different field set) reuses this
   function unmodified.
2. `FIELD_ROLES` (and `preprocess_fl`) — a small, EXPLICIT mapping specific
   to *this* FL formulation's dataset, saying which aggregated fields are
   heterogeneity parameters (uncertainty) versus telemetry objectives
   (quality objectives). dtype alone can't distinguish an input condition
   from a measured outcome (e.g. `CPU` and `CPU Usage Avg` are both
   numeric), so this role assignment stays explicit rather than inferred.
   A differently-shaped FL variation supplies its own mapping.
"""

from __future__ import annotations

import re
from typing import Dict

import pandas as pd

# Matches columns like "Client 1 CPU", "Client 12 Data Distribution", etc.
# Group 1: the client index (unused for aggregation, only for detection).
# Group 2: the field name (everything after "Client <N> ").
CLIENT_COLUMN_PATTERN = re.compile(r"^Client (\d+) (.+)$")


def aggregate_per_client_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Aggregates `Client <N> <field>` columns into per-row summary columns.

    For every field detected across the per-client columns:
      - If the field's columns are numeric, aggregate via
        `.mean(axis=1, skipna=True)` into a new `<field> Mean` column.
      - If the field's columns are non-numeric (categorical/object),
        aggregate via `.nunique(axis=1)` into a new `<field> Diversity`
        column.

    Original columns are preserved; new columns are appended. If no
    `Client <N> <field>`-shaped columns are present, this is a no-op that
    returns the input DataFrame unchanged.

    This function hardcodes no client count and no field name — it works
    purely off the `Client <N> <field>` naming convention.
    """
    # Group matched columns by field name, preserving first-seen order.
    field_to_columns: Dict[str, list] = {}
    for col in df.columns:
        match = CLIENT_COLUMN_PATTERN.match(col)
        if not match:
            continue
        field_name = match.group(2)
        field_to_columns.setdefault(field_name, []).append(col)

    if not field_to_columns:
        return df

    result = df.copy()

    for field_name, cols in field_to_columns.items():
        subset = df[cols]

        # Determine numeric-ness by checking each contributing column's dtype.
        all_numeric = all(pd.api.types.is_numeric_dtype(df[c]) for c in cols)

        if all_numeric:
            result[f"{field_name} Mean"] = subset.mean(axis=1, skipna=True)
        else:
            result[f"{field_name} Diversity"] = subset.nunique(axis=1)

    return result


# --- Explicit field-role mapping (specific to THIS FL formulation) ---
#
# Aggregated <field> names (as produced by aggregate_per_client_columns,
# i.e. the part after "Client N ") mapped to their role:
#   "parameter" -> declared as an `uncertainty` parameter (client
#                  heterogeneity input, R7)
#   "objective" -> declared as a quality objective (usage telemetry
#                  outcome, R8)
#
# This mapping is data-specific: a different FL dataset with a different
# set of per-client fields supplies its own FIELD_ROLES. The aggregation
# mechanism above is unaffected by this mapping.
FIELD_ROLES: Dict[str, str] = {
    "CPU": "parameter",
    "RAM": "parameter",
    "Alpha Dirichlet": "parameter",
    "JSD": "parameter",
    "Data Distribution": "parameter",
    "Data Persistence": "parameter",
    "CPU Usage Avg": "objective",
    "RAM Usage Avg": "objective",
}


def preprocess_fl(df: pd.DataFrame, config_name: str = None) -> pd.DataFrame:
    """Preprocessor hook suitable for `session.load(preprocessor=preprocess_fl)`.

    Applies the generic per-client aggregation (`aggregate_per_client_columns`),
    then drops any aggregated column whose field isn't in `FIELD_ROLES` --
    e.g. a per-client `ID` column matches the same `Client <N> <field>` shape
    as real telemetry but isn't a modeled parameter or objective. This keeps
    `aggregate_per_client_columns` itself fully generic (it hardcodes no
    field names) while `FIELD_ROLES` is what actually decides which
    aggregated fields reach the spec, per KTD9. `config_name` is accepted for
    backward-compatibility with `adept/core/loader.py`'s inspect-based
    preprocessor signature check (it is unused here since FL's spec loads a
    single source file, not per-configuration files).
    """
    aggregated = aggregate_per_client_columns(df)
    new_columns = [c for c in aggregated.columns if c not in df.columns]
    unroled = [c for c in new_columns if c.rsplit(" ", 1)[0] not in FIELD_ROLES]
    if unroled:
        aggregated = aggregated.drop(columns=unroled)
    return aggregated


__all__ = [
    "CLIENT_COLUMN_PATTERN",
    "aggregate_per_client_columns",
    "FIELD_ROLES",
    "preprocess_fl",
]
