# Future Feature Note: Policy Variability Diagnosis

**Status:** Proposed / Concept
**Goal:** Explain why a single architectural policy exhibits performance variability ("drift") across different tradeoff regions.

## The Problem
Ideally, an architectural policy (a fixed set of structural decisions) should map deterministically to a single performance outcome (e.g., "Always Fast").

In reality, a Policy often maps to multiple outcomes (e.g., 60% "Fast", 40% "Slow"). This **Variability** has two root causes:
1.  **Loose Design (Levers)**: The policy leaves certain numerical design parameters open (e.g., "Cache Size" is allowed to range from 10MB to 100MB).
2.  **Lack of Robustness (Uncertainties)**: The policy is sensitive to external factors (e.g., "Arrival Rate").

## Proposed Solution: `diagnose_policy_variability()`

We propose a method that isolates the data for a single policy and performs **Local Sensitivity Analysis** to identify the "Culprits" of variance.

### Method Signature
```python
def diagnose_policy_variability(self, policy_name: str, outcome: str) -> Dict[str, Any]:
    """
    Diagnoses the drivers of variance for a specific policy.    
    Returns:
        report: {
            'variability_type': 'Design-Induced' | 'Environment-Induced' | 'Mixed',
            'top_culprits': [('arrival_rate', 0.45, 'uncertainty'), ('buffer_size', 0.12, 'lever')]
        }
    """
```

### Algorithm Steps
1.  **Filter**: Isolate `experiments_df` and `outcomes_df` where `policy == policy_name`.
2.  **Verify Variance**: Check if the target `outcome` actually varies significantly within this subset.
3.  **Local Feature Scoring**: Run `FeatureImportanceAnalyzer` (Random Forest) on this subset.
4.  **Classify Drivers**:
    *   Map the top-ranked parameters to their types defined in `SystemDefinition` (`ParameterType.LEVER` vs `ParameterType.UNCERTAINTY`).
5.  **Conclusion**:
    *   Dominance of **Levers** $\rightarrow$ Recommendation: "Tighten design constraints."
    *   Dominance of **Uncertainties** $\rightarrow$ Recommendation: "Improve robustness or change pattern."

## Visual Verification (Explainability)

Once the culprits are identified, we can visualize *how* they cause drift.

*   **Scatter Plot**: Simple X-Y plot of `Culprit` vs `Outcome` for the specific policy.
*   **ALE Plots (Accumulated Local Effects)**: A more advanced technique (for Phase 7) that isolates the marginal effect of the feature on the prediction, averaging out interactions. This formally confirms the causal link suggested by the feature importance score.
