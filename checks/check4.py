from adept.core.coordinator import ArchSpaceCore
import pandas as pd

# 1. Initialize the coordinator
core = ArchSpaceCore()
# 1. Initialize the coordinator
core = ArchSpaceCore()

# 2. Create sample continuous data
df = pd.DataFrame({
   'L1': [0.1, 0.2, 0.3, 0.4, 0.5, 0.6], # Levers
   'Q1': [10, 20, 30, 40, 50, 60]  # Quality Outcome
 })

# 3. Verify formal Discretization Schemes
# We map Q1 to ['bad', 'good']
labels = {'Q1': ['bad', 'good']}
discrete_df, schemes = core.discretize(df, n_bins=2, all_labels=labels)

print("--- Discretization Schemes ---")
for scheme in schemes:
    print(f"Objective: {scheme.objective_name}")
    for b in scheme.bins:
        print(f"  Label: {b.label} -> Range: [{b.min_value:.2f}, {b.max_value:.2f}]")

# 4. Verify Discretization-based Scenario Discovery
# We want to find which L1 values lead to the 'good' bin
target_spec = {
    'paradigm': 'discretization',
    'target_bin': 'good'
}

# Run discovery targeting the 'good' categorical bin
box, limits, alg = core.discover_scenarios(
    df, 
    outcome='Q1', 
    target_spec=target_spec, 
    discrete_outcomes_df=discrete_df
)

print("\n--- Discovered Scenario for 'good' outcomes ---")
print(f"Parameter Limits: {limits}")