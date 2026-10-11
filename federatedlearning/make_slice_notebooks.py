"""Generates focused FL notebooks from analysis-fl.ipynb.

Two families of notebooks, each the base notebook with its `parameters` cell set:

* pattern notebooks (ablation A1): the baseline, or one pattern alone
      analysis-fl-baseline.ipynb, analysis-fl-client-selector.ipynb, ...
  They load PATTERN_SPEC and fix the tradeoff edges detected on that full dataset, so all
  of them share the same tradeoff regions and their densities are comparable.
* stress notebooks: one client count and one task, every configuration, to compare
  pattern-stress levels (Section 6b of the base notebook)
      analysis-fl-stress-c8-image.ipynb, ...
  They load STRESS_SPEC (both CSVs) and detect their own edges: comparisons happen inside
  each notebook, and accuracy/time ranges differ widely between tasks and client counts.
  By default they keep only the environment points shared by every configuration
  (ENVIRONMENT = 'common'), so configurations are compared under the same conditions.

Every generated notebook keeps the base notebook's markdown unchanged: it explains how to
read each result without describing particular results, so it applies to any slice. A
header explains the slice, and outputs are cleared (or recomputed with --execute).

Generated notebooks are outputs: edit analysis-fl.ipynb and regenerate, e.g. after the
dataset grows.

Usage (from the federatedlearning folder):
    python make_slice_notebooks.py                         # the 4 pattern notebooks
    python make_slice_notebooks.py hdh --include-baseline
    python make_slice_notebooks.py --stress                # 3 client counts x 2 tasks
    python make_slice_notebooks.py --stress --clients 8 --tasks image --environment all
    ... --execute                                          # also run them
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from typing import Any, Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_NOTEBOOK = os.path.join(HERE, "analysis-fl.ipynb")

PATTERN_SPEC = "./compact/FLsystem_compact_individual.json"  # baseline + single patterns
STRESS_SPEC = "./compact/FLsystem_compact_all.json"          # all configurations

DEFAULT_SLICES = ["baseline", "client_selector", "message_compressor", "hdh"]
DEFAULT_CLIENTS = [4, 8, 10]
DEFAULT_TASKS = ["image", "text"]

DESCRIPTIONS = {
    "baseline": "the baseline, **All Patterns Off** (`OFF,OFF,OFF`)",
    "client_selector": "**Client Selector Only** (`ON,OFF,OFF`)",
    "message_compressor": "**Message Compressor Only** (`OFF,ON,OFF`)",
    "hdh": "**HDH Only** (`OFF,OFF,ON`)",
}
TASK_DESCRIPTIONS = {"image": "image classification (CIFAR-10 + CNN 16k)",
                     "text": "text classification (AG_NEWS + MLP)"}


def output_name(slice_name: str, include_baseline: bool = False) -> str:
    suffix = slice_name.replace("_", "-") + ("-vs-baseline" if include_baseline else "")
    return f"analysis-fl-{suffix}.ipynb"


def stress_output_name(clients: int, task: str, environment: str = "common") -> str:
    return f"analysis-fl-stress-c{clients}-{task}" + ("-allenv" if environment == "all" else "") + ".ipynb"


def _parameters_cell(nb: dict) -> dict:
    params = [c for c in nb["cells"] if "parameters" in c.get("metadata", {}).get("tags", [])]
    if len(params) != 1:
        raise ValueError("The base notebook must have exactly one cell tagged 'parameters'.")
    return params[0]


def _read_parameters(cell: dict) -> dict:
    """Values of the base notebook's parameters cell (plain assignments of literals)."""
    namespace: dict = {}
    exec("".join(cell["source"]), {}, namespace)
    return namespace


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


def _format_edges(edges: Dict[str, List[float]]) -> str:
    lines = ["TRADEOFF_EDGES = {  # detected on the full dataset (make_slice_notebooks.py)"]
    lines += [f"    {o!r}: {e!r}," for o, e in edges.items()]
    return "\n".join(lines + ["}"])


def _set_parameters(cell: dict, values: Dict[str, Any], edges: Optional[Dict[str, List[float]]] = None) -> None:
    """Rewrites single-line assignments `NAME = ...` and, optionally, TRADEOFF_EDGES = None."""
    src = "".join(cell["source"])
    for name, value in values.items():
        src, n = re.subn(rf"^{name} = .*$", lambda _: f"{name} = {value!r}", src, flags=re.M)
        if n != 1:
            raise ValueError(f"The parameters cell must assign {name} once, on one line.")
    if edges is not None:
        src, n = re.subn(r"^TRADEOFF_EDGES = None$", lambda _: _format_edges(edges), src, flags=re.M)
        if n != 1:
            raise ValueError("The parameters cell must define TRADEOFF_EDGES = None once.")
    cell["source"] = src.splitlines(keepends=True)


def _header(text: str) -> dict:
    return {"cell_type": "markdown", "id": "slice-header", "metadata": {"tags": ["slice-header"]},
            "source": text.splitlines(keepends=True)}


def _build(values: Dict[str, Any], header: str, edges: Optional[Dict[str, List[float]]] = None) -> dict:
    with open(BASE_NOTEBOOK) as f:
        nb = copy.deepcopy(json.load(f))
    _set_parameters(_parameters_cell(nb), values, edges)
    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"], cell["execution_count"] = [], None
    nb["cells"].insert(1, _header(header))
    return nb


