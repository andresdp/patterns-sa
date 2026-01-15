import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Tuple, Any
from ..core.models import DiscretizationScheme, Tradeoff, QualityBin
import sankeyflow as sf
from sklearn.manifold import MDS
from sklearn.preprocessing import MinMaxScaler

def show_tradeoff_distribution(
    outcomes_df: pd.DataFrame, 
    schemes: List[DiscretizationScheme], 
    tradeoff: Optional[Tradeoff] = None,
    highlight_indices: Optional[np.ndarray] = None,
    figsize: Tuple[int, int] = (10, 6),
    title: Optional[str] = None,
    bins: int = 30
) -> plt.Figure:
    """
    Plots the distribution of outcomes with an overlay of tradeoff regions/bins.
    
    This function generates a vertical stack of histograms (one per quality objective) 
    showing the overall distribution of the population, with the option to highlight 
    a specific architectural tradeoff.

    Args:
        outcomes_df (pd.DataFrame): [Mandatory] Continuous outcome data. 
            Must contain columns matching the objective names in 'schemes'.
        schemes (List[DiscretizationScheme]): [Mandatory] Definitions of bins and 
            labels for each objective.
        tradeoff (Optional[Tradeoff]): [Optional] A tradeoff object for context. 
            If provided, its name and description will be used in the plot title.
        highlight_indices (Optional[np.ndarray]): [Optional] Array of row indices 
            from 'outcomes_df' that satisfy the target tradeoff. These will be 
            rendered as an overlaid histogram in a distinct color (orange).
        figsize (Tuple[int, int]): [Optional] Size of each individual objective 
            subplot. Defaults to (10, 6).
        title (Optional[str]): [Optional] Title of the plot. If not provided, a default title will be generated.
        bins (int): [Optional] Number of bins to use for histograms. Defaults to 30.
        
    Returns:
        matplotlib.figure.Figure: The generated figure object.
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
        
        # Calculate explicit bin edges based on the overall data range
        # This ensures that both the overall and subset histograms align perfectly
        bin_edges = np.histogram_bin_edges(data.dropna(), bins=bins)

        # 1. Overall Distribution (Blue)
        sns.histplot(data, bins=bin_edges, kde=True, ax=ax, color='skyblue', label='Overall', alpha=0.4)
        
        # 2. Highlight Subset (Orange)
        if highlight_indices is not None and len(highlight_indices) > 0:
            valid_indices = highlight_indices[highlight_indices < len(data)]
            subset_data = data.iloc[valid_indices]
            if not subset_data.empty:
                sns.histplot(subset_data, bins=bin_edges, kde=False, ax=ax, color='orange', label='Target Tradeoff', alpha=0.8)
                ax.legend()

        # 3. Overlay Bin Boundaries and Labels
        boundaries = set()
        for b in scheme.bins:
            min_val = b.min_value if np.isfinite(b.min_value) else data.min()
            max_val = b.max_value if np.isfinite(b.max_value) else data.max()
            boundaries.add(min_val)
            boundaries.add(max_val)
            
            mid_point = (min_val + max_val) / 2
            if data.min() <= mid_point <= data.max():
                ax.text(mid_point, ax.get_ylim()[1] * 0.9, b.label, 
                        ha='center', va='top', fontsize=9, color='red', fontweight='bold',
                        bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

        print("BOUNDARIES",boundaries)
        for b in boundaries:
            if data.min() <= b <= data.max():
                ax.axvline(b, color='red', linestyle='--', alpha=0.8)
        
        # ax.set_title(f"Distribution of {col_name}")
        ax.set_xlabel(col_name)
        ax.set_ylabel("Frequency")

    title = f"Outcome Distributions" if title is None else title
    if tradeoff:
        # title += f"\n({tradeoff.name}: {tradeoff.description})"
        title += f" / Target Tradeoff: {tradeoff.name}"
    fig.suptitle(title, fontsize=14)
    
    return fig


def show_quality_objective_space(
    outcomes_df: pd.DataFrame, 
    x_metric: str, 
    y_metric: str, 
    schemes: List[DiscretizationScheme], 
    highlight_indices_map: Optional[Dict[str, np.ndarray]] = None,
    policy_series: Optional[pd.Series] = None,
    show_overall: bool = True,
    color_points: bool = True,
    draw_rectangles: bool = False,
    **kwargs
) -> plt.Figure:
    """
    Plots a 2D scatter of outcomes with tradeoff overlays.
    """
    title = kwargs.pop('title', None)
    
    fig, ax = plt.subplots(figsize=kwargs.get('figsize', (12, 8)))
    alpha = kwargs.get('alpha', 0.3)
    s = kwargs.get('s', 20)
    
    # Determine mode
    coloring_by_policy = policy_series is not None
    
    if coloring_by_policy:
        # If coloring by policy, we disable point coloring for tradeoffs to avoid conflict
        # and enforce rectangles if they weren't explicitly disabled (or we can just respect the user's choice,
        # but the prompt suggested enforcing it). 
        # "If these policies are enabled, then tradeoff regions can be only selected/shown using rectangles"
        color_points = False
        draw_rectangles = True

    # 1. Plot Background (all points)
    # If coloring by policy, we plot the gray background first (zorder=0) to show unselected/NaN policies
    if coloring_by_policy and show_overall:
        sns.scatterplot(
            data=outcomes_df, x=x_metric, y=y_metric, 
            ax=ax, color='gray', alpha=alpha, s=s, zorder=0
        )
    elif not coloring_by_policy:
         sns.scatterplot(
            data=outcomes_df, x=x_metric, y=y_metric, 
            ax=ax, 
            color='gray' if show_overall else 'white', 
            alpha=alpha if show_overall else 0, 
            label='Overall' if show_overall else None, 
            s=s
        )
    
    # 2. Plot Policies (if enabled)
    if coloring_by_policy:
        plot_data = outcomes_df.copy()
        plot_data['__policy__'] = policy_series
        # Filter out NaNs to avoid clutter or errors, assuming background already shows them
        plot_data = plot_data.dropna(subset=['__policy__'])
        
        if not plot_data.empty:
            sns.scatterplot(
                data=plot_data, x=x_metric, y=y_metric,
                hue='__policy__',
                ax=ax,
                alpha=alpha,
                s=s,
                legend='full'
            )

    # 3. Draw Segmentation Boundaries and Interval Labels
    x_scheme = next((s for s in schemes if s.objective_name == x_metric), None)
    y_scheme = next((s for s in schemes if s.objective_name == y_metric), None)
    
    _apply_axis_segmentation(ax, x_scheme, outcomes_df[x_metric], orientation='x')
    _apply_axis_segmentation(ax, y_scheme, outcomes_df[y_metric], orientation='y')

    # 4. Highlight Specific Tradeoffs
    if highlight_indices_map:
        # Use a distinct palette for tradeoffs if we are coloring points by tradeoff
        # If coloring by policy, color_points is False, so we only use colors for Rectangles
        colors = sns.color_palette("bright", n_colors=len(highlight_indices_map))
        
        for i, (label, indices) in enumerate(highlight_indices_map.items()):
            subset = outcomes_df.iloc[indices]
            if subset.empty:
                continue
                
            color = colors[i]
            
            if draw_rectangles:
                x_min, x_max = subset[x_metric].min(), subset[x_metric].max()
                y_min, y_max = subset[y_metric].min(), subset[y_metric].max()
                rect = patches.Rectangle(
                    (x_min, y_min), x_max - x_min, y_max - y_min,
                    linewidth=2, edgecolor=color, facecolor=color, alpha=0.2,
                    label=f"{label} (tradeoff area)"
                )
                ax.add_patch(rect)

            if color_points:
                sns.scatterplot(
                    data=subset, x=x_metric, y=y_metric, 
                    ax=ax, color=color, label=label, s=s, alpha=alpha, edgecolors='none'
                )

    if title is None:
        ax.set_title(f"Quality Objective Space: {x_metric} vs {y_metric}", pad=30)
    else:
        ax.set_title(title, pad=30)
    
    # Handle Legend
    # If both hue (policies) and rectangles (tradeoffs) are present, legend might need adjustment
    # Seaborn automatically adds hue to legend. We might need to manually ensure rects are added.
    # But usually standard legend handles it.
    # We move legend outside
    ax.legend(loc='upper left', bbox_to_anchor=(1.05, 1), borderaxespad=0.)
    
    plt.tight_layout(rect=[0, 0, 0.85, 0.95])
    return fig


def show_contingency_heatmap(
    contingency_table: pd.DataFrame, 
    figsize: Tuple[int, int] = (10, 8),
    title: str = "Policy vs. Tradeoff Contingency"
) -> plt.Figure:
    """
    Plots a heatmap of the policy-tradeoff contingency table.
    
    Args:
        contingency_table: DataFrame with percentages (0-1) or counts.
        figsize: Figure size.
        title: Plot title.
        
    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        contingency_table, 
        annot=True, 
        fmt=".1f", # Assuming percentages like 15.5
        cmap="YlGnBu", 
        ax=ax,
        cbar_kws={'label': 'Percentage / Frequency'}
    )
    ax.set_title(title, pad=20)
    ax.set_xlabel("Tradeoff")
    ax.set_ylabel("Decision / Policy")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, horizontalalignment='right')

    plt.tight_layout()
    return fig

