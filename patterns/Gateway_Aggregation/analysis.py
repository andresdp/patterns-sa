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
    
    # 2.5 Optional Preprocessing (Standardized Renames are in JSON)
    # Gateway Aggregation sorting logic from legacy code
    if 'N_A' in session.experiments_df.columns:
        session.experiments_df = session.experiments_df.sort_values(by='N_A')
        session.outcomes_df = session.outcomes_df.loc[session.experiments_df.index]

    # 3. Check for programmatic tradeoffs if none defined in JSON
    if not session.get_tradeoffs():
        print("No tradeoffs defined in JSON. Defining programmatically...")
        session.add_tradeoff(
            name="performance-optimized",
            elements={"response_time": "fast", "utilization": "average"}
        )
        session.add_tradeoff(
            name="balanced",
            elements={"response_time": "average", "utilization": "average"}
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
        else: continue

        # --- Data Split ---
        session.split_data(test_size=0.2)

        # Generate Distribution Plots
        for tradeoff in tradeoffs:
            try:
                indices = session.get_indices_for_tradeoff(tradeoff)
                fig = session.coordinator.plot_distributions(session.outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=indices)
                fig.savefig(os.path.join(outdir, f"distribution_{tradeoff.name}.png"))
            except Exception as e: print(f"Error plot {tradeoff.name}: {e}")

        # Generate 2D Scatter Plots
        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                fig = session.show_quality_objective_space(x_col, y_col, highlight_tradeoffs=tradeoffs, subset='all')
                fig.savefig(os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}.png"))
            except Exception as e: print(f"Error scatter {x_col} vs {y_col}: {e}")

        # Contingency
        print("\n--- Generating Contingency Analysis ---")
        decisions = session.get_decisions()
        for decision_key in decisions.keys():
            dec_name_clean = decision_key.replace(":", "_")
            try:
                fig_h = session.show_policy_contingency(decision_key, type='heatmap', subset='train', title=f"Contingency: {decision_key} (Train)")
                fig_h.savefig(os.path.join(outdir, f"contingency_heatmap_{dec_name_clean}.png"))
            except Exception as e: print(f"Error contingency {decision_key}: {e}")

        # Robustness
        print("\n--- Generating Robustness Analysis ---")
        for tradeoff in tradeoffs:
            try:
                ranking = session.get_policy_robustness_ranking(tradeoff.name, metric='starr')
                if ranking:
                    top_pol = ranking[0][0]
                    regret = session.compute_robustness(top_pol, tradeoff.name, metric='regret')
                    print(f"    Top Policy '{top_pol}' for {tradeoff.name}: {ranking[0][1]:.2f}% STARR, {regret.get('value', 0.0):.4f} Regret")
            except Exception as e: print(f"Error robustness {tradeoff.name}: {e}")

        try:
            fig_rob = session.show_robustness_heatmap(metric='starr', title=f"Robustness (STARR): {scheme_name}")
            fig_rob.savefig(os.path.join(outdir, f"robustness_heatmap_{scheme_name}.png"))
        except Exception as e: print(f"Error robust heatmap: {e}")

        # Feature Scoring
        print("\n--- Generating Feature Importance Analysis ---")
        try:
            scores_df = session.compute_feature_scores(use_smart_correlation=True, subset='train')
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence: {scheme_name} (Train)")
            fig_imp.savefig(os.path.join(outdir, f"feature_importance_{scheme_name}.png"))
        except Exception as e: print(f"Error scoring: {e}")

        # Scenario Discovery
        print("\n--- Generating Scenario Discovery (PRIM) ---")
        for tradeoff in tradeoffs:
            try:
                boxes = session.discover_scenarios(tradeoff.name, method='prim', threshold=0.7, standardize=True)
                if boxes:
                    with open(os.path.join(outdir, f"discovery_{tradeoff.name.replace(' ', '_')}.json"), 'w') as f:
                        json.dump(boxes[0].model_dump(), f, indent=2)
            except Exception as e: print(f"Error discovery {tradeoff.name}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="patterns/Gateway_Aggregation/Gateway_Aggregation.json")
    parser.add_argument("--outdir", default="patterns/Gateway_Aggregation/out")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()
