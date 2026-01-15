import argparse
import os
import json
import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from adept import PatternAnalysis


# Specific parameters for Gateway Offloading
S_GW_DECISIONS = [0, 5, 10]
INPUT_PARAMETERS = ['N_A', 'N_B', 'r_Z_A', 'r_Z_B', 'r_gw', 'r_A_s1', 'r_B_s2', 'r_B_s3']
OUTPUTS = ['response_time', 'utilization'] #['sim_time_sec', 'response_time', 'utilization_gw']
CONFIGURATIONS = {
    0: 'no-offloading',
    5: 'short-services-offloaded',
    10: 'long-services-offloaded'
}

def preprocess_gateway_offloading(df: pd.DataFrame) -> pd.DataFrame:
    """
    Pattern-specific preprocessing for Gateway Offloading.
    Transforms raw simulation rates into service times and renames objectives.
    """

    # 1. Rename raw simulation outputs
    renames = {'R0': 'response_time', 'Ugw': 'utilization'}
    df.rename(columns={k: v for k, v in renames.items() if k in df.columns}, inplace=True)

    # 2. Compute Derived Columns
    if 'r_gw' in df.columns:
        df['S_gw'] = df['r_gw'].apply(lambda x: 0.0 if x > 1e10 else (1.0 / x if x != 0 else 0.0))

    # 3. Process policies
    list_dfs = []
    for s in df['S_gw'].unique():
        # print(s,int(s))
        if int(s) in S_GW_DECISIONS:
            temp = df[df['S_gw'] == s][INPUT_PARAMETERS + OUTPUTS].copy()                
            temp['policy'] = CONFIGURATIONS[int(s)] #int(s) #np.nan #float('nan')
            temp['policy'] = temp['policy'].astype('category')
            temp['S_gw'] = s
            list_dfs.append(temp)
    
    experiments_df = pd.concat(list_dfs)
    experiments_df.index.name = 'scenario'
    experiments_df.reset_index(inplace=True)
    experiments_df['model'] = 'gateway_offloading'

    # 4. Sort
    sort_cols = [c for c in ['N_A', 'S_gw'] if c in experiments_df.columns]
    if sort_cols:
        experiments_df.sort_values(by=sort_cols, inplace=True)
        experiments_df.reset_index(drop=True, inplace=True)

    return experiments_df

# Main method to perform all the analyses
def run_analysis(json_path: str, outdir: str, validate_integrity: bool = True) -> None:
    os.makedirs(outdir, exist_ok=True)
    
    # 1. Initialize Analysis Session
    print(f"Initializing analysis session for: {json_path}")
    session = PatternAnalysis(json_path)
    
    # 2. Load with Programmatic Hook
    session.load(validate_integrity=validate_integrity, preprocessor=preprocess_gateway_offloading)
    
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
        
        # 4. Define Tradeoffs (Discretization)
        if scheme_name == 'discretization':
            target_labels = {qa.name: ['fast', 'average', 'slow'] if 'time' in qa.name else ['low', 'average', 'high'] 
                             for qa in session.get_outcomes()}
            discrete_df, schemes = session.define_tradeoffs(n_bins=3, labels=target_labels, method='discretization')
        elif scheme_name in ['pareto', 'pareto_nadir']:
            discrete_df, schemes = session.define_tradeoffs(method='pareto')
        else:
            continue

        # --- Data Split ---
        print("\n--- Splitting Data ---")
        session.split_data(test_size=0.2)

        # 5. Visual Confirmation (Distributions)
        for tradeoff in tradeoffs:
            try:
                indices = session.get_indices_for_tradeoff(tradeoff)
                fig = session.coordinator.plot_distributions(session.outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=indices)
                fig.savefig(os.path.join(outdir, f"distribution_{tradeoff.name}.png"))
                print(f"Distribution plot saved for: {tradeoff.name}")
            except Exception as e: print(f"Error plot {tradeoff.name}: {e}")

        # 6. Quality Objective Space (2D Scatter)
        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                fig = session.show_quality_objective_space(x_col, y_col, highlight_tradeoffs=tradeoffs, subset='all')
                fig.savefig(os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}_all.png"))
            except Exception as e: print(f"Error scatter {x_col} vs {y_col}: {e}")

        # 7. Contingency Analysis
        print("\n--- Generating Contingency Analysis ---")
        decisions = session.get_decisions()
        for decision_key in decisions.keys():
            dec_name_clean = decision_key.replace(":", "_")
            try:
                fig_h = session.show_policy_contingency(decision_key, type='heatmap', subset='train', title=f"Contingency: {decision_key} (Train)")
                fig_h.savefig(os.path.join(outdir, f"contingency_heatmap_{dec_name_clean}.png"))
            except Exception as e: print(f"Error contingency {decision_key}: {e}")

        # 8. Robustness Analysis
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

        # 9. Feature Importance
        print("\n--- Generating Feature Importance Analysis ---")
        try:
            scores_df = session.compute_feature_scores(use_smart_correlation=True, subset='train')
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence: {scheme_name} (Train)")
            fig_imp.savefig(os.path.join(outdir, f"feature_importance_{scheme_name}.png"))
        except Exception as e: print(f"Error scoring: {e}")

        # 10. Scenario Discovery (PRIM)
        print("\n--- Generating Scenario Discovery (PRIM) ---")
        for tradeoff in tradeoffs:
            try:
                boxes = session.discover_scenarios(tradeoff.name, method='prim', threshold=0.7, standardize=True)
                if boxes:
                    box_path = os.path.join(outdir, f"discovery_{tradeoff.name.replace(' ', '_')}.json")
                    with open(box_path, 'w') as f:
                        json.dump(boxes[0].model_dump(), f, indent=2)
            except Exception as e: print(f"Error discovery {tradeoff.name}: {e}")


# -------------------

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="patterns/Gateway_Offloading/Gateway_Offloading.json")
    parser.add_argument("--outdir", default="patterns/Gateway_Offloading/out")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()