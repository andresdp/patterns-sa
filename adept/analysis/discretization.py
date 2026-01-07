from typing import Dict, Optional, Tuple
import pandas as pd
import numpy as np
from collections import Counter


class DataProcessor:
    """Handles data discretization and labeling.
    
    This class implements the 'Discretization-Based Exploration' paradigm.
    It transforms continuous performance metrics into categorical labels 
    (e.g., fast, average, slow), which simplifies the architectural solution 
    space and makes trade-offs more intuitive for human interpretation and 
    scenario discovery algorithms.
    """

    @staticmethod
    def get_bins(col: pd.Series, n: int, min_max: Tuple[Optional[float], Optional[float]] = (None, None)) -> list:
        """Calculates bin boundaries for a given numeric column. 
        
        Args:
            col: The numeric data series to bin.
            n: Number of bins.
            min_max: Predefined (min, max) limits to use instead of column range.
            
        Returns:
            A list of bin boundaries.
        """
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
        """Counts unique combinations of categorical outcomes. 
        
        A 'tradeoff' is represented as a comma-separated string of category labels 
        (e.g., 'fast,high').
        """
        temp = df.to_string(header=False, index=False, index_names=False).split('\n')
        tradeoffs = [separator.join(ele.split()) for ele in temp]
        return Counter(tradeoffs)

    @staticmethod
    def discretize(df: pd.DataFrame, n_bins: int = 3, mins_maxs: Tuple[Optional[float], Optional[float]] = (None, None), all_labels: Optional[Dict] = None) -> Tuple[pd.DataFrame, Counter]:
        """Transforms a continuous DataFrame into categorical bins. 
        
        Args:
            df: DataFrame containing continuous metrics.
            n_bins: Default number of bins per column.
            mins_maxs: List of (min, max) tuples for each column.
            all_labels: Dictionary mapping column names to lists of label strings.
            
        Returns:
            A tuple containing (discretized_df, tradeoffs_counter).
        """
        discrete_df = df.copy()
        for idx, c in enumerate(df.columns):
            qa = df[c]
            min_max = (None, None)
            if mins_maxs != (None, None):
                min_max = mins_maxs[idx]
            qa_bins = DataProcessor.get_bins(qa, n_bins, min_max=min_max)
            
            if all_labels and c in all_labels:
                qa_labels = pd.cut(qa, bins=qa_bins, labels=all_labels[c])
            else:
                qa_labels = pd.cut(qa, bins=qa_bins)

            discrete_df[c] = qa_labels

        available_tradeoffs = DataProcessor.get_tradeoffs(discrete_df)
        return discrete_df, available_tradeoffs