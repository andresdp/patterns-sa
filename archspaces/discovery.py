from abc import ABC, abstractmethod
from typing import Any, Dict, List
import pandas as pd


class ScenarioDiscovery(ABC):
    @abstractmethod
    def discover(self, df: pd.DataFrame, outcome: str, **kwargs) -> List[Dict[str, Any]]:
        """Return a list of discovered scenarios (each scenario is a dict)."""


class PRIMDiscovery(ScenarioDiscovery):
    def discover(self, df: pd.DataFrame, outcome: str, **kwargs) -> List[Dict[str, Any]]:
        # Minimal stub: return a placeholder
        return [{"method": "PRIM", "note": "stub - implement PRIM algorithm", "outcome": outcome}]


class CARTDiscovery(ScenarioDiscovery):
    def discover(self, df: pd.DataFrame, outcome: str, **kwargs) -> List[Dict[str, Any]]:
        # Minimal stub: return a placeholder
        return [{"method": "CART", "note": "stub - implement CART algorithm", "outcome": outcome}]


__all__ = ["ScenarioDiscovery", "PRIMDiscovery", "CARTDiscovery"]
