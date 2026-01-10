"""
"""
import argparse
import os
import json
from adept import PatternAnalysis

def run_analysis(json_path: str, outdir: str, validate_integrity: bool = True) -> None:
    os.makedirs(outdir, exist_ok=True)
    
    # 1. Initialize Analysis Session
    print(f"Initializing analysis session for: {json_path}")
    session = PatternAnalysis(json_path)
    
    # 2. Load
    session.load(validate_integrity=validate_integrity)
    
    print("DEBUG: Sampling data to 1%...")
    sample_df = session.raw_df.sample(frac=0.01, random_state=42)
    session.raw_df = sample_df
    session.experiments_df = session.experiments_df.loc[sample_df.index]
    session.outcomes_df = session.outcomes_df.loc[sample_df.index]

    # Group tradeoffs by scheme
    tradeoffs_by_scheme = {}
    for t in session.sys_def.system.tradeoffs:
        tradeoffs_by_scheme.setdefault(t.scheme, []).append(t)

    all_results = {}

    for scheme_name, tradeoffs in tradeoffs_by_scheme.items():
        print(f"\n--- Processing Scheme: {scheme_name} ---")
        
        # 3. Define Tradeoffs
        if scheme_name == 'discretization':
            target_labels = {qa.name: ['low', 'avg', 'high'] for qa in session.sys_def.dataspace.quality_objectives}
            discrete_df, schemes = session.define_tradeoffs(n_bins=3, labels=target_labels, method='discretization')
        elif scheme_name == 'pareto' or scheme_name == 'pareto_nadir':
            discrete_df, schemes = session.define_tradeoffs(method='pareto')
        elif scheme_name == 'threshold':
            # Extract params from the first tradeoff of this scheme
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='threshold', params=params)
        elif scheme_name == 'pareto_epsilon':
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='pareto_epsilon', params=params)
        elif scheme_name == 'pareto_knee':
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='pareto_knee', params=params)
        else:
            print(f"Skipping unknown scheme: {scheme_name}")
            continue

        print("Schemes defined:")
        for scheme in schemes:
            print(f"  Objective: {scheme.objective_name}")
            for b in scheme.bins:
                print(f"    Label: {b.label} -> Range: [{b.min_value:.2f}, {b.max_value:.2f}]")

        # Generate Distribution Plots for each tradeoff in this scheme
        for tradeoff in tradeoffs:
            try:
                indices = session.get_indices_for_tradeoff(tradeoff)
                fig = session.coordinator.plot_distributions(
                    session.outcomes_df, 
                    schemes, 
                    tradeoff=tradeoff,
                    highlight_indices=indices
                )
                plot_path = os.path.join(outdir, f"distribution_{tradeoff.name}.png")
                fig.savefig(plot_path)
                print(f"Distribution plot saved to: {plot_path} (Highlighting {len(indices)} points)")
            except Exception as e:
                print(f"Error generating plot for {tradeoff.name}: {e}")

        # Generate 2D Scatter Plots for all pairs of outcomes
        import itertools
        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                # Standard plot (with background)
                fig = session.show_quality_objective_space(
                    x_col, y_col, 
                    highlight_tradeoffs=tradeoffs,
                    show_overall=True
                )
                scatter_path = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}.png")
                fig.savefig(scatter_path)
                print(f"Scatter plot saved to: {scatter_path}")
            except Exception as e:
                print(f"Error generating scatter plot for {x_col} vs {y_col}: {e}")

        # 4. Discover
        print(f"Discovering scenarios for {len(tradeoffs)} tradeoffs...")
        # Only discover for the current batch of tradeoffs
        # We manually call discover for each because discover_tradeoffs iterates ALL tradeoffs
        for tradeoff in tradeoffs:
            print(f"  Analyzing Tradeoff: {tradeoff.name} ({tradeoff.description})")
            try:
                box, limits, alg = session.coordinator.discover_scenarios(
                    session.experiments_df, 
                    'cost',
                    method='prim',
                    tradeoff=tradeoff,
                    discrete_outcomes_df=discrete_df,
                    outcomes_df=session.outcomes_df
                )
                print(f"    Discovered Limits: {limits}")
                all_results[f"tradeoff_{tradeoff.name}"] = limits
            except Exception as e:
                print(f"    Error analyzing {tradeoff.name}: {e}")
                all_results[f"tradeoff_{tradeoff.name}_error"] = str(e)

    # 5. Export
    results_path = os.path.join(outdir, "analysis_results.json")
    with open(results_path, "w") as fh:
        json.dump({
            "system": session.sys_def.system.name,
            "tradeoffs": all_results
        }, fh, indent=2, default=str)
    
    if session.pareto_front is not None:
        pareto_path = os.path.join(outdir, "pareto_front.csv")
        session.pareto_front.to_csv(pareto_path, index=False)
        print(f"Pareto front exported to: {pareto_path}")
    
    print(f"\nResults exported to: {results_path}")

def main():
    parser = argparse.ArgumentParser()
    # Default to the local ArchExample_Discretization.json
    parser.add_argument("--config", default="patterns/Toy_Example/ArchExample_Discretization.json")
    parser.add_argument("--outdir", default="patterns/Toy_Example/out")
    parser.add_argument("--no-validate", action="store_true", help="Disable data integrity validation")
    args = parser.parse_args()
    
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()
