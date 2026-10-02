"""Generates focused FL notebooks (one per slice) from analysis-fl.ipynb.

Each generated notebook is the base notebook with:
* its `parameters` cell set to the slice (SLICE, INCLUDE_BASELINE) and, when the base
  notebook detects the tradeoff edges (TRADEOFF_EDGES = None), to the edges detected on the
  full dataset, so every notebook has the same tradeoff regions;
* a header explaining the slice;
* the markdown cells tagged `full-dataset-interpretation` replaced by placeholders, since
  their text interprets the results of the full dataset (section titles are kept);
* outputs cleared, or recomputed with --execute.

Generated notebooks are outputs: edit analysis-fl.ipynb and regenerate, e.g. after the
dataset grows.

Usage (from the federatedlearning folder):
    python make_slice_notebooks.py                       # the 4 default slices
    python make_slice_notebooks.py --execute             # ... and run them
    python make_slice_notebooks.py hdh --include-baseline
"""
from __future__ import annotations

import argparse
import copy
import json
import os
import re
import sys
from typing import Dict, List, Optional

HERE = os.path.dirname(os.path.abspath(__file__))
BASE_NOTEBOOK = os.path.join(HERE, "analysis-fl.ipynb")
INTERPRETATION_TAG = "full-dataset-interpretation"
DEFAULT_SLICES = ["baseline", "client_selector", "message_compressor", "hdh"]

DESCRIPTIONS = {
    "baseline": "the baseline, **All Patterns Off** (`OFF,OFF,OFF`)",
    "client_selector": "**Client Selector Only** (`ON,OFF,OFF`)",
    "message_compressor": "**Message Compressor Only** (`OFF,ON,OFF`)",
    "hdh": "**HDH Only** (`OFF,OFF,ON`)",
}


def output_name(slice_name: str, include_baseline: bool) -> str:
    suffix = slice_name.replace("_", "-") + ("-vs-baseline" if include_baseline else "")
    return f"analysis-fl-{suffix}.ipynb"


def _read_parameters(cell: dict) -> dict:
    """Values of the base notebook's parameters cell (plain assignments of literals)."""
    namespace: dict = {}
    exec("".join(cell["source"]), {}, namespace)
    return namespace


def full_dataset_edges(spec: str, labels: Dict[str, List[str]]) -> Dict[str, List[float]]:
    """Tradeoff edges detected on the full dataset, as the base notebook detects them.

    Edges are rounded to the fewest decimals (5 to 12) that keep every run's label, so the
    focused notebooks reproduce the base notebook's regions exactly.
    """
    import contextlib
    import io

    sys.path.insert(0, os.path.dirname(HERE))
    from adept import PatternAnalysis

    def session(edges=None):
        s = PatternAnalysis(os.path.join(HERE, spec))
        with contextlib.redirect_stdout(io.StringIO()):
            s.load()
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


def _set_parameters(cell: dict, slice_name: str, include_baseline: bool,
                    edges: Optional[Dict[str, List[float]]] = None) -> None:
    src = "".join(cell["source"])
    src, n1 = re.subn(r"^SLICE = .*$", f"SLICE = {slice_name!r}", src, flags=re.M)
    src, n2 = re.subn(r"^INCLUDE_BASELINE = .*$", f"INCLUDE_BASELINE = {include_baseline}", src, flags=re.M)
    if n1 != 1 or n2 != 1:
        raise ValueError("The parameters cell must define SLICE and INCLUDE_BASELINE once each.")
    if edges is not None:
        src, n3 = re.subn(r"^TRADEOFF_EDGES = None$", lambda _: _format_edges(edges), src, flags=re.M)
        if n3 != 1:
            raise ValueError("The parameters cell must define TRADEOFF_EDGES = None once.")
    cell["source"] = src.splitlines(keepends=True)


def _placeholder(cell: dict) -> None:
    lines = "".join(cell["source"]).splitlines()
    title = lines[0] if lines and lines[0].startswith("#") else ""
    text = (f"{title}\n\n" if title else "") + (
        "> *Interpretation to be written for this slice.* The corresponding text in "
        "`analysis-fl.ipynb` interprets the full dataset and does not apply here."
    )
    cell["source"] = text.splitlines(keepends=True)


