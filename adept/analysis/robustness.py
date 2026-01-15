from typing import Dict, Any, Optional, List
import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from scipy.spatial import distance

class RobustnessAnalyzer:
    """
    Calculates quantitative robustness metrics for architectural designs.
    
    Supported Metrics:
    - 'starr': Success rate (fraction of scenarios hitting the target).
    - 'regret': Standardized Euclidean distance from the target tradeoff.
    - 'stability_radius': Minimum distance from parameter centroid to the nearest failure mode.
    """

    @staticmethod
    def compute_starr(is_target_mask: pd.Series) -> Dict[str, Any]:
        """
        Calculates Starr's Domain Criterion (Success Rate).
        """
        total = len(is_target_mask)
        successes = is_target_mask.sum()
        score = float(successes / total) if total > 0 else 0.0
        
        return {
            'metric': 'starr',
            'value': score,
            'details': {
                'success_count': int(successes),
                'total_count': total
            }
        }

    @staticmethod
    def compute_regret(
        outcomes_df: pd.DataFrame, 
        is_target_mask: pd.Series, 
        boundaries: Dict[str, Dict[str, float]], 
        stats: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Calculates the Regret metric based on standardized distance to the target boundaries.
        
        Distance is 0 for scenarios that satisfy the tradeoff.
        For others, we calculate the standardized Euclidean distance to the nearest boundary.
        """
        if outcomes_df.empty:
            return {'metric': 'regret', 'value': 0.0, 'details': {}}

        # 1. Identify failing scenarios
        # We compute regret for ALL, but it's 0 for successes
        failing_mask = ~is_target_mask
        
        # 2. Calculate Slack (distance to boundary) per objective
        # slack = max(0, val - max, min - val)
        slack_df = pd.DataFrame(index=outcomes_df.index)
        
        for qa, limits in boundaries.items():
            if qa not in outcomes_df.columns:
                continue
                
            col = outcomes_df[qa]
            q_min = limits.get('min', -np.inf)
            q_max = limits.get('max', np.inf)
            
            # Distance to boundaries
            d_max = (col - q_max).clip(lower=0)
            d_min = (q_min - col).clip(lower=0)
            slack_df[qa] = d_max + d_min

        # 3. Standardize Slack (Strategy 1: Z-Score)
        # We use standard deviations from the provided stats
        if stats and 'scaler' in stats:
            scaler = stats['scaler']
            # Map QA names to their positions in the scaler
            qa_cols = stats.get('numeric_cols', outcomes_df.columns.tolist())
            stds = dict(zip(qa_cols, scaler.scale_))
            
            for qa in slack_df.columns:
                std = stds.get(qa, 1.0)
                if std > 0:
                    slack_df[qa] = slack_df[qa] / std

        # 4. Compute Euclidean Distance per Scenario
        distances = np.sqrt((slack_df**2).sum(axis=1))
        
        # 5. Aggregate Results
        # Regret is usually 0 for successful scenarios
        # We can report mean over failing, or mean over all. 
        # Standard approach: Mean regret over all scenarios.
        mean_regret = float(distances.mean())
        max_regret = float(distances.max())
        
        # Detailed objective-wise average regret when failing
        obj_regret = {}
        if failing_mask.any():
            obj_regret = slack_df[failing_mask].mean().to_dict()

        return {
            'metric': 'regret',
            'value': mean_regret,
            'details': {
                'max_regret': max_regret,
                'avg_regret_failing': float(distances[failing_mask].mean()) if failing_mask.any() else 0.0,
                'objective_regret_contribution': obj_regret
            }
        }

    @staticmethod
    def compute_stability_radius(
        experiments_df: pd.DataFrame,
        is_target_mask: pd.Series,
        parameter_cols: List[str],
        distance_metric: str = 'euclidean',
        baseline: Optional[Dict[str, float]] = None
    ) -> Dict[str, Any]:
        """
        Calculates the minimum distance from the parameter centroid to the nearest failure mode.
        
        A 'failure' is defined as any point where is_target_mask is False.
        Distances are calculated in the normalized (MinMax) parameter space.
        
        Args:
            experiments_df: DataFrame of input parameters (rows filtered for specific policy).
            is_target_mask: Boolean Series where True = Success, False = Failure.
            parameter_cols: List of column names to include in the distance calculation.
            distance_metric: 'euclidean' (default) or 'cosine'.
            baseline: Optional dict defining the nominal point {param: value}.
                      If None, uses the centroid of the experiments_df.
            
        Returns:
            Dict with 'value' (radius), 'baseline' (coordinates), and 'nearest_failure'.
        """
        if experiments_df.empty:
            return {'metric': 'stability_radius', 'value': 0.0, 'details': {}}

        # 1. Prepare and Normalize Data
        # Filter to numeric parameter columns provided
        X = experiments_df[parameter_cols].select_dtypes(include=[np.number])
        if X.empty:
             return {'metric': 'stability_radius', 'value': 0.0, 'details': 'No numeric parameters found'}

        scaler = MinMaxScaler()
        X_norm_arr = scaler.fit_transform(X)
        X_norm = pd.DataFrame(X_norm_arr, index=X.index, columns=X.columns)

        # 2. Determine Baseline
        if baseline is not None:
            # Validate and Normalize user baseline
            # Order must match X columns
            try:
                base_vector = np.array([baseline[col] for col in X.columns]).reshape(1, -1)
                baseline_norm = scaler.transform(base_vector)
            except KeyError as e:
                raise ValueError(f"Baseline dict missing parameter: {e}")
        else:
            # Default: Centroid of normalized space
            baseline_norm = X_norm.mean().values.reshape(1, -1)

        # 3. Identify Failure Modes
        failing_indices = is_target_mask[~is_target_mask].index
        
        if len(failing_indices) == 0:
            # If no failures, the radius is theoretically infinite within the sampled space.
            # We return the distance to the farthest corner of the [0,1]^N hypercube as a proxy.
            # Max possible Euclidean distance in unit hypercube is sqrt(N).
            max_val = np.sqrt(len(parameter_cols)) if distance_metric == 'euclidean' else 2.0
            
            # Use original scale for reporting if possible, or normalized
            display_baseline = baseline if baseline else X.mean().to_dict()
            
            return {
                'metric': 'stability_radius',
                'value': float(max_val),
                'details': {
                    'status': 'no_failures',
                    'baseline': display_baseline
                }
            }

        X_failures = X_norm.loc[failing_indices].values

        # 4. Compute Distances from Baseline to Failures
        if distance_metric == 'cosine':
            # Cosine distance = 1 - cosine_similarity
            dists = distance.cdist(baseline_norm, X_failures, metric='cosine').flatten()
        else:
            # Default Euclidean
            dists = distance.cdist(baseline_norm, X_failures, metric='euclidean').flatten()

        # 5. Determine Radius
        min_dist_idx = np.argmin(dists)
        stability_radius = dists[min_dist_idx]
        
        # Details about the nearest failure
        nearest_fail_idx = failing_indices[min_dist_idx]
        nearest_fail_params = experiments_df.loc[nearest_fail_idx, parameter_cols].to_dict()
        
        display_baseline = baseline if baseline else X.mean().to_dict()

        return {
            'metric': 'stability_radius',
            'value': float(stability_radius),
            'details': {
                'distance_metric': distance_metric,
                'baseline': display_baseline,
                'normalized_baseline': baseline_norm.flatten().tolist(),
                'nearest_failure_index': int(nearest_fail_idx),
                'nearest_failure_parameters': nearest_fail_params
            }
        }
