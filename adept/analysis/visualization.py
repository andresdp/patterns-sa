import matplotlib
# matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import pandas as pd
import numpy as np
from typing import List, Optional, Dict, Tuple, Any, Union
from ..core.models import DiscretizationScheme, Tradeoff, QualityBin
import sankeyflow as sf
from sklearn.manifold import MDS
from sklearn.preprocessing import MinMaxScaler
import matplotlib.gridspec as gridspec

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
        bin_edges = np.histogram_bin_edges(data.dropna(), bins=bins)

        sns.histplot(data, bins=bin_edges, kde=True, ax=ax, color='skyblue', label='Overall', alpha=0.4)
        
        if highlight_indices is not None and len(highlight_indices) > 0:
            valid_indices = highlight_indices[highlight_indices < len(data)]
            subset_data = data.iloc[valid_indices]
            if not subset_data.empty:
                sns.histplot(subset_data, bins=bin_edges, kde=False, ax=ax, color='orange', label='Target Tradeoff', alpha=0.8)
                ax.legend()

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

        for b in boundaries:
            if data.min() <= b <= data.max():
                ax.axvline(b, color='red', linestyle='--', alpha=0.8)
        
        ax.set_xlabel(col_name)
        ax.set_ylabel("Frequency")

    title = f"Outcome Distributions" if title is None else title
    if tradeoff:
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
    
    coloring_by_policy = policy_series is not None
    
    if coloring_by_policy:
        color_points = False
        draw_rectangles = True

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

    x_scheme = next((s for s in schemes if s.objective_name == x_metric), None)
    y_scheme = next((s for s in schemes if s.objective_name == y_metric), None)
    
    _apply_axis_segmentation(ax, x_scheme, outcomes_df[x_metric], orientation='x')
    _apply_axis_segmentation(ax, y_scheme, outcomes_df[y_metric], orientation='y')

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
    
    if annotation_text:
        pos_x, pos_y, ha, va = _get_best_annotation_position(outcomes_df, x_metric, y_metric, annotation_loc)
        props = dict(boxstyle='round', facecolor='white', alpha=0.85, edgecolor='gray')
        ax.text(pos_x, pos_y, annotation_text, transform=ax.transAxes, fontsize=9,
                verticalalignment=va, horizontalalignment=ha, multialignment='left',
                bbox=props, zorder=15, family='monospace')

    ax.legend(loc='upper center', bbox_to_anchor=(0.5, -0.15), ncol=3, borderaxespad=0.)
    
    plt.tight_layout()
    return fig

def _get_best_annotation_position(df, x_col, y_col, manual_loc='auto'):
    if manual_loc != 'auto':
        mapping = {
            'upper left': (0.02, 0.98, 'left', 'top'),
            'upper right': (0.98, 0.98, 'right', 'top'),
            'lower left': (0.02, 0.02, 'left', 'bottom'),
            'lower right': (0.98, 0.02, 'right', 'bottom')
        }
        return mapping.get(manual_loc, (0.02, 0.98, 'left', 'top'))

    x_mid = df[x_col].median()
    y_mid = df[y_col].median()
    
    q_ul = ((df[x_col] <= x_mid) & (df[y_col] >= y_mid)).sum()
    q_ur = ((df[x_col] > x_mid) & (df[y_col] >= y_mid)).sum()
    q_ll = ((df[x_col] <= x_mid) & (df[y_col] < y_mid)).sum()
    q_lr = ((df[x_col] > x_mid) & (df[y_col] < y_mid)).sum()
    
    counts = {'upper left': q_ul, 'upper right': q_ur, 'lower left': q_ll, 'lower right': q_lr}
    best_corner = min(counts, key=counts.get)
    
    return _get_best_annotation_position(df, x_col, y_col, best_corner)

