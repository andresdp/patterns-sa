from typing import Any, Dict, Optional, Tuple, List
import pandas as pd
import numpy as np
from collections import Counter

from .loader import DataLoader, GenericDataLoader
from .models import SystemDefinition, DiscretizationScheme, Tradeoff
from ..utils.validation import SchemaValidator, SimpleValidator
from ..utils.exceptions import (
    ADEPTError, DataLoadingError, ValidationError, DiscoveryError,
    ConfigurationError, AnalysisError, TradeoffDefinitionError, VisualizationError
)
from ..analysis.discretization import DataProcessor
from ..analysis.robustness import RobustnessAnalyzer
from ..analysis.tradeoffs import TradeoffAnalyzer
from ..analysis.discovery import ScenarioDiscoveryManager
from ..analysis.explainer import ExplanationManager
from ..analysis.visualization_manager import VisualizationManager
import matplotlib.pyplot as plt


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
                 visualization_manager: Optional[VisualizationManager] = None,
                 data_processor: Optional[DataProcessor] = None,
                 robustness_analyzer: Optional[RobustnessAnalyzer] = None,
                 tradeoff_analyzer: Optional[TradeoffAnalyzer] = None):
        """Initializes the coordinator with default or injected components."""
        self.loader = loader or GenericDataLoader()
        self.validator = validator or SimpleValidator()
        self.discovery_manager = discovery_manager or ScenarioDiscoveryManager()
        self.explanation_manager = explanation_manager or ExplanationManager()
        self.visualization_manager = visualization_manager or VisualizationManager()
        
        self.data_processor = data_processor or DataProcessor()
        self.robustness_analyzer = robustness_analyzer or RobustnessAnalyzer()
        self.tradeoff_analyzer = tradeoff_analyzer or TradeoffAnalyzer()

    def load_data(self, source: Any, validate_integrity: bool = True, preprocessor: Optional[callable] = None) -> pd.DataFrame:
        """Loads raw data from the specified source.
        
        Args:
            source: Path to data source or data object
            validate_integrity: Whether to validate data integrity
            preprocessor: Optional function(df) -> df to transform raw data.
            
        Returns:
            DataFrame containing loaded data
            
        Raises:
            DataLoadingError: If data loading fails
            ValueError: If source is invalid
        """
        if source is None:
            raise ValueError("Data source cannot be None")
        
        try:
            if isinstance(self.loader, GenericDataLoader):
                return self.loader.load(source, validate_integrity=validate_integrity, preprocessor=preprocessor)
            return self.loader.load(source)
        except Exception as e:
            raise DataLoadingError(f"Failed to load data from {source}", {"original_error": str(e)})

    def load_system_definition(self, source: Any) -> SystemDefinition:
        """Loads the system definition from the specified source.
        
        Requires a GenericDataLoader.
        """
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load_system_definition(source)
        raise TypeError("System definition loading requires GenericDataLoader")

    def load_detailed_data(self, source: Any, validate_integrity: bool = True, preprocessor: Optional[callable] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """Loads and automatically partitions data into raw, experiments, and outcomes.
        
        Requires a GenericDataLoader configured with a system.json.
        """
        if isinstance(self.loader, GenericDataLoader):
            return self.loader.load_data(source, validate_integrity=validate_integrity, preprocessor=preprocessor)
        raise TypeError("Detailed data loading requires GenericDataLoader")

    def validate(self, df: pd.DataFrame) -> bool:
        """Validates the data against internal schema requirements.
        
        Args:
            df: DataFrame to validate
            
        Returns:
            True if validation passes, False otherwise
            
        Raises:
            ValidationError: If validation fails with specific issues
            ValueError: If input is invalid
        """
        if df is None:
            raise ValueError("DataFrame cannot be None")
        
        if not isinstance(df, pd.DataFrame):
            raise ValueError("Input must be a pandas DataFrame")
        
        if df.empty:
            raise ValidationError("DataFrame is empty")
        
        try:
            return self.validator.validate(df)
        except Exception as e:
            raise ValidationError(f"Data validation failed", {"original_error": str(e)})

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

    def show_distributions(self, outcomes_df: pd.DataFrame, schemes: List[DiscretizationScheme], tradeoff: Optional[Tradeoff] = None, highlight_indices: Optional[np.ndarray] = None, **kwargs) -> plt.Figure:
        """Plots outcome distributions with tradeoff overlays.
        
        Delegates to the VisualizationManager.
        
        Args:
            outcomes_df: DataFrame containing outcome data
            schemes: List of discretization schemes
            tradeoff: Optional tradeoff to highlight
            highlight_indices: Optional indices to highlight
            **kwargs: Additional plotting parameters
            
        Returns:
            Matplotlib figure with the visualization
            
        Raises:
            VisualizationError: If plotting fails
        """
        return self.visualization_manager.show_tradeoff_distribution(outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=highlight_indices, **kwargs)
    
    def show_quality_objective_space(self, outcomes_df: pd.DataFrame, x_metric: str, y_metric: str, schemes: List[DiscretizationScheme], highlight_indices_map: Optional[Dict[str, np.ndarray]] = None, policy_series: Optional[pd.Series] = None, show_overall: bool = True, color_points: bool = True, draw_rectangles: bool = False, eps: float = 0.01, background_alpha: float = 0.6, annotation_text: Optional[str] = None, **kwargs) -> plt.Figure:
        """Plots a 2D scatter of outcomes with tradeoff overlays.
        
        Delegates to the VisualizationManager.
        
        Args:
            outcomes_df: DataFrame containing outcome data
            x_metric: Name of metric for x-axis
            y_metric: Name of metric for y-axis
            schemes: List of discretization schemes
            highlight_indices_map: Mapping of tradeoff names to row indices
            policy_series: Series mapping indices to policy names
            show_overall: Whether to show overall distribution
            color_points: Whether to color points by tradeoff
            draw_rectangles: Whether to draw tradeoff rectangles
            eps: Epsilon factor to enlarge tradeoff rectangles
            background_alpha: Alpha for gray background points
            annotation_text: Optional text to display in a box inside the plot
            **kwargs: Additional plotting parameters
            
        Returns:
            Matplotlib figure with the visualization
            
        Raises:
            VisualizationError: If plotting fails
        """
        return self.visualization_manager.show_quality_objective_space(
            outcomes_df, x_metric, y_metric, schemes,
            highlight_indices_map=highlight_indices_map,
            policy_series=policy_series,
            show_overall=show_overall,
            color_points=color_points,
            draw_rectangles=draw_rectangles,
            eps=eps,
            background_alpha=background_alpha,
            annotation_text=annotation_text,
            **kwargs
        )

    def show_stability_radius_plot(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, target_mask: pd.Series, parameter_cols: List[str], radius_info: Dict[str, Any], objective_cols: Tuple[str, str], schemes: List[DiscretizationScheme], target_tradeoff: Optional[Tradeoff] = None, policy_name: Optional[str] = None, **kwargs) -> plt.Figure:
        """Visualizes the stability radius in both parameter and objective space.
        
        Delegates to the VisualizationManager.
        """
        return self.visualization_manager.show_stability_radius_plot(
            experiments_df, outcomes_df, target_mask, parameter_cols, 
            radius_info, objective_cols, schemes, target_tradeoff=target_tradeoff, 
            policy_name=policy_name, **kwargs
        )

    def show_robustness_heatmap(self, matrix: pd.DataFrame, metric: str = 'starr', **kwargs) -> plt.Figure:
        """Visualizes a robustness matrix as a heatmap."""
        return self.visualization_manager.show_robustness_heatmap(matrix, metric=metric, **kwargs)

    def show_robustness_comparison_heatmap(self, baseline_matrix: pd.DataFrame, improved_matrix: pd.DataFrame, metric: str = 'starr', **kwargs) -> plt.Figure:
        """Visualizes a comparison of robustness matrices."""
        return self.visualization_manager.show_robustness_comparison_heatmap(baseline_matrix, improved_matrix, metric=metric, **kwargs)


__all__ = ["ArchSpaceCore", "VisualizationManager"]