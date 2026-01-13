from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional
import pandas as pd
import os
from .definitions import SystemDefinition, Dataspace

class DataLoader(ABC):
    @abstractmethod
    def load(self, source: Any) -> pd.DataFrame:
        """Load data from `source` and return a pandas DataFrame."""

class PandasDataLoader(DataLoader):
    def __init__(self, **read_kwargs):
        self.read_kwargs = read_kwargs

    def load(self, source: Any) -> pd.DataFrame:
        """Load CSV (or any pandas-supported source) into a DataFrame."""
        return pd.read_csv(source, **self.read_kwargs)

class GenericDataLoader(DataLoader):
    def load(self, source: Any) -> pd.DataFrame:
        """
        Loads data based on a system definition JSON file.
        Returns the raw dataframe.
        """
        sys_def = self.load_system_definition(source)
        return self._load_from_definition(sys_def, base_path=os.path.dirname(source))

    def load_system_definition(self, json_path: str) -> SystemDefinition:
        return SystemDefinition.from_json(json_path)

    def load_data(self, source: Any) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Loads data and splits it into (raw_df, experiments_df, outcomes_df).
        """
        sys_def = self.load_system_definition(source)
        df = self._load_from_definition(sys_def, base_path=os.path.dirname(source))
        
        experiments_cols = []
        outcomes_cols = []
        
        # Identify experiment columns from system components parameters
        for comp_name, comp in sys_def.system.components.items():
            for param_name in comp.parameters.keys():
                # Try simple match or component_param match
                if param_name in df.columns:
                    experiments_cols.append(param_name)
                elif f"{comp_name}_{param_name}" in df.columns:
                    experiments_cols.append(f"{comp_name}_{param_name}")
        
        # Identify outcome columns from quality objectives
        for qa in sys_def.dataspace.quality_objectives:
            if qa.name in df.columns:
                outcomes_cols.append(qa.name)
        
        # Also include policy/config columns in experiments if defined
        if sys_def.dataspace.policy_identification.column:
             col = sys_def.dataspace.policy_identification.column
             if col in df.columns:
                 experiments_cols.append(col)

        # Fallback if no specific columns found (e.g. discovery mode or simple CSV)
        if not experiments_cols and not outcomes_cols:
             return df, df, df # Return full df for everything

        experiments_df = df[experiments_cols].copy() if experiments_cols else pd.DataFrame()
        outcomes_df = df[outcomes_cols].copy() if outcomes_cols else pd.DataFrame()
        
        return df, experiments_df, outcomes_df

    def _load_from_definition(self, sys_def: SystemDefinition, base_path: str) -> pd.DataFrame:
        if sys_def.dataspace.source_file:
            # Resolve path relative to JSON location
            path = sys_def.dataspace.source_file
            if not os.path.isabs(path):
                path = os.path.join(base_path, path)
            
            df = pd.read_csv(path)
            
            # Apply renames
            if sys_def.dataspace.column_renames:
                df.rename(columns=sys_def.dataspace.column_renames, inplace=True)
            
            return df
        
        # Handle split files logic (if policy_identification.from == "file")
        if sys_def.dataspace.policy_identification.from_ == "file":
            dfs = []
            policies = sys_def.dataspace.policy_identification.policies
            policy_list = policies if isinstance(policies, list) else list(policies.values())
            
            for policy in policy_list:
                if policy.source_file:
                    path = policy.source_file
                    if not os.path.isabs(path):
                        path = os.path.join(base_path, path)
                    temp_df = pd.read_csv(path)
                    # Inject policy name
                    temp_df['policy'] = policy.name
                    dfs.append(temp_df)
            
            if dfs:
                df = pd.concat(dfs, ignore_index=True)
                if sys_def.dataspace.column_renames:
                    df.rename(columns=sys_def.dataspace.column_renames, inplace=True)
                return df

        raise ValueError("Could not determine data source from SystemDefinition")

__all__ = ["DataLoader", "PandasDataLoader", "GenericDataLoader"]