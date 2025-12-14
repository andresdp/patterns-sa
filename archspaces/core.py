from typing import Any, Dict, Optional
import warnings
import pandas as pd

from .loader import DataLoader, PandasDataLoader
from .validator import SchemaValidator, SimpleValidator
from .metrics import MetricsEngine, ToyMetricsEngine
from .discovery import ScenarioDiscovery, PRIMDiscovery, CARTDiscovery


class ArchSpaceCore:
    """Core orchestrator that composes small components.

    This class is designed for composition and dependency injection. Each
    component has a small, testable interface.
    """

    def __init__(self,
                 loader: Optional[DataLoader] = None,
                 validator: Optional[SchemaValidator] = None,
                 metrics_engine: Optional[MetricsEngine] = None,
                 discovery_engine: Optional[ScenarioDiscovery] = None):
        self.loader = loader or PandasDataLoader()
        self.validator = validator or SimpleValidator()
        self.metrics_engine = metrics_engine or ToyMetricsEngine()
        self.discovery_engine = discovery_engine or PRIMDiscovery()

    def load_data(self, source: Any) -> pd.DataFrame:
        return self.loader.load(source)

    def validate(self, df: pd.DataFrame) -> bool:
        return self.validator.validate(df)

    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        return self.metrics_engine.compute(df)

    def discover_scenarios(self, df: pd.DataFrame, outcome: str, method: Optional[str] = None, **kwargs):
        if method is None or method.lower() == "prim":
            engine = self.discovery_engine if isinstance(self.discovery_engine, PRIMDiscovery) else PRIMDiscovery()
        elif method.lower() == "cart":
            engine = CARTDiscovery()
        else:
            warnings.warn(f"Unknown discovery method '{method}', defaulting to PRIM")
            engine = PRIMDiscovery()
        return engine.discover(df, outcome, **kwargs)

    def export_report(self, report: Dict[str, Any], path: str) -> None:
        import json
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)


__all__ = ["ArchSpaceCore"]