def make_notebook(slice_name: str, include_baseline: bool = False,
                  edges: Optional[Dict[str, List[float]]] = None, spec: str = PATTERN_SPEC) -> dict:
    """The pattern notebook of a slice (baseline or one pattern).

    edges: tradeoff edges to fix in the notebook; by default (None) they are detected on
    the full dataset of `spec` when the base notebook detects them, and kept otherwise.
    """
    if slice_name not in DESCRIPTIONS:
        raise ValueError(f"Unknown slice '{slice_name}'. Available: {list(DESCRIPTIONS)}")
    with open(BASE_NOTEBOOK) as f:
        base = _read_parameters(_parameters_cell(json.load(f)))
    if edges is None and base.get("TRADEOFF_EDGES") is None:
        edges = full_dataset_edges(spec, base["TRADEOFF_LABELS"])

    scope = DESCRIPTIONS[slice_name]
    if include_baseline and slice_name != "baseline":
        scope += ", together with the baseline runs (pattern ON vs. not applied)"
    header = f"""> **Focused analysis: {scope}.**
>
> Generated from `analysis-fl.ipynb` by `make_slice_notebooks.py`; edit the base notebook and regenerate instead of editing this one.
> Only the runs of this slice are loaded (`fl_slices.py`) from `{spec}`. Tradeoffs use **fixed bin edges** (`TRADEOFF_EDGES` in the parameters cell): the edges detected on that full dataset, so `S`/`M`/`L` and the regions are the same in every pattern notebook and densities are comparable across them (paper plan §4.4-4.5).
"""
    values = {"SLICE": slice_name, "INCLUDE_BASELINE": include_baseline, "SPEC": spec,
              "CLIENTS": None, "TASK": None, "ENVIRONMENT": "all"}
    return _build(values, header, edges)


def make_stress_notebook(clients: int, task: str, environment: str = "common", spec: str = STRESS_SPEC) -> dict:
    """The stress notebook of one client count and one task (every configuration)."""
    if task not in TASK_DESCRIPTIONS:
        raise ValueError(f"Unknown task '{task}'. Available: {list(TASK_DESCRIPTIONS)}")
    env_text = ("only the environment points at which **every** configuration was run "
                "(`ENVIRONMENT = 'common'`), so configurations and stress levels are compared under identical conditions"
                if environment == "common" else
                "every environment point (`ENVIRONMENT = 'all'`): configurations were not run at the same points, "
                "so differences between stress levels mix pattern and environment effects")
    header = f"""> **Pattern-stress analysis: {clients} clients, {TASK_DESCRIPTIONS[task]}.**
>
> Generated from `analysis-fl.ipynb` by `make_slice_notebooks.py`; edit the base notebook and regenerate instead of editing this one.
> All configurations are loaded from `{spec}` (both CSVs), restricted to {clients} clients, this task, and {env_text}. Section 6b compares the pattern-stress levels; its assumptions on pattern instances are listed in `compact/README.md`.
> Tradeoff edges are **detected on this notebook's runs**: regions are comparable inside the notebook, not with other client counts or tasks.
"""
    values = {"SLICE": "all", "INCLUDE_BASELINE": False, "SPEC": spec,
              "CLIENTS": clients, "TASK": task, "ENVIRONMENT": environment}
    return _build(values, header)


def execute(path: str, timeout: int = 600) -> None:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    nb = nbformat.read(path, as_version=4)
    ExecutePreprocessor(timeout=timeout).preprocess(nb, {"metadata": {"path": HERE}})
    nbformat.write(nb, path)


def _write(nb: dict, name: str, run: bool) -> None:
    path = os.path.join(HERE, name)
    with open(path, "w") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
        f.write("\n")
    print(f"Wrote {name}")
    if run:
        execute(path)
        print(f"  executed {name}")


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slices", nargs="*", default=DEFAULT_SLICES,
                        help=f"pattern notebooks (default: {' '.join(DEFAULT_SLICES)})")
    parser.add_argument("--include-baseline", action="store_true",
                        help="single-pattern slices also keep the baseline runs (written as *-vs-baseline)")
    parser.add_argument("--stress", action="store_true", help="generate the stress notebooks instead")
    parser.add_argument("--clients", nargs="*", type=int, default=DEFAULT_CLIENTS)
    parser.add_argument("--tasks", nargs="*", default=DEFAULT_TASKS)
    parser.add_argument("--environment", choices=["common", "all"], default="common")
    parser.add_argument("--execute", action="store_true", help="run each generated notebook")
    args = parser.parse_args(argv)

    if args.stress:
        for clients in args.clients:
            for task in args.tasks:
                _write(make_stress_notebook(clients, task, args.environment),
                       stress_output_name(clients, task, args.environment), args.execute)
        return

    with open(BASE_NOTEBOOK) as f:
        base = _read_parameters(_parameters_cell(json.load(f)))
    edges = None
    if base.get("TRADEOFF_EDGES") is None:  # detect once, reuse for every pattern notebook
        edges = full_dataset_edges(PATTERN_SPEC, base["TRADEOFF_LABELS"])
        print(f"Tradeoff edges detected on {PATTERN_SPEC}: {edges}")
    for name in args.slices:
        _write(make_notebook(name, args.include_baseline, edges), output_name(name, args.include_baseline), args.execute)


if __name__ == "__main__":
    sys.exit(main())
