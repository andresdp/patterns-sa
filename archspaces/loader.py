from abc import ABC, abstractmethod
from typing import Any
import pandas as pd


class DataLoader(ABC):
    @abstractmethod
    def load(self, source: Any) -> pd.DataFrame:
        """Load data from `source` and return a pandas DataFrame."""


class PandasDataLoader(DataLoader):
    def __init__(self, **read_kwargs):
        self.read_kwargs = read_kwargs

    def load(self, source: Any) -> pd.DataFrame:
        """Load CSV (or any pandas-supported source) into a DataFrame."""
        return pd.read_csv(source, **self.read_kwargs)


__all__ = ["DataLoader", "PandasDataLoader"]
