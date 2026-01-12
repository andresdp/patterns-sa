from typing import List, Dict, Any, Optional, Tuple, Union
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from .coordinator import ArchSpaceCore
from .models import SystemDefinition, DiscretizationScheme, Tradeoff

class PatternAnalysis:
    """Encapsulates the state and workflow for analyzing a single pattern configuration. 
    
    This class manages the lifecycle of data loading, processing, and analysis 
    for a given SystemDefinition.
    """

    def __init__(self, json_path: str, coordinator: Optional[ArchSpaceCore] = None):
        self.json_path = json_path
        self.coordinator = coordinator or ArchSpaceCore()
        self.reset()

    def reset(self) -> None:
        """
        Clears all temporal analysis state, including loaded dataframes, 
        tradeoff definitions, split indices, and feature statistics.
        """
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
        
        # Data Split & Processing State
        self.train_indices: Optional[np.ndarray] = None
        self.test_indices: Optional[np.ndarray] = None
        self.feature_stats: Optional[Dict[str, Any]] = None

    def load(self, validate_integrity: bool = True) -> None:
        """Loads the system definition and then the experimental data."""
        # 1. Load Definition
        self.sys_def = self.coordinator.load_system_definition(self.json_path)
        
        # 2. Load Data (using the definition to parse it)
        self.raw_df, self.experiments_df, self.outcomes_df = \
            self.coordinator.load_detailed_data(self.json_path, validate_integrity=validate_integrity)

    def define_tradeoffs(self, n_bins: int = 3, labels: Optional[Dict[str, List[str]]] = None, ranges: Optional[Dict[str, Tuple[float, float]]] = None, method: str = 'discretization', params: Optional[Dict[str, Any]] = None) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Defines tradeoff regions in the outcome space.
        
        Args:
            n_bins: Number of bins to use for discretization.
            labels: Optional dictionary mapping objective names to lists of labels.
                    If None, labels will be generated automatically.
            ranges: Optional dictionary mapping objective names to (min, max) tuples.
                    If provided, these bounds define the binning range instead of the data min/max.
            method: 'discretization', 'pareto', 'threshold', 'pareto_epsilon', 'pareto_knee'.
            params: Dictionary of parameters for specific methods (e.g. {'epsilon': 0.05} or {'thresholds': ...}).
        """
        if self.outcomes_df is None or self.sys_def is None:
            raise RuntimeError("Data must be loaded before defining tradeoffs.")

        # Prepare kwargs based on method
        kwargs = {}
        if method == 'discretization':
            kwargs = {'n_bins': n_bins, 'all_labels': labels, 'ranges': ranges}
        elif method in ['pareto', 'pareto_epsilon', 'pareto_knee', 'threshold']:
            kwargs = {'objectives': self.sys_def.dataspace.quality_objectives}
            if params:
                kwargs['params'] = params

        self.discrete_df, self.schemes, self.tradeoff_indices, self.pareto_front = self.coordinator.define_tradeoffs(
            self.outcomes_df, method=method, **kwargs
        )
        return self.discrete_df, self.schemes

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

    def plot_distributions(self, tradeoff: Optional[Tradeoff] = None, highlight_indices: Optional[np.ndarray] = None, **kwargs) -> plt.Figure:
        """Plots outcome distributions with tradeoff overlays for the current session."""
        return self.coordinator.plot_distributions(
            self.outcomes_df, self.schemes, tradeoff=tradeoff, highlight_indices=highlight_indices, **kwargs
        )

    def show_quality_objective_space(self, x_metric: str, y_metric: str, highlight_tradeoffs: Optional[List[Tradeoff]] = None, highlight_policies: Optional[List[str]] = None, show_overall: bool = True, color_points: bool = True, draw_rectangles: bool = False, subset: str = 'all', **kwargs) -> plt.Figure:
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
        """
        X, Y, _ = self._get_subset_data(subset)
        
        highlight_indices_map = {}
        if highlight_tradeoffs:
            for t in highlight_tradeoffs:
                indices = self.get_indices_for_tradeoff(t)
                filtered = self._filter_indices_for_subset(indices, subset)
                if len(filtered) > 0:
                    highlight_indices_map[t.name] = filtered
                    
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
            color_points=color_points, draw_rectangles=draw_rectangles, **kwargs
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

    def compute_robustness(
        self, 
        policy_name: str, 
        tradeoff_name: str, 
        metric: str = 'starr', 
        subset: str = 'all', 
        **kwargs
    ) -> Dict[str, Any]:
        """
        Calculates a specific robustness metric for a policy relative to a tradeoff.
        
        Args:
            policy_name: Name of the policy.
            tradeoff_name: Name of the target tradeoff.
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.
            
        Returns:
            Dict[str, Any]: Metric value and detailed computation information.
        """
        from ..analysis.robustness import RobustnessAnalyzer
        from ..analysis.contingency import ContingencyAnalyzer
        
        # 1. Prepare Data Subsets
        indices = self._filter_indices_for_subset(range(len(self.raw_df)), subset)
        
        # Filter for Policy
        # We need the decision key to find which column to look at, 
        # but if names are unique we can search.
        # Better: Assume user knows the policy.
        # Find which decision this policy belongs to
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
        
        # Intersection of subset and policy
        final_indices = [idx for idx in indices if policy_mask.iloc[idx]]
        
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

        # 3. Compute
        if metric == 'starr':
            return RobustnessAnalyzer.compute_starr(target_subset)
        elif metric == 'regret':
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
                outcomes_subset, target_subset, boundaries, stats=self.feature_stats
            )
        else:
            raise ValueError(f"Unknown robustness metric: {metric}")

    def get_robustness_report(
        self, 
        decision_key: Optional[str] = None, 
        tradeoff_names: Optional[List[str]] = None, 
        metric: str = 'starr', 
        subset: str = 'all', 
        policy_names: Optional[List[str]] = None,
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
            
        Returns:
            pd.DataFrame: Index=Policies, Columns=Tradeoffs, Values=Metric.
        """
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
            row = {'Policy': policy}
            for t_name in tradeoff_names:
                try:
                    res = self.compute_robustness(policy, t_name, metric=metric, subset=subset, **kwargs)
                    row[t_name] = res.get('value', 0.0)
                except Exception:
                    # Policy might not exist in this context or tradeoff issues
                    row[t_name] = np.nan
            report_data.append(row)
            
        return pd.DataFrame(report_data).set_index('Policy')

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
        **kwargs
    ) -> plt.Figure:
        """
        Visualizes the robustness report as a heatmap.
        
        Args:
            metric: 'starr' or 'regret'.
            subset: 'all', 'train', or 'test'.
            decision_key: Optional decision to filter policies.
            tradeoff_names: Optional list of tradeoffs to include.
            **kwargs: Arguments passed to seaborn.heatmap (e.g., cmap, annot).
            
        Returns:
            plt.Figure: The matplotlib figure object.
        """
        import seaborn as sns
        
        # 1. Get Data
        df = self.get_robustness_report(
            decision_key=decision_key, 
            tradeoff_names=tradeoff_names, 
            metric=metric, 
            subset=subset
        )
        
        if df.empty:
            raise ValueError("Robustness report is empty. Cannot generate heatmap.")
            
        # 2. Setup Plot
        fig, ax = plt.subplots(figsize=kwargs.pop('figsize', (10, len(df)*0.5 + 2)))
        
        # 3. Determine Color Map based on Metric
        # STARR: 0..1 (Higher is better) -> Blues or Greens
        # Regret: 0..inf (Lower is better) -> Reds or reversed sequential
        cmap = kwargs.pop('cmap', None)
        if cmap is None:
            if metric == 'starr':
                cmap = 'Greens'
            else:
                cmap = 'Reds' # Higher regret = Red
        
        # 4. Draw Heatmap
        sns.heatmap(df, annot=kwargs.pop('annot', True), fmt=kwargs.pop('fmt', '.2f'), 
                    cmap=cmap, ax=ax, **kwargs)
        
        ax.set_title(f"Robustness Heatmap ({metric.upper()}) - Subset: {subset}")
        plt.tight_layout()
        
        return fig

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

    def get_decisions(self) -> Dict[str, Any]:
        """
        Returns a flat dictionary of all decisions across all patterns.
        Key format: "component_name:decision_name"
        """
        if not self.sys_def: return {}
        decisions = {}
        for comp_name, comp in self.sys_def.system.components.items():
            for dec_name, decision in comp.decisions.items():
                decisions[f"{comp_name}:{dec_name}"] = decision
        return decisions
    
    def get_policies(self) -> Dict[str, Any]:
        """
        Returns all system-level configurations (policies) identified in the dataspace.
        """
        if not self.sys_def: return {}
        configs = self.sys_def.dataspace.configuration_identification.configurations
        if isinstance(configs, list):
            return {c.name: c for c in configs}
        return configs

    def get_outcomes(self) -> List[Any]:
        """Returns the list of quality objectives (outcomes)."""
        if not self.sys_def: return []
        return self.sys_def.dataspace.quality_objectives

    def get_tradeoffs(self) -> List[Tradeoff]:
        """Returns the list of defined tradeoffs."""
        if not self.sys_def: return []
        return self.sys_def.system.tradeoffs

    def get_adaptive_processes(self) -> List[Any]:
        """Returns the list of adaptive processes."""
        if not self.sys_def: return []
        return self.sys_def.system.adaptive_processes

    # --- Feature Scoring ---

    def split_data(self, test_size: float = 0.2, random_state: int = 42) -> None:
        """
        Splits data into train/test sets, stratifying by tradeoff membership.
        Indices are stored in self.train_indices and self.test_indices.
        """
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        if self.experiments_df is None or not self.tradeoff_indices:
            raise RuntimeError("Data must be loaded and tradeoffs defined before splitting.")

        analyzer = FeatureImportanceAnalyzer(self.sys_def)
        self.train_indices, self.test_indices = analyzer.create_stratified_split(
            self.experiments_df,
            self.tradeoff_indices,
            test_size=test_size,
            random_state=random_state
        )
        print(f"Data split: {len(self.train_indices)} train, {len(self.test_indices)} test.")

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
            results[outcome_col] = scores
            
        return pd.DataFrame(results)

    def show_feature_heatmap(self, scores_df: pd.DataFrame, **kwargs) -> plt.Figure:
        """Visualizes feature importance scores as a heatmap."""
        from ..analysis.visualization import show_importance_heatmap
        return show_importance_heatmap(scores_df, **kwargs)

    def discover_scenarios(
        self, 
        tradeoff_names: Optional[Union[str, List[str]]] = None, 
        method: str = 'prim', 
        parameters: Optional[List[str]] = None,
        standardize: bool = False,
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
            
        Returns:
            List[Box]: Structured box objects with limits and performance metrics.
        """
        from ..analysis.discovery import Box, BoxEvaluator
        from ..analysis.feature_importance import FeatureImportanceAnalyzer
        
        # 1. Normalize input names
        if tradeoff_names is None:
            tradeoff_names = [t.name for t in self.get_tradeoffs()]
        elif isinstance(tradeoff_names, str):
            tradeoff_names = [tradeoff_names]

        # 2. Handle PRIM (Iterative)
        if method == 'prim':
            all_boxes = []
            for name in tradeoff_names:
                # We call ourselves recursively or just use the logic for one
                # To avoid complex recursion, we extract the core logic
                boxes = self._discover_single_prim(
                    name, parameters=parameters, standardize=standardize, **kwargs
                )
                all_boxes.extend(boxes)
            return all_boxes

        # 3. Handle CART (Global + Filter)
        # For CART, we run global discovery on all unique label combinations
        # and then filter the resulting boxes to only those matching target tradeoffs.
        
        if self.train_indices is None:
            self.split_data()
            
        analyzer = FeatureImportanceAnalyzer(self.sys_def)
        if parameters is None:
            parameters = analyzer.get_parameter_columns(self.experiments_df)
            
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
             X_train, _, stats = analyzer.preprocess_features(X_train, standardize=True)
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
        
        _, cart_boxes, _ = result
        boxes = []
        for label, limits in cart_boxes.items():
            class_str = str(label)
            # Check if this class matches ANY of the requested tradeoffs
            matched_tradeoff = None
            for t_name in tradeoff_names:
                if self._matches_tradeoff(class_str, t_name):
                    matched_tradeoff = t_name
                    break
            
            # If no specific names were requested, we return all (matched_tradeoff is just informational)
            # But here the user specifically wants to filter.
            if matched_tradeoff:
                box = Box(limits=limits, target_tradeoff=class_str, method='cart')
                # Include the named tradeoff as metadata
                box.target_tradeoff_name = matched_tradeoff 
                
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
        _, limits_dict, _ = result
        
        box = Box(limits=limits_dict, target_tradeoff=tradeoff_name, method='prim')
        box.metrics = BoxEvaluator.evaluate(box.limits, X_test, y_test, population_prevalence=prevalence)
        box.population_prevalence = prevalence
        
        if standardize and current_stats:
            self._destandardize_box(box, current_stats)
            
        return [box]

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

    def get_weighted_feature_ranking(self, scores_df: pd.DataFrame, weights: Optional[Dict[str, float]] = None) -> List[str]:
        """
        Aggregates multi-outcome importance scores into a single ranked list of features.
        
        Args:
            scores_df: The matrix of scores (Rows=Features, Cols=Outcomes).
            weights: Optional dictionary mapping outcome names to weights. 
                     If None, all outcomes are weighted equally.
                     
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
        
        # 3. Sort and Return
        return aggregated_scores.sort_values(ascending=False).index.tolist()




    