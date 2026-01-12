from typing import Dict, Any, Optional
import pandas as pd
import numpy as np

class RobustnessAnalyzer:
    """
    Calculates quantitative robustness metrics for architectural designs.
    
    Supported Metrics:
    - 'starr': Success rate (fraction of scenarios hitting the target).
    - 'regret': Standardized Euclidean distance from the target tradeoff.
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
