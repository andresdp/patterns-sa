"""Parse the compact campaign's categorical ``pattern_stress`` source field.

The field records pattern-specific percentages as tokens such as ``CS=25%``. Each
token is a conditional view of an existing environment factor, present only when
its associated pattern is enabled. Parsed values are therefore derived features,
not additional independent experiment factors.
"""
from __future__ import annotations

import math
import re
from typing import Dict, List, Optional, Tuple

import pandas as pd

SOURCE_COLUMN = "pattern_stress"
CONFIG_COLUMN = "config_id"

# code: (feature name, config_id position, matching environment column)
PATTERN_STRESS: Dict[str, Tuple[str, int, str]] = {
    "CS": ("Client Selector Stress Percentage", 0, "low_spec_percentage"),
    "MC": ("Message Compressor Stress Percentage", 1, "delay_percentage"),
    "HDH": ("HDH Stress Percentage", 2, "non_iid_percentage"),
}
FEATURE_COLUMNS: List[str] = [spec[0] for spec in PATTERN_STRESS.values()]
_TOKEN = re.compile(r"([A-Z]+)\s*=\s*(\d+(?:\.\d+)?)\s*%")


def add_pattern_stress_features(df: pd.DataFrame) -> pd.DataFrame:
    """Add validated nullable numeric pattern-stress features; preserve the source field.

    Missing parsed values mean that the corresponding pattern is OFF. The literal 0%
    remains a numeric zero (not the same as OFF). For the compact campaign, each parsed
    value must agree with the matching environment percentage and the active pattern
    encoded in ``config_id``.

    If ``pattern_stress`` is absent, return a copy unchanged. This permits use of the
    shared slice helper with datasets that predate or do not use this campaign field.
    """
    out = df.copy()
    if SOURCE_COLUMN not in out.columns:
        return out
    if CONFIG_COLUMN not in out.columns:
        raise ValueError(f"Cannot parse {SOURCE_COLUMN!r} without {CONFIG_COLUMN!r}.")

    parsed: Dict[str, List[Optional[float]]] = {
        feature: [] for feature in FEATURE_COLUMNS
    }
    for row_position, (row_index, raw_value) in enumerate(out[SOURCE_COLUMN].items()):
        if pd.isna(raw_value):
            raise ValueError(f"Missing {SOURCE_COLUMN!r} at row {row_index!r}.")
        raw = str(raw_value).strip()
        config_value = out.iloc[row_position][CONFIG_COLUMN]
        config = [part.strip().upper() for part in str(config_value).split(",")]
        if len(config) != len(PATTERN_STRESS) or any(p not in {"ON", "OFF"} for p in config):
            raise ValueError(f"Invalid {CONFIG_COLUMN!r} at row {row_index!r}: {config_value!r}.")

        tokens: Dict[str, float] = {}
        if raw.lower() != "none":
            for text in raw.split(";"):
                match = _TOKEN.fullmatch(text.strip())
                if not match:
                    raise ValueError(f"Unrecognized {SOURCE_COLUMN!r} token at row {row_index!r}: {text!r}.")
                code, value_text = match.groups()
                if code not in PATTERN_STRESS:
                    raise ValueError(f"Unknown pattern code {code!r} at row {row_index!r}.")
                if code in tokens:
                    raise ValueError(f"Duplicate {code!r} token at row {row_index!r}.")
                value = float(value_text)
                if not 0.0 <= value <= 100.0:
                    raise ValueError(f"{code} percentage out of bounds at row {row_index!r}: {value}.")
                tokens[code] = value

        for code, (feature, position, environment_column) in PATTERN_STRESS.items():
            active = config[position] == "ON"
            value = tokens.get(code)
            if active != (value is not None):
                raise ValueError(
                    f"{SOURCE_COLUMN!r} disagrees with {CONFIG_COLUMN!r} for {code} at row {row_index!r}."
                )
            if value is not None:
                if environment_column not in out.columns:
                    raise ValueError(f"Required context column {environment_column!r} is missing.")
                context_value = pd.to_numeric(pd.Series([out.iloc[row_position][environment_column]]), errors="coerce").iloc[0]
                if pd.isna(context_value) or not math.isclose(value, float(context_value), abs_tol=1e-9):
                    raise ValueError(
                        f"{code} stress {value:g}% disagrees with {environment_column}="
                        f"{out.iloc[row_position][environment_column]!r} at row {row_index!r}."
                    )
            parsed[feature].append(value)

    for feature, values in parsed.items():
        out[feature] = pd.Series(values, dtype="float64").to_numpy()
    return out
