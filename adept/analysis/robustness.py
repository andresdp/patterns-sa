from typing import Optional, Tuple
import pandas as pd
import warnings
from .discretization import DataProcessor


class RobustnessAnalyzer:
    """Calculates quantitative robustness metrics for architectural designs.
    
    In the ADEPT framework, robustness is initially quantified as the 
    conditional probability of achieving a target 'tradeoff' (set of outcome bins) 
    given a specific system configuration.
    """

    def compute_robustness(self, discrete_outcomes_df: pd.DataFrame, qa_tradeoff: Optional[str] = None) -> Tuple[float, str]:
        """
        Computes the robustness of a set of outcomes.
        
        Robustness is calculated as: (count of target tradeoff) / (total scenarios).
        
        Args:
            discrete_outcomes_df: DataFrame of outcomes after discretization.
            qa_tradeoff: The target tradeoff label (e.g., 'fast,high'). 
                         If None, the most frequent tradeoff in the set is used.
                         
        Returns:
            A tuple of (robustness_value [0-1], tradeoff_label).
        """
        if discrete_outcomes_df is None or discrete_outcomes_df.empty:
            warnings.warn("Discrete outcomes DataFrame is empty or None.")
            return 0.0, ""

        local_tradeoffs = DataProcessor.get_tradeoffs(discrete_outcomes_df)

        if qa_tradeoff is None:
            # Auto-select the 'best' (most frequent) available tradeoff
            most_common = local_tradeoffs.most_common(1)
            if not most_common:
                return 0.0, ""
            qa_tradeoff_val = most_common[0]
            reference_tradeoff = qa_tradeoff_val[0]
            count = qa_tradeoff_val[1]
        else:
            reference_tradeoff = qa_tradeoff
            count = local_tradeoffs[qa_tradeoff]
        
        total = local_tradeoffs.total()
        if total == 0:
            return 0.0, reference_tradeoff

        # Simple robustness: density of the target tradeoff in outcome space
        r = count / total
        return r, reference_tradeoff