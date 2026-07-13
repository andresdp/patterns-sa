import pandas as pd
import numpy as np
from typing import List, Dict, Any, Optional, Tuple
from ..core.models import Parameter, QualityObjective

class SemanticNaNHandler:
    """Implements JIT transformations for semantic NaN handling.
    
    This class handles the logic for:
    1. Auditing NaN proportions in datasets.
    2. Imputing outcome NaNs as 'failures' based on architectural policies.
    3. Transforming optional input NaNs into sentinel values for numeric algorithms.
    """
    
    @staticmethod
    def audit_nan_proportions(df: pd.DataFrame) -> Dict[str, Any]:
        """Calculates NaN proportions for the given DataFrame."""
        if df is None or df.empty:
            return {}
        
        total_cells = df.size
        total_nans = df.isnull().sum().sum()
        overall_prop = (total_nans / total_cells) * 100 if total_cells > 0 else 0
        
        col_nans = df.isnull().sum()
        stats = {
            "overall_pct": overall_prop,
            "total_nans": int(total_nans),
            "total_cells": int(total_cells),
            "columns": (col_nans / len(df) * 100).to_dict()
        }
        return stats

    @staticmethod
    def impute_outcomes(df: pd.DataFrame, objectives: List[QualityObjective]) -> pd.DataFrame:
        """Applies nan_policy to outcome columns.
        
        By default, NaNs in outcomes are treated as 'worst-case' failures.
        """
        df_imputed = df.copy()
        for obj in objectives:
            if obj.name not in df_imputed.columns:
                continue
            
            if not df_imputed[obj.name].isnull().any():
                continue
                
            policy = obj.nan_policy
            if policy == "worst_case":
                # Determine worst case value: slightly outside the current range in the 'bad' direction
                p_min = df_imputed[obj.name].min()
                p_max = df_imputed[obj.name].max()
                p_range = p_max - p_min
                if p_range == 0: p_range = abs(p_min) if p_min != 0 else 1.0
                
                if obj.maximize:
                    # Worst case is below minimum
                    val = p_min - (0.1 * p_range)
                else:
                    # Worst case is above maximum
                    val = p_max + (0.1 * p_range)
                df_imputed[obj.name] = df_imputed[obj.name].fillna(val)
            elif policy == "fixed_value" and obj.nan_value is not None:
                df_imputed[obj.name] = df_imputed[obj.name].fillna(obj.nan_value)
            elif policy == "drop":
                # Handled by caller or ignored here
                pass
                
        return df_imputed

    @staticmethod
    def apply_sentinel_transformation(df: pd.DataFrame, parameters: List[Parameter]) -> Tuple[pd.DataFrame, Dict[str, float]]:
        """Maps NaNs in optional parameters to sentinel values for discovery.
        
        Allows PRIM/CART to treat 'Option Not Selected' as a distinct numeric region.
        """
        df_trans = df.copy()
        sentinels = {}
        for param in parameters:
            # We only transform if the parameter is explicitly marked as optional
            if param.name not in df_trans.columns or not getattr(param, 'optional', False):
                continue
                
            if not df_trans[param.name].isnull().any():
                continue
            
            # Use a value slightly below the current minimum
            p_min = df_trans[param.name].min()
            p_max = df_trans[param.name].max()
            p_range = p_max - p_min
            if p_range == 0: p_range = abs(p_min) if p_min != 0 else 1.0
            
            sentinel = p_min - (0.1 * p_range)
            df_trans[param.name] = df_trans[param.name].fillna(sentinel)
            sentinels[param.name] = sentinel
            
        return df_trans, sentinels
