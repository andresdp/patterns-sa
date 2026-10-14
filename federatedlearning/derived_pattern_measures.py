"""Derived pattern measures for a federated learning run.

The module derives measures from the configuration and client columns. It does not parse
the source CSV's categorical `pattern_stress` field (e.g. `CS=25%` or `none`).

Two measures (see compact/README.md, "Derived pattern measures"):

* `Pattern Types Active` (S_types, 0-3): how many of the three pattern decisions are ON,
  read from `config_id`. It depends on the configuration only.
* `Pattern Instances` (S_inst): how many pattern instances are deployed, i.e. the sum of
  `Client Selector Instances`, `Message Compressor Instances` and `HDH Instances`. The
  same pattern type can have several instances (e.g. one per client), so S_inst also
  depends on the client environment (how many clients participate, how many are non-IID)
  and on the other decisions (the client selector removes clients, and their instances).

`Pattern Instances` is a derived deployment-size measure;
`Pattern Types Active` is secondary but exact. The compact CSVs do not record instances, so they are
derived from the per-client columns with the deployment rules in INSTANCE_RULES, which are
ASSUMPTIONS about AP4FED (compact/README.md lists them with the open questions):

  A1. Client selector: one instance, on the server.
  A2. Message compressor: one instance per participating client (the server-side
      decompression is not counted).
  A3. HDH: one instance per participating non-IID client.
  A4. A client participates iff it exists in the run (index <= Total Clients) and its
      `CPU Usage Avg` is recorded. Verified on the compact data: with the client selector
      ON, the participants are exactly the clients that are not low-spec; with it OFF,
      every client participates.

HDH instances can be MEASURED instead of assumed: the per-round data in `detailed/` (one
row per client and round, linked by `run_id`) records `HDH Time`, and A3 does not hold for
the image task, where HDH almost never runs. `load_measured_hdh()` counts, per run, the
participating clients with HDH Time > 0; `add_derived_pattern_measures(df, measured_hdh=...)` uses
those counts for the runs they cover and A3 for the others.
"""
from __future__ import annotations

import functools
import os
import re
from typing import Dict, Iterable, Optional

import pandas as pd

CONFIG_COLUMN = "config_id"
CLIENTS_COLUMN = "Total Clients"
CLIENT_COLUMN = re.compile(r"^Client (\d+) (.+)$")

# Order of the decisions in config_id
PATTERNS = ("client_selector", "message_compressor", "hdh")

INSTANCE_COLUMNS = {
    "client_selector": "Client Selector Instances",
    "message_compressor": "Message Compressor Instances",
    "hdh": "HDH Instances",
}
# Per-round data (one row per client and round), not in git because of its size
DETAILED_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "detailed")
DETAILED_FILES = ("adept_experiments_all_waves_client_rounds.csv",
                  "adept_experiments_all_waves_combinedAP_client_rounds.csv")
RUN_COLUMN = "run_id"

TYPES_COLUMN = "Pattern Types Active"
INSTANCES_COLUMN = "Pattern Instances"
PARTICIPANTS_COLUMN = "Participating Clients"


def _client_frame(df: pd.DataFrame, field: str) -> pd.DataFrame:
    """Per-client values of a field, one column per client index."""
    cols = {int(m.group(1)): c for c in df.columns for m in [CLIENT_COLUMN.match(str(c))] if m and m.group(2) == field}
    return pd.DataFrame({i: df[c] for i, c in sorted(cols.items())}, index=df.index)


def active_patterns(df: pd.DataFrame) -> pd.DataFrame:
    """One boolean column per pattern: whether its decision is ON in the run."""
    parts = df[CONFIG_COLUMN].astype(str).str.split(",", expand=True)
    if parts.shape[1] != len(PATTERNS):
        raise ValueError(f"'{CONFIG_COLUMN}' must hold {len(PATTERNS)} comma-separated policies.")
    return pd.DataFrame({p: parts[i].str.strip() == "ON" for i, p in enumerate(PATTERNS)}, index=df.index)


def participating_clients(df: pd.DataFrame) -> pd.DataFrame:
    """Boolean per client: it exists in the run and records CPU usage (assumption A4)."""
    usage = _client_frame(df, "CPU Usage Avg")
    exists = pd.DataFrame({i: df[CLIENTS_COLUMN] >= i for i in usage.columns}, index=df.index)
    return usage.notna() & exists


