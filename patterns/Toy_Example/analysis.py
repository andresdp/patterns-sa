"""ADEPT analysis for the Toy Example.

This script demonstrates the use of the ADEPT framework to:
1. Load a system definition and its associated data.
2. Perform discretization of outcomes.
3. Discover scenarios for a first-class Tradeoff entity.
"""
import argparse
import os
import json
import pandas as pd
from adept.core.coordinator import ArchSpaceCore

def run_analysis(json_path: str, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)
    
    # 1. Initialize ADEPT Coordinator
    core = ArchSpaceCore()
    
    print(f"Loading system definition from: {json_path}")
    # 2. Load metadata-driven data
    df, experiments_df, outcomes_df = core.loader.load_data(json_path)
    sys_def = core.loader.load_system_definition(json_path)
    
    # 3. Discretize Outcomes
    # Map objectives to 3 bins (low, avg, high)
    labels = {qa.name: ['low', 'avg', 'high'] for qa in sys_def.dataspace.quality_objectives}
    discrete_df, schemes = core.discretize(outcomes_df, n_bins=3, all_labels=labels)
    
    print("\n--- Discretization Schemes ---")
    for scheme in schemes:
        print(f"Objective: {scheme.objective_name}")
        for b in scheme.bins:
            print(f"  Label: {b.label} -> Range: [{b.min_value:.2f}, {b.max_value:.2f}]")

    # 4. Perform Scenario Discovery for each defined Tradeoff
    artifacts = {}
    print("\n--- Scenario Discovery ---")
    for tradeoff in sys_def.system.tradeoffs:
        print(f"Analyzing Tradeoff: {tradeoff.name} ({tradeoff.description})")
        try:
            # We pass the outcome name for PRIM initialization, 
            # but the tradeoff object now defines the ROI mask internally in Manager
            box, limits, alg = core.discover_scenarios(
                experiments_df,
                'cost', # Pass as positional
                method='prim',
                tradeoff=tradeoff,
                discrete_outcomes_df=discrete_df
            )
            print(f"  Discovered Limits: {limits}")
            artifacts[f"tradeoff_{tradeoff.name}"] = limits
        except Exception as e:
            print(f"  Error analyzing {tradeoff.name}: {e}")

    # 5. Export results
    results_path = os.path.join(outdir, "analysis_results.json")
    with open(results_path, "w") as fh:
        json.dump({
            "system": sys_def.system.name,
            "tradeoffs": artifacts
        }, fh, indent=2, default=str)
    
    print(f"\nResults exported to: {results_path}")

def main():
    parser = argparse.ArgumentParser()
    # Default to the local ToyExample.json
    parser.add_argument("--config", default="patterns/Toy_Example/ToyExample.json")
    parser.add_argument("--outdir", default="patterns/Toy_Example/out")
    args = parser.parse_args()
    
    run_analysis(args.config, args.outdir)

if __name__ == "__main__":
    main()

