"""FL-campaign adapter that writes ADEPT box analysis as Markdown."""

from __future__ import annotations

import math
from numbers import Real
from pathlib import Path
from typing import Any, Mapping, Sequence

from adept.analysis.box_quality import (
    calculate_box_fitness,
    identify_duplicate_boxes,
    rank_box_results,
    rank_box_results_globally,
)


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


def _heldout_by_target(metrics: Any) -> dict[str, list[dict[str, Any]]]:
    if metrics is None:
        return {}
    if hasattr(metrics, "to_dict"):
        rows = metrics.to_dict(orient="records")
    else:
        rows = list(metrics)
    result: dict[str, list[dict[str, Any]]] = {}
    for row in rows:
        target = str(row.get("target", ""))
        result.setdefault(target, []).append(row)
    return result


def _as_number(value: Any) -> float | None:
    if not isinstance(value, Real):
        return None
    value = float(value)
    return value if math.isfinite(value) else None


def _heldout_values(box: Any, row: Mapping[str, Any] | None) -> dict[str, float | None]:
    """Normalize notebook summary rows and attached Box metrics to one shape."""
    if row is not None:
        values = {
            "test_n": row.get("test_n"),
            "target_n": row.get("baseline_target_n"),
            "box_n": row.get("box_n"),
            "hits": row.get("target_in_box"),
            "baseline": row.get("baseline_rate"),
            "precision": row.get("box_precision"),
            "coverage": row.get("test_recall_coverage"),
        }
    else:
        metrics = box.heldout_metrics or {}
        values = {
            "test_n": metrics.get("population_size"),
            "target_n": metrics.get("total_targets"),
            "box_n": metrics.get("samples_in_box"),
            "hits": metrics.get("targets_in_box"),
            "baseline": metrics.get("population_prevalence"),
            "precision": metrics.get("density"),
            "coverage": metrics.get("coverage"),
        }
    return {key: _as_number(value) for key, value in values.items()}


def _box_record(box: Any, row: Mapping[str, Any] | None) -> dict[str, Any]:
    values = _heldout_values(box, row)
    train_metrics = box.discovery_metrics or {}
    train_fitness = calculate_box_fitness({
        "population_size": train_metrics.get("population_size"),
        "target_count": train_metrics.get("total_targets"),
        "selected_count": train_metrics.get("samples_in_box"),
        "precision": train_metrics.get("density"),
        "prevalence": train_metrics.get("population_prevalence"),
        "coverage": train_metrics.get("coverage"),
    })
    test_fitness = calculate_box_fitness({
        "population_size": values["test_n"],
        "target_count": values["target_n"],
        "selected_count": values["box_n"],
        "precision": values["precision"],
        "prevalence": values["baseline"],
        "coverage": values["coverage"],
    })
    status = test_fitness.status
    status = {
        "Unvalidated: evaluation unavailable": "Unvalidated: held-out evaluation unavailable",
        "Unvalidated: target count unavailable": "Unvalidated: held-out target count unavailable",
        "Unvalidated: no target examples": "Unvalidated: no held-out target examples",
        "Evaluated: no rows selected": "Evaluated: no held-out rows selected",
        "Not scoreable: evaluation metrics incomplete": "Not scoreable: held-out metrics incomplete",
    }.get(status, status)
    enrichment = test_fitness.normalized_enrichment
    score = test_fitness.score
    train_score = train_fitness.score

    return {
        **values,
        "enrichment": enrichment,
        "score": score,
        "train_score": train_score,
        "score_change": score - train_score if score is not None and train_score is not None else None,
        "status": status,
        "condition_count": len(box.limits),
    }


def _membership_masks(session: Any, records: list[dict[str, Any]]) -> dict[str, Any]:
    """Build shared-evaluator masks over held-out rows for behavior-level comparison."""
    try:
        raw, _, _ = session._get_subset_data("test")
    except (RuntimeError, AttributeError):
        return {}
    if raw.empty:
        return {}
    from adept.analysis.discovery import BoxEvaluator

    encoded = session._encode_for_boxes(raw)
    masks = {}
    for record in records:
        try:
            masks[record["id"]] = BoxEvaluator.membership_mask(
                encoded, record["box"], raw_X=raw
            )
        except (KeyError, TypeError, ValueError):
            continue
    return masks


