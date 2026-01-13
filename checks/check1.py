from archspaces.core import ArchSpaceCore
import pandas as pd

# Initialize coordinator

core = ArchSpaceCore()

# Create sample data
df = pd.DataFrame({'R': [0.1, 0.5, 0.9], 'U': [0.2, 0.6, 0.8]})

# Verify DataProcessor delegation
labels = {'R': ['fast', 'avg', 'slow'],'U': ['low', 'avg', 'high']}
discrete_df, tradeoffs = core.discretize(df, n_bins=3, all_labels=labels)
print("Tradeoffs discovered:", tradeoffs)

# Verify RobustnessAnalyzer delegation
robustness, label = core.compute_robustness(discrete_df)
print(f"Robustness: {robustness} for tradeoff: {label}")