def show_contingency_heatmap(
    contingency_table: pd.DataFrame, 
    figsize: Tuple[int, int] = (10, 8),
    title: str = "Policy vs. Tradeoff Contingency"
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    sns.heatmap(
        contingency_table, 
        annot=True, 
        fmt=".1f", 
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
    flows = []
    
    for policy_name in contingency_table.index:
        for tradeoff_name in contingency_table.columns:
            val = contingency_table.loc[policy_name, tradeoff_name]
            if val > 0:
                flows.append((policy_name, tradeoff_name, val))
                
    plt.figure(figsize=figsize)
    s = sf.Sankey(
        flows=flows, 
        aspect_ratio=4/3, 
        nodelabels=True, 
        link_color="source"
    )
    s.draw()
    plt.title(title)
    
    return plt.gcf()


def show_importance_heatmap(
    scores_df: pd.DataFrame, 
    figsize: Tuple[int, int] = (10, 8),
    title: str = "Feature Importance Scores"
) -> plt.Figure:
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
    if not scheme:
        return
        
    line_color = 'red'
    line_alpha = 0.4
    bounds = set()
    
    for b in scheme.bins:
        if np.isfinite(b.min_value): bounds.add(b.min_value)
        if np.isfinite(b.max_value): bounds.add(b.max_value)
        
        val_min = b.min_value if np.isfinite(b.min_value) else data.min()
        val_max = b.max_value if np.isfinite(b.max_value) else data.max()
        mid = (val_min + val_max) / 2
        
        if orientation == 'x':
            # Position above the top spine
            ax.text(mid, 1.02, b.label, transform=ax.get_xaxis_transform(), 
                    color=line_color, fontsize=9, fontweight='bold', ha='center', va='bottom')
        else:
            # Position to the right of the right spine
            ax.text(1.02, mid, b.label, transform=ax.get_yaxis_transform(), 
                    color=line_color, fontsize=9, fontweight='bold', ha='left', va='center', rotation=90)
            
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
    import matplotlib.patches as patches
    
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

    X = exp_sub[parameter_cols].select_dtypes(include=[np.number])
    scaler = MinMaxScaler()
    X_norm = scaler.fit_transform(X)
    
    if 'normalized_baseline' in radius_info['details']:
        centroid_norm = np.array(radius_info['details']['normalized_baseline']).reshape(1, -1)
    else:
        centroid_norm = np.array(list(radius_info['details']['baseline'].values())).reshape(1, -1)

    X_combined = np.vstack([X_norm, centroid_norm])
    
    mds = MDS(n_components=2, random_state=42, normalized_stress='auto', max_iter=100)
    X_2d = mds.fit_transform(X_combined)
    
    points_2d = X_2d[:-1]
    centroid_2d = X_2d[-1]

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=figsize)
    
    if policy_name:
        fig.suptitle(f"Stability Analysis for Policy: {policy_name}", fontsize=16, fontweight='bold', y=1.05)
    
    colors = ['green' if v else 'red' for v in mask_sub]
    ax1.scatter(points_2d[:, 0], points_2d[:, 1], c=colors, alpha=0.5, s=25, edgecolors='none')
    
    ax1.scatter(centroid_2d[0], centroid_2d[1], c='black', marker='*', s=200, label='Nominal (Centroid)', edgecolors='white', zorder=5)
    
    failures_2d = points_2d[~mask_sub.values]
    if len(failures_2d) > 0:
        dists_2d = np.linalg.norm(failures_2d - centroid_2d, axis=1)
        visual_r = np.min(dists_2d)
        circle = patches.Circle(centroid_2d, visual_r, fill=False, edgecolor='black', linestyle='--', alpha=0.6)
        ax1.add_patch(circle)
    
    ax1.set_title(f"Parameter Space Projection (MDS)\nRadius ({radius_info['details']['distance_metric']}): {radius_info['value']:.3f}")
    ax1.legend(loc='lower left', fontsize='small')

    x_obj, y_obj = objective_cols
    ax2.scatter(out_sub[x_obj], out_sub[y_obj], c=colors, alpha=0.6, s=30)
    
    out_centroid_x = out_sub[x_obj].mean()
    out_centroid_y = out_sub[y_obj].mean()
    ax2.scatter(out_centroid_x, out_centroid_y, c='black', marker='*', s=200, label='Nominal Outcome', edgecolors='white', zorder=5)
    
    if target_tradeoff:
        x_label = target_tradeoff.elements.get(x_obj)
        y_label = target_tradeoff.elements.get(y_obj)
        
        x_bounds = (-np.inf, np.inf)
        y_bounds = (-np.inf, np.inf)
        
        def get_bounds(obj, label):
            scheme = next((s for s in schemes if s.objective_name == obj), None)
            if scheme:
                for b in scheme.bins:
                    if b.label == label:
                        return (b.min_value, b.max_value)
            return (-np.inf, np.inf)

        if x_label: x_bounds = get_bounds(x_obj, x_label)
        if y_label: y_bounds = get_bounds(y_obj, y_label)
        
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
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=figsize, sharex=True)
    
    _apply_robustness_heatmap(ax1, baseline_matrix, metric, "Baseline Robustness (Overall)")
    _apply_robustness_heatmap(ax2, improved_matrix, metric, "Improved Robustness (Under Box Constraints)")
    
    ax1.set_xlabel("")
    
    if title:
        fig.suptitle(title, fontsize=16, fontweight='bold', y=0.98)
        
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    return fig