def _mark_duplicates(
    session: Any,
    records: list[dict[str, Any]],
    condition_threshold: float,
    membership_threshold: float,
) -> None:
    masks = _membership_masks(session, records)
    parameter_ranges = {}
    raw = getattr(session, "experiments_df", None)
    if raw is not None:
        for name in raw.columns:
            try:
                values = raw[name].astype(float)
                if values.notna().any():
                    parameter_ranges[name] = (float(values.min()), float(values.max()))
            except (TypeError, ValueError):
                continue
    matches = identify_duplicate_boxes(
        {record["id"]: record["box"] for record in records},
        parameter_ranges=parameter_ranges,
        membership_masks=masks,
        condition_threshold=condition_threshold,
        membership_threshold=membership_threshold,
    )
    records_by_id = {record["id"]: record for record in records}
    for match in matches:
        details = []
        if match.kind != "Exact duplicate":
            details.append(f"condition similarity {match.condition_similarity:.0%}")
            if match.membership_jaccard is not None:
                details.append(f"held-out membership Jaccard {match.membership_jaccard:.0%}")
            else:
                details.append("condition-only comparison")
        suffix = f" ({'; '.join(details)})" if details else ""
        records_by_id[match.box_id]["duplicate_mark"] = (
            f"{match.kind} of {match.representative_id}{suffix}"
        )
        records_by_id[match.representative_id].setdefault("duplicate_peers", []).append(match.box_id)


