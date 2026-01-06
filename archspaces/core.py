from typing import Any, Dict, Optional, Tuple, List
import warnings
import pandas as pd
import numpy as np
from natsort import natsorted
from collections import Counter

from .loader import DataLoader, PandasDataLoader, GenericDataLoader
from .validator import SchemaValidator, SimpleValidator
from .metrics import MetricsEngine, ToyMetricsEngine
from .discovery import ScenarioDiscovery, PRIMDiscovery, CARTDiscovery, ScenarioDiscoveryManager
from .explanations import ExplanationManager


class DataProcessor:
    """Handles data discretization and labeling."""

    @staticmethod
    def get_bins(col: pd.Series, n: int, min_max: Tuple[Optional[float], Optional[float]] = (None, None)) -> list:
        unique_values = sorted((set(col.values)))
        if min_max == (None, None):
            min_x = np.min(unique_values)
            max_x = np.max(unique_values)
        else:
            min_x = min_max[0]
            max_x = min_max[1]
        
        # Ensure we cover the full range with a small buffer
        min_x = min_x - 0.1
        max_x = max_x + 0.1
        delta = (max_x - min_x) / n
        return ([min_x + i * delta for i in range(0, n)] + [max_x])

    @staticmethod
    def get_tradeoffs(df: pd.DataFrame, separator: str = ',') -> Counter:
        temp = df.to_string(header=False, index=False, index_names=False).split('\n')
        tradeoffs = [separator.join(ele.split()) for ele in temp]
        return Counter(tradeoffs)

    @staticmethod
    def discretize(df: pd.DataFrame, n_bins: int = 3, mins_maxs: Tuple[Optional[float], Optional[float]] = (None, None), all_labels: Optional[Dict] = None) -> Tuple[pd.DataFrame, Counter]:
        discrete_df = df.copy()
        for idx, c in enumerate(df.columns):
            qa = df[c]
            min_max = (None, None)
            if mins_maxs != (None, None):
                min_max = mins_maxs[idx]
            qa_bins = DataProcessor.get_bins(qa, n_bins, min_max=min_max)
            
            if all_labels and c in all_labels:
                qa_labels = pd.cut(qa, bins=qa_bins, labels=all_labels[c])
            else:
                 # Fallback if no labels provided
                qa_labels = pd.cut(qa, bins=qa_bins)

            discrete_df[c] = qa_labels

        available_tradeoffs = DataProcessor.get_tradeoffs(discrete_df)
        return discrete_df, available_tradeoffs


from sklearn.neighbors import NearestNeighbors

class RobustnessAnalyzer:
    """Calculates robustness metrics."""

    def compute_robustness(self, discrete_outcomes_df: pd.DataFrame, qa_tradeoff: Optional[str] = None) -> Tuple[float, str]:
        """
        Computes the robustness of a set of outcomes.
        
        Args:
            discrete_outcomes_df: DataFrame containing discretized outcomes.
            qa_tradeoff: The specific tradeoff label to calculate robustness for. 
                         If None, the most common tradeoff is used.
        
        Returns:
            Tuple containing (robustness value, tradeoff label)
        """
        if discrete_outcomes_df is None or discrete_outcomes_df.empty:
            warnings.warn("Discrete outcomes DataFrame is empty or None.")
            return 0.0, ""

        local_tradeoffs = DataProcessor.get_tradeoffs(discrete_outcomes_df)

        if qa_tradeoff is None:
            # Select most common
            most_common = local_tradeoffs.most_common(1)
            if not most_common:
                return 0.0, ""
            qa_tradeoff_val = most_common[0]
            reference_tradeoff = qa_tradeoff_val[0]
            count = qa_tradeoff_val[1]
        else:
            reference_tradeoff = qa_tradeoff
            count = local_tradeoffs[qa_tradeoff]
        
        total = local_tradeoffs.total()
        if total == 0:
            return 0.0, reference_tradeoff

        r = count / total
        return r, reference_tradeoff