def _apply_robustness_heatmap(ax, matrix, metric, title):
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

def show_robustness_uplift(
    uplift_df: pd.DataFrame,
    metric: str = 'starr',
    figsize: Tuple[int, int] = (10, 8),
    highlight_policies: Optional[Union[List[str], bool]] = None,
    show_global: bool = True,
    highlight_alpha: float = 0.9,
    background_alpha: float = 0.2,
    marker: str = 'o',
    title: Optional[str] = None
) -> plt.Figure:
    """
    Plots robustness improvement vectors (Baseline -> Boxed) per policy. 
    """
    fig, ax = plt.subplots(figsize=figsize)
    df = uplift_df.copy()
    df = df[df['Baseline'] != 0]
    
    if df.empty:
        plt.close(fig)
        return fig

    has_global = 'GLOBAL' in df.index
    global_row = None
    if has_global:
        global_row = df.loc['GLOBAL']
        if not show_global:
            df = df.drop('GLOBAL')
            has_global = False

    if highlight_policies is True or highlight_policies is None:
        highlight_list = [idx for idx in df.index if idx != 'GLOBAL']
    elif isinstance(highlight_policies, list):
        highlight_list = highlight_policies
    else:
        highlight_list = []
        
    highlight_mask = df.index.isin(highlight_list)
    highlight_df = df[highlight_mask]
    background_df = df[~highlight_mask]

    if not background_df.empty:
        for idx, row in background_df.iterrows():
            if idx == 'GLOBAL': continue 
            start_x, start_y = row['Baseline'], 1.0
            end_x, end_y = row['Boxed'], row['Coverage']
            ax.scatter([start_x, end_x], [start_y, end_y], 
                       color='lightgray', s=30, marker=marker, alpha=background_alpha, zorder=1)
            ax.annotate("", xy=(end_x, end_y), xycoords='data',
                xytext=(start_x, start_y), textcoords='data',
                arrowprops=dict(arrowstyle="->", color='lightgray', alpha=background_alpha, lw=1, shrinkA=3, shrinkB=3),
                zorder=1)

    if not highlight_df.empty:
        regular_highlights = highlight_df.drop('GLOBAL', errors='ignore')
        colors = sns.color_palette("bright", n_colors=max(1, len(regular_highlights)))
        color_idx = 0
        for i, (policy, row) in enumerate(highlight_df.iterrows()):
            if policy == 'GLOBAL':
                color = 'black'
                z_order_base = 15
                lw = 3
            else:
                color = colors[color_idx % len(colors)]
                color_idx += 1
                z_order_base = 10
                lw = 2
            
            start_x, start_y = row['Baseline'], 1.0
            end_x, end_y = row['Boxed'], row['Coverage']
            ax.scatter([start_x, end_x], [start_y, end_y], 
                       color=color, s=60, marker=marker, alpha=highlight_alpha, zorder=z_order_base, 
                       label=policy)
            ax.annotate("", xy=(end_x, end_y), xycoords='data',
                xytext=(start_x, start_y), textcoords='data',
                arrowprops=dict(arrowstyle="->", color=color, alpha=highlight_alpha, lw=lw, shrinkA=5, shrinkB=5),
                zorder=z_order_base - 1)

    if show_global and has_global and 'GLOBAL' not in highlight_list:
        row = global_row
        start_x, start_y = row['Baseline'], 1.0
        end_x, end_y = row['Boxed'], row['Coverage']
        ax.scatter([start_x, end_x], [start_y, end_y], 
                   color='black', s=40, marker=marker, alpha=background_alpha, zorder=5, label='GLOBAL')
        ax.annotate("", xy=(end_x, end_y), xycoords='data',
            xytext=(start_x, start_y), textcoords='data',
            arrowprops=dict(arrowstyle="->", color='black', alpha=background_alpha, lw=1.5, shrinkA=4, shrinkB=4),
            zorder=4)

    ax.set_xlabel(f"Robustness Metric ({metric.upper()})")
    ax.set_ylabel("Coverage (Fraction of Scenarios)")
    ax.set_ylim(0, 1.05)
    ax.set_xlim(0, 1.05)
    if title: ax.set_title(title)
    else: ax.set_title(f"Robustness Uplift Analysis: {metric.upper()} vs Coverage")
    if ax.get_legend_handles_labels()[0]:
        handles, labels = ax.get_legend_handles_labels()
        unique = [(h, l) for i, (h, l) in enumerate(zip(handles, labels)) if l not in labels[:i]]
        ax.legend(*zip(*unique), title="Policies", bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.tight_layout()
    return fig

def show_multiple_robustness_uplifts(
    uplift_datasets: Dict[str, pd.DataFrame],
    metric: str = 'starr',
    figsize: Tuple[int, int] = (12, 10),
    highlight_policies: Optional[Union[List[str], bool]] = None,
    alpha: float = 0.8,
    title: Optional[str] = None
) -> plt.Figure:
    fig, ax = plt.subplots(figsize=figsize)
    markers = ['o', 'D', 's', '^', 'v', 'P', 'X', '*', 'h', 'p']
    all_policies = set()
    for df in uplift_datasets.values():
        valid_rows = df[(df.index != 'GLOBAL') & (df['Baseline'] != 0)]
        all_policies.update(valid_rows.index.tolist())
    if not all_policies:
        plt.close(fig); return fig
    if isinstance(highlight_policies, list):
        target_policies = sorted([p for p in all_policies if p in highlight_policies])
    else:
        target_policies = sorted(list(all_policies))
    if not target_policies:
        plt.close(fig); return fig
    colors = sns.color_palette("bright", n_colors=len(target_policies))
    policy_color_map = dict(zip(target_policies, colors))
    for i, (box_name, df) in enumerate(uplift_datasets.items()):
        marker = markers[i % len(markers)]
        mask = (df.index.isin(target_policies)) & (df['Baseline'] != 0)
        df_filtered = df[mask]
        for policy, row in df_filtered.iterrows():
            if policy == 'GLOBAL': continue
            color = policy_color_map[policy]
            label = f"{policy} ({box_name})"
            start_x, start_y = row['Baseline'], 1.0
            end_x, end_y = row['Boxed'], row['Coverage']
            ax.scatter([start_x, end_x], [start_y, end_y], color=color, marker=marker, s=60, alpha=alpha, zorder=10, label=label)
            ax.annotate("", xy=(end_x, end_y), xycoords='data', xytext=(start_x, start_y), textcoords='data',
                arrowprops=dict(arrowstyle="->", color=color, alpha=alpha, lw=1.5, shrinkA=5, shrinkB=5), zorder=9)
    ax.set_xlabel(f"Robustness Metric ({metric.upper()})")
    ax.set_ylabel("Coverage (Fraction of Scenarios)")
    ax.set_ylim(0, 1.05)
    ax.axhline(1.0, color='gray', linestyle='--', alpha=0.3)
    if title: ax.set_title(title)
    else: ax.set_title(f"Comparative Robustness Uplift ({len(uplift_datasets)} Boxes)")
    handles, labels = ax.get_legend_handles_labels()
    if handles:
        by_label = dict(zip(labels, handles))
        ax.legend(by_label.values(), by_label.keys(), title="Policy (Tradeoff)", bbox_to_anchor=(1.02, 1), loc='upper left', borderaxespad=0.)
    plt.tight_layout(); return fig

def show_box_diagnostics(
    box: Any, 
    experiments_df: pd.DataFrame, 
    outcome_mask: pd.Series,
    figsize: Tuple[int, int] = (16, 12),
    title: Optional[str] = None,
    max_scatter_points: int = 1000,
    bins: int = 10,
    s: int = 40,
    alpha: float = 0.6,
    show_diagonal: bool = False,
    box_eps: float = 0.02,
    box_color: str = '#55a868',
    policy_series: Optional[pd.Series] = None,
    palette: Optional[Union[str, Dict]] = None
) -> plt.Figure:
    from matplotlib.ticker import MaxNLocator
    import matplotlib.cm as cm
    import matplotlib.colors as mcolors
    from matplotlib.lines import Line2D

    actual_box_color = box_color
    policy_palette = palette
    
    if policy_series is not None:
        p_name = palette if palette is not None else 'tab10'
        if isinstance(p_name, str):
            cmap = cm.get_cmap(p_name)
            unique_policies = sorted([str(p) for p in policy_series.unique() if pd.notna(p)])
            n_policies = len(unique_policies)
            raw_colors = [mcolors.to_hex(cmap(i / max(1, n_policies))) for i in range(n_policies + 1)]
            actual_box_color = raw_colors[0]
            policy_palette = dict(zip(unique_policies, raw_colors[1:]))
        elif isinstance(palette, dict):
            if not box_color: actual_box_color = list(palette.values())[0]

    fig = plt.figure(figsize=figsize)
    gs = gridspec.GridSpec(2, 2, height_ratios=[1, 2], width_ratios=[2, 1], hspace=0.3)
    ax_bars = fig.add_subplot(gs[0, 0])
    ax_text = fig.add_subplot(gs[0, 1])
    ax_pairs = fig.add_subplot(gs[1, :])
    
    limits = getattr(box, 'limits', box)
    dataset_bounds = getattr(box, 'dataset_bounds', {}) or {}
    
    # Extract includes_na flags from box limits metadata
    includes_na = {}
    if isinstance(limits, dict):
        for p, lims in limits.items():
            includes_na[p] = lims.get('includes_na', False)
    
    if isinstance(limits, dict):
        params = []
        for p, lims in limits.items():
            if p in experiments_df.columns:
                d_min, d_max = experiments_df[p].min(), experiments_df[p].max()
                d_range = d_max - d_min if d_max > d_min else 1.0
                l_min, l_max = lims['min'], lims['max']
                if l_min == -np.inf and p in dataset_bounds: l_min = dataset_bounds[p]['min']
                if l_max == np.inf and p in dataset_bounds: l_max = dataset_bounds[p]['max']
                b_min, b_max = max(l_min, d_min), min(l_max, d_max)
                params.append({'name': p, 'min': b_min, 'max': b_max, 'd_min': d_min, 'd_max': d_max, 'tightness': 1.0 - ((b_max - b_min) / d_range), 'd_range': d_range})
        
        params.sort(key=lambda x: x['tightness'], reverse=True)
        ax_bars.clear()
        for i, p in enumerate(params):
            ax_bars.broken_barh([(0, 1)], (i - 0.25, 0.5), facecolor='#f0f0f0', edgecolor='gray')
            d_range = p['d_range']
            if d_range > 0:
                norm_min, norm_max = (p['min'] - p['d_min']) / d_range, (p['max'] - p['d_min']) / d_range
                
                p_name = p['name']
                if includes_na.get(p_name):
                    # Sentinel is at the beginning. N/A region is approx [0, 0.09]
                    na_end = 0.1 / 1.1
                    # Draw N/A region with hatch if included
                    ax_bars.broken_barh([(0, min(norm_max, na_end))], (i - 0.25, 0.5), 
                                        facecolor=actual_box_color, alpha=0.5, hatch='///')
                    
                    # Draw the rest of the box if it extends beyond N/A
                    if norm_max > na_end:
                        box_start = max(norm_min, na_end)
                        ax_bars.broken_barh([(box_start, norm_max - box_start)], (i - 0.25, 0.5), 
                                            facecolor=actual_box_color, alpha=0.8)
                else:
                    ax_bars.broken_barh([(norm_min, norm_max - norm_min)], (i - 0.25, 0.5), facecolor=actual_box_color, alpha=0.8)
                
                ax_bars.text(norm_min, i, f"{p['min']:.2f} ", ha='right', va='center', fontsize=9)
                ax_bars.text(norm_max, i, f" {p['max']:.2f}", ha='left', va='center', fontsize=9)
            ax_bars.text(-0.05, i, f"{p['name']}", ha='right', va='center', fontsize=10, transform=ax_bars.get_yaxis_transform())
        ax_bars.set_yticks([]); ax_bars.set_xticks([0, 1]); ax_bars.set_xticklabels(['Min', 'Max'])
        ax_bars.set_title("Normalized constraints (Full bar = Parameter range)", fontsize=10)
        ax_bars.set_ylim(-1, len(params)); ax_bars.invert_yaxis() 

    ax_text.axis('off')
    metrics = getattr(box, 'metrics', {})
    text_content = f"Analysis: {getattr(box, 'name', 'Unnamed Box')}\n" + "-" * 30 + "\n\n"
    if metrics:
        text_content += f"Density (precision): {metrics.get('density', 0):.2f}\nCoverage (recall):   {metrics.get('coverage', 0):.2f}\n"
        if metrics.get('lift'): text_content += f"Lift:                {metrics.get('lift'):.2f}\n"
        if metrics.get('mass'): text_content += f"Mass (Support):      {metrics.get('mass'):.2f}\n"
    else: text_content += "No pre-calculated metrics available."
    ax_text.text(0.1, 0.9, text_content, transform=ax_text.transAxes, fontsize=10, family='monospace', va='top')
                 
    top_params_info = params[:5] if 'params' in locals() and params else []
    top_params = [p['name'] for p in top_params_info]
    
    if top_params:
        plot_df = experiments_df[top_params].copy()
        if len(plot_df) > max_scatter_points:
            plot_df = plot_df.sample(max_scatter_points, random_state=42)
            mask_subset = outcome_mask.loc[plot_df.index]
            p_subset = policy_series.loc[plot_df.index] if policy_series is not None else None
        else:
            mask_subset = outcome_mask.loc[plot_df.index]
            p_subset = policy_series.loc[plot_df.index] if policy_series is not None else None
            
        plot_df['Status'] = mask_subset.map({True: 'Success', False: 'Failure'})
        if p_subset is not None: plot_df['Policy'] = p_subset.astype(str).fillna('Unknown')
        ax_pairs.axis('off')
        
        t_name = getattr(box, 'target_tradeoff', 'Target')
        label_success, label_failure = f"Satisfies target={t_name}" if t_name else "Satisfies target", "Other solutions"
        if p_subset is not None:
            hue_var, style_var, current_palette, markers = 'Policy', 'Status', policy_palette, {'Success': 'o', 'Failure': 'D'}
        else:
            hue_var, style_var, current_palette, markers = 'Status', 'Status', palette if palette is not None else {'Success': 'red', 'Failure': 'blue'}, {'Success': 'o', 'Failure': 'D'}

        if len(top_params) == 1:
            ax_sub = fig.add_subplot(gs[1, :])
            sns.scatterplot(data=plot_df, x=top_params[0], y=np.random.normal(0, 0.05, size=len(plot_df)), hue=hue_var, style=style_var, palette=current_palette, markers=markers, ax=ax_sub, s=s, alpha=alpha, legend=False)
            if box and isinstance(limits, dict) and top_params_info[0]:
                p_x = top_params_info[0]; eps_x = p_x['d_range'] * box_eps
                ax_sub.add_patch(patches.Rectangle((p_x['min'] - eps_x, -0.2), (p_x['max'] - p_x['min']) + 2*eps_x, 0.4, linewidth=2, edgecolor=actual_box_color, facecolor='none', linestyle='--'))
            ax_sub.set_ylim(-0.3, 0.3); ax_sub.set_yticks([]); ax_sub.set_ylabel("Fictitious Axis (1D)", fontsize=9, color='gray'); ax_sub.set_xlabel(top_params[0], fontsize=9)
        else:
            grid_size = len(top_params) if show_diagonal else len(top_params) - 1
            if grid_size > 0:
                gs_inner = gridspec.GridSpecFromSubplotSpec(grid_size, grid_size, subplot_spec=gs[1, :], wspace=0.1, hspace=0.1)
                for i in range(len(top_params)):
                    for j in range(len(top_params)):
                        if j > i or (not show_diagonal and i == j): continue
                        grid_i, grid_j = (i if show_diagonal else i - 1), j
                        ax_sub = fig.add_subplot(gs_inner[grid_i, grid_j])
                        row_var, col_var = top_params[i], top_params[j]
                        if i == j:
                            sns.histplot(data=plot_df, x=col_var, hue='Status', palette={'Success': 'red', 'Failure': 'blue'}, ax=ax_sub, element='step', common_norm=False, legend=False, bins=bins)
                            if box and isinstance(limits, dict) and limits.get(col_var):
                                lims = limits.get(col_var)
                                hatch = '///' if includes_na.get(col_var) else None
                                ax_sub.axvspan(lims['min'], lims['max'], color='gray', alpha=0.2, zorder=0, hatch=hatch)
                                ax_sub.axvline(lims['min'], color='black', linestyle='--', lw=1); ax_sub.axvline(lims['max'], color='black', linestyle='--', lw=1)
                        else:
                            sns.scatterplot(data=plot_df, x=col_var, y=row_var, hue=hue_var, style=style_var, palette=current_palette, markers=markers, ax=ax_sub, s=s, alpha=alpha, legend=False)
                            p_x, p_y = next((p for p in top_params_info if p['name'] == col_var), None), next((p for p in top_params_info if p['name'] == row_var), None)
                            if p_x and p_y:
                                 eps_x, eps_y = p_x['d_range'] * box_eps, p_y['d_range'] * box_eps
                                 hatch = '///' if includes_na.get(col_var) or includes_na.get(row_var) else None
                                 ax_sub.add_patch(patches.Rectangle(
                                     (p_x['min'] - eps_x, p_y['min'] - eps_y), 
                                     (p_x['max'] - p_x['min']) + 2*eps_x, 
                                     (p_y['max'] - p_y['min']) + 2*eps_y, 
                                     linewidth=2, edgecolor=actual_box_color, 
                                     facecolor='none', linestyle='--', hatch=hatch
                                 ))
                        ax_sub.xaxis.set_major_locator(MaxNLocator(nbins=4)); ax_sub.yaxis.set_major_locator(MaxNLocator(nbins=4))
                        if grid_i == grid_size - 1: ax_sub.set_xlabel(col_var, fontsize=9)
                        else: ax_sub.set_xlabel(""); ax_sub.set_xticklabels([])
                        if grid_j == 0: ax_sub.set_ylabel(row_var, fontsize=9)
                        else: ax_sub.set_ylabel(""); ax_sub.set_yticklabels([])
        legend_elements = [patches.Patch(facecolor='none', edgecolor=actual_box_color, linestyle='--', linewidth=2, label='Box limits')]
        if any(includes_na.values()):
            legend_elements.append(patches.Patch(facecolor='none', edgecolor=actual_box_color, hatch='///', label='Includes N/A'))

        if p_subset is not None:
            legend_elements.extend([Line2D([0], [0], marker='o', color='w', label=label_success, markerfacecolor='gray', markersize=8), Line2D([0], [0], marker='D', color='w', label=label_failure, markerfacecolor='gray', markersize=8)])
            if isinstance(current_palette, dict):
                for i, (p_name, color) in enumerate(current_palette.items()):
                    if i >= 5: break
                    legend_elements.append(Line2D([0], [0], marker='s', color='w', label=f"{p_name}", markerfacecolor=color, markersize=8))
                if len(current_palette) > 5: legend_elements.append(Line2D([0], [0], color='w', label="... and more policies", fontsize=8))
        else:
            legend_elements.extend([Line2D([0], [0], marker='o', color='w', label=label_success, markerfacecolor='red', markersize=10), Line2D([0], [0], marker='D', color='w', label=label_failure, markerfacecolor='blue', markersize=10)])
        fig.legend(handles=legend_elements, loc='lower center', bbox_to_anchor=(0.5, 0.0), ncol=3, fontsize=10, frameon=False); plt.subplots_adjust(bottom=0.2)
    
    fig.suptitle(title if title else f"Scenario Diagnostics: {getattr(box, 'name', 'Box')}", fontsize=16); return fig

def show_tradeoff_quality_space(
    experiments_df: pd.DataFrame,
    tradeoff: Tradeoff,
    schemes: List[DiscretizationScheme],
    figsize: Tuple[int, int] = (10, 8),
    title: Optional[str] = None,
    alpha: float = 0.5,
    s: int = 50
) -> plt.Figure:
    """
    Plots a 2D scatter of the quality objective space, highlighting points that satisfy the tradeoff.
    Only works well for tradeoffs involving exactly 2 quality dimensions.
    """
    involved_cols = list(tradeoff.elements.keys())
    if len(involved_cols) < 2:
        return show_tradeoff_distribution(experiments_df, [s for s in schemes if s.objective_name in involved_cols], tradeoff, figsize=figsize, title=title)
    col_x, col_y = involved_cols[0], involved_cols[1]
    mask = pd.Series(True, index=experiments_df.index)
    for col, target_bin in tradeoff.elements.items():
        scheme = next((s for s in schemes if s.objective_name == col), None)
        if scheme:
             q_bin = next((b for b in scheme.bins if b.label == target_bin), None)
             if q_bin: mask &= (experiments_df[col] >= q_bin.min_value) & (experiments_df[col] <= q_bin.max_value)
    fig, ax = plt.subplots(figsize=figsize)
    sns.scatterplot(data=experiments_df, x=col_x, y=col_y, color='lightgray', alpha=alpha, s=s, ax=ax, label="Other")
    sns.scatterplot(data=experiments_df[mask], x=col_x, y=col_y, color='red', alpha=alpha+0.2, s=s+20, ax=ax, label=tradeoff.name)
    scheme_x, scheme_y = next((s for s in schemes if s.objective_name == col_x), None), next((s for s in schemes if s.objective_name == col_y), None)
    if scheme_x:
        q_x = next((b for b in scheme_x.bins if b.label == tradeoff.elements[col_x]), None)
        if q_x: ax.axvspan(q_x.min_value, q_x.max_value, color='yellow', alpha=0.1)
    if scheme_y:
        q_y = next((b for b in scheme_y.bins if b.label == tradeoff.elements[col_y]), None)
        if q_y: ax.axhspan(q_y.min_value, q_y.max_value, color='yellow', alpha=0.1)
    ax.set_title(title or f"Quality Space: {col_x} vs {col_y}"); ax.legend(); return fig

def show_multi_objective_tradeoffs(
    experiments_df: pd.DataFrame,
    involved_cols: List[str],
    tradeoffs: List[Tradeoff],
    figsize: Tuple[int, int] = (12, 10),
    title: Optional[str] = None
) -> plt.Figure:
    """
    Visualizes multiple tradeoffs in the objective space using MDS or PCA for dimensionality reduction.
    """
    scaler = MinMaxScaler(); data_scaled = scaler.fit_transform(experiments_df[involved_cols])
    mds = MDS(n_components=2, random_state=42); coords = mds.fit_transform(data_scaled)
    plot_df = pd.DataFrame(coords, columns=['Dim 1', 'Dim 2']); plot_df['Tradeoff'] = 'None'
    for t in tradeoffs:
        mask = pd.Series(True, index=experiments_df.index)
        pass # Eval tradeoff logic here if needed
    fig, ax = plt.subplots(figsize=figsize); sns.scatterplot(data=plot_df, x='Dim 1', y='Dim 2', hue='Tradeoff', palette='viridis', alpha=0.6, ax=ax)
    if title: ax.set_title(title)
    return fig