def write_box_report(
    session: Any,
    boxes_by_algorithm: Mapping[str, Sequence[Any]],
    heldout_metrics: Mapping[str, Any],
    output_path: str | Path,
    title: str,
    metadata: Mapping[str, Any] | None = None,
    duplicate_condition_threshold: float = 0.90,
    duplicate_membership_threshold: float = 0.95,
) -> Path:
    """Write PRIM/CART boxes, architectural context and available metrics to Markdown.

    `heldout_metrics` accepts per-algorithm DataFrames returned by the compact
    notebooks' `heldout_box_summary` function. Per-box discovery metrics are read from
    `box.discovery_metrics`; `box.metrics` is intentionally not used because it is a
    legacy compatibility alias for held-out metrics in the session API. The report
    ranks boxes per target by the harmonic mean of normalized held-out enrichment and
    coverage. Duplicate thresholds control near-duplicate labels; duplicates remain
    in the report. Boxes without held-out target evidence are marked unvalidated.
    """
    if not 0.0 <= duplicate_condition_threshold <= 1.0:
        raise ValueError("duplicate_condition_threshold must be between 0 and 1.")
    if not 0.0 <= duplicate_membership_threshold <= 1.0:
        raise ValueError("duplicate_membership_threshold must be between 0 and 1.")

    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    records: list[dict[str, Any]] = []
    records_by_algorithm: dict[str, list[dict[str, Any]]] = {}
    for algorithm, boxes in boxes_by_algorithm.items():
        queues = _heldout_by_target(heldout_metrics.get(algorithm))
        offsets: dict[str, int] = {}
        algorithm_records = []
        for index, box in enumerate((candidate for candidate in boxes if not candidate.is_empty()), start=1):
            target = str(box.target_tradeoff)
            offset = offsets.get(target, 0)
            target_rows = queues.get(target, [])
            heldout_row = target_rows[offset] if offset < len(target_rows) else None
            offsets[target] = offset + 1
            record = {
                "id": f"{algorithm} Box {index}",
                "algorithm": algorithm,
                "index": index,
                "box": box,
                "heldout_row": heldout_row,
            }
            record.update(_box_record(box, heldout_row))
            algorithm_records.append(record)
            records.append(record)
        records_by_algorithm[algorithm] = algorithm_records

    _mark_duplicates(
        session,
        records,
        condition_threshold=duplicate_condition_threshold,
        membership_threshold=duplicate_membership_threshold,
    )

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
        "## Cross-algorithm box ranking and duplicate marks",
        "",
        "The table includes a **global rank** across all scoreable boxes and a **within-target rank** that compares PRIM/CART boxes for the same tradeoff. The held-out score is the harmonic mean of normalized enrichment and target coverage: normalized enrichment = max(0, (precision − baseline prevalence) / (1 − baseline prevalence)); score = 2 × enrichment × coverage / (enrichment + coverage). The score ranges from 0 to 1. Compare ranks alongside target support counts because tradeoffs can have different numbers of held-out examples; training-to-test stability and rule complexity are also shown.",
        "",
        "**Unvalidated** means the held-out evaluation is unavailable or contains no target examples, so the rule has no held-out target evidence. A supported rule that selects no held-out rows is evaluated with score 0. Duplicate checks compare boxes for the same target only. Exact duplicates have identical readable conditions, including categories and NaN/not-selected inclusion. Near duplicates require the same constrained parameters and at least "
        f"{duplicate_condition_threshold:.0%} condition similarity; when held-out membership can be compared, it must also reach {duplicate_membership_threshold:.0%} Jaccard similarity. Duplicate boxes are retained and individually marked.",
        "",
    ])

    ranking_inputs = [
        {**record, "target": str(record["box"].target_tradeoff)} for record in records
    ]
    ranked_by_target = rank_box_results(ranking_inputs)
    ranked_globally = rank_box_results_globally(ranking_inputs)
    if ranked_globally:
        target_rank_by_id = {
            record["id"]: rank
            for target_records in ranked_by_target.values()
            for rank, record in target_records
        }
        lines.extend([
            "| Global rank | Within-target rank | Target | Box | Status | Test score | Train score | Score Δ (test−train) | Enrichment | Coverage | Hits / targets | Retained / test | Conditions | Duplicate mark |",
            "|---:|---:|:---|:---|:---|---:|---:|---:|---:|---:|---:|---:|---:|:---|",
        ])
        for global_rank, record in ranked_globally:
            global_rank_text = str(global_rank) if global_rank is not None else "—"
            target_rank = target_rank_by_id.get(record["id"])
            target_rank_text = str(target_rank) if target_rank is not None else "—"
            target = record["target"]
            values = record
            hits = f"{_format_value(values['hits'])} / {_format_value(values['target_n'])}"
            retained = f"{_format_value(values['box_n'])} / {_format_value(values['test_n'])}"
            duplicate = values.get("duplicate_mark")
            if not duplicate and values.get("duplicate_peers"):
                duplicate = "Representative for " + ", ".join(values["duplicate_peers"])
            duplicate = duplicate or "—"
            lines.append(
                f"| {global_rank_text} | {target_rank_text} | {target} | {record['id']} | {values['status']} | "
                f"{_format_value(values['score'])} | {_format_value(values['train_score'])} | "
                f"{_format_value(values['score_change'])} | {_format_value(values['enrichment'])} | "
                f"{_format_value(values['coverage'])} | {hits} | {retained} | "
                f"{values['condition_count']} | {duplicate} |"
            )
        lines.append("")

    for algorithm, algorithm_records in records_by_algorithm.items():
        lines.extend([f"## {algorithm}", ""])
        if not algorithm_records:
            lines.extend(["No non-empty boxes were discovered by this algorithm.", ""])
            continue
        for record in algorithm_records:
            box = record["box"]
            index = record["index"]
            labels = f" ({box.target_tradeoff_labels})" if box.target_tradeoff_labels else ""
            marks = []
            if record["status"].startswith("Unvalidated"):
                marks.append(record["status"])
            if record.get("duplicate_mark"):
                marks.append(record["duplicate_mark"])
            elif record.get("duplicate_peers"):
                marks.append("Representative for " + ", ".join(record["duplicate_peers"]))
            mark_text = " — " + "; ".join(marks) if marks else ""
            lines.extend([
                f"### Box {index} — {box.target_tradeoff}{labels}{mark_text}",
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
            test = record["heldout_row"]
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
