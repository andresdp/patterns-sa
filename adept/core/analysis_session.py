from typing import List, Dict, Any, Optional, Tuple
import pandas as pd
from .coordinator import ArchSpaceCore
from .models import SystemDefinition, DiscretizationScheme

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
        self.schemes: List[DiscretizationScheme] = []

    def load(self, validate_integrity: bool = True) -> None:
        """Loads the system definition and then the experimental data."""
        # 1. Load Definition
        self.sys_def = self.coordinator.load_system_definition(self.json_path)
        
        # 2. Load Data (using the definition to parse it)
        self.raw_df, self.experiments_df, self.outcomes_df = \
            self.coordinator.load_detailed_data(self.json_path, validate_integrity=validate_integrity)

    def define_tradeoffs(self, n_bins: int = 3, labels: Optional[Dict[str, List[str]]] = None, ranges: Optional[Dict[str, Tuple[float, float]]] = None, method: str = 'discretization') -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Defines tradeoff regions in the outcome space.
        
        Args:
            n_bins: Number of bins to use for discretization.
            labels: Optional dictionary mapping objective names to lists of labels.
                    If None, labels will be generated automatically.
            ranges: Optional dictionary mapping objective names to (min, max) tuples.
                    If provided, these bounds define the binning range instead of the data min/max.
            method: 'discretization' or 'pareto'.
        """
        if self.outcomes_df is None or self.sys_def is None:
            raise RuntimeError("Data must be loaded before defining tradeoffs.")

        # Prepare kwargs based on method
        kwargs = {}
        if method == 'discretization':
            kwargs = {'n_bins': n_bins, 'all_labels': labels, 'ranges': ranges}
        elif method == 'pareto':
            kwargs = {'objectives': self.sys_def.dataspace.quality_objectives}

        self.discrete_df, self.schemes, self.pareto_front = self.coordinator.define_tradeoffs(
            self.outcomes_df, method=method, **kwargs
        )
        return self.discrete_df, self.schemes

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