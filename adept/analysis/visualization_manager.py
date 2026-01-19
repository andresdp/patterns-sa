from typing import Any, Dict, Optional, List, Tuple
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
    
    def show_tradeoff_distribution(self, outcomes_df: pd.DataFrame, schemes: List[Dict], tradeoff: Optional[Dict] = None, highlight_indices: Optional[np.ndarray] = None, **kwargs) -> plt.Figure:
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
            from .visualization import show_tradeoff_distribution
            return show_tradeoff_distribution(outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=highlight_indices, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot tradeoff distribution: {str(e)}")
    
    def show_quality_objective_space(self, outcomes_df: pd.DataFrame, x_metric: str, y_metric: str, schemes: List[Dict], eps: float = 0.01, background_alpha: float = 0.6, annotation_text: Optional[str] = None, **kwargs) -> plt.Figure:
        """Plots a 2D scatter of outcomes with tradeoff overlays.
        
        Args:
            outcomes_df: DataFrame containing outcome data
            x_metric: Name of metric for x-axis
            y_metric: Name of metric for y-axis
            schemes: List of discretization schemes
            eps: Epsilon factor to enlarge tradeoff rectangles
            background_alpha: Alpha for gray background points
            annotation_text: Optional text to display in a box inside the plot
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
            return show_quality_objective_space(
                outcomes_df, x_metric, y_metric, schemes, 
                eps=eps, background_alpha=background_alpha, 
                annotation_text=annotation_text, **kwargs
            )
        except Exception as e:
            raise VisualizationError(f"Failed to plot quality objective space: {str(e)}")

    def show_stability_radius_plot(self, experiments_df: pd.DataFrame, outcomes_df: pd.DataFrame, target_mask: pd.Series, parameter_cols: List[str], radius_info: Dict[str, Any], objective_cols: Tuple[str, str], schemes: List[Any], target_tradeoff: Optional[Any] = None, policy_name: Optional[str] = None, **kwargs) -> plt.Figure:
        """
        Visualizes the stability radius in both parameter and objective space.
        """
        try:
            from .visualization import show_stability_radius_plot
            return show_stability_radius_plot(
                experiments_df, outcomes_df, target_mask, parameter_cols, 
                radius_info, objective_cols, schemes, target_tradeoff=target_tradeoff, 
                policy_name=policy_name, **kwargs
            )
        except Exception as e:
            raise VisualizationError(f"Failed to plot stability radius: {str(e)}")

    def show_robustness_heatmap(self, matrix: pd.DataFrame, metric: str = 'starr', **kwargs) -> plt.Figure:
        """Plots a heatmap of the policy vs. tradeoff robustness matrix."""
        try:
            from .visualization import show_robustness_heatmap
            return show_robustness_heatmap(matrix, metric=metric, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot robustness heatmap: {str(e)}")

    def show_robustness_comparison_heatmap(self, baseline_matrix: pd.DataFrame, improved_matrix: pd.DataFrame, metric: str = 'starr', **kwargs) -> plt.Figure:
        """Plots stacked heatmaps comparing baseline vs. improved robustness."""
        try:
            from .visualization import show_robustness_comparison_heatmap
            return show_robustness_comparison_heatmap(baseline_matrix, improved_matrix, metric=metric, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot robustness comparison: {str(e)}")

    def show_robustness_uplift(self, uplift_df: pd.DataFrame, metric: str = 'starr', highlight_policies: Optional[List[str]] = None, **kwargs) -> plt.Figure:
        """
        Plots a scatter chart of Baseline vs. Uplift per policy.
        """
        try:
            from .visualization import show_robustness_uplift
            return show_robustness_uplift(uplift_df, metric=metric, highlight_policies=highlight_policies, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot robustness uplift: {str(e)}")

    def show_multiple_robustness_uplifts(self, uplift_datasets: Dict[str, pd.DataFrame], metric: str = 'starr', highlight_policies: Optional[List[str]] = None, **kwargs) -> plt.Figure:
        """
        Plots robustness uplifts for multiple boxes/tradeoffs on the same chart.
        """
        try:
            from .visualization import show_multiple_robustness_uplifts
            return show_multiple_robustness_uplifts(uplift_datasets, metric=metric, highlight_policies=highlight_policies, **kwargs)
        except Exception as e:
            raise VisualizationError(f"Failed to plot multiple robustness uplifts: {str(e)}")
    
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
