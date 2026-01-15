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

        # print("BOUNDARIES",boundaries)
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
    eps: float = 0.01,
    background_alpha: float = 0.6,
    annotation_text: Optional[str] = None,
    annotation_loc: str = 'auto',
    **kwargs
) -> plt.Figure:
    """
    Plots a 2D scatter of outcomes with tradeoff overlays.
    """
    title = kwargs.pop('title', None)
    figsize = kwargs.get('figsize', (12, 8))
    
    fig, ax = plt.subplots(figsize=figsize)
    
    alpha = kwargs.get('alpha', 0.3)
    s = kwargs.get('s', 20)
    
    # Determine mode
    coloring_by_policy = policy_series is not None
    
    if coloring_by_policy:
        color_points = False
        draw_rectangles = True

    # 1. Plot Background (all points)
    if coloring_by_policy and show_overall:
        sns.scatterplot(
            data=outcomes_df, x=x_metric, y=y_metric, 
            ax=ax, color='gray', alpha=background_alpha, s=s, zorder=0
        )
    elif not coloring_by_policy:
         sns.scatterplot(
            data=outcomes_df, x=x_metric, y=y_metric, 
            ax=ax, 
            color='gray' if show_overall else 'white', 
            alpha=background_alpha if show_overall else 0, 
            label='Overall' if show_overall else None, 
            s=s
        )
    
    # 2. Plot Policies (if enabled)
    if coloring_by_policy:
        plot_data = outcomes_df.copy()
        plot_data['__policy__'] = policy_series
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
        colors = sns.color_palette("bright", n_colors=len(highlight_indices_map))
        
        for i, (label, indices) in enumerate(highlight_indices_map.items()):
            subset = outcomes_df.iloc[indices]
            if subset.empty:
                continue
                
            color = colors[i]
            
            if draw_rectangles:
                x_range_all = outcomes_df[x_metric].max() - outcomes_df[x_metric].min()
                y_range_all = outcomes_df[y_metric].max() - outcomes_df[y_metric].min()
                
                eps_x = x_range_all * eps if x_range_all > 0 else 0.5
                eps_y = y_range_all * eps if y_range_all > 0 else 0.5
                
                x_min, x_max = subset[x_metric].min() - eps_x, subset[x_metric].max() + eps_x
                y_min, y_max = subset[y_metric].min() - eps_y, subset[y_metric].max() + eps_y
                
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
    
    # 5. Add Annotation Text (Inset)
    if annotation_text:
        pos_x, pos_y, ha, va = _get_best_annotation_position(outcomes_df, x_metric, y_metric, annotation_loc)
        props = dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='gray')
        ax.text(pos_x, pos_y, annotation_text, transform=ax.transAxes, fontsize=9,
                verticalalignment=va, horizontalalignment=ha, multialignment='left',
                bbox=props, zorder=15, family='monospace')

    # Handle Legend
    # Move legend to the bottom, horizontal layout
    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, borderaxespad=0.)
    
    plt.tight_layout()
    return fig

