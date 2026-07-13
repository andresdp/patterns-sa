from abc import ABC, abstractmethod
from typing import Any, Tuple, Optional, List, Dict
import pandas as pd
import os
import glob
import warnings
import inspect
from .models import SystemDefinition, DataSpace, BehavioralTrace
from ..utils.linter import SystemLinter

class DataLoader(ABC):
    """Abstract base class for data loaders.
    
    A DataLoader's responsibility is to bridge the gap between external 
    storage (CSV, SQL, etc.) and internal pandas-based analysis engine.
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
    1. Locate data files (relative to JSON or absolute).
    2. Merge data from multiple policy files if necessary.
    3. Rename columns to align with internal framework expectations.
    4. Automatically split data into 'experiments' (parameters) and 
       'outcomes' (objectives) based on the architectural model.
    5. Inject parameter values from pattern definitions based on configuration IDs.
    """
    def load(self, source: Any, validate_integrity: bool = True, preprocessor: Optional[callable] = None) -> pd.DataFrame:
        """
        Loads data based on a system definition JSON file.
        
        Args:
            source: Path to system definition JSON file.
            validate_integrity: Whether to run SystemLinter.
            preprocessor: Optional function(df) -> df to apply custom transformations immediately after loading.
        
        Returns:
            The raw, combined DataFrame after renames and parameter injection.
        """
        sys_def = self.load_system_definition(source)
        df = self._load_from_definition(sys_def, base_path=os.path.dirname(source), preprocessor=preprocessor)
        
        # Inject parameter bindings from pattern policies
        df = self._apply_parameter_bindings(sys_def, df)
        
        if validate_integrity:
            self.validate_data_integrity(sys_def, df)
        return df

    def load_system_definition(self, json_path: str) -> SystemDefinition:
        """Parses a system.json file into a SystemDefinition model."""
        return SystemDefinition.from_json(json_path)

    def validate_data_integrity(self, sys_def: SystemDefinition, df: pd.DataFrame) -> None:
        """Runs SystemLinter to check consistency between JSON and Data."""
        linter = SystemLinter()
        issues = linter.lint(sys_def, df)
        if not issues:
            print("Data integrity validation passed successfully.")
        for issue in issues:
            if issue.level == "ERROR":
                warnings.warn(str(issue))
            else:
                print(str(issue))

    def report_nan_proportions(self, df: pd.DataFrame, label: str = "Dataset") -> Dict[str, float]:
        """Calculates and prints the proportion of NaN values in the DataFrame."""
        if df is None or df.empty:
            return {}
        
        total_cells = df.size
        total_nans = df.isnull().sum().sum()
        overall_prop = (total_nans / total_cells) * 100 if total_cells > 0 else 0
        
        print(f"\n--- NaN Proportion Report: {label} ---")
        print(f"Overall NaN proportion: {overall_prop:.2f}% ({total_nans}/{total_cells} cells)")
        
        col_nans = df.isnull().sum()
        high_nan_cols = col_nans[col_nans > 0]
        
        if not high_nan_cols.empty:
            print("Columns with NaNs:")
            for col, count in high_nan_cols.items():
                prop = (count / len(df)) * 100
                print(f"  - {col}: {prop:.2f}% ({count}/{len(df)} rows)")
        
        return {"overall": overall_prop, "columns": (col_nans / len(df)).to_dict()}

    def load_data(self, source: Any, validate_integrity: bool = True, preprocessor: Optional[callable] = None) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
        """
        Loads data and automatically partitions it based on the architectural model.
        
        Args:
            source: Path to system definition JSON file.
            validate_integrity: Whether to run validation.
            preprocessor: Optional transformation function.
            
        Returns:
            A tuple of (raw_df, experiments_df, outcomes_df).
        """
        sys_def = self.load_system_definition(source)
        df = self._load_from_definition(sys_def, base_path=os.path.dirname(source), preprocessor=preprocessor)
        
        # Inject parameter bindings from pattern policies
        df = self._apply_parameter_bindings(sys_def, df)
        
        if validate_integrity:
            self.validate_data_integrity(sys_def, df)
        
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
        if sys_def.dataspace.configuration_identification.column:
             col = sys_def.dataspace.configuration_identification.column
             if col in df.columns:
                 experiments_cols.append(col)

        experiments_df = df[experiments_cols].copy() if experiments_cols else pd.DataFrame()
        outcomes_df = df[outcomes_cols].copy() if outcomes_cols else pd.DataFrame()

        # Report NaNs
        self.report_nan_proportions(experiments_df, label="Experiments")
        self.report_nan_proportions(outcomes_df, label="Outcomes")
        
        return df, experiments_df, outcomes_df

    def load_behavioral_traces(self, source: str) -> List[BehavioralTrace]:
        """
        Loads behavioral traces from the directory specified in the system definition.
        
        Traces represent cycle-by-cycle performance of adaptive processes.
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
        # Assume traces are CSV files in directory, named by scenario_id
        for filepath in glob.glob(os.path.join(traces_path, "*.csv")):
            scenario_id = os.path.splitext(os.path.basename(filepath))[0]
            df = pd.read_csv(filepath)
            traces.append(BehavioralTrace(
                trace_id=scenario_id,
                scenario_id=scenario_id,
                outcomes=df
            ))
            
        return traces

    def _apply_parameter_bindings(self, sys_def: SystemDefinition, df: pd.DataFrame) -> pd.DataFrame:
        """Injects parameter values from Pattern Policies into the DataFrame based on configuration ID."""
        ident = sys_def.dataspace.configuration_identification
        if not ident.column or ident.column not in df.columns:
            return df 

        config_param_map = {}
        
        # Helper to process a single configuration
        def process_config(config_obj):
            bindings = {}
            for ref in config_obj.pattern_policy_references:
                # Find component
                comp = sys_def.system.components.get(ref.component)
                if not comp: continue
                
                # Find decision
                decision = comp.decisions.get(ref.decision)
                if not decision: continue
                
                # Find policy
                policy = decision.policies.get(ref.policy)
                if not policy: continue
                
                # Extract bindings for all types
                for p_type in ["levers", "uncertainties", "constraints"]:
                    p_dict = getattr(policy.parameter_bindings, p_type, {})
                    for p_name, p_val in p_dict.items():
                        bindings[p_name] = p_val
            return bindings

        if isinstance(ident.configurations, dict):
            for cfg_id, cfg_obj in ident.configurations.items():
                config_param_map[cfg_id] = process_config(cfg_obj)
        elif isinstance(ident.configurations, list):
             # For file-based loading, we might need a different approach or mapping
             # Assuming 'name' matches identification column value or similar logic
             # This part might need adaptation if 'from: file' uses names differently
             for cfg_obj in ident.configurations:
                 # Assuming config object name is the key if we are mapping
                 # But usually file loading is separate. 
                 # If from='column' but configs are a list, we might assume 'name' is the key
                 config_param_map[cfg_obj.name] = process_config(cfg_obj)

        
        # 1. Identify all parameters implicated
        all_params = set()
        for p_map in config_param_map.values():
            all_params.update(p_map.keys())
            
        # 2. For each parameter, create/update column
        for param in all_params:
            # Filter out wildcards/None from the value mapping
            val_map = {}
            for cid, props in config_param_map.items():
                val = props.get(param)
                if val is not None and val != "*":
                    val_map[cid] = val
            
            if not val_map: continue
            
            # Map values based on identification column
            mapped_values = df[ident.column].astype(str).map(val_map)
            
            if param not in df.columns:
                # If column doesn't exist, we can only inject where we have values
                # (Remaining will be NaN, which is appropriate for 'dynamic' values)
                df[param] = mapped_values
            else:
                # Overwrite existing values where mapping exists (JSON is source of truth)
                # mask() applies to change where condition is True.
                # mapped_values.notna() correctly identifies where we have an explicit override.
                df[param] = df[param].mask(mapped_values.notna(), mapped_values)
                
        return df

    def _load_from_definition(self, sys_def: SystemDefinition, base_path: str, preprocessor: Optional[callable] = None) -> pd.DataFrame:
        """Internal helper to resolve file paths and perform renames/preprocessing."""
        df = None
        
        # Helper to apply preprocessor with backward compatibility
        def _apply_pp(dataframe, conf_name=None):
            if not preprocessor:
                return dataframe
            
            # Check if preprocessor accepts 'config_name'
            sig = inspect.signature(preprocessor)
            params = sig.parameters
            # Look for 2nd arg or **kwargs
            accepts_config = (len(params) >= 2) or any(p.kind == inspect.Parameter.VAR_KEYWORD for p in params.values())
            
            if accepts_config:
                return preprocessor(dataframe, config_name=conf_name)
            else:
                return preprocessor(dataframe)

        # --- MOMENT 1: Loading individual files ---
        if sys_def.dataspace.source_file:
            path = sys_def.dataspace.source_file
            if not os.path.isabs(path):
                path = os.path.join(base_path, path)
            
            print(f"Loading single source file: {path}")
            
            # Check for CSV delimiter in discovery options
            csv_args = {}
            if hasattr(sys_def.dataspace, 'discovery_options') and sys_def.dataspace.discovery_options:
                if hasattr(sys_def.dataspace.discovery_options, 'csv_delimiter'):
                    csv_args['sep'] = sys_def.dataspace.discovery_options.csv_delimiter
                    print(f"Using CSV delimiter: '{csv_args['sep']}'")
            
            df = pd.read_csv(path, **csv_args)
            print(f"Loaded {len(df)} rows.")
            
            # Apply hook immediately
            if preprocessor:
                print("Applying preprocessor hook to single file...")
                df = _apply_pp(df, conf_name=None)
            
        elif sys_def.dataspace.configuration_identification.from_ == "file":
            dfs = []
            configs = sys_def.dataspace.configuration_identification.configurations
            config_list = configs if isinstance(configs, list) else list(configs.values())
            
            for config in config_list:
                if config.source_file:
                    path = config.source_file
                    if not os.path.isabs(path):
                        path = os.path.join(base_path, path)
                    
                    print(f"Loading configuration file ({config.name}): {path}")
                    try:
                        temp_df = pd.read_csv(path)
                        print(f"  -> Loaded {len(temp_df)} rows.")
                        
                        # Apply hook BEFORE merging
                        if preprocessor:
                            print(f"  -> Applying preprocessor to {config.name}...")
                            temp_df = _apply_pp(temp_df, conf_name=config.name)

                        # Inject configuration name so mapping can work
                        # Note: We do this AFTER preprocessing in case user wants to rename columns first,
                        # but typically we want to ID there. 
                        # However, if preprocessor returns a new DF, we should ensure to ID persists.
                        # Let's inject it AGAIN to be safe, or check.
                        col_name = sys_def.dataspace.configuration_identification.column or 'policy'
                        if col_name not in temp_df.columns:
                             temp_df[col_name] = config.name
                        
                        dfs.append(temp_df)
                    except FileNotFoundError:
                        warnings.warn(f"File not found: {path}")
            
            # --- MOMENT 2: Merging (Concatenation) ---
            if dfs:
                df = pd.concat(dfs, ignore_index=True)
                print(f"Merged {len(dfs)} files into dataframe with shape: {df.shape}")

        if df is None:
            raise ValueError("Could not determine data source from SystemDefinition")

        # --- MOMENT 3: Final Declarative Steps ---
        # (Preprocessor removed from here as it is now applied per-file)

        # 2. Apply declarative column renames (if not handled by preprocessor)
        if sys_def.dataspace.column_renames:
            df.rename(columns=sys_def.dataspace.column_renames, inplace=True)
            
        return df

__all__ = ["DataLoader", "PandasDataLoader", "GenericDataLoader"]