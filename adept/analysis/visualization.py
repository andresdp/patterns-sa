import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional
from ..core.models import DiscretizationScheme, Tradeoff

def plot_tradeoff_distribution(
    outcomes_df: pd.DataFrame, 
    schemes: List[DiscretizationScheme], 
    tradeoff: Optional[Tradeoff] = None,
    highlight_indices: Optional[np.ndarray] = None,
    figsize: tuple = (10, 6)
) -> plt.Figure:
    """
    Plots the distribution of outcomes with overlay for tradeoff regions/bins.
    
    Args:
        outcomes_df: DataFrame containing the continuous outcome data.
        schemes: List of DiscretizationScheme objects defining the bins/thresholds.
        tradeoff: Optional Tradeoff object for context (title, specific focus).
        highlight_indices: Optional array of indices to highlight in the plots.
        figsize: Size of the figure.
        
    Returns:
        matplotlib Figure object.
    """
    
    n_plots = len(schemes)
    fig, axes = plt.subplots(n_plots, 1, figsize=(figsize[0], figsize[1] * n_plots), constrained_layout=True)
    
    if n_plots == 1:
        axes = [axes]
    
    for i, scheme in enumerate(schemes):
        ax = axes[i]
        col_name = scheme.objective_name
        
        if col_name not in outcomes_df.columns:
            continue
            
        data = outcomes_df[col_name]
        
        # Plot Overall Histogram/KDE
        sns.histplot(data, kde=True, ax=ax, color='skyblue', label='Overall', alpha=0.4)
        
        # Plot Highlighted Subset
        if highlight_indices is not None and len(highlight_indices) > 0:
            # Ensure we only use indices within bounds
            valid_indices = highlight_indices[highlight_indices < len(data)]
            subset_data = data.iloc[valid_indices]
            if not subset_data.empty:
                sns.histplot(subset_data, kde=False, ax=ax, color='orange', label='Target Tradeoff', alpha=0.8)
                ax.legend()

        # Overlay Bins
        # We collect boundaries from the bins. 
        # Bins are [min, max]. We only need unique boundaries.
        boundaries = set()
        for b in scheme.bins:
            # Handle infinite boundaries for plotting
            min_val = b.min_value
            max_val = b.max_value
            
            # Replace infinities with data limits for visual sanity
            if min_val == float('-inf'):
                min_val = data.min()
            if max_val == float('inf'):
                max_val = data.max()
                
            boundaries.add(min_val)
            boundaries.add(max_val)
            
            # Add text label for the region
            mid_point = (min_val + max_val) / 2
            # Check if mid_point is within data range to avoid labeling empty space
            if data.min() <= mid_point <= data.max():
                ax.text(mid_point, ax.get_ylim()[1] * 0.9, b.label, 
                        ha='center', va='top', fontsize=9, fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        # Plot vertical lines for boundaries
        for b in boundaries:
            if data.min() < b < data.max(): # Only plot lines within the data range
                ax.axvline(b, color='red', linestyle='--', alpha=0.8)
        
        ax.set_title(f"Distribution of {col_name}")
        ax.set_xlabel(col_name)
        ax.set_ylabel("Frequency")

    title = f"Outcome Distributions & Tradeoff Definitions"
    if tradeoff:
        title += f"\n({tradeoff.name}: {tradeoff.description})"
    fig.suptitle(title, fontsize=14)
    
    return fig
