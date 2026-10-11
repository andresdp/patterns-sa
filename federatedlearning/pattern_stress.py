"""Pattern stress of a federated learning run: how much patterning the system carries.

Two measures (see compact/README.md, "Pattern stress"):

* `Pattern Types Active` (S_types, 0-3): how many of the three pattern decisions are ON,
  read from `config_id`. It depends on the configuration only.
* `Pattern Instances` (S_inst): how many pattern instances are deployed, i.e. the sum of
  `Client Selector Instances`, `Message Compressor Instances` and `HDH Instances`. The
  same pattern type can have several instances (e.g. one per client), so S_inst also
  depends on the client environment (how many clients participate, how many are non-IID)
  and on the other decisions (the client selector removes clients, and their instances).

The CSVs do not record instances, so they are derived from the per-client columns with
the deployment rules in INSTANCE_RULES. These rules are ASSUMPTIONS about AP4FED, to be
confirmed (compact/README.md lists them with the open questions):

  A1. Client selector: one instance, on the server.
  A2. Message compressor: one instance per participating client (the server-side
      decompression is not counted).
  A3. HDH: one instance per participating non-IID client.
  A4. A client participates iff it exists in the run (index <= Total Clients) and its
      `CPU Usage Avg` is recorded. Verified on the compact data: with the client selector
      ON, the participants are exactly the clients that are not low-spec; with it OFF,
      every client participates.
"""
from __future__ import annotations

import re
from typing import Dict

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


def add_pattern_stress(df: pd.DataFrame) -> pd.DataFrame:
    """Adds the pattern-stress columns (the original columns are kept)."""
    out = df.copy()
    active = active_patterns(df)
    part = participating_clients(df)
    out[TYPES_COLUMN] = active.sum(axis=1).astype(int)
    out[PARTICIPANTS_COLUMN] = part.sum(axis=1).astype(int)
    for pattern, column in INSTANCE_COLUMNS.items():
        out[column] = INSTANCE_RULES[pattern](df, part).where(active[pattern], 0).astype(int)
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
