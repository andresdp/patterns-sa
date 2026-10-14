"""Markdown reports for ADEPT scenario-discovery boxes."""

from __future__ import annotations

import math
from numbers import Real
from pathlib import Path
from typing import Any, Mapping, Sequence


def _format_value(value: Any) -> str:
    if value is None:
        return "not available"
    if isinstance(value, Real):
        if not math.isfinite(float(value)):
            return "not available"
        if float(value).is_integer():
            return str(int(value))
        return f"{float(value):.4f}"
    return str(value).replace("|", "\\|")


def _heldout_by_target(metrics: Any) -> dict[str, dict[str, Any]]:
    if metrics is None:
        return {}
    if hasattr(metrics, "to_dict"):
        rows = metrics.to_dict(orient="records")
    else:
        rows = list(metrics)
    result = {}
    for row in rows:
        target = str(row.get("target", ""))
        result[target] = row
    return result


def write_box_report(
    session: Any,
    boxes_by_algorithm: Mapping[str, Sequence[Any]],
    heldout_metrics: Mapping[str, Any],
    output_path: str | Path,
    title: str,
    metadata: Mapping[str, Any] | None = None,
) -> Path:
    """Write PRIM/CART boxes, architectural context and available metrics to Markdown.

    `heldout_metrics` accepts per-algorithm DataFrames returned by the compact
    notebooks' `heldout_box_summary` function. Per-box discovery metrics are read from
    `box.discovery_metrics`; `box.metrics` is intentionally not used because it is a
    legacy compatibility alias for held-out metrics in the session API.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    lines = [f"# {title}", "", "## Analysis scope", ""]
    if metadata:
        lines.extend(f"- **{key}:** {_format_value(value)}" for key, value in metadata.items())
    else:
        lines.append("- Scope metadata was not supplied.")
    lines.extend([
        "",
        "## How to read the metrics",
        "",
        "- **Discovery metrics = training partition.** ADEPT uses these training runs to rank parameters and fit the PRIM/CART boxes. The table evaluates each learned rule on those same training runs.",
        "- **Held-out metrics = test partition.** Each fixed rule is applied to separate runs set aside by `partition_seed`; those runs were not used to discover the box. Every reported held-out metric, including prevalence and lift, is calculated from that test partition.",
        "- Compare the two sets: a drop in test precision or lift can indicate that the training association is less stable out of sample. Test recall/coverage shows how many target runs the rule still captures.",
        "- Precision is the share of runs inside the box that reach the target; recall/coverage is the share of target runs captured by the box. Absolute lift is precision minus the target prevalence in the same partition, reported as a proportion.",
        "- These are observational performance measures, not causal effects or guarantees for future deployments.",
        "",
        "The architectural interpretation traces conditions through declared system-spec relationships.",
        "",
    ])

    for algorithm, boxes in boxes_by_algorithm.items():
        lines.extend([f"## {algorithm}", ""])
        non_empty = [box for box in boxes if not box.is_empty()]
        if not non_empty:
            lines.extend(["No non-empty boxes were discovered by this algorithm.", ""])
            continue
        by_target = _heldout_by_target(heldout_metrics.get(algorithm))
        for index, box in enumerate(non_empty, start=1):
            labels = f" ({box.target_tradeoff_labels})" if box.target_tradeoff_labels else ""
            lines.extend([
                f"### Box {index} — {box.target_tradeoff}{labels}",
                "",
                "**Learned box conditions**",
                "",
            ])
            readable = box.describe_limits(digits=3)
            if readable:
                lines.extend(f"- `{parameter}`: {condition}" for parameter, condition in readable.items())
            else:
                lines.append("- No parameter conditions recorded.")
            missing = sorted(name for name, includes in (box.includes_na or {}).items() if includes)
            if missing:
                lines.append("- **Includes NaN / not-selected values:** " + ", ".join(f"`{name}`" for name in missing))
            else:
                lines.append("- **Includes NaN / not-selected values:** No")

            explanation = session.explain_box_context(box, output_format="markdown").get("text", "")
            explanation_lines = explanation.splitlines()
            if explanation_lines and explanation_lines[0].strip().lower() in {
                "**architectural interpretation**", "## architectural interpretation"
            }:
                explanation = "\n".join(explanation_lines[1:]).lstrip()
            lines.extend(["", "**Architectural interpretation**", "", explanation, ""])

            lines.extend(["**Discovery metrics (training partition)**", "", "| Metric | Value |", "|:---|---:|"])
            metric_labels = {
                "density": "Train precision / density",
                "coverage": "Train recall / coverage",
                "lift": "Train absolute lift",
                "population_prevalence": "Train target prevalence",
                "population_size": "Train observations",
                "total_targets": "Train target observations",
                "samples_in_box": "Train samples in box",
                "targets_in_box": "Train targets in box",
                "mean": "Discovery mean",
                "mass": "Discovery mass",
            }
            if box.discovery_metrics:
                lines.extend(
                    f"| {metric_labels.get(key, key.replace('_', ' ').capitalize())} | {_format_value(value)} |"
                    for key, value in box.discovery_metrics.items()
                )
            else:
                lines.append("| Discovery metrics | Not available |")

            if box.fit_diagnostics:
                lines.extend(["", "**Algorithm fit diagnostics**", "", "| Diagnostic | Value |", "|:---|---:|"])
                lines.extend(
                    f"| {key.replace('_', ' ').capitalize()} | {_format_value(value)} |"
                    for key, value in box.fit_diagnostics.items()
                )

            lines.extend(["", "**Held-out metrics (test partition)**", "", "| Metric | Value |", "|:---|---:|"])
            test = by_target.get(str(box.target_tradeoff))
            # The caller's partition evaluation is authoritative. Box metrics may
            # have been attached earlier in another feature representation.
            heldout = box.heldout_metrics
            if test is not None:
                heldout_items = [
                    ("Test runs", test.get("test_n")),
                    ("Target runs before box", test.get("baseline_target_n")),
                    ("Runs retained by box", test.get("box_n")),
                    ("Target runs inside box", test.get("target_in_box")),
                    ("Target prevalence before box", test.get("baseline_rate")),
                    ("Precision inside box", test.get("box_precision")),
                    ("Recall / target coverage", test.get("test_recall_coverage")),
                    ("Absolute lift over held-out prevalence", test.get("test_delta_rate")),
                ]
                lines.extend(f"| {label} | {_format_value(value)} |" for label, value in heldout_items)
            elif heldout:
                heldout_items = [
                    ("Test runs", heldout.get("population_size")),
                    ("Target runs before box", heldout.get("total_targets")),
                    ("Runs retained by box", heldout.get("samples_in_box")),
                    ("Target runs inside box", heldout.get("targets_in_box")),
                    ("Target prevalence before box", heldout.get("population_prevalence")),
                    ("Precision inside box", heldout.get("density")),
                    ("Recall / target coverage", heldout.get("coverage")),
                    ("Absolute lift over held-out prevalence", heldout.get("lift")),
                ]
                lines.extend(f"| {label} | {_format_value(value)} |" for label, value in heldout_items)
            else:
                lines.append("| Held-out evaluation | Not available |")
            lines.append("")

    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")
    return path


__all__ = ["write_box_report"]