def show_policy_tradeoff_sankey(
    contingency_table: pd.DataFrame,
    figsize: Tuple[int, int] = (12, 8),
    title: str = "Policy -> Tradeoff Flow"
) -> plt.Figure:
    """
    Plots a Sankey diagram showing flow from Policies to Tradeoffs.
    
    Args:
        contingency_table: DataFrame with percentages or counts.
                           Index: Source nodes (Policies).
                           Columns: Target nodes (Tradeoffs).
        figsize: Figure size.
        title: Plot title.
        
    Returns:
        matplotlib.figure.Figure
    """
    # 1. Prepare data for SankeyFlow
    # It expects: flows list of (source, target, value)
    flows = []
    
    for policy_name in contingency_table.index:
        for tradeoff_name in contingency_table.columns:
            val = contingency_table.loc[policy_name, tradeoff_name]
            if val > 0:
                flows.append((policy_name, tradeoff_name, val))
                
    # 2. Plot
    plt.figure(figsize=figsize)
    s = sf.Sankey(
        flows=flows, 
        aspect_ratio=4/3, 
        nodelabels=True, 
        link_color="source" # Or "target", "none"
    )
    s.draw()
    plt.title(title)
    
    return plt.gcf()


def show_importance_heatmap(
    scores_df: pd.DataFrame, 
    figsize: Tuple[int, int] = (10, 8),
    title: str = "Feature Importance Scores"
) -> plt.Figure:
    """
    Plots a heatmap of feature importance scores.
    
    Args:
        scores_df: DataFrame with importance scores (Rows=Features, Cols=Outcomes).
        figsize: Figure size.
        title: Plot title.
        
    Returns:
        matplotlib.figure.Figure
    """
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        scores_df, 
        annot=True, 
        fmt=".3f", 
        cmap="Reds", 
        ax=ax,
        cbar_kws={'label': 'Importance Score'}
    )
    ax.set_title(title, pad=20)
    ax.set_xlabel("Quality Objectives")
    ax.set_ylabel("Parameters")
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, horizontalalignment='right')

    plt.tight_layout()
    return fig


