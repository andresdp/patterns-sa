from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional, List
import pandas as pd
import os
import glob
import warnings
from .models import SystemDefinition, Dataspace, BehavioralTrace

class DataLoader(ABC):
    """Abstract base class for data loaders.
    
    A DataLoader's responsibility is to bridge the gap between external 
    storage (CSV, SQL, etc.) and the internal pandas-based analysis engine.
    """
    @abstractmethod
    def load(self, source: Any) -> pd.DataFrame:
        """Load data from `source` and return a pandas DataFrame."""

class PandasDataLoader(DataLoader):
    """A thin wrapper around pandas.read_csv for simple loading tasks."""
    def __init__(self, **read_kwargs):
        self.read_kwargs = read_kwargs

    def load(self, source: Any) -> pd.DataFrame:
        """Load CSV (or any pandas-supported source) into a DataFrame."""
        return pd.read_csv(source, **self.read_kwargs)

class GenericDataLoader(DataLoader):
    """The primary ADEPT loader that implements metadata-driven data ingestion.
    
    This loader uses a SystemDefinition (JSON) to understand how to:
    1. Locate data files (relative to the JSON or absolute).
    2. Merge data from multiple policy files if necessary.
    3. Rename columns to align with internal framework expectations.
    4. Automatically split data into 'experiments' (parameters) and 
       'outcomes' (objectives) based on the architectural model.
    """
    def load(self, source: Any) -> pd.DataFrame:
        """
        Loads data based on a system definition JSON file.
        
        Returns:
            The raw, combined DataFrame after renames.
        """
        sys_def = self.load_system_definition(source)
        return self._load_from_definition(sys_def, base_path=os.path.dirname(source))

    def load_system_definition(self, json_path: str) -> SystemDefinition:
        """Parses a system.json file into a SystemDefinition model."""
        return SystemDefinition.from_json(json_path)

    def load_data(self, source: Any) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Loads data and automatically partitions it based on the architectural model.
        
        Args:
            source: Path to the system definition JSON file.
            
        Returns:
            A tuple of (raw_df, experiments_df, outcomes_df).
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
             return df, df, df 

        experiments_df = df[experiments_cols].copy() if experiments_cols else pd.DataFrame()
        outcomes_df = df[outcomes_cols].copy() if outcomes_cols else pd.DataFrame()
        
        return df, experiments_df, outcomes_df

    def load_behavioral_traces(self, source: str) -> List[BehavioralTrace]:
        """
        Loads behavioral traces from the directory specified in the system definition.
        
        Traces represent the cycle-by-cycle performance of adaptive processes.
        """
        sys_def = self.load_system_definition(source)
        if not sys_def.dataspace.traces_path:
            return []
        
        base_path = os.path.dirname(source)
        traces_path = sys_def.dataspace.traces_path
        if not os.path.isabs(traces_path):
            traces_path = os.path.join(base_path, traces_path)
            
        if not os.path.exists(traces_path):
            warnings.warn(f"Traces path {traces_path} does not exist.")
            return []
            
        traces = []
        # Assume traces are CSV files in the directory, named by scenario_id
        for filepath in glob.glob(os.path.join(traces_path, "*.csv")):
            scenario_id = os.path.splitext(os.path.basename(filepath))[0]
            df = pd.read_csv(filepath)
            traces.append(BehavioralTrace(
                trace_id=scenario_id,
                scenario_id=scenario_id,
                outcomes=df
            ))
            
        return traces

    def _load_from_definition(self, sys_def: SystemDefinition, base_path: str) -> pd.DataFrame:
        """Internal helper to resolve file paths and perform renames."""
        if sys_def.dataspace.source_file:
            path = sys_def.dataspace.source_file
            if not os.path.isabs(path):
                path = os.path.join(base_path, path)
            
            df = pd.read_csv(path)
            
            if sys_def.dataspace.column_renames:
                df.rename(columns=sys_def.dataspace.column_renames, inplace=True)
            
            return df
        
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
                    temp_df['policy'] = policy.name
                    dfs.append(temp_df)
            
            if dfs:
                df = pd.concat(dfs, ignore_index=True)
                if sys_def.dataspace.column_renames:
                    df.rename(columns=sys_def.dataspace.column_renames, inplace=True)
                return df

        raise ValueError("Could not determine data source from SystemDefinition")

__all__ = ["DataLoader", "PandasDataLoader", "GenericDataLoader"]