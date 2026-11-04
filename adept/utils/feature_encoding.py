"""Numeric encoding of parameter columns for feature scoring and scenario discovery.

RandomForest, PRIM and CART need numeric, NaN-free inputs, while ADEPT parameters can be
categorical and/or optional (NaN = "option not selected"). FeatureEncoder is fitted once
(on the training slice) and then applied to every other slice that is compared against its
results (test slice, box evaluation, dataset bounds), so all of them share one encoding.
See docs/nan_strategy.md.

Encoding rules (only declared parameter columns are touched):

* Categorical (non-numeric) parameters -> ordinal codes 1..k, following the sorted category
  labels seen when fitting. NaN (and categories unseen at fit time) -> 0, the
  "not selected" code. A single-valued optional parameter therefore becomes the familiar
  0/1 presence flag.
* Numeric optional parameters with NaNs -> NaN replaced by a sentinel just below the
  observed minimum (min - 10% of the range).
* Numeric non-optional parameters -> unchanged (callers fill remaining NaNs).
"""
from typing import Any, Dict, Iterable, List, Optional

import pandas as pd

from ..core.models import Parameter

NOT_SELECTED_CODE = 0.0


class FeatureEncoder:
    """Fitted encoder for parameter columns (see module docstring)."""

    def __init__(
        self,
        sentinels: Optional[Dict[str, float]] = None,
        categories: Optional[Dict[str, List[str]]] = None,
        optional_na: Optional[Iterable[str]] = None,
    ):
        self.sentinels: Dict[str, float] = dict(sentinels or {})
        self.categories: Dict[str, List[str]] = dict(categories or {})
        # Columns whose NaNs mean "not selected" (optional and NaN at fit time)
        self.optional_na: List[str] = list(optional_na or [])

    @classmethod
    def fit(cls, df: pd.DataFrame, parameters: Iterable[Parameter]) -> "FeatureEncoder":
        """Learns the encoding of the declared parameter columns present in df."""
        sentinels, categories, optional_na = {}, {}, []
        for param in parameters:
            if param.name not in df.columns:
                continue
            col = df[param.name]
            is_optional = bool(getattr(param, 'optional', False))
            if not pd.api.types.is_numeric_dtype(col):
                categories[param.name] = sorted({str(v) for v in col.dropna().unique()})
                if is_optional and col.isnull().any():
                    optional_na.append(param.name)
            elif is_optional and col.isnull().any():
                sentinels[param.name] = cls._numeric_sentinel(col)
                optional_na.append(param.name)
        return cls(sentinels, categories, optional_na)

    @staticmethod
    def _numeric_sentinel(col: pd.Series) -> float:
        """A value just below the observed minimum (0.0 when the column is all NaN)."""
        if col.dropna().empty:
            return 0.0
        p_min, p_max = col.min(), col.max()
        p_range = p_max - p_min
        if p_range == 0:
            p_range = abs(p_min) if p_min != 0 else 1.0
        return float(p_min - 0.1 * p_range)

    def transform(self, df: pd.DataFrame) -> pd.DataFrame:
        """Applies the fitted encoding to df (columns the encoder does not know are kept as-is)."""
        out = df.copy()
        for col, levels in self.categories.items():
            if col in out.columns:
                codes = {level: float(i + 1) for i, level in enumerate(levels)}
                out[col] = out[col].map(
                    lambda v: codes.get(str(v), NOT_SELECTED_CODE) if pd.notna(v) else NOT_SELECTED_CODE
                ).astype(float)
        for col, sentinel in self.sentinels.items():
            if col in out.columns:
                out[col] = out[col].fillna(sentinel)
        return out

    # --- Interpreting results expressed in the encoded space ---

    def not_selected_value(self, col: str) -> Optional[float]:
        """Encoded value of "not selected" for an optional column, or None."""
        if col not in self.optional_na:
            return None
        return NOT_SELECTED_CODE if col in self.categories else self.sentinels.get(col)

    def includes_not_selected(self, col: str, limits: Dict[str, float]) -> bool:
        """Whether an encoded [min, max] range covers the column's "not selected" value."""
        value = self.not_selected_value(col)
        if value is None:
            return False
        return limits['min'] <= value + 1e-6 and limits['max'] >= value - 1e-6

    def decode_categories(self, col: str, limits: Dict[str, float]) -> List[str]:
        """Category labels whose code lies within an encoded [min, max] range."""
        levels = self.categories.get(col, [])
        return [level for i, level in enumerate(levels) if limits['min'] <= i + 1 <= limits['max']]

    def state(self) -> Dict[str, Any]:
        return {'sentinels': self.sentinels, 'categories': self.categories, 'optional_na': self.optional_na}
