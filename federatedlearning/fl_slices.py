"""Focused slices of the federated learning dataset (paper plan §4.4).

A slice keeps only some runs, so the same analysis notebook can study a part of the
design space next to the analysis of the full dataset. Filters combine:

* configurations: the baseline, or one pattern alone (ablation A1)
      session.load(preprocessor=slice_filter('hdh'))                         # HDH Only
      session.load(preprocessor=slice_filter('hdh', include_baseline=True))  # + baseline
* client count (`Total Clients`): the system structure changes with it
      slice_filter(clients=8)
* task: the dataset-model pair ('image' = CIFAR-10 + CNN 16k, 'text' = AG_NEWS + MLP)
      slice_filter(clients=8, task='image')
* environment: environment='common' keeps the environment points (low-spec, non-IID and
  delay shares) that every configuration in the slice was run at, so configurations are
  compared under identical conditions.

The preprocessor also adds the pattern-stress columns (pattern_stress.py) when the data
has the columns they are derived from. HDH instances are measured from the per-round data
in `detailed/` when it is available, and assumed (rule A3) otherwise.

Tradeoff labels must mean the same thing across the notebooks being compared, so those
notebooks define the tradeoffs with fixed bin edges (create_tradeoffs(..., edges=...))
instead of detecting them from the loaded runs (the "static grid", paper plan §4.5).

Configurations are identified by `config_id` = '<client_selector>,<message_compressor>,<hdh>'.
"""
from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Optional, Tuple

import pandas as pd

import pattern_stress

CONFIG_COLUMN = "config_id"
CLIENTS_COLUMN = "Total Clients"

# Order of the decisions in config_id
PATTERNS = ("client_selector", "message_compressor", "hdh")

BASELINE = "OFF,OFF,OFF"

# Task -> (Dataset, Model): the model is chosen for the dataset, so the pair is one task
TASKS: Dict[str, Tuple[str, str]] = {
    "image": ("CIFAR-10", "CNN 16k"),
    "text": ("AG_NEWS", "MLP"),
}

# Run-level environment factors of the compact campaign
ENVIRONMENT_COLUMNS = ("low_spec_percentage", "non_iid_percentage", "delay_percentage")


def config_id(active: Iterable[str] = ()) -> str:
    """config_id of the configuration in which exactly the given patterns are ON."""
    active = set(active)
    unknown = active - set(PATTERNS)
    if unknown:
        raise ValueError(f"Unknown pattern(s) {sorted(unknown)}. Available: {list(PATTERNS)}")
    return ",".join("ON" if p in active else "OFF" for p in PATTERNS)


# Slice name -> configurations it keeps (None = every configuration)
SLICES: Dict[str, Optional[List[str]]] = {
    "all": None,
    "baseline": [BASELINE],
    **{p: [config_id([p])] for p in PATTERNS},
}


def slice_configs(name: str, include_baseline: bool = False) -> Optional[List[str]]:
    """Configurations kept by a slice (None for 'all')."""
    if name not in SLICES:
        raise ValueError(f"Unknown slice '{name}'. Available: {list(SLICES)}")
    configs = SLICES[name]
    if configs is None:
        return None
    if include_baseline and BASELINE not in configs:
        configs = [BASELINE] + configs
    return configs


def common_environment(df: pd.DataFrame, columns: Iterable[str] = ENVIRONMENT_COLUMNS) -> pd.Series:
    """Mask of the runs whose environment point every configuration in df was run at."""
    columns = [c for c in columns if c in df.columns]
    if not columns:
        raise ValueError(f"None of the environment columns {list(ENVIRONMENT_COLUMNS)} is in the data.")
    points = df[columns].apply(tuple, axis=1)
    shared = set.intersection(*(set(p) for _, p in points.groupby(df[CONFIG_COLUMN])))
    return points.isin(shared)


def slice_filter(name: str = "all", include_baseline: bool = False, clients: Optional[int] = None,
                 task: Optional[str] = None, environment: str = "all",
                 measured_instances: bool = True) -> Callable:
    """Loader preprocessor: adds the pattern-stress columns and keeps the runs of a slice.

    Args:
        name: Configurations: 'all', 'baseline', or one pattern: 'client_selector',
            'message_compressor', 'hdh'.
        include_baseline: For a single-pattern slice, also keep the baseline runs, so the
            pattern is compared with not applying it (A1-vs-baseline).
        clients: Keep only runs with this number of clients (`Total Clients`).
        task: Keep only one task: 'image' (CIFAR-10 + CNN 16k) or 'text' (AG_NEWS + MLP).
        environment: 'all', or 'common' to keep only the environment points shared by every
            configuration left after the other filters.
        measured_instances: Count HDH instances from the per-round data in `detailed/`
            when available (False: always use assumption A3).
    """
    configs = slice_configs(name, include_baseline)
    if task is not None and task not in TASKS:
        raise ValueError(f"Unknown task '{task}'. Available: {list(TASKS)}")
    if environment not in ("all", "common"):
        raise ValueError("environment must be 'all' or 'common'.")

    def preprocessor(df: pd.DataFrame, **_) -> pd.DataFrame:
        n_all = len(df)
        if pattern_stress.can_compute(df):
            measured = pattern_stress.load_measured_hdh() if measured_instances else None
            df = pattern_stress.add_pattern_stress(df, measured_hdh=measured)
            if measured is None:
                print("HDH instances: assumed (rule A3, one per participating non-IID client).")
            else:
                n = int(df[pattern_stress.RUN_COLUMN].isin(measured.index).sum()) if pattern_stress.RUN_COLUMN in df else 0
                print(f"HDH instances: measured from the per-round data for {n} of {len(df)} runs "
                      f"(HDH Time > 0); rule A3 for the others.")
        steps = []
        if configs is not None:
            df = df[df[CONFIG_COLUMN].astype(str).isin(configs)]
            steps.append(f"configurations {configs}")
        if clients is not None:
            df = df[df[CLIENTS_COLUMN] == clients]
            steps.append(f"{clients} clients")
        if task is not None:
            dataset, model = TASKS[task]
            df = df[(df["Dataset"] == dataset) & (df["Model"] == model)]
            steps.append(f"task '{task}' ({dataset} + {model})")
        if environment == "common" and not df.empty:
            df = df[common_environment(df)]
            steps.append("common environment points")
        df = df.reset_index(drop=True)
        if steps:
            print(f"Slice: kept {len(df)} of {n_all} runs ({'; '.join(steps)}).")
        if df.empty:
            raise ValueError("The slice has no runs in this dataset.")
        return df

    return preprocessor
