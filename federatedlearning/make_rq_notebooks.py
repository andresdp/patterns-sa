"""Generate the six compact FL notebooks for the two-RQ experimental plan."""
from __future__ import annotations
import copy, json, os, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE.parent))
sys.path.insert(0, str(HERE))

SPEC = './compact/FLsystem_compact_all.json'
LABELS = {'final_val_accuracy': ['S', 'M', 'L'], 'avg_total_time': ['S', 'M', 'L']}
SCENARIOS = [(c, t) for c in (4, 8, 10) for t in ('image', 'text')]
TASKS = {'image': 'CIFAR-10/CNN 16k', 'text': 'AG_NEWS/MLP'}


def full_dataset_edges(spec: str, labels: Dict[str, List[str]]) -> Dict[str, List[float]]:
    """Tradeoff edges detected on a full dataset, as the base notebook detects them.

    Edges are rounded to the fewest decimals (5 to 12) that keep every run's label, so the
    focused notebooks reproduce the detected regions exactly.
    """
    import contextlib
    import io

    sys.path.insert(0, os.path.dirname(HERE))
    sys.path.insert(0, HERE)
    from adept import PatternAnalysis
    import fl_slices

    def session(edges=None):
        s = PatternAnalysis(os.path.join(HERE, spec))
        with contextlib.redirect_stdout(io.StringIO()):
            s.load(preprocessor=fl_slices.slice_filter())
            s.create_tradeoffs(method="discretization", labels=labels, edges=edges)
        return s

    detected = session()
    exact = {sc.objective_name: [sc.bins[0].min_value] + [b.max_value for b in sc.bins] for sc in detected.schemes}
    for digits in range(5, 13):
        rounded = {o: [round(e, digits) for e in edges] for o, edges in exact.items()}
        if session(rounded).discrete_df.astype(str).equals(detected.discrete_df.astype(str)):
            return rounded
    return exact



def md(text):
    return {'cell_type':'markdown','metadata':{},'source':text.splitlines(keepends=True)}
def code(text):
    return {'cell_type':'code','execution_count':None,'metadata':{},'outputs':[],'source':text.splitlines(keepends=True)}