class TradeoffAnalyzer:
    """Analyzes tradeoffs."""

    def get_nearest_tradeoffs(self, qa_tradeoff: str, available_tradeoffs: List[str], all_labels: Dict[str, List[str]], outputs: List[str], k: int = 5, metric: str = 'euclidean', separator: str = ',') -> List[str]:
        """
        Finds the nearest available tradeoffs to a given reference tradeoff.
        """
        reference_tradeoff = qa_tradeoff.split(separator)
        tradeoff_list = [qat.split(separator) for qat in available_tradeoffs]
        df = pd.DataFrame(tradeoff_list, columns=outputs) 
        
        # Create mapper object
        mapper = dict()
        for c in all_labels.keys():
            mapper[c] = dict()
            value = -1
            for label in all_labels[c]:
                mapper[c][label] = value
                value = value + 1

        for c in df.columns:
            if c in mapper:
                df[c] = df[c].replace(mapper[c]) 
        
        nbrs = NearestNeighbors(n_neighbors=k, metric=metric)
        nbrs.fit(df.values)
        
        ref_df = pd.DataFrame(np.array(reference_tradeoff).reshape(1, len(outputs)), columns=outputs) 
        for c in ref_df.columns:
            if c in mapper:
                ref_df[c] = ref_df[c].replace(mapper[c])
        
        y = ref_df.loc[0, :].values.tolist()
        distances, indices = nbrs.kneighbors([y])
        
        # Use available_tradeoffs (list of strings) directly
        # tradeoff_list was just the split version
        # We need to map back to original strings
        # indices[0] are indices into the dataframe which corresponds to tradeoff_list order
        
        # But available_tradeoffs passed might be a dict or list. Type hint says List[str]
        # In ArchSpace it was keys of a dict.
        
        return [available_tradeoffs[i] for i in indices[0]]


class ArchSpaceCore:
    """Core orchestrator that composes small components.

    This class is designed for composition and dependency injection. Each
    component has a small, testable interface.
    """

    def __init__(self,
                 loader: Optional[DataLoader] = None,
                 validator: Optional[SchemaValidator] = None,
                 metrics_engine: Optional[MetricsEngine] = None,
                 discovery_manager: Optional[ScenarioDiscoveryManager] = None,
                 explanation_manager: Optional[ExplanationManager] = None,
                 data_processor: Optional[DataProcessor] = None,
                 robustness_analyzer: Optional[RobustnessAnalyzer] = None,
                 tradeoff_analyzer: Optional[TradeoffAnalyzer] = None):
        self.loader = loader or GenericDataLoader()
        self.validator = validator or SimpleValidator()
        self.metrics_engine = metrics_engine or ToyMetricsEngine()
        self.discovery_manager = discovery_manager or ScenarioDiscoveryManager()
        self.explanation_manager = explanation_manager or ExplanationManager()
        
        self.data_processor = data_processor or DataProcessor()
        self.robustness_analyzer = robustness_analyzer or RobustnessAnalyzer()
        self.tradeoff_analyzer = tradeoff_analyzer or TradeoffAnalyzer()

    def load_data(self, source: Any) -> pd.DataFrame:
        return self.loader.load(source)

    def load_detailed_data(self, source: Any) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Returns (raw_df, experiments_df, outcomes_df) using GenericDataLoader."""
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load_data(source)
        raise TypeError("Detailed data loading requires GenericDataLoader")

    def validate(self, df: pd.DataFrame) -> bool:
        return self.validator.validate(df)

    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        return self.metrics_engine.compute(df)

    def discover_scenarios(self, df: pd.DataFrame, outcome: str, method: Optional[str] = None, **kwargs):
        experiments_df = kwargs.get('experiments_df', df)
        outcomes_df = kwargs.get('outcomes_df', df)
        return self.discovery_manager.discover(experiments_df, outcomes_df, method=method, **kwargs)

    def explain(self, artifact: Any, method: Optional[str] = None, **kwargs) -> Dict[str, str]:
        return self.explanation_manager.explain(artifact, method=method, **kwargs)

    def discretize(self, df: pd.DataFrame, **kwargs) -> Tuple[pd.DataFrame, Counter]:
        return self.data_processor.discretize(df, **kwargs)

    def compute_robustness(self, df: pd.DataFrame, **kwargs) -> Tuple[float, str]:
        return self.robustness_analyzer.compute_robustness(df, **kwargs)
    
    def get_nearest_tradeoffs(self, qa_tradeoff: str, available_tradeoffs: List[str], all_labels: Dict[str, List[str]], outputs: List[str], **kwargs) -> List[str]:
        return self.tradeoff_analyzer.get_nearest_tradeoffs(qa_tradeoff, available_tradeoffs, all_labels, outputs, **kwargs)

    def export_report(self, report: Dict[str, Any], path: str) -> None:
        import json
        with open(path, "w", encoding="utf-8") as fh:
            json.dump(report, fh, indent=2)


__all__ = ["ArchSpaceCore"]
