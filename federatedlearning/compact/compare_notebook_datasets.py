#!/usr/bin/env python3
"""Compare the exact source rows selected by compact task notebooks.

The script reads each task notebook's literal filter parameters and applies the same
configuration, client-count, task, and target-stress restrictions as fl_slices.slice_filter.
It uses datacompy to compare every pair's selected row values, aligned by unique run_id.
Original column names are replaced with positional names before comparison, so equality
is based on the data values rather than matching field labels.

Run from any directory with:
    conda run -n perfmodels python federatedlearning/compact/compare_notebook_datasets.py
"""

from __future__ import annotations

import argparse
import ast
import csv
import json
import re
from itertools import combinations
from pathlib import Path
from typing import Any

import pandas as pd
from datacompy import PandasCompare


ROOT = Path(__file__).resolve().parents[2]
COMPACT = ROOT / "federatedlearning" / "compact"
TASKS = {
    "image": ("CIFAR-10", "CNN 16k"),
    "text": ("AG_NEWS", "MLP"),
}
PATTERNS = ("client_selector", "message_compressor", "hdh")
STRESS_CODES = {"CS": 0, "MC": 1, "HDH": 2}
STRESS_TOKEN = re.compile(r"([A-Z]+)\s*=\s*(\d+(?:\.\d+)?)\s*%")
FILTER_NAMES = {"SLICE", "INCLUDE_BASELINE", "CLIENTS", "TASK", "ENVIRONMENT", "TARGET_STRESS"}


def notebook_filters(path: Path) -> dict[str, Any]:
    notebook = json.loads(path.read_text(encoding="utf-8"))
    values: dict[str, Any] = {}
    for cell in notebook.get("cells", []):
        if cell.get("cell_type") != "code":
            continue
        source = cell.get("source", "")
        source = "".join(source) if isinstance(source, list) else str(source)
        try:
            tree = ast.parse(source)
        except SyntaxError:
            continue
        for node in ast.walk(tree):
            if not isinstance(node, ast.Assign):
                continue
            names = [target.id for target in node.targets if isinstance(target, ast.Name)]
            if not FILTER_NAMES.intersection(names):
                continue
            try:
                value = ast.literal_eval(node.value)
            except (ValueError, TypeError):
                continue
            for name in names:
                if name in FILTER_NAMES:
                    values[name] = value

    required = {"SLICE", "INCLUDE_BASELINE", "CLIENTS", "TASK", "ENVIRONMENT"}
    missing = required - values.keys()
    if missing:
        raise ValueError(f"{path.relative_to(ROOT)} is missing literal filter(s): {sorted(missing)}")
    if values["ENVIRONMENT"] != "all":
        raise ValueError(
            f"{path.relative_to(ROOT)} uses ENVIRONMENT={values['ENVIRONMENT']!r}; "
            "this checker currently verifies the maintained all-environment notebooks only."
        )
    return values


def allowed_configs(slice_name: str, include_baseline: bool) -> set[str] | None:
    if slice_name == "all":
        return None
    if slice_name == "baseline":
        return {"OFF,OFF,OFF"}
    if slice_name not in PATTERNS:
        raise ValueError(f"Unsupported SLICE={slice_name!r}.")
    positions = {name: index for index, name in enumerate(PATTERNS)}
    config = ["OFF"] * len(PATTERNS)
    config[positions[slice_name]] = "ON"
    configs = {",".join(config)}
    if include_baseline:
        configs.add("OFF,OFF,OFF")
    return configs


def row_stress_tokens(row: dict[str, str], source: Path) -> dict[str, float]:
    raw = row.get("pattern_stress", "").strip()
    config = [part.strip().upper() for part in row.get("config_id", "").split(",")]
    if len(config) != 3:
        raise ValueError(f"Invalid config_id at {source}: {row.get('config_id')!r}")
    tokens: dict[str, float] = {}
    if raw.lower() != "none":
        for item in raw.split(";"):
            match = STRESS_TOKEN.fullmatch(item.strip())
            if not match:
                raise ValueError(f"Invalid pattern_stress token at {source}: {item!r}")
            code, raw_value = match.groups()
            if code not in STRESS_CODES or code in tokens:
                raise ValueError(f"Unknown or duplicate stress token at {source}: {code!r}")
            tokens[code] = float(raw_value)
    for code, position in STRESS_CODES.items():
        if (config[position] == "ON") != (code in tokens):
            raise ValueError(f"pattern_stress disagrees with config_id at {source} for {code}")
    return tokens


