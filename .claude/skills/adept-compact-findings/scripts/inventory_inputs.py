#!/usr/bin/env python3
"""Validate and fingerprint current compact ADEPT notebook analysis inputs."""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


TASKS = ("image", "text")
CASES = ("c4", "c8", "c10", "baseline", "client_selector", "message_compressor", "hdh")


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    return "".join(source) if isinstance(source, list) else str(source)


def relative(path: Path, root: Path) -> str:
    return path.relative_to(root).as_posix()


def file_record(path: Path, root: Path) -> dict[str, Any]:
    return {"path": relative(path, root), "size_bytes": path.stat().st_size, "sha256": sha256(path)}


def inspect_notebook(path: Path, root: Path, issues: list[str]) -> dict[str, Any]:
    notebook_path = relative(path, root)
    try:
        notebook = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        issues.append(f"Cannot read notebook {notebook_path}: {exc}")
        return {"path": notebook_path, "status": "invalid"}

    cells = notebook.get("cells", [])
    code_cells = [cell for cell in cells if cell.get("cell_type") == "code"]
    errors = [
        {"cell_id": cell.get("id"), "ename": output.get("ename"), "evalue": output.get("evalue")}
        for cell in cells for output in cell.get("outputs", [])
        if output.get("output_type") == "error"
    ]
    unexecuted = [
        cell.get("id", f"cell-{index}")
        for index, cell in enumerate(code_cells)
        if source_text(cell).strip() and cell.get("execution_count") is None
    ]
    if errors:
        issues.append(f"Notebook {notebook_path} contains {len(errors)} error output(s).")
    if unexecuted:
        issues.append(f"Notebook {notebook_path} has nonempty unexecuted code cells: {', '.join(unexecuted)}")

    sections = []
    for cell in cells:
        if cell.get("cell_type") == "markdown":
            sections.extend(line.strip() for line in source_text(cell).splitlines() if line.startswith("#"))
    all_source = "\n".join(source_text(cell) for cell in cells)
    plot_match = re.search(r"^PLOT_STEM\s*=\s*['\"]([^'\"]+)['\"]", all_source, re.MULTILINE)
    heatmap_match = re.search(r"^HEATMAP_STEM\s*=\s*['\"]([^'\"]+)['\"]", all_source, re.MULTILINE)
    if not plot_match or not heatmap_match:
        issues.append(f"Notebook {notebook_path} does not declare PLOT_STEM and HEATMAP_STEM.")
        return {"path": notebook_path, "sha256": sha256(path), "status": "invalid", "errors": errors, "unexecuted_cells": unexecuted, "sections": sections}

    task_dir = path.parent
    plot_paths = [
        task_dir / "plots" / f"{plot_match.group(1)}__final_val_accuracy-vs-avg_total_time.png",
        task_dir / "plots" / f"{heatmap_match.group(1)}.png",
    ]
    report_name = plot_match.group(1).replace("quality-space__", "boxes__") + ".md"
    report_path = task_dir / "boxes" / report_name
    for artifact in [*plot_paths, report_path]:
        if not artifact.is_file():
            issues.append(f"Missing expected artifact for {notebook_path}: {relative(artifact, root)}")

    stream_text = "\n".join(
        "".join(output.get("text", []))
        for cell in cells for output in cell.get("outputs", [])
        if output.get("output_type") == "stream"
    )
    if report_path.is_file() and "Saved box report:" not in stream_text:
        issues.append(f"Notebook {notebook_path} has no recorded successful box-report export output.")

    return {
        "path": notebook_path,
        "sha256": sha256(path),
        "status": "ready" if not errors and not unexecuted else "invalid",
        "code_cells": len(code_cells),
        "output_cells": sum(bool(cell.get("outputs")) for cell in code_cells),
        "errors": errors,
        "unexecuted_cells": unexecuted,
        "sections": sections,
        "box_report": file_record(report_path, root) if report_path.is_file() else None,
        "plots": [file_record(item, root) for item in plot_paths if item.is_file()],
    }


def inspect_task(root: Path, task: str) -> tuple[dict[str, Any], list[str]]:
    task_dir = root / "federatedlearning" / "compact" / task
    issues: list[str] = []
    notebooks = []
    for case in CASES:
        path = task_dir / f"analysis-fl-rq-{case}-{task}.ipynb"
        if path.is_file():
            notebooks.append(inspect_notebook(path, root, issues))
        else:
            issues.append(f"Missing expected notebook: {relative(path, root)}")

    campaign = root / "federatedlearning" / "compact"
    sources = []
    for path in (
        campaign / "FLsystem_compact_all.json",
        campaign / "adept_experiments_all_waves.csv",
        campaign / "adept_experiments_all_waves_combinedAP.csv",
    ):
        if path.is_file():
            sources.append(file_record(path, root))
        else:
            issues.append(f"Missing analysis source: {relative(path, root)}")

    manifest = {
        "task": task,
        "generated_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "status": "ready" if not issues and len(notebooks) == len(CASES) else "blocked",
        "research_questions": {
            "RQ1": "Which tradeoffs occur, and how do design choices relate to them?",
            "RQ2": "Which joint conditions identify a target tradeoff, and what changes inside the box?",
        },
        "sources": sources,
        "notebooks": notebooks,
        "issues": issues,
    }
    output_dir = task_dir / "findings"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / "evidence-manifest.json"
    manifest["manifest_path"] = relative(output_path, root)
    output_path.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return manifest, issues


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--task", choices=("image", "text", "both"), default="both")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[4]
    tasks = TASKS if args.task == "both" else (args.task,)
    failed = False
    for task in tasks:
        manifest, issues = inspect_task(root, task)
        print(f"{task}: {manifest['status']} — {manifest['manifest_path']}")
        if issues:
            failed = True
            for issue in issues:
                print(f"  - {issue}")
        else:
            print(f"  - {len(manifest['notebooks'])} executed notebooks; expected plots and box reports found")
    return 1 if failed else 0


if __name__ == "__main__":
    sys.exit(main())
