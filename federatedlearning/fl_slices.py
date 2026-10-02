"""Focused slices of the federated learning dataset (ablation A1, paper plan §4.4).

A slice keeps only the runs of some configurations, so the same analysis notebook can
study the baseline, or one pattern at a time, next to the analysis of the full dataset:

    session.load(preprocessor=slice_filter('hdh'))                       # HDH Only runs
    session.load(preprocessor=slice_filter('hdh', include_baseline=True))  # + baseline

Tradeoff labels must mean the same thing in every slice, so the notebooks define the
tradeoffs with fixed bin edges (create_tradeoffs(..., edges=...)) instead of detecting them
from the loaded runs (the "static grid", paper plan §4.5).

Configurations are identified by `config_id` = '<client_selector>,<message_compressor>,<hdh>'.
"""
from __future__ import annotations

from typing import Callable, Dict, Iterable, List, Optional

import pandas as pd

CONFIG_COLUMN = "config_id"

# Order of the decisions in config_id (FLsystem_split.json)
PATTERNS = ("client_selector", "message_compressor", "hdh")

BASELINE = "OFF,OFF,OFF"


def config_id(active: Iterable[str] = ()) -> str:
    """config_id of the configuration in which exactly the given patterns are ON."""
    active = set(active)
    unknown = active - set(PATTERNS)
    if unknown:
        raise ValueError(f"Unknown pattern(s) {sorted(unknown)}. Available: {list(PATTERNS)}")
    return ",".join("ON" if p in active else "OFF" for p in PATTERNS)


# Slice name -> configurations it keeps (None = every run)
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


def slice_filter(name: str = "all", include_baseline: bool = False) -> Optional[Callable]:
    """Loader preprocessor that keeps the runs of a slice (None for 'all').

    Args:
        name: 'all', 'baseline', or one pattern: 'client_selector', 'message_compressor', 'hdh'.
        include_baseline: For a single-pattern slice, also keep the baseline runs, so the
            pattern is compared with not applying it (A1-vs-baseline). Otherwise only the
            runs where that pattern alone is ON are kept (A1-alone).
    """
    configs = slice_configs(name, include_baseline)
    if configs is None:
        return None

    def preprocessor(df: pd.DataFrame, **_) -> pd.DataFrame:
        kept = df[df[CONFIG_COLUMN].astype(str).isin(configs)].reset_index(drop=True)
        print(f"Slice '{name}': kept {len(kept)} of {len(df)} runs (configurations {configs}).")
        if kept.empty:
            raise ValueError(f"Slice '{name}' has no runs in this dataset.")
        return kept

    return preprocessor

