from typing import List, Dict, Any, Optional, Tuple, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .coordinator import ArchSpaceCore
from .models import SystemDefinition, DiscretizationScheme, Tradeoff

from ..utils import sort_tradeoff_labels, get_tradeoff_sort_key

import seaborn as sns

class PatternAnalysis:
    """Encapsulates the state and workflow for analyzing a single pattern configuration. 
    
    This class manages the lifecycle of data loading, processing, and analysis 
    for a given SystemDefinition.
    """

    def __init__(self, json_path: str, coordinator: Optional[ArchSpaceCore] = None):
        self.json_path = json_path
        self.coordinator = coordinator or ArchSpaceCore()
        self.reset()

    def reset(self, full: bool = True) -> None:
        """
        Clears analysis state.
        
        Args:
            full: If True (default), clears EVERYTHING (data, tradeoffs, splits).
                  If False, keeps loaded data and tradeoff definitions, 
                  but clears splits, feature stats, and any downstream analysis.
        """
        if full:
            # Data State
            self.sys_def: Optional[SystemDefinition] = None
            self.raw_df: Optional[pd.DataFrame] = None
            self.experiments_df: Optional[pd.DataFrame] = None
            self.outcomes_df: Optional[pd.DataFrame] = None
            
            # Tradeoff State
            self.discrete_df: Optional[pd.DataFrame] = None
            self.pareto_front: Optional[pd.DataFrame] = None
            self.tradeoff_indices: Dict[str, np.ndarray] = {}
            self.schemes: List[DiscretizationScheme] = []
        
        # Data Split & Processing State (Always cleared on reset)
        self.train_indices: Optional[np.ndarray] = None
        self.test_indices: Optional[np.ndarray] = None
        self.feature_stats: Optional[Dict[str, Any]] = None
        self.outcome_stats: Optional[Dict[str, Any]] = None

    def load(self, validate_integrity: bool = True, preprocessor: Optional[callable] = None) -> None:
        """Loads the system definition and then the experimental data.
        
        Args:
            validate_integrity: Whether to run validation checks.
            preprocessor: Optional function(df) -> df to transform raw data.
        """
        # 1. Load Definition
        self.sys_def = self.coordinator.load_system_definition(self.json_path)
        
        # 2. Load Data (using the definition to parse it)
        self.raw_df, self.experiments_df, self.outcomes_df = \
            self.coordinator.load_detailed_data(self.json_path, validate_integrity=validate_integrity, preprocessor=preprocessor)

        # 3. Handle Missing Values (NaN)
        for name, df in [("Experiments", self.experiments_df), ("Outcomes", self.outcomes_df)]:
            if df is not None and df.isnull().values.any():
                nan_count = df.isnull().sum().sum()
                nan_cols = df.columns[df.isnull().any()].tolist()
                print(f"Warning: {name} data contains {nan_count} NaN values in columns: {nan_cols}. Filling numeric NaNs with 0.0.")
                numeric_cols = df.select_dtypes(include=[np.number]).columns
                df[numeric_cols] = df[numeric_cols].fillna(0.0)

    def _ensure_outcome_stats(self) -> None:
        """Computes statistics (mean/std) for outcomes to support standardized metrics."""
        if self.outcome_stats is not None:
            return

        from sklearn.preprocessing import StandardScaler
        
        # Use train set if available, else full
        if self.train_indices is not None:
             target_df = self.outcomes_df.iloc[self.train_indices]
        else:
             target_df = self.outcomes_df
             
        # Select numeric columns
        numeric_cols = target_df.select_dtypes(include=[np.number]).columns.tolist()
        
        if not numeric_cols:
            self.outcome_stats = {'scaler': None, 'numeric_cols': []}
            return

        scaler = StandardScaler()
        scaler.fit(target_df[numeric_cols])
        
        self.outcome_stats = {
            'scaler': scaler,
            'numeric_cols': numeric_cols
        }

    def define_tradeoffs(self, method: str = 'discretization', n_bins: int = 3, labels: Optional[Union[Dict[str, List[str]], List[str]]] = None, ranges: Optional[Dict[str, Tuple[float, float]]] = None, params: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Defines tradeoff regions in the outcome space.
        
        Args:
            method: 'discretization', 'pareto', 'threshold', 'pareto_epsilon', 'pareto_knee', 'clustering'.
            n_bins: Number of bins (for discretization/clustering).
            labels: Labels for bins. Can be Dict {obj: [labels]} for discretization, 
                    or List [labels] for others.
            ranges: Optional fixed ranges for bins.
            params: Dict of parameters for specific methods.
        """
        if self.outcomes_df is None or self.sys_def is None:
            raise RuntimeError("Data must be loaded before defining tradeoffs.")

        # 1. Parameter Validation
        self._validate_tradeoff_params(method, params)

        # 2. Prepare kwargs based on method
        kwargs = {}
        if method in ['discretization', 'clustering']:
            kwargs = {'n_bins': n_bins, 'all_labels': labels, 'ranges': ranges}
            if method == 'clustering':
                kwargs['params'] = params
        else:
            kwargs = {'objectives': self.sys_def.dataspace.quality_objectives}
            if params:
                kwargs['params'] = params
            if labels:
                kwargs['labels'] = labels

        self.discrete_df, self.schemes, self.tradeoff_indices, self.pareto_front = self.coordinator.define_tradeoffs(
            self.outcomes_df, method=method, **kwargs
        )
        
        # 4. Update Tradeoff models with membership flags
        self._update_tradeoff_membership()
        
        return self.discrete_df, self.schemes

    def _update_tradeoff_membership(self) -> None:
        """Updates the has_points and point_count flags in all system tradeoffs."""
        if not self.sys_def:
            return
            
        for tradeoff in self.sys_def.system.tradeoffs:
            indices = self.get_indices_for_tradeoff(tradeoff)
            count = len(indices)
            tradeoff.point_count = count
            tradeoff.has_points = (count > 0)

    def _validate_tradeoff_params(self, method: str, params: Optional[Dict[str, Any]]) -> None:
        """Ensures mandatory parameters are present for the chosen method."""
        if method == 'threshold':
            if not params or 'thresholds' not in params:
                raise ValueError("Method 'threshold' requires 'params' with 'thresholds' dictionary.")
        elif method == 'pareto_epsilon':
            if not params or 'epsilon' not in params:
                raise ValueError("Method 'pareto_epsilon' requires 'params' with 'epsilon' float.")

    def get_indices_for_tradeoff(self, tradeoff: Tradeoff) -> np.ndarray:
        """Returns row indices satisfying the given tradeoff definition.
        
        Uses the precomputed tradeoff_indices map for performance.
        """
        if not self.tradeoff_indices:
            return np.array([])

        # A tradeoff might match multiple label combinations if it's partially specified.
        # But our current framework assumes tradeoff defines exact labels for its objectives.
        
        # 1. Identify all outcome columns
        outcome_cols = list(self.discrete_df.columns)
        
        # 2. Filter the index map
        all_matches = []
        
        for tradeoff_str, indices in self.tradeoff_indices.items():
            # tradeoff_str is e.g. "low,high"
            labels = tradeoff_str.split(',')
            label_map = dict(zip(outcome_cols, labels))
            
            # Check if this combination matches all elements in our target tradeoff
            match = True
            for obj_name, target_label in tradeoff.elements.items():
                if label_map.get(obj_name) != target_label:
                    match = False
                    break
            
            if match:
                all_matches.append(indices)
        
        if not all_matches:
            return np.array([])
            
        return np.concatenate(all_matches)

    def discover_tradeoffs(self, primary_outcome: str = 'cost', method: str = 'prim') -> Dict[str, Any]:
        """Runs scenario discovery for all tradeoffs defined in the system.
        
        Args:
            primary_outcome: The name of the primary outcome column to use for 
                             algorithm initialization (e.g. PRIM requires a y vector).
            method: The discovery algorithm to use ('prim' or 'cart').
            
        Returns:
            A dictionary mapping tradeoff names to discovered parameter limits.
        """
        if self.experiments_df is None or self.discrete_df is None:
            raise RuntimeError("Data must be loaded and discretized before discovery.")

        results = {}
        for tradeoff in self.sys_def.system.tradeoffs:
            try:
                box, limits, alg = self.coordinator.discover_scenarios(
                    self.experiments_df, # Pass as positional 'df'
                    experiments_df=self.experiments_df,
                    outcomes_df=self.outcomes_df, # Explicitly passed for safety
                    outcome=primary_outcome,
                    method=method,
                    tradeoff=tradeoff,
                    discrete_outcomes_df=self.discrete_df
                )
                results[f"tradeoff_{tradeoff.name}"] = limits
            except Exception as e:
                # We catch errors to allow other tradeoffs to proceed
                results[f"tradeoff_{tradeoff.name}_error"] = str(e)
        
        return results

    def show_distributions(self, tradeoff: Optional[Tradeoff] = None, highlight_indices: Optional[np.ndarray] = None, **kwargs) -> plt.Figure:
        """Plots outcome distributions with tradeoff overlays for the current session."""
        return self.coordinator.show_distributions(
            self.outcomes_df, self.schemes, tradeoff=tradeoff, highlight_indices=highlight_indices, **kwargs
        )

    def show_quality_objective_space(self, x_metric: str, y_metric: str, highlight_tradeoffs: Optional[List[Tradeoff]] = None, highlight_policies: Optional[List[str]] = None, show_overall: bool = True, color_points: bool = True, draw_rectangles: bool = False, subset: str = 'all', eps: float = 0.01, background_alpha: float = 0.6, **kwargs) -> plt.Figure:
        """Plots a 2D scatter of outcomes with tradeoff overlays and highlighting.
        
        Args:
            x_metric: Metric for X-axis.
            y_metric: Metric for Y-axis.
            highlight_tradeoffs: List of Tradeoffs to highlight (as rectangles or points).
            highlight_policies: List of policy names to highlight/color. 
            show_overall: Whether to show background points.
            color_points: Whether to color tradeoff points.
            draw_rectangles: Whether to draw rectangles for tradeoffs.
            subset: 'all' (default), 'train', or 'test'.
            eps: Epsilon factor to enlarge tradeoff rectangles.
            background_alpha: Alpha for gray background points.
        """
        X, Y, _ = self._get_subset_data(subset)
        
        highlight_indices_map = {}
        if highlight_tradeoffs:
            for t in highlight_tradeoffs:
                indices = self.get_indices_for_tradeoff(t)
                filtered = self._filter_indices_for_subset(indices, subset)
                if len(filtered) > 0:
                    # Use the human-readable label for the plot legend
                    highlight_indices_map[t.label] = filtered
                    
        policy_series = None
        if highlight_policies is not None:
             if self.sys_def and self.sys_def.dataspace.configuration_identification.column:
                 col_name = self.sys_def.dataspace.configuration_identification.column
                 if col_name in X.columns:
                     series = X[col_name].copy()
                     if len(highlight_policies) > 0:
                         series = series.where(series.isin(highlight_policies))
                     policy_series = series
                    
        return self.coordinator.show_quality_objective_space(
            Y, x_metric, y_metric, self.schemes, 
            highlight_indices_map=highlight_indices_map, 
            policy_series=policy_series,
            show_overall=show_overall, 
            color_points=color_points, draw_rectangles=draw_rectangles, 
            eps=eps, background_alpha=background_alpha, **kwargs
        )

    def show_box_impact_objective_space(
        self, 
        box: Any, 
        x_metric: str, 
        y_metric: str, 
        tradeoff: Optional[Union[str, Tradeoff]] = None, 
        subset: str = 'all', 
        background_alpha: float = 0.6,
        show_box_summary: bool = False,
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the impact of a discovered box on the quality objective space.
        
        Shows all points in gray, but highlights those satisfying the box constraints
        using their original policy colors. Optionally draws a rectangle around a 
        target tradeoff region and shows a summary of constraints.
        
        Args:
            box: Box object defining parameter constraints.
            x_metric: Metric for X-axis.
            y_metric: Metric for Y-axis.
            tradeoff: Optional tradeoff name or object to highlight with a rectangle.
            subset: 'all', 'train', or 'test'.
            background_alpha: Alpha for gray background points.
            show_box_summary: Whether to display a text box with parameter constraints.
            **kwargs: Additional plotting parameters.
        """
        X, Y, _ = self._get_subset_data(subset)
        
        # 1. Create Box Mask
        mask = pd.Series(True, index=X.index)
        for param, limits in box.limits.items():
            if param in X.columns:
                mask &= (X[param] >= limits['min']) & (X[param] <= limits['max'])
        
        # 2. Prepare Policy Series (Only show colors for points inside the box)
        config_col = self.sys_def.dataspace.configuration_identification.column
        if not config_col:
            raise RuntimeError("Configuration column not defined.")
        
        # Get all policy names to ensure they appear in the legend
        all_policies = sorted(self.experiments_df[config_col].dropna().unique())
        
        # Create categorical series with all policy names as categories
        policy_series = X[config_col].copy().astype(pd.CategoricalDtype(categories=all_policies))
        
        # Points outside the box will be NaN in the policy series, thus plotted in gray
        policy_series = policy_series.where(mask)
        
        # 3. Handle Tradeoff Rectangle
        highlight_indices_map = {}
        if tradeoff:
            if isinstance(tradeoff, str):
                tradeoff_obj = self.get_tradeoff(tradeoff)
            else:
                tradeoff_obj = tradeoff
                
            if tradeoff_obj:
                indices = self.get_indices_for_tradeoff(tradeoff_obj)
                filtered = self._filter_indices_for_subset(indices, subset)
                if len(filtered) > 0:
                    highlight_indices_map[tradeoff_obj.label] = filtered

        # 4. Generate Box Summary Text
        annotation_text = None
        if show_box_summary:
            lines = []
            if box.name:
                lines.append(f"NAME: {box.name}")
                lines.append("-" * 20)
            
            lines.append(f"Metrics:")
            density = box.metrics.get('density', 0.0)
            coverage = box.metrics.get('coverage', 0.0)
            lines.append(f"- Density:  {density:.2f}")
            lines.append(f"- Coverage: {coverage:.2f}")
            lines.append("")
            lines.append("Constraints:")
            for param, lims in box.limits.items():
                lines.append(f"- {param}: [{lims['min']:.2f}, {lims['max']:.2f}]")
            annotation_text = "\n".join(lines)

        # 5. Delegate to standard plotter
        title = kwargs.pop('title', f"What-If: Impact of Box ({box.target_tradeoff or 'discovered region'})")
        
        return self.coordinator.show_quality_objective_space(
            Y, x_metric, y_metric, self.schemes,
            highlight_indices_map=highlight_indices_map,
            policy_series=policy_series,
            show_overall=True,
            draw_rectangles=len(highlight_indices_map) > 0,
            title=title,
            background_alpha=background_alpha,
            annotation_text=annotation_text,
            **kwargs
        )

    def get_policy_contingency_matrix(self, decision_key: str, normalization_mode: str = 'population', subset: str = 'all') -> pd.DataFrame:
        """
        Computes the contingency matrix of Policies vs Tradeoffs.
        
        Args:
            decision_key: The specific decision to analyze.
            normalization_mode: 'population', 'row', 'none'.
            subset: 'all' (default), 'train', or 'test'.
        """
        from ..analysis.contingency import ContingencyAnalyzer
        
        X, _, _ = self._get_subset_data(subset)
        analyzer = ContingencyAnalyzer(self.sys_def)
        
        # 1. Get Policy Map
        config_col = self.sys_def.dataspace.configuration_identification.column
        if not config_col:
             raise RuntimeError("Configuration column not defined.")
        
        policy_df = analyzer.get_decision_policy_map(X, config_col)
        
        if decision_key not in policy_df.columns:
            approximate_match = False
            for col in policy_df.columns:
                col_suffix = col.split(':')[-1]
                if decision_key == col_suffix:
                    decision_key = col
                    approximate_match = True
                    print(f"Warning: Using approximate match for decision: {decision_key} -> {col_suffix}")
                    break
            if not approximate_match:
                available = list(policy_df.columns)
                raise ValueError(f"Decision '{decision_key}' not found. Available: {available}")

        # 2. Get Tradeoff Mask
        tradeoff_mask = pd.DataFrame(index=X.index)
        for t in self.sys_def.system.tradeoffs:
            indices = self.get_indices_for_tradeoff(t)
            filtered_indices = self._filter_indices_for_subset(indices, subset)
            
            series = pd.Series(False, index=X.index)
            if len(filtered_indices) > 0:
                # We use iloc since filtered_indices are relative integer positions in the subset
                series.iloc[filtered_indices] = True
            
            tradeoff_mask[t.name] = series

        # 3. Compute
        return analyzer.compute_contingency(policy_df, tradeoff_mask, decision_key=decision_key, normalization_mode=normalization_mode)

    def show_policy_contingency(self, decision_key: str, type: str = 'heatmap', subset: str = 'all', **kwargs) -> plt.Figure:
        """
        Visualizes the contingency table for a specific decision.
        
        Args:
            decision_key: The decision to visualize.
            type: 'heatmap' or 'sankey'.
            subset: 'all' (default), 'train', or 'test'.
        """
        from ..analysis.visualization import show_contingency_heatmap, show_policy_tradeoff_sankey
        
        norm_mode = kwargs.pop('normalization_mode', 'population')
        df = self.get_policy_contingency_matrix(decision_key=decision_key, normalization_mode=norm_mode, subset=subset)
        
        title = kwargs.pop('title', f"Impact of {decision_key} on Tradeoffs ({subset})")
        
        if type == 'heatmap':
            return show_contingency_heatmap(df, title=title, **kwargs)
        elif type == 'sankey':
            return show_policy_tradeoff_sankey(df, title=title, **kwargs)
        else:
            raise ValueError(f"Unknown visualization type: {type}")

    def get_policy_tradeoff_distribution(self, decision_key: str, policy_name: str, subset: str = 'all') -> Dict[str, float]:
        """
        Returns the distribution of tradeoffs for a specific policy.
        
        Args:
            decision_key: The decision containing the policy.
            policy_name: The name of the policy to inspect.
            subset: 'all', 'train', or 'test'.
            
        Returns:
            Dict[str, float]: {tradeoff_name: percentage (0.0 to 1.0)}
        """
        df = self.get_policy_contingency_matrix(decision_key, normalization_mode='row', subset=subset)
        
        if policy_name not in df.index:
            raise ValueError(f"Policy '{policy_name}' not found in decision '{decision_key}'.")
            
        return df.loc[policy_name].to_dict()

    def get_variable_policies(self, decision_key: str, subset: str = 'all', threshold: float = 0.0) -> List[str]:
        """
        Returns policies that result in more than one tradeoff.
        
        Args:
            decision_key: The decision to analyze.
            subset: 'all', 'train', or 'test'.
            threshold: Minimum percentage (0.0 to 1.0) to consider a tradeoff as "present".
            
        Returns:
            List[str]: Names of policies with variability in outcomes.
        """
        df = self.get_policy_contingency_matrix(decision_key, normalization_mode='row', subset=subset)
        
        # Count tradeoffs where percentage > threshold
        variability_mask = (df > threshold).sum(axis=1) > 1
        
        return df.index[variability_mask].tolist()

    def get_deterministic_policies(self, decision_key: str, subset: str = 'all', threshold: float = 0.99) -> List[Tuple[str, str]]:
        """
        Returns policies that consistently result in a single specific tradeoff.
        
        Args:
            decision_key: The decision to analyze.
            subset: 'all', 'train', or 'test'.
            threshold: Minimum percentage (0.0 to 1.0) to consider a policy "deterministic" 
                       for a tradeoff. Default is 0.99 (99%).
            
        Returns:
            List[Tuple[str, str]]: List of (policy_name, tradeoff_name) pairs.
        """
        df = self.get_policy_contingency_matrix(decision_key, normalization_mode='row', subset=subset)
        
        deterministic_pairs = []
        
        for policy_name, row in df.iterrows():
            # Find tradeoffs where percentage >= threshold
            matching_tradeoffs = row[row >= threshold].index.tolist()
            
            if len(matching_tradeoffs) == 1:
                deterministic_pairs.append((str(policy_name), str(matching_tradeoffs[0])))
                
        return deterministic_pairs

    def get_exclusive_tradeoffs(self, decision_key: str, subset: str = 'all', threshold: float = 0.0) -> List[Tuple[str, str]]:
        """
        Returns tradeoffs that are exclusively achieved by a single policy.
        
        Args:
            decision_key: The decision to analyze.
            subset: 'all', 'train', or 'test'.
            threshold: Minimum count to consider a policy-tradeoff relationship.
            
        Returns:
            List[Tuple[str, str]]: List of (policy_name, tradeoff_name) pairs.
        """
        # Use raw counts to check column exclusivity
        df = self.get_policy_contingency_matrix(decision_key, normalization_mode='none', subset=subset)
        
        exclusive_pairs = []
        
        for tradeoff_name in df.columns:
            col = df[tradeoff_name]
            # Find rows (policies) where count > threshold
            active_policies = col[col > threshold].index.tolist()
            
            if len(active_policies) == 1:
                exclusive_pairs.append((str(active_policies[0]), str(tradeoff_name)))
                
        return exclusive_pairs

    # --- Robustness Analysis ---

    def get_policy_robustness_improvement_matrix(
        self, 
        boxes: List[Optional[Any]], 
        metric: str = 'starr', 
        subset: str = 'all', 
        min_samples: int = 1
    ) -> pd.DataFrame:
        """
        Computes a matrix of Policy vs. Tradeoff robustness under box constraints.
        
        Args:
            boxes: List of Box objects (one per tradeoff in system.tradeoffs, or None).
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.
            min_samples: Minimum points required to calculate the metric.
            
        Returns:
            pd.DataFrame: Policies as rows, Tradeoff names as columns.
        """
        from ..analysis.discovery import BoxEvaluator
        
        X, Y, discrete = self._get_subset_data(subset)
        config_col = self.sys_def.dataspace.configuration_identification.column
        if not config_col:
            raise RuntimeError("Configuration column not defined.")
        
        policy_series = X[config_col]
        tradeoffs = self.get_tradeoffs()
        
        return BoxEvaluator.compute_policy_robustness_matrix(
            X, Y, discrete, policy_series, tradeoffs, boxes, self.schemes,
            metric=metric, stats=self.outcome_stats, min_samples=min_samples
        )

    def show_policy_robustness_improvement_heatmap(
        self, 
        boxes: Optional[List[Optional[Any]]] = None, 
        metric: str = 'starr', 
        subset: str = 'all', 
        matrix: Optional[pd.DataFrame] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 10),
        **kwargs
    ) -> plt.Figure:
        """
        Calculates and visualizes the policy robustness improvement matrix as a heatmap.
        """
        if matrix is None:
            if boxes is None:
                raise ValueError("Either 'matrix' or 'boxes' must be provided.")
            matrix = self.get_policy_robustness_improvement_matrix(boxes, metric=metric, subset=subset, **kwargs)
            
        return self.coordinator.show_robustness_heatmap(matrix, metric=metric, title=title, figsize=figsize)

    def show_policy_robustness_comparison_heatmap(
        self, 
        boxes: Optional[List[Optional[Any]]] = None, 
        metric: str = 'starr', 
        subset: str = 'all', 
        baseline_matrix: Optional[pd.DataFrame] = None,
        improved_matrix: Optional[pd.DataFrame] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (14, 12),
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes a vertical comparison of Baseline vs. Improved (Boxed) robustness.
        
        Args:
            boxes: List of Box objects. Required if improved_matrix is None.
            metric: 'starr' or 'regret'.
            subset: Data subset to use.
            baseline_matrix: Pre-calculated baseline DataFrame. If None, it will be computed.
            improved_matrix: Pre-calculated improved DataFrame. If None, it will be computed using boxes.
            title: Custom plot title.
            figsize: Figure size.
            **kwargs: Additional parameters for matrix calculation.
        """
        # 1. Get Baseline Matrix (Overall)
        if baseline_matrix is None:
            baseline_matrix = self.get_robustness_report(metric=metric, subset=subset)
        
        # 2. Get Improved Matrix (What-If)
        if improved_matrix is None:
            if boxes is None:
                raise ValueError("Either 'improved_matrix' or 'boxes' must be provided.")
            improved_matrix = self.get_policy_robustness_improvement_matrix(boxes, metric=metric, subset=subset, **kwargs)
        
        # 3. Delegate to coordinator
        return self.coordinator.show_robustness_comparison_heatmap(
            baseline_matrix, improved_matrix, metric=metric, title=title, figsize=figsize
        )

    def compute_robustness(
        self, 
        policy_name: str, 
        tradeoff_name: str, 
        metric: str = 'starr', 
        subset: str = 'all', 
        matrix: Optional[pd.DataFrame] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculates a specific robustness metric for a policy relative to a tradeoff.
        
        Args:
            policy_name: Name of the policy.
            tradeoff_name: Name of the target tradeoff.
            metric: 'starr', 'regret', or 'stability_radius'.
            subset: 'all', 'train', or 'test'.
            matrix: Optional pre-calculated matrix to extract the value from.
            
        Returns:
            Dict[str, Any]: Metric value and detailed computation information.
        """
        if matrix is not None:
            val = matrix.loc[policy_name, tradeoff_name] if tradeoff_name in matrix.columns else 0.0
            return {'metric': metric, 'value': float(val), 'details': 'Extracted from matrix'}

        from ..analysis.robustness import RobustnessAnalyzer
        from ..analysis.contingency import ContingencyAnalyzer
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        # 1. Prepare Data Subsets
        # Fix: Get actual global indices for the subset to align with policy_map
        if subset == 'all':
            subset_indices = self.experiments_df.index
        elif subset == 'train' and self.train_indices is not None:
            subset_indices = self.train_indices
        elif subset == 'test' and self.test_indices is not None:
            subset_indices = self.test_indices
        else:
            raise ValueError(f"Invalid subset '{subset}' or data not split.")
        
        # Filter for Policy
        config_col = self.sys_def.dataspace.configuration_identification.column
        analyzer_cont = ContingencyAnalyzer(self.sys_def)
        policy_map = analyzer_cont.get_decision_policy_map(self.experiments_df, config_col)
        
        policy_col = None
        for col in policy_map.columns:
            if (policy_map[col] == policy_name).any():
                policy_col = col
                break
        
        if policy_col is None:
            raise ValueError(f"Policy '{policy_name}' not found in any decision.")
            
        policy_mask = (policy_map[policy_col] == policy_name)
        
        # Intersection of subset and policy using global indices
        final_indices = [idx for idx in subset_indices if policy_mask.iloc[idx]]
        
        if not final_indices:
            return {'metric': metric, 'value': 0.0, 'details': 'No data for policy/subset'}

        # 2. Get Targets
        tradeoff = next((t for t in self.get_tradeoffs() if t.name == tradeoff_name), None)
        if not tradeoff:
            raise ValueError(f"Tradeoff '{tradeoff_name}' not found.")
            
        # Boolean mask for the target tradeoff
        is_target = pd.Series(True, index=self.discrete_df.index)
        for obj, label in tradeoff.elements.items():
            if obj in self.discrete_df.columns:
                is_target &= (self.discrete_df[obj] == label)
        
        target_subset = is_target.iloc[final_indices]
        outcomes_subset = self.outcomes_df.iloc[final_indices]
        experiments_subset = self.experiments_df.iloc[final_indices]

        # 3. Compute
        if metric == 'starr':
            return RobustnessAnalyzer.compute_starr(target_subset)
        elif metric == 'regret':
            # Ensure stats are available for standardized distance
            self._ensure_outcome_stats()
            
            # Extract boundaries
            boundaries = {}
            for obj, label in tradeoff.elements.items():
                # Find scheme for this objective
                scheme = next((s for s in self.schemes if s.objective_name == obj), None)
                if scheme:
                    q_bin = next((b for b in scheme.bins if b.label == label), None)
                    if q_bin:
                        boundaries[obj] = {'min': q_bin.min_value, 'max': q_bin.max_value}
            
            return RobustnessAnalyzer.compute_regret(
                outcomes_subset, target_subset, boundaries, stats=self.outcome_stats
            )
        elif metric == 'stability_radius':
            analyzer_fi = FeatureImportanceAnalyzer(self.sys_def)
            parameter_cols = kwargs.get('parameters')
            if parameter_cols is None:
                parameter_cols = analyzer_fi.get_parameter_columns(self.experiments_df)
                
            distance_metric = kwargs.get('distance_metric', 'euclidean')
            baseline = kwargs.get('baseline', None)
            
            return RobustnessAnalyzer.compute_stability_radius(
                experiments_subset, target_subset, parameter_cols, 
                distance_metric=distance_metric, baseline=baseline
            )
        else:
            raise ValueError(f"Unknown robustness metric: {metric}")

    def analyze_robustness_uplift(
        self,
        box: Any,
        tradeoff_name: str,
        metric: str = 'starr',
        subset: str = 'all'
    ) -> pd.DataFrame:
        """
        Computes the robustness uplift (Baseline vs Boxed) per policy.

        Args:
            box: A Box object (e.g., from discover_scenarios) or a dict with limits.
            tradeoff_name: The target tradeoff defining 'Success'.
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.

        Returns:
            pd.DataFrame: Columns [Policy, Baseline, Boxed, Uplift, Coverage, Count].
        """
        from ..analysis.robustness import RobustnessAnalyzer
        from ..analysis.contingency import ContingencyAnalyzer

        # 1. Prepare Data
        X, Y, discrete = self._get_subset_data(subset)
        
        # 2. Identify Policies
        config_col = self.sys_def.dataspace.configuration_identification.column
        if not config_col:
            raise RuntimeError("Configuration column not defined.")
        
        # We need the exact column(s) that define the policy.
        # Usually, this is just the config_col in X.
        design_vars = [config_col]

        # 3. Create Target Mask (Baseline Success)
        tradeoff = self.get_tradeoff(tradeoff_name)
        if not tradeoff:
            raise ValueError(f"Tradeoff '{tradeoff_name}' not found.")
            
        is_target_mask = pd.Series(True, index=discrete.index)
        for obj, label in tradeoff.elements.items():
            if obj in discrete.columns:
                is_target_mask &= (discrete[obj] == label)

        # 4. Create Box Mask (Inside Box)
        # If 'box' is a Box object, use box.limits. If dict, use it directly.
        limits = getattr(box, 'limits', box)
        if not isinstance(limits, dict):
             raise ValueError("Invalid box object provided. Must have 'limits' attribute or be a dict.")

        box_mask = pd.Series(True, index=X.index)
        for param, bounds in limits.items():
            if param in X.columns:
                box_mask &= (X[param] >= bounds['min']) & (X[param] <= bounds['max'])

        # 5. Prepare Regret Args (if needed)
        boundaries = None
        stats = None
        if metric == 'regret':
            self._ensure_outcome_stats()
            stats = self.outcome_stats
            boundaries = {}
            for obj, label in tradeoff.elements.items():
                scheme = next((s for s in self.schemes if s.objective_name == obj), None)
                if scheme:
                    q_bin = next((b for b in scheme.bins if b.label == label), None)
                    if q_bin:
                        boundaries[obj] = {'min': q_bin.min_value, 'max': q_bin.max_value}

        # 6. Compute
        return RobustnessAnalyzer.analyze_robustness_uplift(
            experiments_df=X,
            outcomes_df=Y,
            is_target_mask=is_target_mask,
            box_mask=box_mask,
            design_vars=design_vars,
            metric=metric,
            boundaries=boundaries,
            stats=stats
        )

    def show_robustness_uplift(
        self,
        uplift_df: pd.DataFrame,
        metric: str = 'starr',
        highlight_policies: Optional[Union[List[str], bool]] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 8),
        show_global: bool = True,
        highlight_alpha: float = 0.9,
        background_alpha: float = 0.2,
        marker: str = 'o',
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the results of analyze_robustness_uplift.
        
        Plots vectors per policy: Baseline (Coverage=1.0) -> Boxed (Coverage=Actual).
        X-axis: Robustness Metric
        Y-axis: Coverage
        
        Args:
            uplift_df: DataFrame from analyze_robustness_uplift.
            metric: Metric name.
            highlight_policies: List of policies to emphasize (colored arrows) OR True to highlight all.
                                The GLOBAL policy is handled via show_global.
            show_global: Whether to include the 'GLOBAL' aggregate.
            highlight_alpha: Opacity for highlighted policies.
            background_alpha: Opacity for non-highlighted policies (gray).
            marker: Symbol for the points (e.g., 'o', 'D', '*').
        """
        return self.coordinator.visualization_manager.show_robustness_uplift(
            uplift_df, 
            metric=metric, 
            highlight_policies=highlight_policies, 
            title=title, 
            figsize=figsize,
            show_global=show_global,
            highlight_alpha=highlight_alpha,
            background_alpha=background_alpha,
            marker=marker,
            **kwargs
        )

    def show_multiple_robustness_uplifts(
        self,
        uplift_datasets: Dict[str, pd.DataFrame],
        metric: str = 'starr',
        highlight_policies: Optional[Union[List[str], bool]] = None,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (12, 10),
        alpha: float = 0.8,
        **kwargs
    ) -> plt.Figure:
        """
        Plots robustness uplifts for multiple boxes/tradeoffs on the same chart.
        
        Args:
            uplift_datasets: Dict mapping Label (e.g. Box Name) -> Uplift DataFrame.
            metric: Metric name.
            highlight_policies: List of policies to include.
            alpha: Opacity.
        """
        return self.coordinator.visualization_manager.show_multiple_robustness_uplifts(
            uplift_datasets, 
            metric=metric, 
            highlight_policies=highlight_policies, 
            title=title, 
            figsize=figsize,
            alpha=alpha,
            **kwargs
        )

    def get_robustness_report(
        self, 
        decision_key: Optional[str] = None, 
        tradeoff_names: Optional[List[str]] = None, 
        metric: str = 'starr', 
        subset: str = 'all', 
        policy_names: Optional[List[str]] = None,
        matrix: Optional[pd.DataFrame] = None,
        **kwargs
    ) -> pd.DataFrame:
        """
        Generates a consolidated robustness report for a set of policies.
        
        Args:
            decision_key: The decision (e.g., 'Comp:Dec') to analyze. 
                          If None and policy_names is None, includes all policies.
            tradeoff_names: List of tradeoffs to use as columns. 
                            If None, targets all defined tradeoffs.
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.
            policy_names: Explicit list of policy names to include.
            matrix: Pre-calculated DataFrame. If provided, it is returned directly.
            
        Returns:
            pd.DataFrame: Index=Policies, Columns=Tradeoffs, Values=Metric.
        """
        if matrix is not None:
            return matrix

        from ..analysis.contingency import ContingencyAnalyzer
        from ..analysis.contingency import ContingencyAnalyzer
        config_col = self.sys_def.dataspace.configuration_identification.column
        analyzer_cont = ContingencyAnalyzer(self.sys_def)
        policy_map = analyzer_cont.get_decision_policy_map(self.experiments_df, config_col)
        
        # 1. Determine Policies
        if policy_names is not None:
            policies = policy_names
        elif decision_key is not None:
            if decision_key not in policy_map.columns:
                raise ValueError(f"Decision '{decision_key}' not found.")
            policies = [p for p in policy_map[decision_key].unique() if pd.notna(p)]
        else:
            # All policies in the system
            all_p = []
            for col in policy_map.columns:
                all_p.extend(policy_map[col].unique())
            policies = sorted(list(set([p for p in all_p if pd.notna(p)])))
            
        # 2. Determine Tradeoffs
        if tradeoff_names is None:
            tradeoff_names = [t.name for t in self.get_tradeoffs()]

        # 3. Build Report
        report_data = []
        for policy in policies:
            row = {'policy': policy}
            for t_name in tradeoff_names:
                try:
                    res = self.compute_robustness(policy, t_name, metric=metric, subset=subset, **kwargs)
                    row[t_name] = res.get('value', 0.0)
                except Exception:
                    # Policy might not exist in this context or tradeoff issues
                    row[t_name] = np.nan
            report_data.append(row)
            
        return pd.DataFrame(report_data).set_index('policy')

    def get_aggregate_robustness_stats(
        self,
        boxes: List[Any],
        metric: str = 'starr',
        subset: str = 'all'
    ) -> pd.DataFrame:
        """
        Consolidates robustness uplift across multiple discovered boxes/tradeoffs.
        
        Assumes each box targets a specific tradeoff (box.target_tradeoff).
        Computes the 'GLOBAL' uplift for each box and aggregates the results.
        
        Args:
            boxes: List of Box objects (from discover_scenarios).
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.
            
        Returns:
            pd.DataFrame: Rows=Tradeoffs, Columns=[Baseline, Boxed, Uplift, Coverage].
                          Includes an 'AVERAGE' row at the bottom.
        """
        results = []
        
        for box in boxes:
            t_name = box.target_tradeoff
            if not t_name:
                continue
                
            try:
                # Analyze Uplift for this box against its target
                uplift_df = self.analyze_robustness_uplift(
                    box=box, 
                    tradeoff_name=t_name, 
                    metric=metric, 
                    subset=subset
                )
                
                # Extract GLOBAL row
                if 'GLOBAL' in uplift_df.index:
                    glob = uplift_df.loc['GLOBAL']
                    results.append({
                        'Tradeoff': t_name,
                        'Baseline': glob['Baseline'],
                        'Boxed': glob['Boxed'],
                        'Uplift': glob['Uplift'],
                        'Coverage': glob['Coverage'],
                        'Count': glob['Count']
                    })
            except Exception as e:
                print(f"Warning: Failed to aggregate stats for box targeting '{t_name}': {e}")

        if not results:
            return pd.DataFrame()
            
        df = pd.DataFrame(results).set_index('Tradeoff')
        
        # Calculate Summary Stats
        summary = df.mean().to_dict()
        summary_std = df.std().to_dict()
        
        # Add AVERAGE row
        df.loc['AVERAGE'] = summary
        df.loc['STD_DEV'] = summary_std
        
        return df

    def get_tradeoff_impact_matrix(
        self,
        boxes: List[Any],
        policy_name: Optional[str] = None,
        subset: str = 'all'
    ) -> pd.DataFrame:
        """
        Computes a matrix of Boxed Densities for all tradeoffs when specific boxes are applied.
        
        Rows: The Tradeoff targeted by the Box.
        Columns: The Tradeoff being measured (Collateral impact).
        Values: The absolute density (0.0 - 1.0) of the column tradeoff within the box.
        
        Args:
            boxes: List of Box objects.
            policy_name: Specific policy to analyze. If None, uses Global data.
            subset: 'all', 'train', or 'test'.
            
        Returns:
            pd.DataFrame: A square-ish matrix of densities.
        """
        from ..analysis.contingency import ContingencyAnalyzer
        
        # 1. Prepare Data
        X, _, discrete = self._get_subset_data(subset)
        
        # 2. Filter by Policy (if requested)
        if policy_name:
            config_col = self.sys_def.dataspace.configuration_identification.column
            if not config_col:
                raise RuntimeError("Configuration column not defined.")
            
            analyzer_cont = ContingencyAnalyzer(self.sys_def)
            policy_map = analyzer_cont.get_decision_policy_map(self.experiments_df, config_col)
            
            # Find matching indices
            policy_col = None
            for col in policy_map.columns:
                if (policy_map[col] == policy_name).any():
                    policy_col = col
                    break
            
            if policy_col:
                # Get global indices matching policy
                global_mask = (policy_map[policy_col] == policy_name)
                # Intersect with subset indices
                subset_indices = self._filter_indices_for_subset(np.where(global_mask)[0], subset)
                
                if len(subset_indices) == 0:
                    raise ValueError(f"No data found for policy '{policy_name}' in subset '{subset}'")
                
                X = X.iloc[subset_indices]
                discrete = discrete.iloc[subset_indices]
            else:
                raise ValueError(f"Policy '{policy_name}' not found.")

        # 3. Precompute Tradeoff Masks
        all_tradeoffs = self.get_tradeoffs()
        tradeoff_masks = {}
        
        for t in all_tradeoffs:
            # Create mask: True if row satisfies tradeoff t
            mask = pd.Series(True, index=discrete.index)
            for obj, label in t.elements.items():
                if obj in discrete.columns:
                    mask &= (discrete[obj] == label)
            tradeoff_masks[t.name] = mask

        # 4. Iterate Boxes (Rows)
        rows = []
        row_indices = []
        
        for box in boxes:
            target_name = box.target_tradeoff
            if not target_name:
                continue
                
            row_indices.append(target_name)
            
            # Apply Box Limits to X
            limits = getattr(box, 'limits', box)
            box_mask = pd.Series(True, index=X.index)
            for param, bounds in limits.items():
                if param in X.columns:
                    box_mask &= (X[param] >= bounds['min']) & (X[param] <= bounds['max'])
            
            # 5. Compute Boxed Density for ALL Tradeoffs (Cols)
            row_values = {}
            boxed_count = box_mask.sum()
            
            for t in all_tradeoffs:
                if boxed_count == 0:
                    boxed_density = 0.0
                else:
                    # Intersection of Box AND Tradeoff
                    success_in_box = (tradeoff_masks[t.name] & box_mask).sum()
                    boxed_density = success_in_box / boxed_count
                
                row_values[t.name] = boxed_density
            
            rows.append(row_values)
            
        if not rows:
            return pd.DataFrame()
            
        return pd.DataFrame(rows, index=row_indices)

    def get_tradeoff_coverage_matrix(
        self,
        boxes: List[Any],
        subset: str = 'all'
    ) -> pd.DataFrame:
        """
        Computes a matrix of Coverages for all tradeoffs when specific boxes are applied.
        
        Coverage = (Points in Box AND Satisfying Tradeoff) / (Total Points Satisfying Tradeoff)
        
        Rows: The Tradeoff targeted by the Box.
        Columns: The Tradeoff being measured.
        
        Args:
            boxes: List of Box objects.
            subset: 'all', 'train', or 'test'.
            
        Returns:
            pd.DataFrame: A square-ish matrix of coverages (0.0 - 1.0).
        """
        # 1. Prepare Data
        X, _, discrete = self._get_subset_data(subset)
        
        # 2. Precompute Tradeoff Masks & Totals (Denominators)
        all_tradeoffs = self.get_tradeoffs()
        tradeoff_masks = {}
        tradeoff_totals = {}
        
        for t in all_tradeoffs:
            # Create mask: True if row satisfies tradeoff t
            mask = pd.Series(True, index=discrete.index)
            for obj, label in t.elements.items():
                if obj in discrete.columns:
                    mask &= (discrete[obj] == label)
            tradeoff_masks[t.name] = mask
            tradeoff_totals[t.name] = mask.sum()

        # 3. Iterate Boxes (Rows)
        rows = []
        row_indices = []
        
        for box in boxes:
            target_name = box.target_tradeoff
            if not target_name:
                continue
                
            row_indices.append(target_name)
            
            # Apply Box Limits to X
            limits = getattr(box, 'limits', box)
            box_mask = pd.Series(True, index=X.index)
            for param, bounds in limits.items():
                if param in X.columns:
                    box_mask &= (X[param] >= bounds['min']) & (X[param] <= bounds['max'])
            
            # 4. Compute Coverage for ALL Tradeoffs (Cols)
            row_values = {}
            
            for t in all_tradeoffs:
                total_t = tradeoff_totals[t.name]
                if total_t == 0:
                    coverage = 0.0
                else:
                    # Intersection of Box AND Tradeoff
                    success_in_box = (tradeoff_masks[t.name] & box_mask).sum()
                    coverage = success_in_box / total_t
                
                row_values[t.name] = coverage
            
            rows.append(row_values)
            
        if not rows:
            return pd.DataFrame()
            
        return pd.DataFrame(rows, index=row_indices)

    def get_algorithm_performance_scores(
        self,
        boxes: List[Any],
        subset: str = 'all',
        weights: Optional[Union[Dict[str, float], str]] = None,
        return_std: bool = False
    ) -> Dict[str, float]:
        """
        Computes Global Average metrics (Macro-Averaged) for an algorithm's output.
        
        Evaluates the set of boxes against the defined tradeoffs.
        
        Metrics:
        - Precision (Density): Weighted avg of (Intersection / Box_Count).
        - Recall (Coverage): Weighted avg of (Intersection / Target_Count).
        - F1 Score: Weighted avg of harmonic mean(Precision, Recall).
        - Lift: Weighted avg of (Precision - Baseline_Density).
        - Complexity: Avg number of restricted parameters across FOUND boxes only.
        - Success Rate: (Number of Tradeoffs with a Box) / (Total Defined Tradeoffs).
        
        If a Tradeoff has no corresponding box (or an empty box), it contributes:
        - Precision: 0.0
        - Recall: 0.0
        - Lift: -Baseline_Density
        - Success Rate: Counted as a Failure (0).
        
        Note: Tradeoffs with 0% or 100% baseline density are excluded from Lift 
        and Success Rate calculations as improvement is impossible.
        
        Args:
            boxes: List of Box objects found by the algorithm.
            subset: 'all', 'train', or 'test'.
            weights: Weighting strategy. 
                     - None (default): Equal weighting (1.0 per tradeoff).
                     - 'frequency': Weight by number of points in the tradeoff region.
                     - Dict[str, float]: Manual weights {tradeoff_name: weight}.
            return_std: If True, includes standard deviation for metrics.
            
        Returns:
            Dict[str, float]: Dictionary of average scores (and std devs if requested).
        """
        # 1. Prepare Data
        X, _, discrete = self._get_subset_data(subset)
        
        # 2. Map Boxes to Tradeoffs
        # If multiple boxes target the same tradeoff, we take the first one
        box_map = {}
        for box in boxes:
            t_name = getattr(box, 'target_tradeoff', None)
            if t_name and t_name not in box_map:
                box_map[t_name] = box
        
        # 3. Iterate ALL Tradeoffs
        # Lists to store values for std dev calculation
        vals_prec = []
        vals_rec = []
        vals_f1 = []
        vals_lift = []
        vals_complexity = [] # Only for found boxes
        vals_weights = []
        vals_can_improve = [] # Flag for valid lift context
        vals_box_found = []   # Flag for success rate calculation
        
        # Only consider tradeoffs that actually exist in the data (non-empty)
        # Empty regions (0 points) are structurally impossible to improve and shouldn't count as misses.
        all_tradeoffs = self.get_tradeoffs(non_empty=True, subset=subset)
        if not all_tradeoffs:
            return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'lift': 0.0, 'complexity': 0.0, 'success_rate': 0.0}

        total_points = len(discrete)

        # Pre-calculate counts if frequency weighting is requested
        tradeoff_counts = {}
        if weights == 'frequency':
            for t in all_tradeoffs:
                t_mask = pd.Series(True, index=discrete.index)
                for obj, label in t.elements.items():
                    if obj in discrete.columns:
                        t_mask &= (discrete[obj] == label)
                tradeoff_counts[t.name] = t_mask.sum()

        print(len(all_tradeoffs), "tradeoffs to evaluate.", len(box_map.keys()), len(boxes))
        for t in all_tradeoffs:
            # Determine Weight
            if isinstance(weights, dict):
                weight = weights.get(t.name, 1.0)
            elif weights == 'frequency':
                weight = tradeoff_counts.get(t.name, 0.0)
            else:
                weight = 1.0
            
            vals_weights.append(weight)
            
            # Ground Truth Mask for Tradeoff T
            t_mask = pd.Series(True, index=discrete.index)
            for obj, label in t.elements.items():
                if obj in discrete.columns:
                    t_mask &= (discrete[obj] == label)
            
            target_count = t_mask.sum()
            baseline_density = target_count / total_points if total_points > 0 else 0.0
            # print("Baseline:", t.name, baseline_density)

            # Valid context for improvement: baseline is not 0 (impossible) or 1 (perfect)
            can_improve = (baseline_density > 0.0) and (baseline_density < 1.0)
            vals_can_improve.append(can_improve)
            
            # Check if we have a box
            box = box_map.get(t.name)
            
            if box:
                # Calculate Complexity
                limits = getattr(box, 'limits', box)
                
                # Calculate Metrics
                # Box Mask
                b_mask = pd.Series(True, index=X.index)
                if isinstance(limits, dict):
                    for param, bounds in limits.items():
                        if param in X.columns:
                            b_mask &= (X[param] >= bounds['min']) & (X[param] <= bounds['max'])
                
                box_count = b_mask.sum()
                
                if box_count > 0:
                    vals_box_found.append(True)
                    if isinstance(limits, dict):
                        vals_complexity.append(len(limits))
                    
                    intersection = (t_mask & b_mask).sum()
                    
                    # Precision (Density)
                    prec = intersection / box_count
                    
                    # Recall (Coverage)
                    rec = intersection / target_count if target_count > 0 else 0.0
                    
                    # F1
                    if (prec + rec) > 0:
                        f1 = 2 * (prec * rec) / (prec + rec)
                    else:
                        f1 = 0.0

                    # Lift
                    lift = prec - baseline_density
                        
                    vals_prec.append(prec)
                    vals_rec.append(rec)
                    vals_f1.append(f1)
                    vals_lift.append(lift)
                else:
                    # Treat empty box as a miss
                    vals_box_found.append(False)
                    vals_prec.append(0.0)
                    vals_rec.append(0.0)
                    vals_f1.append(0.0)
                    vals_lift.append(-baseline_density)
                
            else:
                vals_box_found.append(False)
                # Algorithm failed to find this tradeoff
                vals_prec.append(0.0)
                vals_rec.append(0.0)
                vals_f1.append(0.0)
                # Missed tradeoff has 0 precision, so lift = 0 - baseline
                vals_lift.append(-baseline_density)

        # 4. Compute Weighted Averages and Std Devs
        # Convert to numpy arrays for vectorized math
        a_prec = np.array(vals_prec)
        a_rec = np.array(vals_rec)
        a_f1 = np.array(vals_f1)
        a_lift = np.array(vals_lift)
        a_weights = np.array(vals_weights)
        a_can_improve = np.array(vals_can_improve, dtype=bool)
        a_found = np.array(vals_box_found, dtype=bool)
        
        total_weight = np.sum(a_weights)
        
        if total_weight == 0:
             return {'precision': 0.0, 'recall': 0.0, 'f1': 0.0, 'lift': 0.0, 'complexity': 0.0, 'success_rate': 0.0}

        avg_prec = np.average(a_prec, weights=a_weights)
        avg_rec = np.average(a_rec, weights=a_weights)
        avg_f1 = np.average(a_f1, weights=a_weights)
        
        # Lift & Success Rate: Only consider cases where improvement was possible
        if np.any(a_can_improve):
            # Lift
            valid_lifts = a_lift[a_can_improve]
            # print("Valid lifts:", valid_lifts)
            valid_weights = a_weights[a_can_improve]
            if np.sum(valid_weights) > 0:
                avg_lift = np.average(valid_lifts, weights=valid_weights)
            else:
                avg_lift = np.mean(valid_lifts)

            # Success Rate: Fraction of improvable cases where a box was actually found
            # Note: We don't weight success rate, it's a raw count metric usually.
            success_rate = np.sum(a_found & a_can_improve) / np.sum(a_can_improve)
        else:
            avg_lift = 0.0
            success_rate = 0.0
        
        avg_comp = np.mean(vals_complexity) if vals_complexity else 0.0

        results = {
            'precision': avg_prec,
            'recall': avg_rec,
            'f1': avg_f1,
            'lift': avg_lift,
            'complexity': avg_comp,
            'success_rate': success_rate
        }
        
        if return_std:
            # Helper for weighted std
            def weighted_std(values, weights, mean):
                variance = np.average((values - mean)**2, weights=weights)
                return np.sqrt(variance)
            
            results['precision_std'] = weighted_std(a_prec, a_weights, avg_prec)
            results['recall_std'] = weighted_std(a_rec, a_weights, avg_rec)
            results['f1_std'] = weighted_std(a_f1, a_weights, avg_f1)
            
            if np.any(a_can_improve):
                valid_lifts = a_lift[a_can_improve]
                valid_weights = a_weights[a_can_improve]
                if np.sum(valid_weights) > 0:
                    results['lift_std'] = weighted_std(valid_lifts, valid_weights, avg_lift)
                else:
                    results['lift_std'] = np.std(valid_lifts)
            else:
                results['lift_std'] = 0.0
                
            results['complexity_std'] = np.std(vals_complexity) if vals_complexity else 0.0

        return results

    def show_tradeoff_impact_heatmap(
        self,
        impact_matrix: pd.DataFrame,
        title: Optional[str] = None,
        figsize: Tuple[int, int] = (10, 8),
        cmap: str = 'YlGnBu',
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the Tradeoff Impact Matrix as a heatmap.
        
        Args:
            impact_matrix: DataFrame computed by get_tradeoff_impact_matrix.
            title: Optional plot title.
            figsize: Figure size.
            cmap: Colormap (default 'YlGnBu' for sequential density).
        """
        if impact_matrix.empty:
            raise ValueError("Impact matrix is empty.")
            
        # 2. Plot
        fig, ax = plt.subplots(figsize=figsize)
        
        sns.heatmap(
            impact_matrix, 
            annot=True, 
            fmt=".2f", 
            vmin=0.0,
            vmax=1.0,
            cmap=cmap, 
            ax=ax,
            cbar_kws={'label': 'Boxed Density (Success Rate)'}
        )
        
        full_title = title or "Tradeoff Impact Matrix"
        ax.set_title(full_title, pad=20)
        ax.set_ylabel("Applied Box (Target Tradeoff)")
        ax.set_xlabel("Impacted Tradeoff")
        
        plt.tight_layout()
        return fig

    def get_policy_robustness_ranking(
        self, 
        tradeoff_name: str, 
        metric: str = 'starr', 
        subset: str = 'all',
        decision_key: Optional[str] = None
    ) -> List[Tuple[str, float]]:
        """
        Returns a ranking of policies from most robust to least robust for a given tradeoff.
        
        Args:
            tradeoff_name: The target tradeoff to analyze.
            metric: 'starr' (higher is better) or 'regret' (lower is better).
            subset: 'all', 'train', or 'test'.
            decision_key: Optional. If provided, limits ranking to policies within this decision.
            
        Returns:
            List[Tuple[str, float]]: List of (policy_name, score) pairs, sorted by robustness.
        """
        # 1. Get the report for the single tradeoff
        report_df = self.get_robustness_report(
            decision_key=decision_key,
            tradeoff_names=[tradeoff_name],
            metric=metric,
            subset=subset
        )
        
        if report_df.empty or tradeoff_name not in report_df.columns:
            return []
            
        # 2. Extract series and drop NaNs
        scores = report_df[tradeoff_name].dropna()
        
        # 3. Sort based on metric directionality
        # STARR: Higher is better (Descending)
        # Regret: Lower is better (Ascending)
        ascending = (metric == 'regret')
        
        sorted_scores = scores.sort_values(ascending=ascending)
        
        # 4. Convert to list of tuples
        return list(zip(sorted_scores.index, sorted_scores.values))

    def show_robustness_heatmap(
        self, 
        metric: str = 'starr', 
        subset: str = 'all', 
        decision_key: Optional[str] = None, 
        tradeoff_names: Optional[List[str]] = None,
        matrix: Optional[pd.DataFrame] = None,
        title: Optional[str] = None,
        figsize: Optional[Tuple[int, int]] = None,
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the robustness report as a heatmap.
        
        Args:
            metric: 'starr' or 'regret'.
            subset: Data subset to use.
            decision_key: Optional decision to filter policies.
            tradeoff_names: Optional list of tradeoffs to include.
            matrix: Pre-calculated DataFrame. If None, it will be computed.
            title: Custom plot title.
            figsize: Figure size.
            **kwargs: Additional plotting parameters.
        """
        if matrix is None:
            matrix = self.get_robustness_report(
                decision_key=decision_key, 
                tradeoff_names=tradeoff_names, 
                metric=metric, 
                subset=subset
            )
        
        if matrix.empty:
            raise ValueError("Robustness matrix is empty. Cannot generate heatmap.")
            
        return self.coordinator.show_robustness_heatmap(matrix, metric=metric, title=title, figsize=figsize, **kwargs)

    def show_stability_radius(
        self, 
        policy_name: str, 
        tradeoff_name: str, 
        objective_cols: Optional[Tuple[str, str]] = None,
        subset: str = 'all', 
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the stability radius for a specific policy and tradeoff.
        
        This multi-panel plot shows the parameter space (MDS projection) and 
        the quality objective space, highlighting the nominal center and failure modes.
        
        Args:
            policy_name: Name of the policy to analyze.
            tradeoff_name: Name of the target tradeoff region.
            objective_cols: Pair of outcome names for the objective space panel.
            subset: 'all', 'train', or 'test'.
            **kwargs: Plotting parameters (e.g. figsize, max_points).
        """
        from ..analysis.contingency import ContingencyAnalyzer
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        # 1. Get Radius Info
        radius_info = self.compute_robustness(
            policy_name, tradeoff_name, metric='stability_radius', subset=subset, **kwargs
        )
        
        # 2. Extract Data for the policy
        X_full, Y_full, _ = self._get_subset_data(subset)
        
        config_col = self.sys_def.dataspace.configuration_identification.column
        analyzer_cont = ContingencyAnalyzer(self.sys_def)
        policy_map = analyzer_cont.get_decision_policy_map(self.experiments_df, config_col)
        
        policy_col = None
        for col in policy_map.columns:
            if (policy_map[col] == policy_name).any():
                policy_col = col
                break
        
        if policy_col is None:
            raise ValueError(f"Policy '{policy_name}' not found.")
            
        policy_mask = (policy_map[policy_col] == policy_name)
        
        # Fix: Filter the global policy_mask to match the subset indices
        if subset == 'all':
            subset_indices = self.experiments_df.index
        elif subset == 'train':
            subset_indices = self.train_indices
        else:
            subset_indices = self.test_indices
            
        # Select the policy_mask values corresponding to the subset rows
        final_mask = policy_mask.iloc[subset_indices]
        
        # Apply mask (boolean indexing works because both are aligned/length of subset)
        exp_subset = X_full[final_mask.values]
        out_subset = Y_full[final_mask.values]
        
        # 3. Determine target mask (Success/Failure)
        tradeoff = self.get_tradeoff(tradeoff_name)
        is_target = pd.Series(True, index=out_subset.index)
        for obj, label in tradeoff.elements.items():
            if obj in self.discrete_df.columns:
                is_target &= (self.discrete_df.loc[out_subset.index, obj] == label)
        
        # 4. Parameters and Objectives
        analyzer_fi = FeatureImportanceAnalyzer(self.sys_def)
        parameter_cols = kwargs.get('parameters')
        if parameter_cols is None:
            parameter_cols = analyzer_fi.get_parameter_columns(self.experiments_df)
        
        if objective_cols is None:
            objs = [o.name for o in self.get_outcomes()]
            objective_cols = (objs[0], objs[1]) if len(objs) >= 2 else (objs[0], objs[0])

        return self.coordinator.show_stability_radius_plot(
            exp_subset, out_subset, is_target, parameter_cols, radius_info, objective_cols, self.schemes, target_tradeoff=tradeoff, policy_name=policy_name, **kwargs
        )

    # --- Data Subset Helpers ---

    def _get_subset_data(self, subset: str = 'all') -> Tuple[pd.DataFrame, pd.DataFrame, Optional[pd.DataFrame]]:
        """Returns (experiments, outcomes, discrete) for the chosen subset."""
        if subset == 'all':
            return self.experiments_df, self.outcomes_df, self.discrete_df
        
        if self.train_indices is None:
            raise RuntimeError(f"Cannot access subset '{subset}'. Call split_data() first.")
            
        indices = self.train_indices if subset == 'train' else self.test_indices
        return self.experiments_df.iloc[indices], self.outcomes_df.iloc[indices], self.discrete_df.iloc[indices]

    def _filter_indices_for_subset(self, global_indices: np.ndarray, subset: str) -> np.ndarray:
        """
        Filters global dataset indices to only those in the chosen subset, 
        and returns their NEW integer positions relative to the subset.
        """
        if subset == 'all':
            return global_indices
            
        if self.train_indices is None:
            return np.array([])
            
        subset_indices = self.train_indices if subset == 'train' else self.test_indices
        
        # 1. Intersection: which global_indices are in the subset?
        # We use a set for O(1) lookups
        subset_set = set(subset_indices)
        matching_globals = [idx for idx in global_indices if idx in subset_set]
        
        if not matching_globals:
            return np.array([])
            
        # 2. Map back to integer positions [0...len(subset)-1]
        # We need to know where each matching global index is in the subset_indices array
        lookup = {idx: i for i, idx in enumerate(subset_indices)}
        local_positions = [lookup[idx] for idx in matching_globals]
        
        return np.array(local_positions)

    # --- Accessor Helpers ---

    def get_patterns(self) -> Dict[str, Any]:
        """Returns all architectural patterns in the system."""
        if not self.sys_def: return {}
        return self.sys_def.system.components

    def get_decisions(self, include_component_name: bool = False) -> Dict[str, Any]:
        """
        Returns a flat dictionary of all decisions across all patterns.
        Key format: "component_name:decision_name"
        """
        if not self.sys_def: return {}
        decisions = {}
        for comp_name, comp in self.sys_def.system.components.items():
            for dec_name, decision in comp.decisions.items():
                key = f"{comp_name}:{dec_name}" if include_component_name else dec_name
                decisions[key] = decision
        return decisions
    
    def get_policies(self) -> Dict[str, Any]:
        """
        Returns all system-level configurations (policies) identified in the dataspace.
        """
        if not self.sys_def: return {}

        configs = self.sys_def.dataspace.configuration_identification.configurations
        if isinstance(configs, list):
            policies = {c.name: c for c in configs}
        else:
            policies = configs
        return policies

    def get_outcomes(self) -> List[Any]:
        """Returns the list of quality objectives (outcomes)."""
        if not self.sys_def: return []
        return self.sys_def.dataspace.quality_objectives

    def get_tradeoffs(self, non_empty: bool = False, subset: str = 'all') -> List[Tradeoff]:
        """
        Returns the list of defined tradeoffs.
        
        Args:
            non_empty: If True, only returns tradeoffs that have at least one data point 
                       in the specified subset.
            subset: 'all' (default), 'train', or 'test'. Used only if non_empty=True.
        """
        if not self.sys_def: return []
        
        all_tradeoffs = self.sys_def.system.tradeoffs
        
        if not non_empty:
            return all_tradeoffs
            
        # Filter based on current data subset
        valid_tradeoffs = []
        for t in all_tradeoffs:
            indices = self.get_indices_for_tradeoff(t)
            subset_indices = self._filter_indices_for_subset(indices, subset)
            if len(subset_indices) > 0:
                valid_tradeoffs.append(t)
                
        return valid_tradeoffs

    def get_tradeoff(self, name: str) -> Tradeoff | None:
        """Returns the tradeoff with the given name, or None if not found."""
        if not self.sys_def: return None
        for tradeoff in self.sys_def.system.tradeoffs:
            if tradeoff.name == name:
                return tradeoff
        return None

    def add_tradeoff(self, name: str, elements: Dict[str, Any], label: Optional[str] = None, scheme: str = "discretization", description: str = "", params: Optional[Dict[str, Any]] = None) -> Tradeoff:
        """Programmatically adds a tradeoff definition to the session.
        
        Args:
            name: Unique concise name for the tradeoff.
            elements: Dict mapping outcome names to target labels.
            label: Human-readable display label.
            scheme: The tradeoff scheme.
            description: Optional text description.
            params: Optional additional parameters for the scheme.
            
        Returns:
            The created Tradeoff object.
        """
        if not self.sys_def:
            raise RuntimeError("System definition must be loaded before adding tradeoffs.")
            
        from .models import Tradeoff
        tradeoff = Tradeoff(
            name=name, 
            label=label or name,
            elements=elements, 
            scheme=scheme, 
            description=description,
            params=params or {}
        )
        
        # Check for duplicates
        self.sys_def.system.tradeoffs = [t for t in self.sys_def.system.tradeoffs if t.name != name]
        self.sys_def.system.tradeoffs.append(tradeoff)
        return tradeoff

    def clear_tradeoffs(self) -> None:
        """Removes all tradeoff definitions from the current session."""
        if self.sys_def:
            self.sys_def.system.tradeoffs = []

    def create_static_threshold_tradeoffs(self, thresholds: Dict[str, Union[float, Tuple[float, str]]], labels: Optional[List[str]] = None) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Generates all combinatorial tradeoffs based on static thresholds.
        
        Args:
            thresholds: Dictionary mapping objective names to threshold values OR (value, operator) tuples.
                        e.g., {'latency': 200, 'cost': (50, '<')}
            labels: Optional list of 2 labels [satisfactory, unsatisfactory].
            
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        import itertools
        
        # 1. Process data immediately
        self.define_tradeoffs(method='threshold', params={'thresholds': thresholds}, labels=labels)
        
        # 2. Build Grid
        objs = list(thresholds.keys())
        states = labels if labels else ["satisfactory", "unsatisfactory"]
        
        combinations = list(itertools.product(states, repeat=len(objs)))
        for combo in combinations:
            # Concise ID: sat-sat, sat-unsat
            name = "-".join([s[:3] for s in combo]) # abbreviate to first 3 chars
            
            # Descriptive Label: obj1: sat, obj2: unsat
            label_parts = [f"{obj}: {state}" for obj, state in zip(objs, combo)]
            display_label = ", ".join(label_parts)
            
            elements = dict(zip(objs, combo))
            self.add_tradeoff(
                name=name,
                label=display_label,
                scheme="threshold",
                params={'thresholds': thresholds},
                elements=elements,
                description=f"Threshold combination: {display_label}"
            )
        return self.get_tradeoffs(), self.schemes

    def create_pareto_nadir_tradeoffs(self, objectives: Optional[List[str]] = None, labels: Optional[List[str]] = None) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Generates all combinatorial tradeoffs based on the Pareto Nadir point.
        
        Args:
            objectives: List of objective names to consider. If None, uses all defined outcomes.
            labels: Optional list of 2 labels [pareto-efficient, sub-optimal].
            
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        import itertools
        
        # 1. Process data
        self.define_tradeoffs(method='pareto', labels=labels)
        
        if objectives is None:
            objectives = [obj.name for obj in self.get_outcomes()]
            
        # 2. Extract Labels from Schemes for consistency
        labels_map = {}
        target_schemes = [s for s in self.schemes if s.objective_name in objectives]
        for scheme in target_schemes:
            # Use unique labels only to avoid redundant combinations if a label is repeated in bins
            labels_map[scheme.objective_name] = list(dict.fromkeys([b.label for b in scheme.bins]))
            
        # 3. Generate Combinatorial Tradeoffs
        return self.create_discretization_tradeoffs(labels=labels_map, objectives=objectives, skip_definition=True)

    def create_pareto_epsilon_tradeoffs(self, epsilon: float = 0.05, objectives: Optional[List[str]] = None, labels: Optional[List[str]] = None) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Generates all combinatorial tradeoffs based on Epsilon-Pareto dominance.
        
        Args:
            epsilon: The tolerance parameter (e.g., 0.05 for 5%).
            objectives: List of objective names to consider. If None, uses all defined outcomes.
            labels: Optional list of 2 labels [epsilon-pareto-optimal, out].
            
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        # 1. Process data
        self.define_tradeoffs(method='pareto_epsilon', params={'epsilon': epsilon}, labels=labels)
        
        if objectives is None:
            objectives = [obj.name for obj in self.get_outcomes()]
            
        # 2. Extract Labels from Schemes
        labels_map = {}
        target_schemes = [s for s in self.schemes if s.objective_name in objectives]
        for scheme in target_schemes:
            labels_map[scheme.objective_name] = list(dict.fromkeys([b.label for b in scheme.bins]))
            
        # 3. Generate Combinatorial Tradeoffs
        return self.create_discretization_tradeoffs(labels=labels_map, objectives=objectives, skip_definition=True)

    def create_discretization_tradeoffs(self, n_bins: int = 3, labels: Optional[Dict[str, List[str]]] = None, ranges: Optional[Dict[str, Tuple[float, float]]] = None, objectives: Optional[List[str]] = None, skip_definition: bool = False) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Generates all combinatorial tradeoffs based on discretization bins.
        
        Args:
            n_bins: Number of bins per objective (if labels not provided).
            labels: Dictionary mapping objective names to lists of labels.
            ranges: Optional dictionary mapping objective names to (min, max) tuples.
            objectives: List of objective names to consider. If None, uses all defined outcomes.
            skip_definition: If True, assumes define_tradeoffs has already been called (used for clustering).
            
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        import itertools
        
        # 1. Process data (unless skipped)
        if not skip_definition:
            self.define_tradeoffs(method='discretization', n_bins=n_bins, labels=labels, ranges=ranges)
        
        if objectives is None:
            objectives = [obj.name for obj in self.get_outcomes()]
            
        label_sets = []
        final_objectives = []
        
        for obj in objectives:
            # Get actual labels from schemes if available, or provided labels, or defaults
            scheme = next((s for s in self.schemes if s.objective_name == obj), None)
            if scheme:
                label_sets.append([b.label for b in scheme.bins])
            elif labels and obj in labels:
                label_sets.append(labels[obj])
            else:
                label_sets.append([f"level_{i+1}" for i in range(n_bins)])
            final_objectives.append(obj)
            
        combinations = list(itertools.product(*label_sets))
        for combo in combinations:
            # Concise ID: e.g., low-fast, eff-sub
            name = "-".join([str(val) for val in combo])
            
            # Descriptive Label: obj1: low, obj2: fast
            label_parts = [f"{obj}: {val}" for obj, val in zip(final_objectives, combo)]
            display_label = ", ".join(label_parts)
            
            elements = dict(zip(final_objectives, combo))
            self.add_tradeoff(
                name=name,
                label=display_label,
                scheme="discretization" if not skip_definition else "automated",
                elements=elements,
                description=f"Automated combination: {display_label}"
            )
        return self.get_tradeoffs(), self.schemes

    def create_clustering_tradeoffs(self, min_k: int = 2, max_k: int = 5, objectives: Optional[List[str]] = None) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Generates combinatorial tradeoffs based on Univariate K-Means Clustering.
        
        Args:
            min_k: Minimum number of clusters to test.
            max_k: Maximum number of clusters to test.
            objectives: List of objective names. If None, uses all outcomes.
            
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        # 1. Run Clustering Discretization
        self.define_tradeoffs(method='clustering', params={'min_k': min_k, 'max_k': max_k})
        
        # 2. Extract Labels from Schemes
        labels_map = {}
        target_schemes = self.schemes
        if objectives:
            target_schemes = [s for s in self.schemes if s.objective_name in objectives]
            
        for scheme in target_schemes:
            labels_map[scheme.objective_name] = [b.label for b in scheme.bins]
            
        # 3. Generate Combinatorial Tradeoffs (skipping re-definition)
        return self.create_discretization_tradeoffs(labels=labels_map, objectives=objectives, skip_definition=True)

    def rename_outcome_labels(self, objective: str, mapping: Dict[str, str]) -> None:
        """
        Renames the labels for a specific objective in the discrete dataset, 
        tradeoff definitions, and schemes.
        
        Useful for post-processing automatic labels (e.g., 'cluster_0' -> 'High Performance').
        
        Args:
            objective: Name of the quality objective (e.g. 'response_time').
            mapping: Dictionary mapping old labels to new labels.
        """
        if self.discrete_df is None:
            raise RuntimeError("Tradeoffs not defined.")
            
        if objective not in self.discrete_df.columns:
            raise ValueError(f"Objective '{objective}' not found in discrete data.")

        # 1. Update Data
        self.discrete_df[objective] = self.discrete_df[objective].replace(mapping)
        
        # 2. Update Schemes
        scheme = next((s for s in self.schemes if s.objective_name == objective), None)
        if scheme:
            for bin_def in scheme.bins:
                if bin_def.label in mapping:
                    bin_def.label = mapping[bin_def.label]
                    
        # 3. Update Tradeoffs
        for t in self.sys_def.system.tradeoffs:
            if objective in t.elements:
                old_val = t.elements[objective]
                if old_val in mapping:
                    new_val = mapping[old_val]
                    # Update element
                    t.elements[objective] = new_val
                    
                    # Update Name/Label (Simple string substitution)
                    # We only substitute exact matches to avoid partial string issues
                    if t.name:
                        t.name = t.name.replace(str(old_val), str(new_val))
                    if t.label:
                        t.label = t.label.replace(str(old_val), str(new_val))
                        
        # 4. Rebuild Tradeoff Indices
        # We can't easily patch the dict keys, so we rebuild from current discrete_df
        # This mirrors logic in coordinator.define_tradeoffs
        groups = self.discrete_df.groupby(list(self.discrete_df.columns))
        self.tradeoff_indices = {
            ",".join(map(str, k)) if isinstance(k, tuple) else str(k): v 
            for k, v in groups.indices.items()
        }

    def create_tradeoffs(self, method: str = 'discretization', **kwargs) -> Tuple[List[Tradeoff], List[DiscretizationScheme]]:
        """
        Unified entry point for programmatically generating combinatorial tradeoffs.
        
        Delegates to strategy-specific helpers, ensuring a fresh start by calling 
        clear_tradeoffs() and automatically processing data via define_tradeoffs().
        
        Args:
            method: 'discretization', 'threshold', 'pareto', 'pareto_epsilon', or 'clustering'.
            **kwargs: Arguments passed to the underlying helper method:
                - For 'discretization': 'n_bins', 'labels', 'ranges', 'objectives'.
                - For 'threshold': 'thresholds' (Required), 'labels'.
                - For 'pareto': 'objectives', 'labels'.
                - For 'pareto_epsilon': 'epsilon' (Required), 'objectives', 'labels'.
                - For 'clustering': 'min_k', 'max_k', 'objectives'.
                
        Returns:
            Tuple[List[Tradeoff], List[DiscretizationScheme]]: The created tradeoff objects and their schemes.
        """
        # Validate mandatory parameters for entry point
        if method == 'threshold' and 'thresholds' not in kwargs:
            raise ValueError("Method 'threshold' requires 'thresholds' argument (dict of {objective: value}).")
        if method == 'pareto_epsilon' and 'epsilon' not in kwargs:
            raise ValueError("Method 'pareto_epsilon' requires 'epsilon' argument (float).")

        self.clear_tradeoffs()
        
        if method == 'discretization':
            labels_dict = kwargs.pop('labels', {})
            n_bins = kwargs.pop('n_bins', 3)
            # Try to adapt n_bins to the number of labels included in the (first of the) objectives
            if len(labels_dict) > 0:
                objective_bins = list(labels_dict.values())
                n_values = len(objective_bins[0]) if len(objective_bins) > 0 else 0
                n_bins = n_values if n_values > 0 else n_bins
            print(f"Creating discretization tradeoffs with {n_bins} bins.")
            return self.create_discretization_tradeoffs(labels=labels_dict, n_bins=n_bins, **kwargs)
            
        elif method == 'clustering':
            return self.create_clustering_tradeoffs(**kwargs)
            
        elif method == 'threshold':
            return self.create_static_threshold_tradeoffs(**kwargs)
            
        elif method in ['pareto', 'pareto_nadir']:
            return self.create_pareto_nadir_tradeoffs(**kwargs)
            
        elif method == 'pareto_epsilon':
            return self.create_pareto_epsilon_tradeoffs(**kwargs)
            
        else:
            raise ValueError(f"Unknown tradeoff creation method: {method}")

    def get_adaptive_processes(self) -> List[Any]:
        """Returns the list of adaptive processes."""
        if not self.sys_def: return []
        return self.sys_def.system.adaptive_processes

    # --- Feature Scoring ---

    def split_data(self, test_size: float = 0.2, random_state: int = 42, remove_outliers: bool = False, z_threshold: float = 3.0, verbose: bool = True) -> None:
        """
        Splits data into train/test sets, stratifying by tradeoff membership.
        Indices are stored in self.train_indices and self.test_indices.
        
        Args:
            test_size: Proportion of dataset to include in the test split.
            random_state: Seed for the random number generator.
            remove_outliers: If True, removes rows where any numeric outcome has a Z-score > z_threshold.
            z_threshold: Threshold for outlier detection (default 3.0).
            verbose: If True (default), prints detailed tradeoff distribution statistics.
        """
        from sklearn.model_selection import train_test_split
        
        if self.experiments_df is None or not self.tradeoff_indices:
            raise RuntimeError("Data must be loaded and tradeoffs defined before splitting.")

        # 1. Determine Valid Indices (Optional Outlier Removal)
        valid_indices = np.arange(len(self.experiments_df))
        
        if remove_outliers and self.outcomes_df is not None:
            from sklearn.preprocessing import StandardScaler
            numeric_outcomes = self.outcomes_df.select_dtypes(include=[np.number])
            
            if not numeric_outcomes.empty:
                scaler = StandardScaler()
                # Compute Z-scores just for detection
                z_scores = scaler.fit_transform(numeric_outcomes)
                
                # Keep rows where ALL outcomes are within threshold
                mask = (np.abs(z_scores) <= z_threshold).all(axis=1)
                valid_indices = valid_indices[mask]
                
                dropped_count = len(self.experiments_df) - len(valid_indices)
                if dropped_count > 0 and verbose:
                    print(f"Outlier removal: Dropped {dropped_count} rows based on outcome Z-scores > {z_threshold}.")

        # 2. Prepare Stratification Labels on the Valid Subset
        # We need a single label vector for sklearn's stratify.
        # Strategy:
        # 0 = No Tradeoff (Baseline)
        # 1..N = Specific Tradeoff
        # -1 = Multiple Tradeoffs (Overlap)
        
        n_valid = len(valid_indices)
        labels = np.zeros(n_valid, dtype=int)
        
        # Map global indices to local position in valid_indices
        global_to_local = {idx: i for i, idx in enumerate(valid_indices)}
        
        for i, (t_name, global_idxs) in enumerate(self.tradeoff_indices.items()):
            # Filter indices that are present in the valid set
            valid_t_idxs = [global_to_local[idx] for idx in global_idxs if idx in global_to_local]
            
            if not valid_t_idxs:
                continue
                
            local_idxs = np.array(valid_t_idxs)
            
            # Vectorized update of labels
            current_vals = labels[local_idxs]
            
            # If current is 0, assign this tradeoff ID (i+1)
            is_zero = current_vals == 0
            labels[local_idxs[is_zero]] = i + 1
            
            # If current is > 0 (already assigned), mark as Overlap (-1)
            is_assigned = current_vals > 0
            labels[local_idxs[is_assigned]] = -1

        # 3. Perform Split
        # Check for small classes
        from collections import Counter
        counts = Counter(labels)
        if any(c < 2 for c in counts.values()):
            if verbose:
                print("Warning: Some stratification classes have < 2 samples. Falling back to random split.")
            stratify = None
        else:
            stratify = labels

        train_local, test_local = train_test_split(
            np.arange(n_valid), 
            test_size=test_size, 
            stratify=stratify, 
            random_state=random_state
        )
        
        # 4. Map back to Global Indices
        self.train_indices = valid_indices[train_local]
        self.test_indices = valid_indices[test_local]
        
        # 5. Print Split Statistics
        if verbose:
            print(f"Data split: {len(self.train_indices)} train, {len(self.test_indices)} test.")
            
            # Helper to count tradeoffs in a set of indices
            def print_tradeoff_counts(name, indices):
                print(f"\n--- {name} Set Tradeoff Counts ---")
                idx_set = set(indices)
                for t_name, t_indices in self.tradeoff_indices.items():
                    count = sum(1 for i in t_indices if i in idx_set)
                    percentage = count / len(idx_set)
                    print(f"  {t_name}: {count}" + f" ({percentage:.2%})")
                    
            print_tradeoff_counts("Train", self.train_indices)
            print_tradeoff_counts("Test", self.test_indices)

    def compute_feature_scores(
        self, 
        include_levers: bool = True, 
        include_uncertainties: bool = True,
        include_constraints: bool = False,
        use_smart_correlation: bool = False,
        standardize: bool = False,
        remove_outliers: bool = False,
        z_threshold: float = 3.0,
        subset: str = 'train'
    ) -> pd.DataFrame:
        """
        Computes feature importance for all quality objectives.
        
        Args:
            include_levers: Whether to include design levers.
            include_uncertainties: Whether to include uncertainties.
            include_constraints: Whether to include constraints/fixed parameters.
            use_smart_correlation: Whether to use SmartCorrelatedSelection to prune features.
            standardize: Whether to standardize features (Z-score) before scoring.
            remove_outliers: Whether to remove outliers (Z-score > threshold) before scoring.
            z_threshold: Threshold for outlier detection.
            subset: 'train' (default for scoring), 'test', or 'all'.
            
        Returns:
            pd.DataFrame: Rows=Features, Columns=Outcomes, Values=Importance Score.
        """
        from ..analysis.feature_importance import FeatureImportanceAnalyzer

        if subset != 'all' and self.train_indices is None:
            # Auto-split if not done and subset requested
            print(f"Subset '{subset}' requested but data not split. Performing automatic split (20% test)...")
            self.split_data()

        analyzer = FeatureImportanceAnalyzer(self.sys_def)
        
        # 1. Prepare Data (Chosen subset)
        X_full, y_full, _ = self._get_subset_data(subset)
        
        # 2. Identify Features
        feature_cols = analyzer.get_parameter_columns(
            X_full, 
            include_levers=include_levers, 
            include_uncertainties=include_uncertainties,
            include_constraints=include_constraints
        )
        if not feature_cols:
            raise ValueError("No matching parameter columns found for scoring.")
            
        X = X_full[feature_cols]
        
        # 3. Preprocess (Standardize / Outliers)
        if standardize or remove_outliers:
            X, mask, stats = analyzer.preprocess_features(
                X, 
                standardize=standardize, 
                remove_outliers=remove_outliers, 
                z_threshold=z_threshold
            )
            self.feature_stats = stats
            # Align y with X (if rows removed)
            y_full = y_full[mask]
            
            if remove_outliers:
                print(f"Outlier removal dropped {len(mask) - mask.sum()} rows. Remaining: {len(X)}")
        
        # 4. Score per Outcome
        results = {}
        for outcome_col in y_full.columns:
            print(f"Scoring features for outcome: {outcome_col} (on subset: {subset})")
            scores = analyzer.compute_importance(
                X, 
                y_full[outcome_col], 
                use_smart_correlation=use_smart_correlation
            )
            # Note: Order of scores for each outcome might be different
            scores_sorted = scores.sort_index(ascending=True)
            results[outcome_col] = scores_sorted
            
        return pd.DataFrame(results)

    def show_feature_heatmap(self, scores_df: pd.DataFrame, **kwargs) -> plt.Figure:
        """Visualizes feature importance scores as a heatmap."""
        from ..analysis.visualization import show_importance_heatmap
        return show_importance_heatmap(scores_df, **kwargs)

    def align_boxes_to_tradeoffs(self, boxes: List[Any]) -> List[Optional[Any]]:
        """
        Aligns a list of discovered boxes to the full list of system tradeoffs.
        
        Useful for preparing the input list for robustness matrix methods.
        If multiple boxes match a tradeoff name, the first one is used.
        
        Args:
            boxes: List of Box objects (e.g., from discover_scenarios).
            
        Returns:
            List[Optional[Box]]: A list matching the order of self.get_tradeoffs().
        """
        all_tradeoffs = self.get_tradeoffs()
        box_list = []
        
        for tradeoff in all_tradeoffs:
            # Find the best box for this tradeoff
            best_box = next((b for b in boxes if b.target_tradeoff == tradeoff.name), None)
            box_list.append(best_box)
            
        return box_list

    def discover_scenarios(
        self, 
        tradeoff_names: Optional[Union[str, List[str]]] = None, 
        method: str = 'prim', 
        parameters: Optional[List[str]] = None,
        standardize: bool = False,
        combine_tradeoffs: bool = False,
        threshold: float = 0.8,
        mass_min: Optional[float] = None,
        **kwargs
    ) -> List[Any]:
        """
        Runs scenario discovery to find parameter regions for specific tradeoffs.
        
        Args:
            tradeoff_names: Name or list of names of tradeoffs to target.
                            If None, targets all tradeoffs defined in the system.
            method: 'prim' or 'cart'.
            parameters: List of parameters to include. If None, uses all parameters.
            standardize: Whether to standardize parameters before discovery.
            combine_tradeoffs: If True and multiple tradeoffs are provided, finds a region
                               that satisfies ANY of them (Union/OR logic). Only for PRIM.
            threshold: (PRIM Only) Minimum box density (purity). Higher values increase Density 
                       but may decrease Coverage. Default: 0.8.
            mass_min: Minimum support (fraction of data) for the box.
                      - For PRIM: Higher values increase Coverage but may decrease Density.
                      - For CART: Minimum samples per leaf. Higher values enforce simpler rules 
                        (higher Coverage), lower values allow specific rules (higher Density).
                        Default: None (algorithm default).
            
        Returns:
            List[Box]: Structured box objects with limits and performance metrics.
        """
        from ..analysis.discovery import Box, BoxEvaluator
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        # 1. Resolve parameters to analyze
        analyzer_fi = FeatureImportanceAnalyzer(self.sys_def)
        if parameters is None:
            parameters = analyzer_fi.get_parameter_columns(self.experiments_df)
        
        # 2. Normalize input names
        all_tradeoffs = self.get_tradeoffs()
        if tradeoff_names is None:
            tradeoff_names = [t.name for t in all_tradeoffs]
            tradeoff_labels = [','.join(t.elements.values()) for t in all_tradeoffs]
        elif isinstance(tradeoff_names, str):
            tradeoff_names = [tradeoff_names]
            tradeoff_labels = [','.join(t.elements.values()) for t in all_tradeoffs if t.name == tradeoff_names[0]]
        else:
            # List provided
            tradeoff_labels = []
            for name in tradeoff_names:
                t = next((t for t in all_tradeoffs if t.name == name), None)
                if t:
                    tradeoff_labels.append(','.join(t.elements.values()))
                else:
                    tradeoff_labels.append("unknown")

        # Dataset bounds (restricted to analyzed parameters)
        valid_params = [p for p in parameters if p in self.experiments_df.columns]
        target_df = self.experiments_df[valid_params]
            
        agg_results = target_df.select_dtypes(include=[np.number]).agg(['min', 'max'])
        min_max_dict = agg_results.to_dict()

        # Update kwargs with the explicit controls
        kwargs['threshold'] = threshold
        if mass_min is not None:
            kwargs['mass_min'] = mass_min

        # 3. Handle PRIM (Iterative)
        if method == 'prim':
            all_boxes = []
            
            if combine_tradeoffs and len(tradeoff_names) > 1:
                # Combined Logic
                boxes = self._discover_combined_prim(
                    tradeoff_names, parameters=parameters, standardize=standardize, **kwargs
                )
                
                # Set metadata for combined result
                combined_label = " OR ".join(tradeoff_names)
                for box in boxes:
                    box.target_tradeoff = combined_label
                    box.target_tradeoff_labels = "combined"
                    box.dataset_bounds = min_max_dict
                    box.name = f"Box for {combined_label}"
                
                all_boxes.extend(boxes)
                
            else:
                # Iterative Logic
                for name, label in zip(tradeoff_names, tradeoff_labels):
                    boxes = self._discover_single_prim(
                        name, parameters=parameters, standardize=standardize, **kwargs
                    )
                    print(min_max_dict)
                    for box in boxes:
                        box.target_tradeoff_labels = label
                        box.dataset_bounds = min_max_dict
                        box.name = f"Box for {name}"
                    all_boxes.extend(boxes)
            
            return all_boxes

        # 4. Handle CART (Global + Filter)
        # For CART, we run global discovery on all unique label combinations
        # and then filter the resulting boxes to only those matching target tradeoffs.
        
        if self.train_indices is None:
            self.split_data()
            
        X_train = self.experiments_df.iloc[self.train_indices][parameters]
        X_test = self.experiments_df.iloc[self.test_indices][parameters]
        
        # CART multi-class targets
        y_train = self.discrete_df.iloc[self.train_indices].astype(str).agg(','.join, axis=1)
        unique_classes = y_train.unique()
        
        # Precompute prevalence and test masks for evaluation
        prevalence_map = y_train.value_counts(normalize=True).to_dict()
        y_test_map = {}
        for row_str in unique_classes:
            y_test_map[row_str] = (self.discrete_df.iloc[self.test_indices].astype(str).agg(','.join, axis=1) == row_str)

        # Preprocessing
        current_stats = None
        if standardize:
             X_train, _, stats = analyzer_fi.preprocess_features(X_train, standardize=True)
             current_stats = stats
             X_test_arr = stats['scaler'].transform(X_test[stats['numeric_cols']])
             X_test = pd.DataFrame(X_test_arr, index=X_test.index, columns=stats['numeric_cols'])

        print(f"Running CART global discovery for all tradeoff combinations ...")
        discovery_kwargs = kwargs.copy()
        discovery_kwargs['discrete_outcomes'] = y_train
        
        result = self.coordinator.discover_scenarios(
            X_train, outcome="all", method='cart', experiments_df=X_train, **discovery_kwargs
        )
        
        if not result: return []
        
        # result is List[Box] from CARTDiscovery
        cart_boxes = result
        boxes = []
        for box in cart_boxes:
            class_str = str(box.target_tradeoff)
            # Check if this class matches ANY of the requested tradeoffs
            matched_tradeoff = None
            for t_name in tradeoff_names:
                if self._matches_tradeoff(class_str, t_name):
                    matched_tradeoff = t_name
                    break
            
            box.dataset_bounds = min_max_dict
            
            # If no specific names were requested, we return all (matched_tradeoff is just informational)
            # But here the user specifically wants to filter.
            if matched_tradeoff:
                # Include the named tradeoff as metadata
                box.target_tradeoff_labels = box.target_tradeoff 
                box.target_tradeoff = matched_tradeoff 
                box.name = f"Box for {matched_tradeoff}"
            else:
                box.name = f"Box for {class_str}"

            # Evaluate and Post-process
            y_test = y_test_map.get(class_str)
            prevalence = prevalence_map.get(class_str, 0.0)
            if y_test is not None:
                box.metrics = BoxEvaluator.evaluate(box.limits, X_test, y_test, population_prevalence=prevalence)
                box.population_prevalence = prevalence
            
            # De-standardize
            if standardize and current_stats:
                self._destandardize_box(box, current_stats)
            
            boxes.append(box)
                
        return boxes

    def _discover_combined_prim(self, tradeoff_names: List[str], parameters=None, standardize=False, **kwargs) -> List[Any]:
        """Internal helper for combined PRIM discovery (Union of tradeoffs)."""
        from ..analysis.discovery import Box, BoxEvaluator
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        if self.train_indices is None:
            self.split_data()
            
        analyzer = FeatureImportanceAnalyzer(self.sys_def)
        if parameters is None:
            parameters = analyzer.get_parameter_columns(self.experiments_df)
            
        X_train = self.experiments_df.iloc[self.train_indices][parameters]
        X_test = self.experiments_df.iloc[self.test_indices][parameters]
        
        # Build Combined Mask (Union)
        y_all = pd.Series(False, index=self.experiments_df.index)
        
        for t_name in tradeoff_names:
            tradeoff = next((t for t in self.get_tradeoffs() if t.name == t_name), None)
            if not tradeoff: continue
            
            # Mask for this tradeoff
            t_mask = pd.Series(True, index=self.experiments_df.index)
            for obj_name, target_label in tradeoff.elements.items():
                if obj_name in self.discrete_df.columns:
                    t_mask &= (self.discrete_df[obj_name] == target_label)
            
            # Union
            y_all |= t_mask
        
        y_train = y_all.iloc[self.train_indices]
        y_test = y_all.iloc[self.test_indices]
        prevalence = y_train.sum() / len(y_train) if len(y_train) > 0 else 0.0

        # Preprocessing
        current_stats = None
        if standardize:
             X_train, _, stats = analyzer.preprocess_features(X_train, standardize=True)
             current_stats = stats
             X_test_arr = stats['scaler'].transform(X_test[stats['numeric_cols']])
             X_test = pd.DataFrame(X_test_arr, index=X_test.index, columns=stats['numeric_cols'])

        print(f"Running Combined PRIM discovery for: {tradeoff_names} ...")
        discovery_kwargs = kwargs.copy()
        discovery_kwargs['y_mask'] = y_train
            
        # We pass a dummy outcome name since we provided y_mask
        result = self.coordinator.discover_scenarios(
            X_train, outcome="combined", method='prim', experiments_df=X_train, **discovery_kwargs
        )
        
        if not result: return []
        
        # Post-process
        final_boxes = []
        for box in result:
            # Evaluate on Test Set
            box.metrics = BoxEvaluator.evaluate(box.limits, X_test, y_test, population_prevalence=prevalence)
            box.population_prevalence = prevalence
            
            if standardize and current_stats:
                self._destandardize_box(box, current_stats)
            
            final_boxes.append(box)
            
        return final_boxes

    def _discover_single_prim(self, tradeoff_name: str, parameters=None, standardize=False, **kwargs) -> List[Any]:
        """Internal helper for single PRIM discovery."""
        from ..analysis.discovery import Box, BoxEvaluator
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        if self.train_indices is None:
            self.split_data()
            
        analyzer = FeatureImportanceAnalyzer(self.sys_def)
        if parameters is None:
            parameters = analyzer.get_parameter_columns(self.experiments_df)
            
        X_train = self.experiments_df.iloc[self.train_indices][parameters]
        X_test = self.experiments_df.iloc[self.test_indices][parameters]
        
        # Target prep
        tradeoff = next((t for t in self.get_tradeoffs() if t.name == tradeoff_name), None)
        if not tradeoff: return []
                
        y_all = pd.Series(True, index=self.experiments_df.index)
        for obj_name, target_label in tradeoff.elements.items():
            if obj_name in self.discrete_df.columns:
                y_all &= (self.discrete_df[obj_name] == target_label)
        
        y_train = y_all.iloc[self.train_indices]
        y_test = y_all.iloc[self.test_indices]
        prevalence = y_train.sum() / len(y_train) if len(y_train) > 0 else 0.0

        # Preprocessing
        current_stats = None
        if standardize:
             X_train, _, stats = analyzer.preprocess_features(X_train, standardize=True)
             current_stats = stats
             X_test_arr = stats['scaler'].transform(X_test[stats['numeric_cols']])
             X_test = pd.DataFrame(X_test_arr, index=X_test.index, columns=stats['numeric_cols'])

        print(f"Running PRIM discovery for: {tradeoff_name} ...")
        discovery_kwargs = kwargs.copy()
        discovery_kwargs['y_mask'] = y_train
            
        result = self.coordinator.discover_scenarios(
            X_train, outcome=tradeoff_name, method='prim', experiments_df=X_train, **discovery_kwargs
        )
        
        if not result: return []
        
        # result is List[Box] from PRIMDiscovery
        # Typically PRIM returns one best box, but could be multiple if n_boxes=True
        prim_boxes = result
        final_boxes = []
        
        for box in prim_boxes:
            box.target_tradeoff = tradeoff_name
            # Evaluate on Test Set
            box.metrics = BoxEvaluator.evaluate(box.limits, X_test, y_test, population_prevalence=prevalence)
            box.population_prevalence = prevalence
            
            if standardize and current_stats:
                self._destandardize_box(box, current_stats)
            
            final_boxes.append(box)
            
        return final_boxes

    def _destandardize_box(self, box, stats):
        """Helper to convert box limits back to original scales."""
        scaler = stats['scaler']
        numeric_cols = stats['numeric_cols']
        means_map = dict(zip(numeric_cols, scaler.mean_))
        stds_map = dict(zip(numeric_cols, scaler.scale_))
        
        new_limits = {}
        for param, lims in box.limits.items():
            m = means_map.get(param, 0.0)
            s = stds_map.get(param, 1.0)
            new_limits[param] = {
                'min': float(lims['min'] * s + m),
                'max': float(lims['max'] * s + m)
            }
        box.limits = new_limits

    def _matches_tradeoff(self, class_str: str, tradeoff_name: str) -> bool:
        """Checks if a CART class string matches a named tradeoff definition."""
        outcome_cols = list(self.discrete_df.columns)
        labels = class_str.split(',')
        label_map = dict(zip(outcome_cols, labels))
        
        tradeoff = next((t for t in self.get_tradeoffs() if t.name == tradeoff_name), None)
        if not tradeoff: return False
        
        for obj, target in tradeoff.elements.items():
            if label_map.get(obj) != target:
                return False
        return True

    def get_weighted_feature_ranking(self, scores_df: pd.DataFrame, weights: Optional[Dict[str, float]] = None, tolerance: float = 0.0) -> List[str]:
        """
        Aggregates multi-outcome importance scores into a single ranked list of features.
        
        Args:
            scores_df: The matrix of scores (Rows=Features, Cols=Outcomes).
            weights: Optional dictionary mapping outcome names to weights. 
                     If None, all outcomes are weighted equally.
            tolerance: Minimum weighted score required to include a feature in the ranking.
                     
        Returns:
            List[str]: Feature names sorted by weighted importance (descending).
        """
        if scores_df.empty:
            return []
            
        # 1. Prepare Weights
        outcomes = scores_df.columns
        if weights is None:
            # Equal weights
            w_series = pd.Series(1.0 / len(outcomes), index=outcomes)
        else:
            # Normalize user weights to sum to 1.0
            w_series = pd.Series(weights).reindex(outcomes).fillna(0.0)
            total = w_series.sum()
            if total > 0:
                w_series = w_series / total
            else:
                w_series = pd.Series(1.0 / len(outcomes), index=outcomes)

        # 2. Compute Weighted Sum
        # multiply matrix by weight vector
        aggregated_scores = scores_df.dot(w_series)
        
        # 3. Filter and Sort
        # Keep only features with score > tolerance
        filtered_scores = aggregated_scores[aggregated_scores > tolerance]
        
        return filtered_scores.sort_values(ascending=False).index.tolist()

    @staticmethod
    def select_top_k_parameters(scores_df: pd.DataFrame, k: int=None, threshold=0.2, index_order=None) -> List[str]:
        df = scores_df
        if index_order is not None:
            df = scores_df.reindex(index_order)
        
        rows_with_high_values = (df > threshold).any(axis=1)
        selected_indices = df.index[rows_with_high_values].tolist()
        if (k is not None) and len(selected_indices) > k:
            selected_indices = selected_indices[:k]
        return selected_indices

    def _compute_impacts(self, boxes: List[Any], method: str, subset: str='test') -> pd.DataFrame:

        all_impacts_df = []
        for policy_name in self.get_policies().keys():
            impact_df = self.get_tradeoff_impact_matrix(
                boxes=boxes, 
                policy_name=policy_name, # Optional: analyze a specific policy
                subset=subset                  # 'all', 'train', or 'test'
            )
            impact_df['policy'] = policy_name
            all_impacts_df.append(impact_df)

        all_impacts_df = pd.concat(all_impacts_df)
        all_impacts_df.index.name = 'target'
        all_impacts_df = all_impacts_df.reset_index().set_index('policy')
        all_impacts_df['method'] = method
        
        return all_impacts_df

    def get_robustness_results(self, prim_boxes: List[Any], cart_boxes: List[Any], baseline: pd.DataFrame = None, method: str='test set', metric: str='starr'):
        
        prim_all_impacts_df = self._compute_impacts(prim_boxes, 'prim') # These are usually computed on the test set
        cart_all_impacts_df = self._compute_impacts(cart_boxes, 'cart') # These are usually computed on the test set
        prim_all_impacts_df.reset_index(inplace=True) # 'policy´ is the old index
        cart_all_impacts_df.reset_index(inplace=True) # 'policy´ is the old index

        if baseline is not None:
            base_matrix = baseline.copy()
        else:
            base_matrix = self.get_robustness_report(metric=metric, subset='test')
        base_matrix['method'] = method
        base_matrix['target'] = '' # No target here
        base_matrix.reset_index(inplace=True) # 'policy´ is the old index
      
        prim_all_impacts_df = prim_all_impacts_df.sort_values(by='policy')
        prim_all_impacts_df = prim_all_impacts_df.sort_values(by='target', key=lambda col: col.map(get_tradeoff_sort_key))
        cart_all_impacts_df = cart_all_impacts_df.sort_values(by='policy')
        cart_all_impacts_df = cart_all_impacts_df.sort_values(by='target', key=lambda col: col.map(get_tradeoff_sort_key))
        base_matrix = base_matrix.sort_values(by='policy')
        base_matrix = base_matrix.sort_values(by='target', key=lambda col: col.map(get_tradeoff_sort_key))

        combined_df = pd.concat([base_matrix, prim_all_impacts_df, cart_all_impacts_df], ignore_index=True)
        header = ['method', 'policy', 'target']
        tradeoff_columns = [c for c in combined_df.columns if c not in header]
        columns = header + sort_tradeoff_labels(tradeoff_columns)
        combined_df = combined_df[columns]
        
        return combined_df
