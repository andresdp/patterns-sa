from typing import List, Dict, Any, Optional, Tuple
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
        
        # State
        self.sys_def: Optional[SystemDefinition] = None
        self.raw_df: Optional[pd.DataFrame] = None
        self.experiments_df: Optional[pd.DataFrame] = None
        self.outcomes_df: Optional[pd.DataFrame] = None
        self.discrete_df: Optional[pd.DataFrame] = None
        self.pareto_front: Optional[pd.DataFrame] = None
        self.tradeoff_indices: Dict[str, np.ndarray] = {}
        self.schemes: List[DiscretizationScheme] = []

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

    def show_quality_objective_space(self, x_metric: str, y_metric: str, highlight_tradeoffs: Optional[List[Tradeoff]] = None, **kwargs) -> plt.Figure:
        """Plots a 2D scatter of outcomes with tradeoff overlays and highlighting."""
        highlight_indices_map = {}
        if highlight_tradeoffs:
            for t in highlight_tradeoffs:
                indices = self.get_indices_for_tradeoff(t)
                if len(indices) > 0:
                    highlight_indices_map[t.name] = indices
                    
        return self.coordinator.show_quality_objective_space(
            self.outcomes_df, x_metric, y_metric, self.schemes, 
            highlight_indices_map=highlight_indices_map, **kwargs
        )