def make_notebook(clients, task, edges):
    nb = {'cells':[], 'metadata':{'kernelspec':{'display_name':'Python 3','language':'python','name':'python3'},'language_info':{'name':'python','version':'3'}},'nbformat':4,'nbformat_minor':5}
    nb['cells'] += [md(f"# ADEPT compact FL analysis: {clients} clients, {TASKS[task]}\n\nRQ1 describes the observed objective tradeoffs across configurations and pattern counts. RQ2 searches for operating conditions associated with each observed tradeoff and evaluates the rules on held-out partition seeds. Results are observational associations. Dataset and model are treated as a paired scenario context.")]
    nb['cells'] += [code("import sys, contextlib, io, itertools\nimport pandas as pd\nimport matplotlib.pyplot as plt\nsys.path.append('..')\nfrom adept import PatternAnalysis\nfrom adept.utils.spec_summary import summarize_system\nfrom adept.utils.linter import SystemLinter\nimport fl_slices")]
    for env in ('common','all'):
        scope = 'Common environment' if env == 'common' else 'All environments'
        nb['cells'] += [md(f"## {scope}\n\nThis view uses the same fixed objective bin edges as every other scenario. The common-environment view compares runs at environmental settings shared across configurations. The all-environment view includes all available settings; configuration differences can also reflect differences in sampled environments. These are nested views of the campaign, not independent replications.")]
        nb['cells'] += [code(f"SLICE, INCLUDE_BASELINE = 'all', False\nCLIENTS, TASK, ENVIRONMENT = {clients}, {task!r}, {env!r}\nSPEC = {SPEC!r}\nTRADEOFF_LABELS = {LABELS!r}\nTRADEOFF_EDGES = {edges!r}\nsession = PatternAnalysis(SPEC)\nsession.load(preprocessor=fl_slices.slice_filter(SLICE, INCLUDE_BASELINE, clients=CLIENTS, task=TASK, environment=ENVIRONMENT))\nprint(f'Loaded {{len(session.raw_df)}} experiments')\nprint(summarize_system(session.sys_def))\nissues = SystemLinter().lint(session.sys_def, session.raw_df)\nerrors = [i for i in issues if i.level == 'ERROR']\nwarnings = [i for i in issues if i.level == 'WARNING']\nprint(f'Linter: {{len(errors)}} errors, {{len(warnings)}} warnings')\nassert not errors")]
        nb['cells'] += [md('### RQ1 · Which tradeoffs occur, and how do decisions relate to them?')]
        nb['cells'] += [code("tradeoffs, schemes = session.create_tradeoffs(method='discretization', labels=TRADEOFF_LABELS, edges=TRADEOFF_EDGES)\nfor scheme in schemes:\n    print(scheme.objective_name, [scheme.bins[0].min_value] + [b.max_value for b in scheme.bins])\nprint(f'{len(tradeoffs)} defined regions; {len(session.get_tradeoffs(non_empty=True))} contain observations in this scenario/view')\nsession.split_data(test_size=0.3, random_state=42, remove_outliers=False, verbose=True, group_column='partition_seed')")]
        nb['cells'] += [md('**Reading the objective-space chart.** Each point is one experimental run; axes show measured outcomes, color identifies the number of active pattern types, and the shared grid defines S/M/L tradeoff quadrants. Clustering shows observed associations; it does not isolate a pattern’s causal effect.')]
        nb['cells'] += [code("fig, axes = plt.subplots(1, 2, figsize=(12, 5))\npatterns = session.experiments_df\nfor ax, (x, y) in zip(axes, itertools.combinations(TRADEOFF_LABELS, 2)):\n    view = session.raw_df.copy()\n    view['Pattern Types Active'] = session.experiments_df['Pattern Types Active'].to_numpy()\n    view['Pattern Count Group'] = view['Pattern Types Active'].map(lambda n: '0' if n == 0 else ('1' if n == 1 else '2-3'))\n    for level, group in view.groupby('Pattern Count Group', sort=False):\n        ax.scatter(group[x], group[y], s=22, alpha=.65, label=f'{level} active pattern types')\n    ax.set(xlabel=x, ylabel=y, title=f'{x} vs {y}')\n    for edge in TRADEOFF_EDGES[x][1:-1]: ax.axvline(edge, color='black', linewidth=.8, alpha=.55)\n    for edge in TRADEOFF_EDGES[y][1:-1]: ax.axhline(edge, color='black', linewidth=.8, alpha=.55)\n    ax.legend(fontsize=8)\nplt.tight_layout(); plt.show()")]
        nb['cells'] += [md('**Tradeoff frequency by decision.** Rows show the share of runs in each fixed region for each complete configuration and each pattern-count group (0, 1, 2–3). These conditional frequencies describe how the observed design alternatives are distributed.')]
        nb['cells'] += [code("discrete = session.discrete_df.astype(str).agg('-'.join, axis=1).rename('tradeoff')\nview = session.experiments_df.copy()\nview['tradeoff'] = discrete.to_numpy()\nview['Pattern Count Group'] = view['Pattern Types Active'].map(lambda n: '0' if n == 0 else ('1' if n == 1 else '2-3'))\nconfig_col = session.sys_def.dataspace.configuration_identification.column\nfor group_col in (config_col, 'Pattern Count Group'):\n    counts = pd.crosstab(view[group_col], view['tradeoff'])\n    shares = counts.div(counts.sum(axis=1), axis=0)\n    print(f'Observed tradeoff counts by {group_col}:'); display(counts)\n    print(f'Within-group shares by {group_col}:'); display(shares.round(3))")]
        nb['cells'] += [md('### RQ2 · Which conditions are associated with each tradeoff, and what changes inside the discovered box?\n\nFeature importance uses ADEPT’s existing train-set ranking to prioritize candidate predictors. It screens variables for scenario discovery; it is not a causal effect estimate.')]
        nb['cells'] += [code("scores_df = session.compute_feature_scores(use_smart_correlation=True, include_constraints=True, subset='train')\nsession.show_feature_heatmap(scores_df, title='Train-set feature importance', figsize=(5, 8)); plt.show()\nweighted_features = session.get_weighted_feature_ranking(scores_df)\nkey_parameters = session.select_top_k_parameters(scores_df, index_order=weighted_features, threshold=0.03, k=None)\nprint('Weighted ranking:', weighted_features)\nprint('Candidate parameters (importance threshold 0.03):', key_parameters)")]
        nb['cells'] += [md('PRIM and CART are fitted on the training partition. Empty quadrants remain in the fixed grid but are not discovery targets. A missing box means that method did not return a nonempty rule for that target.')]
        nb['cells'] += [code("prim_boxes = []\nfor tradeoff in session.get_tradeoffs(non_empty=True):\n    boxes = session.discover_scenarios(tradeoff.name, method='prim', threshold=0.8, standardize=True, parameters=key_parameters)\n    found = [b for b in boxes if not b.is_empty()]\n    if found: prim_boxes.append(found[0])\n    else: print('PRIM found no box:', tradeoff.name)\ncart_boxes = [b for b in session.discover_scenarios(method='cart', standardize=True, parameters=key_parameters) if not b.is_empty()]\nfor method, boxes in [('PRIM', prim_boxes), ('CART', cart_boxes)]:\n    print(f'\\n{method}: {len(boxes)} boxes')\n    for i, box in enumerate(boxes, 1):\n        print(i, box.target_tradeoff, box.target_tradeoff_labels, box.metrics)\n        for parameter, condition in box.describe_limits(digits=3).items(): print('  ', parameter, condition)")]
        nb['cells'] += [md('**Architecture context for box predicates.** The explanation expands specification-declared parent/child relationships to make interacting policy conditions readable. The original box predicates and thresholds remain the analytic rules.')]
        nb['cells'] += [code("for method, boxes in [('PRIM', prim_boxes), ('CART', cart_boxes)]:\n    for i, box in enumerate(boxes, 1):\n        explanation = session.explain_box_context(box, output_format='plain')\n        print(f'{method} box {i}: {box.target_tradeoff}\\n{explanation[\"text\"]}\\n')")]
        nb['cells'] += [md('**Held-out what-if comparison.** For each target, compare its baseline frequency in the test partition with its frequency among test runs satisfying the box. Also report box coverage (fraction of all target runs captured), precision (target fraction inside the box), lift (precision minus baseline prevalence), and counts. These are observed conditional differences, not causal improvements. Small or zero test support makes estimates unstable or unavailable.')]
        nb['cells'] += [code("def heldout_box_summary(boxes, method):\n    X, _, discrete_test = session._get_subset_data('test')\n    X = session._encode_for_boxes(X)\n    rows = []\n    for box in boxes:\n        mask = pd.Series(True, index=X.index)\n        for parameter, bounds in box.limits.items():\n            if parameter in X.columns: mask &= X[parameter].between(bounds['min'], bounds['max'])\n        target = pd.Series(True, index=X.index)\n        target_definition = session.get_tradeoff(box.target_tradeoff)\n        for objective, label in target_definition.elements.items(): target &= session.discrete_df.loc[X.index, objective].astype(str).eq(str(label))\n        baseline_n, target_n = len(X), int(target.sum())\n        inside_n, inside_target = int(mask.sum()), int((mask & target).sum())\n        baseline = target_n / baseline_n if baseline_n else float('nan')\n        precision = inside_target / inside_n if inside_n else float('nan')\n        coverage = inside_target / target_n if target_n else float('nan')\n        rows.append({'method':method, 'target':box.target_tradeoff, 'test_n':baseline_n, 'baseline_target_n':target_n, 'box_n':inside_n, 'target_in_box':inside_target, 'baseline_rate':baseline, 'box_rate_precision':precision, 'test_delta_rate':precision-baseline if inside_n else float('nan'), 'train_lift_absolute':box.metrics.get('lift'), 'coverage_recall':coverage})\n    return pd.DataFrame(rows)\nwhat_if = pd.concat([heldout_box_summary(prim_boxes, 'PRIM'), heldout_box_summary(cart_boxes, 'CART')], ignore_index=True)\ndisplay(what_if.round(3))")]
    return nb

def main():
    edges = full_dataset_edges(SPEC, LABELS)
    print('Fixed full-campaign bin edges:', edges)
    for clients, task in SCENARIOS:
        name = f'analysis-fl-rq-c{clients}-{task}.ipynb'
        path = HERE / name
        with path.open('w') as f: json.dump(make_notebook(clients, task, edges), f, indent=1, ensure_ascii=False); f.write('\n')
        print('Wrote', name)
if __name__ == '__main__': main()
