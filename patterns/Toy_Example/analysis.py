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
    
    print("DEBUG: Sampling data to 10%...")
    sample_df = session.raw_df.sample(frac=0.1, random_state=42)
    session.raw_df = sample_df
    session.experiments_df = session.experiments_df.loc[sample_df.index]
    session.outcomes_df = session.outcomes_df.loc[sample_df.index]

    # Group tradeoffs by scheme
    tradeoffs_by_scheme = {}
    for t in session.get_tradeoffs():
        tradeoffs_by_scheme.setdefault(t.scheme, []).append(t)

    all_results = {}

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
        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                # 1. Standard plot (with background)
                fig = session.show_quality_objective_space(
                    x_col, y_col, 
                    highlight_tradeoffs=tradeoffs,
                    show_overall=True
                )
                scatter_path = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}.png")
                fig.savefig(scatter_path)
                print(f"Scatter plot saved to: {scatter_path}")

                # 2. Focused plot (invisible background for scaling)
                fig_f = session.show_quality_objective_space(
                    x_col, y_col, 
                    highlight_tradeoffs=tradeoffs,
                    show_overall=False
                )
                scatter_path_f = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}_focused.png")
                fig_f.savefig(scatter_path_f)
                print(f"Focused scatter plot saved to: {scatter_path_f}")

                # 3. Rectangle plot (no point coloring, just bounding boxes)
                fig_r = session.show_quality_objective_space(
                    x_col, y_col, 
                    highlight_tradeoffs=tradeoffs,
                    show_overall=True,
                    color_points=False,
                    draw_rectangles=True
                )
                scatter_path_r = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}_rect.png")
                fig_r.savefig(scatter_path_r)
                print(f"Rectangle scatter plot saved to: {scatter_path_r}")
            except Exception as e:
                print(f"Error generating scatter plot for {x_col} vs {y_col}: {e}")

        # Generate Contingency Tables & Visualizations for each Decision
        print("\n--- Generating Contingency Analysis ---")
        decisions = session.get_decisions()
        for decision_key in decisions.keys():
            dec_name_clean = decision_key.replace(":", "_")
            print(f"Analyzing Decision: {decision_key}")
            
            try:
                # 1. Heatmap
                fig_h = session.show_policy_contingency(
                    decision_key, 
                    type='heatmap', 
                    normalization_mode='row',
                    title=f"Contingency: {decision_key} (Row Norm)"
                )
                path_h = os.path.join(outdir, f"contingency_heatmap_{dec_name_clean}.png")
                fig_h.savefig(path_h)
                print(f"  Heatmap saved to: {path_h}")
                
                # 2. Sankey
                fig_s = session.show_policy_contingency(
                    decision_key, 
                    type='sankey', 
                    normalization_mode='population',
                    title=f"Flow: {decision_key} -> Tradeoffs"
                )
                path_s = os.path.join(outdir, f"contingency_sankey_{dec_name_clean}.png")
                fig_s.savefig(path_s)
                print(f"  Sankey saved to: {path_s}")
                
            except Exception as e:
                print(f"  Error analyzing contingency for {decision_key}: {e}")

        # --- Feature Scoring ---
        print("\n--- Generating Feature Importance Analysis ---")
        try:
            # 1. Split Data (Stratified by the LAST scheme processed)
            session.split_data(test_size=0.2)

            # 2. Compute Scores
            scores_df = session.compute_feature_scores(
                include_levers=True,
                include_uncertainties=True,
                include_constraints=True,
                use_smart_correlation=True
            )

            # 3. Save Heatmap
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence: {scheme_name}")
            heatmap_path = os.path.join(outdir, f"feature_importance_{scheme_name}.png")
            fig_imp.savefig(heatmap_path)
            print(f"  Feature importance heatmap saved to: {heatmap_path}")

            # 4. Generate Weighted Ranking
            ranking = session.get_weighted_feature_ranking(scores_df)
            print(f"  Overall Feature Ranking (Equal Weights):")
            for i, feat in enumerate(ranking[:10]):
                print(f"    {i+1}. {feat}")

            # 5. Export scores to CSV
            scores_path = os.path.join(outdir, f"feature_scores_{scheme_name}.csv")
            scores_df.to_csv(scores_path)
            print(f"  Scores exported to: {scores_path}")

        except Exception as e:
            print(f"  Error during feature scoring: {e}")

        # --- Scenario Discovery ---
        print("\n--- Generating Scenario Discovery (PRIM) ---")
        for tradeoff in tradeoffs:
            print(f"  Discovering scenarios for Tradeoff: {tradeoff.name}")
            try:
                boxes = session.discover_scenarios(
                    tradeoff.name, 
                    method='prim', 
                    threshold=0.7, 
                    standardize=True
                )
                
                if boxes:
                    best_box = boxes[0]
                    print(f"    Best Box Metrics (Test Set): {best_box.metrics}")
                    print(f"    Key Rules (Method: {best_box.method}):")
                    for p, lims in best_box.limits.items():
                        print(f"      {p}: {lims['min']:.2f} to {lims['max']:.2f}")
                    
                    # Optional: Export boxes to JSON
                    box_path = os.path.join(outdir, f"discovery_{tradeoff.name.replace(' ', '_')}.json")
                    with open(box_path, 'w') as f:
                        json.dump(best_box.model_dump(), f, indent=2)
                else:
                    print(f"    No significant boxes discovered.")
                    
            except Exception as e:
                print(f"    Error during discovery for {tradeoff.name}: {e}")

    # 4. Global Discovery (CART)
    print("\n--- Generating Scenario Discovery (CART - All Tradeoffs) ---")
    try:
        # CART runs on all unique label combinations at once
        boxes_cart = session.discover_scenarios(
            method='cart', 
            standardize=False
        )
        
        for box in boxes_cart:
            # Only print boxes that have some decent targets or are known tradeoffs
            if box.metrics.get('targets_in_box', 0) > 10:
                print(f"  Box for {box.target_tradeoff} (Method: {box.method}):")
                print(f"    Metrics (Test Set): {box.metrics}")
                print(f"    Rules:")
                for p, lims in box.limits.items():
                    print(f"      {p}: {lims['min']:.2f} to {lims['max']:.2f}")

    except Exception as e:
        print(f"  Error during global CART discovery: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="patterns/Toy_Example/ArchExample_Discretization.json")
    parser.add_argument("--outdir", default="patterns/Toy_Example/out")
    parser.add_argument("--no-validate", action="store_true", help="Disable data integrity validation")
    args = parser.parse_args()
    
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()