def non_iid_clients(df: pd.DataFrame) -> pd.DataFrame:
    """Boolean per client: its data distribution is non-IID."""
    return _client_frame(df, "Data Distribution").apply(lambda col: col.astype(str).str.lower() == "non-iid")


# Deployment rules (assumptions A1-A3): instances of each pattern in a run where it is ON
INSTANCE_RULES = {
    "client_selector": lambda df, part: pd.Series(1, index=df.index),
    "message_compressor": lambda df, part: part.sum(axis=1),
    "hdh": lambda df, part: (part & non_iid_clients(df).reindex(columns=part.columns, fill_value=False)).sum(axis=1),
}


def measured_hdh_instances(rounds: pd.DataFrame) -> pd.Series:
    """Per run: participating clients that did HDH work (HDH Time > 0) in some round."""
    worked = rounds["HDH Time"].fillna(0) > 0
    if "participated" in rounds.columns:
        worked &= rounds["participated"].astype(str).str.lower() == "true"
    return rounds[worked].groupby(RUN_COLUMN)["Client ID"].nunique().reindex(
        rounds[RUN_COLUMN].unique(), fill_value=0).astype(int)


@functools.lru_cache(maxsize=4)
def _load_measured_hdh(paths: tuple) -> Optional[pd.Series]:
    found = [p for p in paths if os.path.exists(p)]
    if not found:
        return None
    columns = [RUN_COLUMN, "Client ID", "HDH Time", "participated"]
    return measured_hdh_instances(pd.concat([pd.read_csv(p, usecols=columns) for p in found]))


def load_measured_hdh(paths: Optional[Iterable[str]] = None) -> Optional[pd.Series]:
    """Measured HDH instances per run_id from the per-round CSVs, or None if none is found.

    Args:
        paths: The per-round CSVs (default: DETAILED_FILES in DETAILED_DIR).
    """
    if paths is None:
        paths = [os.path.join(DETAILED_DIR, f) for f in DETAILED_FILES]
    return _load_measured_hdh(tuple(paths))


def add_derived_pattern_measures(df: pd.DataFrame, measured_hdh: Optional[pd.Series] = None) -> pd.DataFrame:
    """Adds derived pattern-measure columns (the original columns are kept).

    Args:
        df: Runs with `config_id`, `Total Clients` and the per-client columns.
        measured_hdh: Measured HDH instances per run_id (load_measured_hdh). Runs it covers
            use the measured count; the others use assumption A3.
    """
    out = df.copy()
    active = active_patterns(df)
    part = participating_clients(df)
    out[TYPES_COLUMN] = active.sum(axis=1).astype(int)
    out[PARTICIPANTS_COLUMN] = part.sum(axis=1).astype(int)
    for pattern, column in INSTANCE_COLUMNS.items():
        out[column] = INSTANCE_RULES[pattern](df, part).where(active[pattern], 0).astype(int)
    if measured_hdh is not None and RUN_COLUMN in df.columns:
        measured = df[RUN_COLUMN].map(measured_hdh)
        covered = measured.notna()
        out.loc[covered, INSTANCE_COLUMNS["hdh"]] = measured[covered].where(active.loc[covered, "hdh"], 0).astype(int)
    out[INSTANCES_COLUMN] = out[list(INSTANCE_COLUMNS.values())].sum(axis=1).astype(int)
    return out


def can_compute(df: pd.DataFrame) -> bool:
    """Whether df has the columns pattern stress is derived from."""
    return (CONFIG_COLUMN in df.columns and CLIENTS_COLUMN in df.columns
            and not _client_frame(df, "CPU Usage Avg").empty)


def stress_summary(df: pd.DataFrame) -> Dict[str, Dict[int, int]]:
    """Run counts per S_types level and per S_inst value (for quick inspection)."""
    return {TYPES_COLUMN: df[TYPES_COLUMN].value_counts().sort_index().to_dict(),
            INSTANCES_COLUMN: df[INSTANCES_COLUMN].value_counts().sort_index().to_dict()}