def _get_best_annotation_position(df, x_col, y_col, manual_loc='auto'):
    """Finds the corner with lowest point density for annotation placement."""
    if manual_loc != 'auto':
        mapping = {
            'upper left': (0.02, 0.98, 'left', 'top'),
            'upper right': (0.98, 0.98, 'right', 'top'),
            'lower left': (0.02, 0.02, 'left', 'bottom'),
            'lower right': (0.98, 0.02, 'right', 'bottom')
        }
        return mapping.get(manual_loc, (0.02, 0.98, 'left', 'top'))

    # Calculate quadrant densities
    x_mid = df[x_col].median()
    y_mid = df[y_col].median()
    
    q_ul = ((df[x_col] <= x_mid) & (df[y_col] >= y_mid)).sum()
    q_ur = ((df[x_col] > x_mid) & (df[y_col] >= y_mid)).sum()
    q_ll = ((df[x_col] <= x_mid) & (df[y_col] < y_mid)).sum()
    q_lr = ((df[x_col] > x_mid) & (df[y_col] < y_mid)).sum()
    
    counts = {'upper left': q_ul, 'upper right': q_ur, 'lower left': q_ll, 'lower right': q_lr}
    best_corner = min(counts, key=counts.get)
    
    # Return coordinates and alignments
    return _get_best_annotation_position(df, x_col, y_col, best_corner)

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
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
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
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha='right')
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
                    b.label, color=line_color, fontsize=9, fontweight='bold', ha='left', va='center', rotation=90)
            
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
    target_tradeoff: Optional[Tradeoff] = None,
    policy_name: Optional[str] = None,
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
        target_tradeoff: The specific Tradeoff object being analyzed.
        policy_name: Name of the policy for labeling.
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
        centroid_norm = np.array(list(radius_info['details']['baseline'].values())).reshape(1, -1)

    X_combined = np.vstack([X_norm, centroid_norm])
    
    mds = MDS(n_components=2, random_state=42, normalized_stress='auto', max_iter=100)
    X_2d = mds.fit_transform(X_combined)
    
    points_2d = X_2d[:-1]
    centroid_2d = X_2d[-1]

    # 3. Setup Plot
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    if policy_name:
        fig.suptitle(f"Stability Analysis for Policy: {policy_name}", fontsize=16, fontweight='bold', y=1.05)
    
    # Left Panel: Parameter Space
    colors = ['green' if v else 'red' for v in mask_sub]
    ax1.scatter(points_2d[:, 0], points_2d[:, 1], c=colors, alpha=0.5, s=25, edgecolors='none')
    
    # Plot Centroid (Nominal Solution) in Black
    ax1.scatter(centroid_2d[0], centroid_2d[1], c='black', marker='*', s=200, label='Nominal (Centroid)', edgecolors='white', zorder=5)
    
    # Draw visual stability radius in 2D
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
    
    # Plot Outcome Centroid (Nominal Outcome)
    out_centroid_x = out_sub[x_obj].mean()
    out_centroid_y = out_sub[y_obj].mean()
    ax2.scatter(out_centroid_x, out_centroid_y, c='black', marker='*', s=200, label='Nominal Outcome', edgecolors='white', zorder=5)
    
    # Highlight Target Region
    if target_tradeoff:
        # Find bounds for x and y
        x_label = target_tradeoff.elements.get(x_obj)
        y_label = target_tradeoff.elements.get(y_obj)
        
        x_bounds = (-np.inf, np.inf)
        y_bounds = (-np.inf, np.inf)
        
        # Helper to get bounds from scheme
        def get_bounds(obj, label):
            scheme = next((s for s in schemes if s.objective_name == obj), None)
            if scheme:
                for b in scheme.bins:
                    if b.label == label:
                        return (b.min_value, b.max_value)
            return (-np.inf, np.inf)

        if x_label: x_bounds = get_bounds(x_obj, x_label)
        if y_label: y_bounds = get_bounds(y_obj, y_label)
        
        # Draw Rectangle (handle infs for plotting)
        # We need plot limits to handle inf
        x_lims = ax2.get_xlim()
        y_lims = ax2.get_ylim()
        
        rect_x_min = x_bounds[0] if np.isfinite(x_bounds[0]) else x_lims[0] - 100
        rect_x_max = x_bounds[1] if np.isfinite(x_bounds[1]) else x_lims[1] + 100
        rect_y_min = y_bounds[0] if np.isfinite(y_bounds[0]) else y_lims[0] - 100
        rect_y_max = y_bounds[1] if np.isfinite(y_bounds[1]) else y_lims[1] + 100
        
        width = rect_x_max - rect_x_min
        height = rect_y_max - rect_y_min
        
        rect = patches.Rectangle((rect_x_min, rect_y_min), width, height, 
                                 linewidth=1, edgecolor='green', facecolor='green', alpha=0.1, zorder=0)
        ax2.add_patch(rect)

    # Add axis segmentation
    scheme_x = next((s for s in schemes if s.objective_name == x_obj), None)
    scheme_y = next((s for s in schemes if s.objective_name == y_obj), None)
    _apply_axis_segmentation(ax2, scheme_x, outcomes_df[x_obj], orientation='x')
    _apply_axis_segmentation(ax2, scheme_y, outcomes_df[y_obj], orientation='y')
    
    ax2.set_title(f"Objective Space: {x_obj} vs {y_obj}")
    ax2.set_xlabel(x_obj)
    ax2.set_ylabel(y_obj)
    plt.tight_layout()
    return fig


def show_robustness_heatmap(
    matrix: pd.DataFrame,
    metric: str = 'starr',
    figsize: Tuple[int, int] = (12, 10),
    title: Optional[str] = None
) -> plt.Figure:
    """
    Plots a heatmap of the policy vs. tradeoff robustness matrix.
    
    Args:
        matrix: DataFrame from compute_policy_robustness_matrix or get_robustness_report.
        metric: 'starr' or 'regret'.
        figsize: Figure size.
        title: Optional plot title.
    """
    fig, ax = plt.subplots(figsize=figsize)
    _apply_robustness_heatmap(ax, matrix, metric, title)
    plt.tight_layout()
    return fig


def show_robustness_comparison_heatmap(
    baseline_matrix: pd.DataFrame,
    improved_matrix: pd.DataFrame,
    metric: str = 'starr',
    figsize: Tuple[int, int] = (14, 12),
    title: Optional[str] = None
) -> plt.Figure:
    """
    Plots two stacked heatmaps comparing baseline robustness vs. improved (box-constrained) robustness.
    """
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    _apply_robustness_heatmap(ax1, baseline_matrix, metric, "Baseline Robustness (Overall)")
    _apply_robustness_heatmap(ax2, improved_matrix, metric, "Improved Robustness (Under Box Constraints)")
    
    # Hide X-label for the top plot to keep it clean (since sharex=True)
    ax1.set_xlabel("")
    
    if title:
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig


def _apply_robustness_heatmap(ax, matrix, metric, title):
    """Internal helper to draw a robustness heatmap on a specific axis."""
    metric_clean = metric.lower()
    if metric_clean in ['starr', 'density']:
        cmap = "YlGn"
    else:
        cmap = "YlOrRd"
    
    sns.heatmap(
        matrix.astype(float), 
        annot=True, 
        fmt=".2f",
        cmap=cmap,
        ax=ax,
        cbar_kws={'label': f'{metric.upper()}'}
    )
    
    ax.set_title(title, pad=15, fontsize=12, fontweight='bold')
    ax.set_xlabel("Target Tradeoff / Box Constraints")
    ax.set_ylabel("Policy / Configuration")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=90, ha='right')
    ax.set_yticklabels(ax.get_yticklabels(), rotation=0, horizontalalignment='right')