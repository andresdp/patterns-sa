from typing import Any, Dict, Optional, List
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Import custom exceptions
try:
    from ..utils.exceptions import VisualizationError
except ImportError:
    # Fallback for backward compatibility
    class VisualizationError(Exception):
        pass

class VisualizationManager:
    """Manages visualizations by providing a unified interface to plotting functions.
    
    This simplified manager directly delegates to the functional visualization API
    after performing input validation.
    """
    
    def __init__(self):
        pass
    
    def plot_tradeoff_distribution(self, outcomes_df: pd.DataFrame, schemes: List[Dict], tradeoff: Optional[Dict] = None, highlight_indices: Optional[np.ndarray] = None, **kwargs) -> plt.Figure:
        """Plots outcome distributions with tradeoff overlays.
        
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
        self._validate_plot_inputs(outcomes_df, schemes)
        
        try:
            from .visualization import plot_tradeoff_distribution
            return plot_tradeoff_distribution(outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=highlight_indices, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot tradeoff distribution: {str(e)}")
    
    def show_quality_objective_space(self, outcomes_df: pd.DataFrame, x_metric: str, y_metric: str, schemes: List[Dict], **kwargs) -> plt.Figure:
        """Plots a 2D scatter of outcomes with tradeoff overlays.
        
        Args:
            outcomes_df: DataFrame containing outcome data
            x_metric: Name of metric for x-axis
            y_metric: Name of metric for y-axis
            schemes: List of discretization schemes
            **kwargs: Additional plotting parameters
            
        Returns:
            Matplotlib figure with the visualization
            
        Raises:
            VisualizationError: If plotting fails
        """
        self._validate_plot_inputs(outcomes_df, schemes)
        self._validate_metrics(outcomes_df, x_metric, y_metric)
        
        try:
            from .visualization import show_quality_objective_space
            # Arguments are passed directly via kwargs, avoiding double-passing issues
            # encountered in the previous Strategy pattern implementation.
            return show_quality_objective_space(outcomes_df, x_metric, y_metric, schemes, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot quality objective space: {str(e)}")
    
    def _validate_plot_inputs(self, outcomes_df: pd.DataFrame, schemes: List[Dict]) -> None:
        """Validates common input parameters for plotting methods."""
        if outcomes_df is None:
            raise VisualizationError("outcomes_df cannot be None")
        
        if not isinstance(outcomes_df, pd.DataFrame):
            raise VisualizationError("outcomes_df must be a pandas DataFrame")
        
        if outcomes_df.empty:
            raise VisualizationError("outcomes_df cannot be empty")
        
        if not schemes or not isinstance(schemes, list):
            raise VisualizationError("schemes must be a non-empty list")
    
    def _validate_metrics(self, outcomes_df: pd.DataFrame, x_metric: str, y_metric: str) -> None:
        """Validates that specified metrics exist in the DataFrame."""
        if not x_metric or not isinstance(x_metric, str):
            raise VisualizationError("x_metric must be a non-empty string")
        
        if not y_metric or not isinstance(y_metric, str):
            raise VisualizationError("y_metric must be a non-empty string")
        
        if x_metric not in outcomes_df.columns:
            raise VisualizationError(f"x_metric '{x_metric}' not found in outcomes DataFrame")
        
        if y_metric not in outcomes_df.columns:
            raise VisualizationError(f"y_metric '{y_metric}' not found in outcomes DataFrame")


__all__ = [
    "VisualizationManager"
]
