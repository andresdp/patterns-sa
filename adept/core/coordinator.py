from typing import Any, Dict, Optional, Tuple, List
import pandas as pd
from collections import Counter

from .loader import DataLoader, GenericDataLoader
from .models import SystemDefinition, DiscretizationScheme
from ..utils.validation import SchemaValidator, SimpleValidator
from ..analysis.discretization import DataProcessor
from ..analysis.robustness import RobustnessAnalyzer
from ..analysis.tradeoffs import TradeoffAnalyzer
from ..analysis.discovery import ScenarioDiscoveryManager
from ..analysis.explainer import ExplanationManager


class ArchSpaceCore:
    """The central orchestrator for the ADEPT framework.
    
    This class implements the Coordinator pattern, composing specialized 
    components for data loading, validation, processing, and analysis. It 
    provides a unified, stable API for client code (scripts, notebooks, APIs) 
    while delegating the complex logic to internal managers and analyzers.
    
    Responsibilities:
    - Orchestrating the analysis pipeline from raw data to explained results.
    - Managing the lifecycle of internal components.
    - Providing high-level entry points for key architectural exploration tasks.
    """

    def __init__(self,
                 loader: Optional[DataLoader] = None,
                 validator: Optional[SchemaValidator] = None,
                 discovery_manager: Optional[ScenarioDiscoveryManager] = None,
                 explanation_manager: Optional[ExplanationManager] = None,
                 data_processor: Optional[DataProcessor] = None,
                 robustness_analyzer: Optional[RobustnessAnalyzer] = None,
                 tradeoff_analyzer: Optional[TradeoffAnalyzer] = None):
        """Initializes the coordinator with default or injected components."""
        self.loader = loader or GenericDataLoader()
        self.validator = validator or SimpleValidator()
        self.discovery_manager = discovery_manager or ScenarioDiscoveryManager()
        self.explanation_manager = explanation_manager or ExplanationManager()
        
        self.data_processor = data_processor or DataProcessor()
        self.robustness_analyzer = robustness_analyzer or RobustnessAnalyzer()
        self.tradeoff_analyzer = tradeoff_analyzer or TradeoffAnalyzer()

    def load_data(self, source: Any, validate_integrity: bool = True) -> pd.DataFrame:
        """Loads raw data from the specified source."""
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load(source, validate_integrity=validate_integrity)
        return self.loader.load(source)

    def load_system_definition(self, source: Any) -> SystemDefinition:
        """Loads the system definition from the specified source.
        
        Requires a GenericDataLoader.
        """
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load_system_definition(source)
        raise TypeError("System definition loading requires GenericDataLoader")

    def load_detailed_data(self, source: Any, validate_integrity: bool = True) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads and automatically partitions data into raw, experiments, and outcomes.
        
        Requires a GenericDataLoader configured with a system.json.
        """
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load_data(source, validate_integrity=validate_integrity)
        raise TypeError("Detailed data loading requires GenericDataLoader")

    def validate(self, df: pd.DataFrame) -> bool:
        """Validates the data against internal schema requirements."""
        return self.validator.validate(df)

    def discover_scenarios(self, df: pd.DataFrame, outcome: str, method: Optional[str] = None, **kwargs):
        """Identifies key parameter regions driving specific outcomes.
        
        Delegates to the ScenarioDiscoveryManager.
        """
        experiments_df = kwargs.pop('experiments_df', df)
        outcomes_df = kwargs.pop('outcomes_df', df)
        return self.discovery_manager.discover(experiments_df, outcomes_df, outcome=outcome, method=method, **kwargs)

    def explain(self, artifact: Any, method: Optional[str] = None, **kwargs) -> Dict[str, str]:
        """Generates natural language explanations for analysis artifacts.
        
        Delegates to the ExplanationManager.
        """
        return self.explanation_manager.explain(artifact, method=method, **kwargs)

    def define_tradeoffs(self, df: pd.DataFrame, method: str = 'discretization', **kwargs) -> Tuple[pd.DataFrame, Any, Optional[pd.DataFrame]]:
        """Defines tradeoff regions in the outcome space.
        
        Delegates to the DataProcessor.
        """
        return self.data_processor.define_tradeoffs(df, method=method, **kwargs)

    def compute_robustness(self, df: pd.DataFrame, **kwargs) -> Tuple[float, str]:
        """Calculates architectural robustness metrics.
        
        Delegates to the RobustnessAnalyzer.
        """
        return self.robustness_analyzer.compute_robustness(df, **kwargs)
    
    def get_nearest_tradeoffs(self, qa_tradeoff: str, available_tradeoffs: List[str], all_labels: Dict[str, List[str]], outputs: List[str], **kwargs) -> List[str]:
        """Explores neighbor regions in the tradeoff space.
        
        Delegates to the TradeoffAnalyzer.
        """
        return self.tradeoff_analyzer.get_nearest_tradeoffs(qa_tradeoff, available_tradeoffs, all_labels, outputs, **kwargs)

    def export_report(self, report: Dict[str, Any], path: str) -> None:
        """Persists analysis results to disk."""
        import json
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)


__all__ = ["ArchSpaceCore"]