import warnings
from typing import Any, Dict
import pandas as pd

from .core import ArchSpaceCore


class LegacyArchSpace:
    """Compatibility wrapper for older API names that delegates to ArchSpaceCore.

    This class emits warnings and maps a few legacy method names to the new core.
    """
    def __init__(self, *args, **kwargs):
        warnings.warn("LegacyArchSpace is a compatibility wrapper; migrate to ArchSpaceCore", DeprecationWarning)
        self._core = ArchSpaceCore(*args, **kwargs)

    def load(self, source: Any) -> pd.DataFrame:
        warnings.warn("LegacyArchSpace.load is deprecated; use ArchSpaceCore.load_data", DeprecationWarning)
        return self._core.load_data(source)

    def validate_schema(self, df: pd.DataFrame) -> bool:
        warnings.warn("LegacyArchSpace.validate_schema is deprecated; use ArchSpaceCore.validate", DeprecationWarning)
        return self._core.validate(df)

    def compute(self, df: pd.DataFrame) -> Dict[str, Any]:
        warnings.warn("LegacyArchSpace.compute is deprecated; use ArchSpaceCore.compute_metrics", DeprecationWarning)
        return self._core.compute_metrics(df)

    def discover(self, df: pd.DataFrame, outcome: str, **kwargs):
        warnings.warn("LegacyArchSpace.discover is deprecated; use ArchSpaceCore.discover_scenarios", DeprecationWarning)
        return self._core.discover_scenarios(df, outcome, **kwargs)


__all__ = ["LegacyArchSpace"]