def load_source_rows() -> list[tuple[str, int, dict[str, str]]]:
    spec = json.loads((COMPACT / "FLsystem_compact_all.json").read_text(encoding="utf-8"))
    sources = spec["dataspace"]["source_file"]
    sources = [sources] if isinstance(sources, str) else sources
    delimiter = spec.get("dataspace", {}).get("discovery_options", {}).get("csv_delimiter", ",")
    rows: list[tuple[str, int, dict[str, str]]] = []
    source_columns: list[str] | None = None
    for relative_source in sources:
        source_path = COMPACT / relative_source
        with source_path.open(newline="", encoding="utf-8-sig") as stream:
            reader = csv.DictReader(stream, delimiter=delimiter)
            required_columns = {"config_id", "run_id", "pattern_stress", "Total Clients", "Dataset", "Model"}
            missing = required_columns - set(reader.fieldnames or [])
            if missing:
                raise ValueError(f"{source_path} is missing columns: {sorted(missing)}")
            if source_columns is None:
                source_columns = list(reader.fieldnames or [])
            elif list(reader.fieldnames or []) != source_columns:
                raise ValueError(
                    "Source files must use the same column order for positional data comparison."
                )
            for row in reader:
                # CSV header is line 1, so the first data row is line 2.
                rows.append((relative_source, reader.line_num, row))
    run_ids = [row["run_id"] for _, _, row in rows]
    if len(run_ids) != len(set(run_ids)):
        raise ValueError("run_id must be unique across the source files to align observations.")
    return rows


def selected_rows(path: Path, rows: list[tuple[str, int, dict[str, str]]]) -> set[tuple[str, int]]:
    filters = notebook_filters(path)
    task = filters["TASK"]
    if task not in TASKS:
        raise ValueError(f"Unknown task {task!r} in {path.name}")
    dataset, model = TASKS[task]
    configs = allowed_configs(filters["SLICE"], filters["INCLUDE_BASELINE"])
    target_stress = filters.get("TARGET_STRESS")
    selected: set[tuple[str, int]] = set()

    for source_name, line_number, row in rows:
        if row["Dataset"] != dataset or row["Model"] != model:
            continue
        if filters["CLIENTS"] is not None and int(float(row["Total Clients"])) != int(filters["CLIENTS"]):
            continue
        config_id = row["config_id"].strip()
        if configs is not None and config_id not in configs:
            continue
        if target_stress is not None:
            config = [part.strip().upper() for part in config_id.split(",")]
            active = [index for index, policy in enumerate(config) if policy == "ON"]
            if not active:
                continue
            stress_tokens = row_stress_tokens(row, f"{source_name}:{line_number}")
            code_by_position = {position: code for code, position in STRESS_CODES.items()}
            if any(
                stress_tokens.get(code_by_position[position]) != float(target_stress)
                for position in active
            ):
                continue
        selected.add((source_name, line_number))
    if not selected:
        raise ValueError(f"The filters in {path.name} select no source rows.")
    return selected


def normalized_data_frame(
    selected: set[tuple[str, int]],
    rows: list[tuple[str, int, dict[str, str]]],
    source_columns: list[str],
) -> tuple[pd.DataFrame, str]:
    """Create a positional-column frame for content comparison, keyed by run_id."""
    row_lookup = {(source, line): row for source, line, row in rows}
    frame = pd.DataFrame([row_lookup[key] for key in sorted(selected)], columns=source_columns)
    # Normalize field labels so DataComPy compares cell values in source-column order,
    # even for campaign labels whose capitalization differs (e.g., Dataset / DataSet).
    rename = {column: f"field_{index:03d}" for index, column in enumerate(source_columns)}
    normalized = frame.rename(columns=rename)
    return normalized, rename["run_id"]


