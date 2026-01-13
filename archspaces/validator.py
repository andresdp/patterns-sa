from abc import ABC, abstractmethod
from typing import Iterable
import pandas as pd


class SchemaValidator(ABC):
    @abstractmethod
    def validate(self, df: pd.DataFrame) -> bool:
        """Return True if DataFrame `df` conforms to the expected schema."""


class SimpleValidator(SchemaValidator):
    def __init__(self, required_columns: Iterable[str] = ()): 
        self.required_columns = list(required_columns)

    def validate(self, df: pd.DataFrame) -> bool:
        missing = [c for c in self.required_columns if c not in df.columns]
        return len(missing) == 0


__all__ = ["SchemaValidator", "SimpleValidator"]
