import argparse
import os
import json
import itertools
from adept import PatternAnalysis

def run_analysis(json_path: str, outdir: str, validate_integrity: bool = True) -> None:
    os.makedirs(outdir, exist_ok=True)
    
    # 1. Initialize Analysis Session
    print(f"Initializing analysis session for: {json_path}")
    session = PatternAnalysis(json_path)
    
    # 2. Load
    session.load(validate_integrity=validate_integrity)
    
    # Group tradeoffs by scheme
    tradeoffs_by_scheme = {}
    for t in session.get_tradeoffs():
        tradeoffs_by_scheme.setdefault(t.scheme, []).append(t)

    for scheme_name, tradeoffs in tradeoffs_by_scheme.items():
        print(f"\n--- Processing Scheme: {scheme_name} ---")
        
        # 3. Define Tradeoffs
        if scheme_name == 'discretization':
            target_labels = {qa.name: ['low', 'avg', 'high'] for qa in session.get_outcomes()}
            discrete_df, schemes = session.define_tradeoffs(n_bins=3, labels=target_labels, method='discretization')
        elif scheme_name == 'pareto' or scheme_name == 'pareto_nadir':
            discrete_df, schemes = session.define_tradeoffs(method='pareto')
        elif scheme_name == 'threshold':
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='threshold', params=params)
        else:
            print(f"Skipping unknown scheme: {scheme_name}")
            continue

        # --- Data Split ---
        print("\n--- Splitting Data ---")
        session.split_data(test_size=0.2)

        # Generate Distribution Plots
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
                print(f"Distribution plot saved to: {plot_path}")
            except Exception as e:
                print(f"Error generating plot for {tradeoff.name}: {e}")

        # Generate 2D Scatter Plots
        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                fig = session.show_quality_objective_space(
                    x_col, y_col, 
                    highlight_tradeoffs=tradeoffs,
                    show_overall=True,
                    subset='all'
                )
                scatter_path = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}.png")
                fig.savefig(scatter_path)
                print(f"Scatter plot saved to: {scatter_path}")
            except Exception as e:
                print(f"Error generating scatter plot for {x_col} vs {y_col}: {e}")

        # --- Feature Scoring ---
        print("\n--- Generating Feature Importance Analysis ---")
        try:
            scores_df = session.compute_feature_scores(use_smart_correlation=True, subset='train')
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence (Train)")
            heatmap_path = os.path.join(outdir, f"feature_importance_{scheme_name}.png")
            fig_imp.savefig(heatmap_path)
            print(f"Feature importance heatmap saved to: {heatmap_path}")
        except Exception as e:
            print(f"Error during feature scoring: {e}")

        # --- Scenario Discovery (PRIM) ---
        print("\n--- Generating Scenario Discovery (PRIM) ---")
        for tradeoff in tradeoffs:
            print(f"  Discovering scenarios for Tradeoff: {tradeoff.name}")
            try:
                boxes = session.discover_scenarios(tradeoff.name, method='prim', threshold=0.7, standardize=True)
                if boxes:
                    box_path = os.path.join(outdir, f"discovery_{tradeoff.name.replace(' ', '_')}.json")
                    with open(box_path, 'w') as f:
                        json.dump(boxes[0].model_dump(), f, indent=2)
                    print(f"    Discovery results saved to: {box_path}")
            except Exception as e:
                print(f"    Error during discovery for {tradeoff.name}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="patterns/Gateway_Aggregation/Gateway_Aggregation.json")
    parser.add_argument("--outdir", default="patterns/Gateway_Aggregation/out")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()