def analyze_task(
    task: str,
    rows: list[tuple[str, int, dict[str, str]]],
) -> tuple[list[tuple[Path, set]], list[str], list[list[str]], bool]:
    task_dir = COMPACT / task
    notebooks = sorted(task_dir.glob("*.ipynb"))
    if not notebooks:
        raise ValueError(f"No notebooks found under {task_dir}")
    selections = [(path, selected_rows(path, rows)) for path in notebooks]
    report = [f"## {task.title()} ({len(selections)} notebooks)", ""]
    report.append("| Notebook | Selected rows |")
    report.append("|:---|---:|")
    for path, selected in selections:
        report.append(f"| `{path.name}` | {len(selected)} |")

    source_columns = list(rows[0][2])
    frames = {
        path: normalized_data_frame(selected, rows, source_columns)
        for path, selected in selections
    }
    data_matches: dict[frozenset[str], tuple[bool, int]] = {}
    for index, (path_a, _) in enumerate(selections):
        for path_b, _ in selections[index + 1 :]:
            frame_a, run_id_a = frames[path_a]
            frame_b, run_id_b = frames[path_b]
            if run_id_a != run_id_b:
                raise ValueError("Internal error: normalized run_id columns do not align.")
            comparison = PandasCompare(
                frame_a,
                frame_b,
                join_columns=[run_id_a],
                abs_tol=0,
                rel_tol=0,
                df1_name=path_a.name,
                df2_name=path_b.name,
                cast_column_names_lower=False,
            )
            data_matches[frozenset((path_a.name, path_b.name))] = (
                comparison.matches(), comparison.count_matching_rows()
            )

    matched_pairs = {pair for pair, (matches, _) in data_matches.items() if matches}
    duplicate_groups: list[list[str]] = []
    for path, _ in selections:
        group = [path.name]
        for other, _ in selections:
            if other == path:
                continue
            if frozenset((path.name, other.name)) in matched_pairs:
                group.append(other.name)
        unique_group = sorted(set(group))
        if len(unique_group) > 1 and unique_group not in duplicate_groups:
            duplicate_groups.append(unique_group)

    report.extend(["", "### Exact duplicate datasets by data values", ""])
    report.extend([
        f"`datacompy.PandasCompare` compared all {len(data_matches)} notebook pairs. Each frame uses positional field names and joins rows on unique `run_id`; all remaining cell values are compared at zero tolerance. `run_id` aligns the same observations, and source row order does not affect the result.",
        "**Review status: unresolved.** These pairs are flagged for review; no notebook is removed or reformulated by this check. Keep both until a decision is made about whether their distinct analysis purpose justifies the shared input population.",
        "",
    ])
    datacompy_mismatch = False
    if duplicate_groups:
        for group in duplicate_groups:
            first = next(path for path, _ in selections if path.name == group[0])
            frame, _ = frames[first]
            report.append(f"- **Review pending — {len(group)} notebooks, {len(frame)} identical rows:** "
                          + ", ".join(f"`{name}`" for name in group))
            for name_a, name_b in combinations(group, 2):
                matches, matched_rows = data_matches[frozenset((name_a, name_b))]
                status = "PASS" if matches else "MISMATCH"
                report.append(f"  - datacompy `{name_a}` ↔ `{name_b}`: **{status}**; {matched_rows} matching row IDs; all row values match={matches}.")
                datacompy_mismatch |= not matches
    else:
        report.append("No pair of notebook datasets has identical row IDs and data values.")

    subset_pairs = []
    overlap_pairs = []
    for index, (path_a, rows_a) in enumerate(selections):
        for path_b, rows_b in selections[index + 1 :]:
            intersection = len(rows_a & rows_b)
            if not intersection or rows_a == rows_b:
                continue
            if rows_a <= rows_b or rows_b <= rows_a:
                smaller, larger = (path_a, path_b) if len(rows_a) < len(rows_b) else (path_b, path_a)
                subset_pairs.append((smaller.name, larger.name, len(rows_a & rows_b), len(rows_a), len(rows_b)))
            else:
                overlap_pairs.append((path_a.name, path_b.name, intersection, len(rows_a), len(rows_b)))

    report.extend(["", "### Strict subset relationships", ""])
    if subset_pairs:
        report.extend(
            f"- `{small}` is fully contained in `{large}` ({shared}/{small_n} rows; larger set has {large_n})."
            for small, large, shared, small_n, large_n in subset_pairs
        )
    else:
        report.append("None.")

    report.extend(["", "### Other non-empty overlaps", ""])
    if overlap_pairs:
        report.append("| Notebook A | Notebook B | Shared rows | A rows | B rows |")
        report.append("|:---|:---|---:|---:|---:|")
        report.extend(
            f"| `{a}` | `{b}` | {shared} | {a_n} | {b_n} |"
            for a, b, shared, a_n, b_n in overlap_pairs
        )
    else:
        report.append("None.")
    return selections, report, duplicate_groups, datacompy_mismatch


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("text", "image", "both"), default="both")
    parser.add_argument("--output", type=Path, default=COMPACT / "notebook_dataset_overlap_report.md")
    args = parser.parse_args()

    rows = load_source_rows()
    tasks = ("text", "image") if args.task == "both" else (args.task,)
    output = [
        "# Compact Notebook Dataset Overlap Check",
        "",
        "Row-overlap counts use source CSV path and physical line number. Exact duplicate datasets are determined separately with DataComPy by comparing the actual selected row values, aligned on `run_id`, with original column labels ignored. Counts refer to source rows before ADEPT feature derivation; the maintained notebook filters do not filter on those derived features.",
        "",
        "An identical input population does not by itself mean the notebooks perform identical analyses: predictor exclusions, plots, summaries, or downstream procedures may differ.",
        "",
    ]
    failed = False
    for task in tasks:
        selections, task_report, duplicate_groups, datacompy_mismatch = analyze_task(task, rows)
        failed |= datacompy_mismatch
        output.extend(task_report + [""])
        print(f"{task}: {len(selections)} notebooks, "
              f"{sum(len(selected) for _, selected in selections)} total selected row memberships")
        if duplicate_groups:
            for group in duplicate_groups:
                print("  exact data match: " + ", ".join(group))
        else:
            print("  no exact duplicate datasets")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text("\n".join(output).rstrip() + "\n", encoding="utf-8")
    print(f"Report: {args.output.relative_to(ROOT) if args.output.is_relative_to(ROOT) else args.output}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
