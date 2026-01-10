from typing import Dict, Optional, Tuple, List, Any
import pandas as pd
import numpy as np
from collections import Counter
from ..core.models import QualityBin, DiscretizationScheme, QualityObjective


class DataProcessor:
    """Handles the definition of tradeoff regions in the outcome space.
    
    This component is responsible for segmenting continuous outcome data into 
    meaningful regions (tradeoffs) that can be analyzed. It supports the 
    'Discretization-Based Exploration' paradigm and is designed to support 
    others (e.g., Pareto-based) in the future.
    """

    @staticmethod
    def define_tradeoffs(df: pd.DataFrame, method: str = 'discretization', **kwargs) -> Tuple[pd.DataFrame, Any, Optional[pd.DataFrame]]:
        """Defines tradeoff regions in the outcome space.
        
        Args:
            df: DataFrame containing continuous metrics.
            method: The method to use for definition ('discretization' or 'pareto').
            **kwargs: Method-specific arguments.
            
        Returns:
            A tuple containing (labeled_df, schemes_metadata, pareto_front_df).
            - labeled_df: DataFrame with categorical labels.
            - schemes_metadata: List of DiscretizationScheme objects.
            - pareto_front_df: DataFrame containing only the Pareto front (if method='pareto').
        """
        if method == 'discretization':
            labeled_df, schemes = DataProcessor._discretize(df, **kwargs)
            return labeled_df, schemes, None
        elif method == 'pareto':
            return DataProcessor._pareto_segmentation(df, **kwargs)
        else:
            raise NotImplementedError(f"Tradeoff definition method '{method}' not implemented.")

    @staticmethod
    def _pareto_segmentation(df: pd.DataFrame, objectives: List[QualityObjective]) -> Tuple[pd.DataFrame, List[DiscretizationScheme], pd.DataFrame]:
        """Segments data based on the Pareto Front Nadir point."""
        try:
            import paretoset
        except ImportError:
            raise ImportError("paretoset library is required for 'pareto' scheme.")

        # 1. Map objectives to paretoset sense
        directions = {}
        for obj in objectives:
            if obj.name in df.columns:
                directions[obj.name] = "max" if obj.maximize else "min"
        
        if not directions:
            raise ValueError("No matching objectives found in DataFrame for Pareto analysis.")

        # 2. Compute Pareto Mask
        subset_cols = list(directions.keys())
        sense_list = [directions[col] for col in subset_cols]
        mask = paretoset.paretoset(df[subset_cols], sense=sense_list)
        pareto_df = df[mask].copy()
        
        # 3. Create Schemes and Segment Data
        discrete_df = df.copy()
        schemes = []
        
        for col, direction in directions.items():
            # Calculate threshold based on the Pareto set's Nadir point
            if direction == "max":
                # For maximization, the threshold is the lowest value found in the Pareto set
                threshold = float(pareto_df[col].min())
                bins = [-float('inf'), threshold, float('inf')]
                labels = ["Sub-optimal", "Pareto-Compliant"]
            else:
                # For minimization, the threshold is the highest value found in the Pareto set
                threshold = float(pareto_df[col].max())
                bins = [-float('inf'), threshold, float('inf')]
                labels = ["Pareto-Compliant", "Sub-optimal"]

            # Apply binning
            discrete_df[col] = pd.cut(discrete_df[col], bins=bins, labels=labels)
            
            # Create Schema Metadata
            q_bins = [
                QualityBin(label=labels[0], min_value=bins[0], max_value=bins[1]),
                QualityBin(label=labels[1], min_value=bins[1], max_value=bins[2])
            ]
            schemes.append(DiscretizationScheme(
                objective_name=col,
                bins=q_bins,
                method="pareto_nadir"
            ))
            
        return discrete_df, schemes, pareto_df

    @staticmethod
    def _discretize(df: pd.DataFrame, n_bins: int = 3, ranges: Optional[Dict[str, Tuple[float, float]]] = None, all_labels: Optional[Dict] = None) -> Tuple[pd.DataFrame, List[DiscretizationScheme]]:
        """Internal implementation of discretization logic."""
        discrete_df = df.copy()
        schemes = []
        all_labels = all_labels or {}
        ranges = ranges or {}
        
        for idx, c in enumerate(df.columns):
            qa = df[c]
            min_max = ranges.get(c, (None, None))
            
            qa_bins = DataProcessor.get_bins(qa, n_bins, min_max=min_max)
            
            # Determine labels for this column
            if c in all_labels:
                labels = all_labels[c]
                if len(labels) != n_bins:
                    raise ValueError(f"Number of labels for '{c}' ({len(labels)}) must match n_bins ({n_bins}).")
            else:
                # Generate default labels: level_1, level_2, ...
                labels = [f"level_{i+1}" for i in range(n_bins)]
            
            qa_labels = pd.cut(qa, bins=qa_bins, labels=labels)
            discrete_df[c] = qa_labels
            
            # Create scheme metadata
            bins = []
            for i in range(len(labels)):
                bins.append(QualityBin(
                    label=str(labels[i]),
                    min_value=float(qa_bins[i]),
                    max_value=float(qa_bins[i+1])
                ))
            
            schemes.append(DiscretizationScheme(
                objective_name=c,
                bins=bins
            ))

        return discrete_df, schemes

    @staticmethod
    def get_bins(col: pd.Series, n: int, min_max: Tuple[Optional[float], Optional[float]] = (None, None)) -> list:
        """Calculates bin boundaries for a given numeric column."""
        unique_values = sorted((set(col.values)))
        if min_max == (None, None):
            min_x = np.min(unique_values)
            max_x = np.max(unique_values)
        else:
            min_x = min_max[0]
            max_x = min_max[1]
        
        # Add small buffer to include endpoints in the cut
        min_x = min_x - 0.1
        max_x = max_x + 0.1
        delta = (max_x - min_x) / n
        return ([min_x + i * delta for i in range(0, n)] + [max_x])

    @staticmethod
    def get_tradeoffs(df: pd.DataFrame, separator: str = ',') -> Counter:
        """Counts unique combinations of categorical outcomes."""
        temp = df.to_string(header=False, index=False, index_names=False).split('\n')
        tradeoffs = [separator.join(ele.split()) for ele in temp]
        return Counter(tradeoffs)
