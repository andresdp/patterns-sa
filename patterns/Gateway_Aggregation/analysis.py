import argparse
import os
import json
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from adept import PatternAnalysis

def run_analysis(json_path: str, outdir: str, validate_integrity: bool = True) -> None:
    os.makedirs(outdir, exist_ok=True)
    
    # 1. Initialize Analysis Session
    print(f"Initializing analysis session for: {json_path}")
    session = PatternAnalysis(json_path)
    
    # 2. Load
    session.load(validate_integrity=validate_integrity)
    
    # 3. Check for programmatic tradeoffs if none defined in JSON
    if not session.get_tradeoffs():
        print("No tradeoffs defined in JSON. Defining programmatically...")
        session.add_tradeoff(
            name="performance-optimized",
            elements={"response_time": "fast", "utilization": "average"},
            scheme="discretization"
        )
        session.add_tradeoff(
            name="balanced",
            elements={"response_time": "average", "utilization": "average"},
            scheme="discretization"
        )

    # Group tradeoffs by scheme
    tradeoffs_by_scheme = {}
    for t in session.get_tradeoffs():
        tradeoffs_by_scheme.setdefault(t.scheme, []).append(t)

    for scheme_name, tradeoffs in tradeoffs_by_scheme.items():
        print(f"\n--- Processing Scheme: {scheme_name} ---")
        
        # 3. Define Tradeoffs
        if scheme_name == 'discretization':
            target_labels = {qa.name: ['fast', 'average', 'slow'] if 'time' in qa.name else ['low', 'average', 'high'] 
                             for qa in session.get_outcomes()}
            discrete_df, schemes = session.define_tradeoffs(n_bins=3, labels=target_labels, method='discretization')
        elif scheme_name == 'pareto' or scheme_name == 'pareto_nadir':
            discrete_df, schemes = session.define_tradeoffs(method='pareto')
        elif scheme_name == 'threshold':
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='threshold', params=params)
        else:
            print(f"Skipping unknown scheme: {scheme_name}")
            continue

        print("Schemes defined:")
        for scheme in schemes:
            print(f"  Objective: {scheme.objective_name}")
            for b in scheme.bins:
                print(f"    Label: {b.label} -> Range: [{b.min_value:.2f}, {b.max_value:.2f}]")

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
                scatter_path = os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}_all.png")
                fig.savefig(scatter_path)
                print(f"Scatter plot (all) saved to: {scatter_path}")
            except Exception as e:
                print(f"Error generating scatter plot for {x_col} vs {y_col}: {e}")

        # Generate Contingency Tables & Visualizations for each Decision
        print("\n--- Generating Contingency Analysis ---")
        decisions = session.get_decisions()
        for decision_key in decisions.keys():
            dec_name_clean = decision_key.replace(":", "_")
            print(f"Analyzing Decision: {decision_key}")
            try:
                fig_h = session.show_policy_contingency(
                    decision_key, 
                    type='heatmap', 
                    normalization_mode='row',
                    subset='train',
                    title=f"Contingency: {decision_key} (Train)"
                )
                path_h = os.path.join(outdir, f"contingency_heatmap_{dec_name_clean}.png")
                fig_h.savefig(path_h)
                print(f"  Heatmap (train) saved to: {path_h}")
            except Exception as e:
                print(f"  Error analyzing contingency for {decision_key}: {e}")

        # --- Robustness Analysis ---
        print("\n--- Generating Robustness Analysis ---")
        for tradeoff in tradeoffs:
            print(f"  Robustness Ranking for Tradeoff: {tradeoff.name}")
            try:
                ranking = session.get_policy_robustness_ranking(tradeoff.name, metric='starr')
                print(f"    Top 3 Policies (STARR):")
                for i, (pol, val) in enumerate(ranking[:3]):
                    print(f"      {i+1}. {pol}: {val:.2f}% success")
                
                if ranking:
                    top_pol = ranking[0][0]
                    regret = session.compute_robustness(top_pol, tradeoff.name, metric='regret')
                    print(f"    Top Policy '{top_pol}' Regret: {regret.get('value', 0.0):.4f} (lower is better)")
            except Exception as e:
                print(f"    Error during robustness ranking for {tradeoff.name}: {e}")

        try:
            fig_rob = session.show_robustness_heatmap(metric='starr', title=f"Robustness (STARR): {scheme_name}")
            rob_path = os.path.join(outdir, f"robustness_heatmap_{scheme_name}.png")
            fig_rob.savefig(rob_path)
            print(f"  Robustness heatmap saved to: {rob_path}")
        except Exception as e:
            print(f"  Error generating robustness heatmap: {e}")

        # --- Feature Scoring ---
        print("\n--- Generating Feature Importance Analysis ---")
        try:
            scores_df = session.compute_feature_scores(use_smart_correlation=True, subset='train')
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence: {scheme_name} (Train)")
            heatmap_path = os.path.join(outdir, f"feature_importance_{scheme_name}.png")
            fig_imp.savefig(heatmap_path)
            print(f"  Feature importance heatmap saved to: {heatmap_path}")
        except Exception as e:
            print(f"  Error during feature scoring: {e}")

        # --- Scenario Discovery ---
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