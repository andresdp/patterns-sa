from typing import List, Dict, Any, Optional, Tuple, Union
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.base import clone
from feature_engine.selection import SmartCorrelatedSelection
from ..core.models import SystemDefinition, Tradeoff, ParameterType

from sklearn.preprocessing import StandardScaler

class FeatureImportanceAnalyzer:
    """
    Analyzes the influence of architectural parameters (levers/uncertainties) 
    on quality objectives (outcomes) using Machine Learning techniques.
    """

    def __init__(self, sys_def: SystemDefinition):
        self.sys_def = sys_def

    def get_parameter_columns(self, df: pd.DataFrame, include_levers: bool = True, include_uncertainties: bool = True, include_constraints: bool = True) -> List[str]:
        """Identifies columns in the dataframe that correspond to system parameters."""
        valid_cols = []
        
        # Helper to iterate components
        for comp in self.sys_def.system.components.values():
            for param in comp.parameters.values():
                is_lever = param.type == ParameterType.LEVER
                is_uncert = param.type == ParameterType.UNCERTAINTY
                is_constraint = param.type == ParameterType.CONSTRAINT
                
                if (is_lever and include_levers) or (is_uncert and include_uncertainties) or (is_constraint and include_constraints):
                    # Check for name or component_name format
                    if param.name in df.columns:
                        valid_cols.append(param.name)
                    # We might need to check for prefixed names if loader did that, 
                    # but usually loader canonicalizes to param.name if unique
        
        # Also check system-level parameters
        for param in self.sys_def.system.parameters.values():
             is_lever = param.type == ParameterType.LEVER
             is_uncert = param.type == ParameterType.UNCERTAINTY
             is_constraint = param.type == ParameterType.CONSTRAINT
             if (is_lever and include_levers) or (is_uncert and include_uncertainties) or (is_constraint and include_constraints):
                 if param.name in df.columns:
                     valid_cols.append(param.name)
                     
        return list(set(valid_cols))

    def create_stratified_split(
        self, 
        experiments_df: pd.DataFrame, 
        tradeoff_indices_map: Dict[str, np.ndarray], 
        test_size: float = 0.2, 
        random_state: int = 42
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Splits the data indices into train and test sets, stratifying based on tradeoff membership.
        
        Args:
            experiments_df: The dataframe defining the index.
            tradeoff_indices_map: Map of {tradeoff_name: [indices]}.
            test_size: Fraction of data to use for testing.
            
        Returns:
            (train_indices, test_indices)
        """
        # Create a stratification label for each row
        # 0 = No Tradeoff
        # 1..N = Tradeoff Index
        # -1 = Multiple Tradeoffs
        
        n_rows = len(experiments_df)
        labels = np.zeros(n_rows, dtype=int) # Default 0 (Non-compliant)
        
        # We assign integers to tradeoffs
        tradeoff_names = list(tradeoff_indices_map.keys())
        
        for i, name in enumerate(tradeoff_names):
            idx = tradeoff_indices_map[name]
            # If current label is 0, set to i+1
            # If current label is > 0, set to -1 (Multiple)
            # If current label is -1, stay -1
            
            # Vectorized update
            current_vals = labels[idx]
            
            # Mask for where it is 0
            is_zero = current_vals == 0
            labels[idx[is_zero]] = i + 1
            
            # Mask for where it is > 0 (already assigned)
            is_assigned = current_vals > 0
            labels[idx[is_assigned]] = -1
            
        # Perform split on indices
        indices = np.arange(n_rows)
        
        # Check if we have enough samples in each stratum
        # If a class has < 2 members, stratify will fail.
        # We fall back to random split if stratification is impossible.
        from collections import Counter
        counts = Counter(labels)
        if any(c < 2 for c in counts.values()):
            print("Warning: Some strata have too few samples. Falling back to non-stratified split.")
            train_idx, test_idx = train_test_split(indices, test_size=test_size, random_state=random_state)
        else:
            train_idx, test_idx = train_test_split(indices, test_size=test_size, stratify=labels, random_state=random_state)
            
        return train_idx, test_idx

    def preprocess_features(
        self, 
        df: pd.DataFrame, 
        standardize: bool = False, 
        remove_outliers: bool = False, 
        z_threshold: float = 3.0
    ) -> Tuple[pd.DataFrame, pd.Series, Dict[str, Any]]:
        """
        Preprocesses features by optionally standardizing and removing outliers.
        
        Args:
            df: Input feature dataframe.
            standardize: Whether to return Z-scores instead of raw values.
            remove_outliers: Whether to remove rows with any feature Z-score > threshold.
            z_threshold: Threshold for Z-score outlier detection.
            
        Returns:
            (processed_df, mask, stats): 
                - processed_df: The processed dataframe.
                - mask: Boolean mask of rows kept.
                - stats: Dict with 'scaler' for de-standardization.
        """
        # Ensure we work with numeric data
        numeric_cols = df.select_dtypes(include=[np.number]).columns
            
        # Initialize and fit scaler
        scaler = StandardScaler()
        z_scores_arr = scaler.fit_transform(df[numeric_cols])
        z_scores = pd.DataFrame(z_scores_arr, index=df.index, columns=numeric_cols)
        
        mask = pd.Series(True, index=df.index)
        
        if remove_outliers:
            # Identify outliers: any row where any feature |z| > threshold
            is_outlier = (z_scores.abs() > z_threshold).any(axis=1)
            mask = ~is_outlier
            
        # Construct result
        df_processed = df.copy()
        
        if standardize:
            # Replace numeric columns with their Z-scores
            df_processed[numeric_cols] = z_scores
            
        # Apply mask
        if remove_outliers:
            df_processed = df_processed[mask]
            
        stats = {
            'scaler': scaler,
            'standardized': standardize,
            'numeric_cols': numeric_cols.tolist()
        }
            
        return df_processed, mask, stats


    def compute_importance(
        self, 
        X_train: pd.DataFrame, 
        y_train: pd.Series, 
        use_smart_correlation: bool = False,
        random_state: int = 42
    ) -> pd.Series:
        """
        Computes feature importance scores for a single target.
        
        Args:
            X_train: Feature matrix (parameters).
            y_train: Target vector (outcome).
            use_smart_correlation: If True, uses feature-engine to drop correlated features first.
        
        Returns:
            pd.Series: Importance scores indexed by feature name.
        """
        # 1. Selection (Optional)
        features_to_use = X_train.columns.tolist()
        
        if use_smart_correlation:
            # SmartCorrelatedSelection groups correlated features and selects one.
            # We use 'variance' as selection method (default) or 'model_performance'
            # Here we use model_performance with a Regressor to pick the most predictive one.
            estimator = RandomForestRegressor(n_estimators=10, random_state=random_state)
            sel = SmartCorrelatedSelection(
                variables=None,
                method="spearman",
                threshold=0.8,
                missing_values="ignore",
                selection_method="model_performance",
                estimator=estimator
            )
            sel.fit(X_train, y_train)
            features_to_use = sel.features_to_drop_
            # Wait, features_to_drop_ are the ones to drop.
            # We want the ones to keep.
            # feature-engine transforms X.
            X_train_transformed = sel.transform(X_train)
            features_to_use = X_train_transformed.columns.tolist()
        else:
            X_train_transformed = X_train

        # 2. Scoring (Random Forest)
        model = RandomForestRegressor(n_estimators=50, random_state=random_state)
        model.fit(X_train_transformed, y_train)
        
        importances = pd.Series(model.feature_importances_, index=features_to_use)
        
        # Reindex to include dropped features (as 0) if any
        if use_smart_correlation:
            full_series = pd.Series(0.0, index=X_train.columns)
            full_series[features_to_use] = importances
            return full_series.sort_values(ascending=False)
            
        return importances.sort_values(ascending=False)