def _apply_axis_segmentation(ax: plt.Axes, scheme: Optional[DiscretizationScheme], data: pd.Series, orientation: str = 'x'):
    """Helper to apply segmentation lines and labels to a specific axis."""
    if not scheme:
        return
        
    line_color = 'red'
    line_alpha = 0.4
    bounds = set()
    
    for b in scheme.bins:
        if np.isfinite(b.min_value): bounds.add(b.min_value)
        if np.isfinite(b.max_value): bounds.add(b.max_value)
        
        # Calculate label position
        val_min = b.min_value if np.isfinite(b.min_value) else data.min()
        val_max = b.max_value if np.isfinite(b.max_value) else data.max()
        mid = (val_min + val_max) / 2
        
        if orientation == 'x':
            ax.text(mid, ax.get_ylim()[1] + (ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.02, 
                    b.label, color=line_color, fontsize=9, fontweight='bold', ha='center', va='bottom')
        else:
            ax.text(ax.get_xlim()[1] + (ax.get_xlim()[1] - ax.get_xlim()[0]) * 0.02, mid, 
                    b.label, color=line_color, fontsize=9, fontweight='bold', ha='left', va='center', rotation=-90)
            
    for val in bounds:
        if orientation == 'x':
            ax.axvline(val, color=line_color, linestyle='--', alpha=line_alpha)
        else:
            ax.axhline(val, color=line_color, linestyle='--', alpha=line_alpha)


def show_stability_radius_plot(
    experiments_df: pd.DataFrame,
    outcomes_df: pd.DataFrame,
    target_mask: pd.Series,
    parameter_cols: List[str],
    radius_info: Dict[str, Any],
    objective_cols: Tuple[str, str],
    schemes: List[DiscretizationScheme],
    figsize: Tuple[int, int] = (14, 6),
    max_points: int = 2000
) -> plt.Figure:
    """
    Visualizes the stability radius in both parameter and objective space.
    
    Args:
        experiments_df: Filtered parameters for the policy.
        outcomes_df: Filtered outcomes for the policy.
        target_mask: Success/Failure mask.
        parameter_cols: Names of parameters used for distance.
        radius_info: Output from compute_stability_radius.
        objective_cols: Pair of outcomes to plot on right panel.
        schemes: Discretization schemes for outcome axes.
        figsize: Figure size.
        max_points: Max points to plot using MDS (downsampling threshold).
    """
    import matplotlib.patches as patches
    
    # 1. Downsampling for performance
    n_points = len(experiments_df)
    if n_points > max_points:
        indices = np.random.choice(n_points, max_points, replace=False)
        exp_sub = experiments_df.iloc[indices]
        out_sub = outcomes_df.iloc[indices]
        mask_sub = target_mask.iloc[indices]
    else:
        exp_sub = experiments_df
        out_sub = outcomes_df
        mask_sub = target_mask

    # 2. MDS Projection of Parameter Space
    X = exp_sub[parameter_cols].select_dtypes(include=[np.number])
    scaler = MinMaxScaler()
    X_norm = scaler.fit_transform(X)
    
    # Add Centroid to projection
    if 'normalized_baseline' in radius_info['details']:
        centroid_norm = np.array(radius_info['details']['normalized_baseline']).reshape(1, -1)
    else:
        # Fallback (should not be reached with current analyzer)
        # Note: If baseline is in original scale, this would be wrong without scaler.transform
        # But previous code assumed baseline was from mean() of X_norm if not provided.
        centroid_norm = np.array(list(radius_info['details']['baseline'].values())).reshape(1, -1)

    X_combined = np.vstack([X_norm, centroid_norm])
    
    mds = MDS(n_components=2, random_state=42, normalized_stress='auto')
    X_2d = mds.fit_transform(X_combined)
    
    points_2d = X_2d[:-1]
    centroid_2d = X_2d[-1]

    # 3. Setup Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    # Left Panel: Parameter Space
    colors = ['green' if v else 'red' for v in mask_sub]
    ax1.scatter(points_2d[:, 0], points_2d[:, 1], c=colors, alpha=0.5, s=25, edgecolors='none')
    
    # Plot Centroid (Nominal Solution) in Black
    ax1.scatter(centroid_2d[0], centroid_2d[1], c='black', marker='*', s=200, label='Nominal (Centroid)', edgecolors='white', zorder=5)
    
    # Draw visual stability radius in 2D
    # We find the nearest 2D distance to a failure point to represent the radius visually
    failures_2d = points_2d[~mask_sub.values]
    if len(failures_2d) > 0:
        dists_2d = np.linalg.norm(failures_2d - centroid_2d, axis=1)
        visual_r = np.min(dists_2d)
        circle = patches.Circle(centroid_2d, visual_r, fill=False, edgecolor='black', linestyle='--', alpha=0.6)
        ax1.add_patch(circle)
    
    ax1.set_title(f"Parameter Space Projection (MDS)\nRadius ({radius_info['details']['distance_metric']}): {radius_info['value']:.3f}")
    ax1.legend(loc='lower left', fontsize='small')

    # Right Panel: Objective Space
    x_obj, y_obj = objective_cols
    ax2.scatter(out_sub[x_obj], out_sub[y_obj], c=colors, alpha=0.6, s=30)
    
    # Add axis segmentation for context
    scheme_x = next((s for s in schemes if s.objective_name == x_obj), None)
    scheme_y = next((s for s in schemes if s.objective_name == y_obj), None)
    _apply_axis_segmentation(ax2, scheme_x, outcomes_df[x_obj], orientation='x')
    _apply_axis_segmentation(ax2, scheme_y, outcomes_df[y_obj], orientation='y')
    
    ax2.set_title(f"Objective Space: {x_obj} vs {y_obj}")
    ax2.set_xlabel(x_obj)
    ax2.set_ylabel(y_obj)

    plt.tight_layout()
    return fig