"""Aggregation of per-instance columns into system-level columns.

Some systems have several instances of a component (e.g. the clients of a federated
learning system), and their datasets record one column per instance and field:
`Client 1 CPU`, `Client 2 CPU`, ... ADEPT's model has one value per parameter/objective
and run, so these columns are summarized per row into `<field> <Statistic>` columns
(`CPU Mean`, `CPU Std`, `Data Distribution Diversity`, ...). The system definition then
declares whichever summaries it analyzes as ordinary parameters or objectives.

Declared in the dataspace (applied by GenericDataLoader after the preprocessor hook and
before column renames):

    "aggregations": [{
        "pattern": "^Client (\\\\d+) (.+)$",
        "numeric": ["mean", "std"],
        "categorical": ["nunique"],
        "fields": ["CPU", "RAM", "Data Distribution"]
    }]
"""
import re
from typing import Dict, Iterable, List, Optional

import pandas as pd

DEFAULT_INSTANCE_PATTERN = r"^Client (\d+) (.+)$"

# Statistic -> column-name suffix
NUMERIC_STATISTICS = {'mean': 'Mean', 'std': 'Std', 'min': 'Min', 'max': 'Max', 'median': 'Median'}
CATEGORICAL_STATISTICS = {'nunique': 'Diversity'}


def aggregate_instance_columns(
    df: pd.DataFrame,
    pattern: str = DEFAULT_INSTANCE_PATTERN,
    numeric: Iterable[str] = ('mean',),
    categorical: Iterable[str] = ('nunique',),
    fields: Optional[Iterable[str]] = None,
) -> pd.DataFrame:
    """Adds per-row summaries of per-instance columns; the original columns are kept.

    Args:
        df: Dataset with one column per instance and field.
        pattern: Regex matching per-instance columns; group 1 is the instance id,
            group 2 the field name.
        numeric: Statistics for numeric fields ('mean', 'std', 'min', 'max', 'median'),
            computed across instances, skipping NaN.
        categorical: Statistics for non-numeric fields ('nunique': number of distinct values).
        fields: Fields to aggregate. Defaults to every field matched by `pattern`.

    Returns:
        A copy of df with `<field> <Statistic>` columns added. Without matching columns,
        df is returned unchanged.
    """
    unknown = (set(numeric) - set(NUMERIC_STATISTICS)) | (set(categorical) - set(CATEGORICAL_STATISTICS))
    if unknown:
        raise ValueError(f"Unknown aggregation statistics {sorted(unknown)}. "
                         f"Numeric: {list(NUMERIC_STATISTICS)}; categorical: {list(CATEGORICAL_STATISTICS)}.")

    regex = re.compile(pattern)
    field_to_columns: Dict[str, List[str]] = {}
    for col in df.columns:
        match = regex.match(str(col))
        if match:
            field_to_columns.setdefault(match.group(2), []).append(col)
    if fields is not None:
        wanted = set(fields)
        field_to_columns = {f: cols for f, cols in field_to_columns.items() if f in wanted}
    if not field_to_columns:
        return df

    result = df.copy()
    for field, cols in field_to_columns.items():
        subset = df[cols]
        if all(pd.api.types.is_numeric_dtype(df[c]) for c in cols):
            for stat in numeric:
                result[f"{field} {NUMERIC_STATISTICS[stat]}"] = getattr(subset, stat)(axis=1, skipna=True)
        else:
            for stat in categorical:
                result[f"{field} {CATEGORICAL_STATISTICS[stat]}"] = subset.nunique(axis=1)
    return result
