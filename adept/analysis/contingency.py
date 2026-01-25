from typing import Dict, List, Optional, Any
import pandas as pd
import numpy as np
from ..core.models import SystemDefinition, Tradeoff

class ContingencyAnalyzer:
    """
    Analyzes the relationship between architectural decisions (Policies) and 
    Outcomes (Tradeoffs), producing contingency tables for visualization.
    """

    def __init__(self, sys_def: SystemDefinition):
        self.sys_def = sys_def

    def get_decision_policy_map(self, df: pd.DataFrame, config_col: str) -> pd.DataFrame:
        """
        Expands a Configuration ID column into multiple columns, one for each Decision,
        containing the specific Policy name selected.

        Args:
            df: DataFrame containing the configuration column.
            config_col: Name of the column containing configuration IDs.

        Returns:
            pd.DataFrame: A DataFrame with the same index as df, where columns are 
                          "Component:Decision" and values are Policy names.
        """
        if config_col not in df.columns:
            return pd.DataFrame(index=df.index)

        # 1. Build Map: ConfigID -> { "Comp:Dec": "Policy" }
        config_map = {}
        
        # configurations can be a dict or list in the model
        configs = self.sys_def.dataspace.configuration_identification.configurations
        if isinstance(configs, list):
             # Convert list to dict assuming 'name' is the ID
             configs = {c.name: c for c in configs}

        for cfg_id, cfg_obj in configs.items():
            row_dict = {}
            for ref in cfg_obj.pattern_policy_references:
                key = f"{ref.component}:{ref.decision}"
                row_dict[key] = ref.policy
            config_map[cfg_id] = row_dict

        # 2. Apply Map efficiently
        # Get unique config IDs from data
        unique_ids = df[config_col].unique()
        
        # Pre-compute rows for each unique ID
        expanded_data = []
        for uid in unique_ids:
            # We treat uid as string for lookup
            uid_str = str(uid)
            if uid_str in config_map:
                row = config_map[uid_str].copy()
                row[config_col] = uid # Keep ID for join
                expanded_data.append(row)
        
        if not expanded_data:
            return pd.DataFrame(index=df.index)

        mapping_df = pd.DataFrame(expanded_data)
        
        # 3. Merge back to preserve original index and row count
        # We perform a left join on the config_col
        # Ensure types match
        df_reset = df[[config_col]].reset_index()
        mapping_df[config_col] = mapping_df[config_col].astype(df[config_col].dtype)
        
        merged = pd.merge(df_reset, mapping_df, on=config_col, how='left')
        merged.set_index('index', inplace=True)
        
        # Drop the config column, we only want the decision columns
        return merged.drop(columns=[config_col])

    def compute_contingency(
        self, 
        policy_df: pd.DataFrame, 
        tradeoff_mask_df: pd.DataFrame, 
        decision_key: Optional[str] = None,
        normalization_mode: str = 'population'
    ) -> pd.DataFrame:
        """
        Computes the contingency table (cross-tabulation).

        Args:
            policy_df: DataFrame of Policies (output of get_decision_policy_map).
            tradeoff_mask_df: Boolean DataFrame of Tradeoff membership.
            decision_key: Specific decision column to analyze. If None, analyzes 'Configuration'.
            normalization_mode: 'population' (default, divides by policy count), 
                                'row' (divides by row sum, so row sums to 100%),
                                'none' (raw counts).

        Returns:
            pd.DataFrame: Rows=Policies, Cols=Tradeoffs.
        """
        # If no specific decision, we use the raw Configuration IDs if available, 
        # or we have to decide what "All" means.
        # But here we assume policy_df has the columns we want to inspect.
        
        if decision_key:
            if decision_key not in policy_df.columns:
                 raise ValueError(f"Decision '{decision_key}' not found in policy map.")
            row_series = policy_df[decision_key]
            row_label = decision_key
        else:
            # If no decision key provided, we might be looking at the overall Config ID
            # But policy_df usually only has decision columns.
            # We can't easily "flatten" all columns unless we stack them.
            # Strategy: Stack all decision columns into one Series (Policy Name)
            # This assumes Policy Names are unique across decisions or we want to aggregate them.
            # For now, let's just stack.
            stacked_df = policy_df.stack().reset_index(level=1, name='Policy')
            # This aligns indices, but we have multiple rows per original index now.
            # We need to replicate the tradeoff mask for these new rows.
            # This is complex.
            # Alternative: User MUST provide decision_key OR we use the Config ID (if passed separate).
            raise ValueError("decision_key must be provided for now.")

        # Join Policies (Rows) and Tradeoffs (Columns)
        # We align them by index.
        # tradeoff_mask_df has boolean columns.
        
        # We can use pd.crosstab, but crosstab expects categorical series for both.
        # Here columns are separate booleans. 
        # We can iterate over tradeoff columns.
        
        results = {}
        for tradeoff_name in tradeoff_mask_df.columns:
            mask = tradeoff_mask_df[tradeoff_name]
            # Count True values grouped by Policy
            counts = mask.groupby(row_series).sum()
            results[tradeoff_name] = counts
            
        result_df = pd.DataFrame(results).fillna(0)
        
        # Normalization logic
        if normalization_mode == 'population':
            totals = row_series.value_counts()
            result_df = result_df.div(totals, axis=0) * 100.0
        elif normalization_mode == 'row':
            row_sums = result_df.sum(axis=1)
            # Avoid division by zero
            row_sums = row_sums.replace(0, 1) 
            result_df = result_df.div(row_sums, axis=0) * 100.0
        elif normalization_mode == 'none':
            pass
        else:
            raise ValueError(f"Unknown normalization_mode: {normalization_mode}")
            
        return result_df
