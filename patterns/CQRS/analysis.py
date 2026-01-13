import argparse
import os
import json
import itertools
from adept import PatternAnalysis

def run_analysis(json_path: str, outdir: str, validate_integrity: bool = True) -> None:
    os.makedirs(outdir, exist_ok=True)
    print(f"Initializing analysis session for: {json_path}")
    session = PatternAnalysis(json_path)
    session.load(validate_integrity=validate_integrity)
    
    tradeoffs_by_scheme = {}
    for t in session.get_tradeoffs():
        tradeoffs_by_scheme.setdefault(t.scheme, []).append(t)

    for scheme_name, tradeoffs in tradeoffs_by_scheme.items():
        print(f"\n--- Processing Scheme: {scheme_name} ---")
        if scheme_name == 'discretization':
            target_labels = {qa.name: ['low', 'avg', 'high'] for qa in session.get_outcomes()}
            discrete_df, schemes = session.define_tradeoffs(n_bins=3, labels=target_labels, method='discretization')
        elif scheme_name == 'pareto' or scheme_name == 'pareto_nadir':
            discrete_df, schemes = session.define_tradeoffs(method='pareto')
        elif scheme_name == 'threshold':
            params = tradeoffs[0].params
            discrete_df, schemes = session.define_tradeoffs(method='threshold', params=params)
        else: continue

        session.split_data(test_size=0.2)

        for tradeoff in tradeoffs:
            try:
                indices = session.get_indices_for_tradeoff(tradeoff)
                fig = session.coordinator.plot_distributions(session.outcomes_df, schemes, tradeoff=tradeoff, highlight_indices=indices)
                fig.savefig(os.path.join(outdir, f"distribution_{tradeoff.name}.png"))
            except Exception as e: print(f"Error plot {tradeoff.name}: {e}")

        outcome_cols = list(session.outcomes_df.columns)
        for x_col, y_col in itertools.combinations(outcome_cols, 2):
            try:
                fig = session.show_quality_objective_space(x_col, y_col, highlight_tradeoffs=tradeoffs, subset='all')
                fig.savefig(os.path.join(outdir, f"scatter_{x_col}_vs_{y_col}.png"))
            except Exception as e: print(f"Error scatter {x_col} vs {y_col}: {e}")

        try:
            scores_df = session.compute_feature_scores(use_smart_correlation=True, subset='train')
            fig_imp = session.show_feature_heatmap(scores_df, title=f"Feature Influence (Train)")
            fig_imp.savefig(os.path.join(outdir, f"feature_importance_{scheme_name}.png"))
        except Exception as e: print(f"Error scoring: {e}")

        for tradeoff in tradeoffs:
            try:
                boxes = session.discover_scenarios(tradeoff.name, method='prim', threshold=0.7, standardize=True)
                if boxes:
                    with open(os.path.join(outdir, f"discovery_{tradeoff.name.replace(' ', '_')}.json"), 'w') as f:
                        json.dump(boxes[0].model_dump(), f, indent=2)
            except Exception as e: print(f"Error discovery {tradeoff.name}: {e}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="patterns/CQRS/CQRS.json")
    parser.add_argument("--outdir", default="patterns/CQRS/out")
    parser.add_argument("--no-validate", action="store_true")
    args = parser.parse_args()
    run_analysis(args.config, args.outdir, validate_integrity=not args.no_validate)

if __name__ == "__main__":
    main()
