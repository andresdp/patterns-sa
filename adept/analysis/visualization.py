import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Dict
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
        
        # Calculate consistent bins for both histograms
        # We use 'auto' or a fixed number to ensure they line up perfectly
        bins = np.histogram_bin_edges(data.dropna(), bins='auto')

        # Plot Overall Histogram/KDE
        sns.histplot(data, bins=bins, kde=True, ax=ax, color='skyblue', label='Overall', alpha=0.4)
        
        # Plot Highlighted Subset
        if highlight_indices is not None and len(highlight_indices) > 0:
            # Ensure we only use indices within bounds
            valid_indices = highlight_indices[highlight_indices < len(data)]
            subset_data = data.iloc[valid_indices]
            if not subset_data.empty:
                sns.histplot(subset_data, bins=bins, kde=False, ax=ax, color='orange', label='Target Tradeoff', alpha=0.8)
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
    


def show_quality_objective_space(
    outcomes_df: pd.DataFrame,
    x_metric: str,
    y_metric: str,
    schemes: List[DiscretizationScheme],
    highlight_indices_map: Optional[Dict[str, np.ndarray]] = None,
    alpha: float = 0.5,
    figsize: tuple = (10, 8)
) -> plt.Figure:
    """
    Plots a 2D scatter of two outcomes with tradeoff segmentation lines and highlighting.
    
    Args:
        outcomes_df: DataFrame containing the continuous outcome data.
        x_metric: Name of the metric for X axis.
        y_metric: Name of the metric for Y axis.
        schemes: List of DiscretizationScheme objects.
        highlight_indices_map: Optional map of {label: indices} to highlight in different colors.
        alpha: Transparency for the default points.
        figsize: Figure size.
        
    Returns:
        matplotlib Figure object.
    """
    fig, ax = plt.subplots(figsize=figsize)
    
    # 1. Plot background (all points)
    sns.scatterplot(
        data=outcomes_df, x=x_metric, y=y_metric, 
        ax=ax, color='gray', alpha=alpha, label='Overall', s=20
    )
    
    # 2. Draw segmentation lines and axis labels
    line_color = 'red'
    line_alpha = 0.4
    
    x_scheme = next((s for s in schemes if s.objective_name == x_metric), None)
    y_scheme = next((s for s in schemes if s.objective_name == y_metric), None)
    
    if x_scheme:
        x_bounds = []
        for b in x_scheme.bins:
            if np.isfinite(b.min_value): x_bounds.append(b.min_value)
            if np.isfinite(b.max_value): x_bounds.append(b.max_value)
            
            # Place interval label at the top (slightly offset)
            x_min = b.min_value if np.isfinite(b.min_value) else outcomes_df[x_metric].min()
            x_max = b.max_value if np.isfinite(b.max_value) else outcomes_df[x_metric].max()
            ax.text((x_min + x_max) / 2, ax.get_ylim()[1] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02, 
                    b.label, color=line_color, fontsize=9, fontweight='bold', ha='center', va='bottom')
            
        for val in set(x_bounds):
            ax.axvline(val, color=line_color, linestyle='--', alpha=line_alpha)
            
    if y_scheme:
        y_bounds = []
        for b in y_scheme.bins:
            if np.isfinite(b.min_value): y_bounds.append(b.min_value)
            if np.isfinite(b.max_value): y_bounds.append(b.max_value)
            
            # Place interval label at the right (slightly offset)
            y_min = b.min_value if np.isfinite(b.min_value) else outcomes_df[y_metric].min()
            y_max = b.max_value if np.isfinite(b.max_value) else outcomes_df[y_metric].max()
            ax.text(ax.get_xlim()[1] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.02, (y_min + y_max) / 2, 
                    b.label, color=line_color, fontsize=9, fontweight='bold', ha='left', va='center', rotation=-90)
            
        for val in set(y_bounds):
            ax.axhline(val, color=line_color, linestyle='--', alpha=line_alpha)

    # 3. Highlight specific tradeoffs if requested
    if highlight_indices_map:
        # Use a qualitative palette for highlights
        colors = sns.color_palette("bright", n_colors=len(highlight_indices_map))
        for i, (label, indices) in enumerate(highlight_indices_map.items()):
            subset = outcomes_df.iloc[indices]
            if not subset.empty:
                sns.scatterplot(
                    data=subset, x=x_metric, y=y_metric, 
                    ax=ax, color=colors[i], label=label, s=20, alpha=alpha, edgecolors='none'
                )

    ax.set_title(f"Architectural Tradeoff Space: {x_metric} vs {y_metric}")
    ax.legend(loc='upper left', bbox_to_anchor=(1.25, 1))
    
    # Adjust layout to make room for labels and legend
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    
    return fig