def _header(slice_name: str, include_baseline: bool) -> dict:
    scope = DESCRIPTIONS[slice_name]
    if include_baseline and slice_name != "baseline":
        scope += ", together with the baseline runs (pattern ON vs. not applied)"
    text = f"""> **Focused analysis: {scope}.**
>
> Generated from `analysis-fl.ipynb` by `make_slice_notebooks.py`; edit the base notebook and regenerate instead of editing this one.
> Only the runs of this slice are loaded (`fl_slices.py`). Tradeoffs use **fixed bin edges** (`TRADEOFF_EDGES` in the parameters cell): the edges the base notebook detects on the full dataset, so `S`/`M`/`L` and the regions are the same as in the other notebooks and densities are comparable across them (paper plan §4.4-4.5).
> With the current 32-run dataset a slice holds 5-10 runs, so expect few or no boxes: the notebook is ready to be re-run on the larger dataset.
"""
    return {"cell_type": "markdown", "id": "slice-header", "metadata": {"tags": ["slice-header"]},
            "source": text.splitlines(keepends=True)}


def make_notebook(slice_name: str, include_baseline: bool = False,
                  edges: Optional[Dict[str, List[float]]] = None) -> dict:
    """The focused notebook of a slice.

    edges: tradeoff edges to fix in the notebook; by default (None) they are detected on
    the full dataset when the base notebook detects them, and kept when it fixes them.
    """
    if slice_name not in DESCRIPTIONS:
        raise ValueError(f"Unknown slice '{slice_name}'. Available: {list(DESCRIPTIONS)}")
    with open(BASE_NOTEBOOK) as f:
        nb = json.load(f)
    nb = copy.deepcopy(nb)

    params = [c for c in nb["cells"] if "parameters" in c.get("metadata", {}).get("tags", [])]
    if len(params) != 1:
        raise ValueError("The base notebook must have exactly one cell tagged 'parameters'.")
    base = _read_parameters(params[0])
    if edges is None and base.get("TRADEOFF_EDGES") is None:
        edges = full_dataset_edges(base["SPEC"], base["TRADEOFF_LABELS"])
    _set_parameters(params[0], slice_name, include_baseline, edges)

    for cell in nb["cells"]:
        if cell["cell_type"] == "code":
            cell["outputs"], cell["execution_count"] = [], None
        elif INTERPRETATION_TAG in cell.get("metadata", {}).get("tags", []):
            _placeholder(cell)

    nb["cells"].insert(1, _header(slice_name, include_baseline))
    return nb


def execute(path: str, timeout: int = 600) -> None:
    import nbformat
    from nbconvert.preprocessors import ExecutePreprocessor

    nb = nbformat.read(path, as_version=4)
    ExecutePreprocessor(timeout=timeout).preprocess(nb, {"metadata": {"path": HERE}})
    nbformat.write(nb, path)


def main(argv: Optional[List[str]] = None) -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("slices", nargs="*", default=DEFAULT_SLICES, help=f"default: {' '.join(DEFAULT_SLICES)}")
    parser.add_argument("--include-baseline", action="store_true",
                        help="single-pattern slices also keep the baseline runs (written as *-vs-baseline)")
    parser.add_argument("--execute", action="store_true", help="run each generated notebook")
    args = parser.parse_args(argv)

    edges = None
    for name in args.slices:
        if edges is None:  # detect once, reuse for every slice
            with open(BASE_NOTEBOOK) as f:
                cells = json.load(f)["cells"]
            base = _read_parameters(next(c for c in cells if "parameters" in c.get("metadata", {}).get("tags", [])))
            if base.get("TRADEOFF_EDGES") is None:
                edges = full_dataset_edges(base["SPEC"], base["TRADEOFF_LABELS"])
                print(f"Tradeoff edges detected on the full dataset: {edges}")
        path = os.path.join(HERE, output_name(name, args.include_baseline))
        nb = make_notebook(name, args.include_baseline, edges)
        with open(path, "w") as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write("\n")
        print(f"Wrote {os.path.basename(path)}")
        if args.execute:
            execute(path)
            print(f"  executed {os.path.basename(path)}")


if __name__ == "__main__":
    sys.exit(main())
