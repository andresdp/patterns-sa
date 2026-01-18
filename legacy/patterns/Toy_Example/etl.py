"""Pandas-based ETL for the Toy Example.

This module provides a lightweight normalizer that ensures the CSV contains
the canonical columns expected by the Toy plugin: `param1`, `param2`,
`latency`, `availability`.
"""
import pandas as pd
from typing import Union


def normalize(input_path: str, output_path: Union[str, None] = None) -> pd.DataFrame:
    df = pd.read_csv(input_path)

    # Ensure canonical columns exist
    if "param1" not in df.columns:
        df["param1"] = 0
    if "param2" not in df.columns:
        df["param2"] = 0.0

    # map response_time -> latency if present
    if "latency" not in df.columns and "response_time" in df.columns:
        df["latency"] = df["response_time"]
    if "latency" not in df.columns:
        df["latency"] = 0.0

    # map avail or availability
    if "availability" not in df.columns and "avail" in df.columns:
        df["availability"] = df["avail"]
    if "availability" not in df.columns:
        df["availability"] = 1

    if output_path:
        df.to_csv(output_path, index=False)
        return pd.read_csv(output_path)

    return df


__all__ = ["normalize"]
