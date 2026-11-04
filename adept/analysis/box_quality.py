"""Domain-neutral scoring, ranking, and comparison for scenario-discovery boxes."""

from __future__ import annotations

import math
from collections.abc import Mapping, Sequence
from typing import Any

import numpy as np
from pydantic import BaseModel, ConfigDict

from ..core.models import Box


class BoxFitness(BaseModel):
    """A target box's validation evidence and normalized fitness components."""

    normalized_enrichment: float | None = None
    coverage: float | None = None
    score: float | None = None
    status: str

    model_config = ConfigDict(extra="allow")


class BoxDuplicateMatch(BaseModel):
    """A duplicate relation; boxes are identified by caller-supplied stable IDs."""

    box_id: str
    representative_id: str
    kind: str
    condition_similarity: float
    membership_jaccard: float | None = None
    comparison_basis: str


def _number(value: Any) -> float | None:
    try:
        result = float(value)
    except (TypeError, ValueError):
        return None
    return result if math.isfinite(result) else None


def _normalized_enrichment(precision: float | None, prevalence: float | None) -> float | None:
    """Scale precision above baseline prevalence to [0, 1]."""
    if precision is None or prevalence is None or prevalence >= 1.0:
        return None
    return max(0.0, min(1.0, (precision - prevalence) / (1.0 - prevalence)))


def calculate_box_fitness(evaluation: Mapping[str, Any]) -> BoxFitness:
    """Score a box from one partition's canonical evaluation metrics.

    Required metric keys are ``population_size``, ``target_count``,
    ``selected_count``, ``precision``, ``prevalence``, and ``coverage``. Missing
    target support is unvalidated; a supported box selecting no rows is evaluated
    with score zero. The score is the harmonic mean of normalized enrichment and
    target coverage.
    """
    population_size = _number(evaluation.get("population_size"))
    target_count = _number(evaluation.get("target_count"))
    selected_count = _number(evaluation.get("selected_count"))
    precision = _number(evaluation.get("precision"))
    prevalence = _number(evaluation.get("prevalence"))
    coverage = _number(evaluation.get("coverage"))

    if population_size is None or population_size <= 0:
        return BoxFitness(status="Unvalidated: evaluation unavailable")
    if target_count is None:
        return BoxFitness(status="Unvalidated: target count unavailable")
    if target_count <= 0:
        return BoxFitness(status="Unvalidated: no target examples")
    if prevalence is not None and prevalence >= 1.0:
        return BoxFitness(status="No baseline headroom")
    if selected_count == 0:
        return BoxFitness(normalized_enrichment=0.0, coverage=0.0, score=0.0,
                          status="Evaluated: no rows selected")

    enrichment = _normalized_enrichment(precision, prevalence)
    if enrichment is None or coverage is None:
        return BoxFitness(status="Not scoreable: evaluation metrics incomplete")
    coverage = max(0.0, min(1.0, coverage))
    denominator = enrichment + coverage
    score = 2.0 * enrichment * coverage / denominator if denominator else 0.0
    return BoxFitness(
        normalized_enrichment=enrichment,
        coverage=coverage,
        score=score,
        status="Evaluated",
    )


def _canonical_conditions(box: Box) -> tuple[Any, ...]:
    conditions = []
    for parameter, entry in sorted(box.readable_limits().items()):
        includes_na = bool(entry.get("includes_na", False))
        if "in" in entry:
            condition = ("categories", tuple(sorted(map(str, entry["in"]))), includes_na)
        else:
            condition = ("numeric", float(entry["min"]), float(entry["max"]), includes_na)
        conditions.append((parameter, condition))
    return tuple(conditions)


def _interval_similarity(first: float, second: float, scale: float) -> float:
    if first == second:
        return 1.0
    if not math.isfinite(first) or not math.isfinite(second):
        return 0.0
    return max(0.0, 1.0 - abs(first - second) / scale)


def _condition_similarity(
    first: Box,
    second: Box,
    parameter_ranges: Mapping[str, tuple[float, float]] | None,
) -> float | None:
    first_conditions = first.readable_limits()
    second_conditions = second.readable_limits()
    if first_conditions.keys() != second_conditions.keys():
        return None
    if not first_conditions:
        return 1.0

    similarities = []
    for parameter in first_conditions:
        a, b = first_conditions[parameter], second_conditions[parameter]
        if bool(a.get("includes_na", False)) != bool(b.get("includes_na", False)):
            return 0.0
        if "in" in a or "in" in b:
            if "in" not in a or "in" not in b:
                similarities.append(0.0)
                continue
            values_a, values_b = set(map(str, a["in"])), set(map(str, b["in"]))
            union = values_a | values_b
            similarities.append(len(values_a & values_b) / len(union) if union else 1.0)
            continue

        scale = 0.0
        if parameter_ranges and parameter in parameter_ranges:
            lower, upper = parameter_ranges[parameter]
            scale = float(upper) - float(lower)
        if scale <= 0:
            finite_bounds = [
                float(value)
                for value in (a["min"], a["max"], b["min"], b["max"])
                if math.isfinite(float(value))
            ]
            scale = max((max(finite_bounds) - min(finite_bounds)) if finite_bounds else 0.0, 1.0)
        lower_similarity = _interval_similarity(float(a["min"]), float(b["min"]), scale)
        upper_similarity = _interval_similarity(float(a["max"]), float(b["max"]), scale)
        similarities.append((lower_similarity + upper_similarity) / 2.0)
    return sum(similarities) / len(similarities)


def _membership_jaccard(first: Any, second: Any) -> float | None:
    if first is None or second is None:
        return None
    first_mask = np.asarray(first, dtype=bool)
    second_mask = np.asarray(second, dtype=bool)
    if first_mask.shape != second_mask.shape:
        return None
    union = np.logical_or(first_mask, second_mask)
    count = int(union.sum())
    return float(np.logical_and(first_mask, second_mask).sum() / count) if count else None


def identify_duplicate_boxes(
    boxes: Mapping[str, Box],
    *,
    parameter_ranges: Mapping[str, tuple[float, float]] | None = None,
    membership_masks: Mapping[str, Any] | None = None,
    condition_threshold: float = 0.90,
    membership_threshold: float = 0.95,
) -> list[BoxDuplicateMatch]:
    """Find exact and near duplicates among boxes with the same target.

    Near-duplicate matching requires the same constrained parameters and the
    configured condition similarity. When masks are supplied for both boxes,
    their selected-row Jaccard similarity must also meet ``membership_threshold``.
    Without comparable masks the result is explicitly marked as condition-only.
    The function returns relationships and never removes or mutates boxes.
    """
    for name, threshold in (
        ("condition_threshold", condition_threshold),
        ("membership_threshold", membership_threshold),
    ):
        if not 0.0 <= threshold <= 1.0:
            raise ValueError(f"{name} must be between 0 and 1.")

    representatives: dict[str, list[tuple[str, Box]]] = {}
    matches: list[BoxDuplicateMatch] = []
    masks = membership_masks or {}
    for box_id, box in boxes.items():
        target = str(box.target_tradeoff)
        prior = representatives.setdefault(target, [])
        for representative_id, representative in prior:
            exact = _canonical_conditions(box) == _canonical_conditions(representative)
            similarity = _condition_similarity(box, representative, parameter_ranges)
            membership_similarity = _membership_jaccard(
                masks.get(box_id), masks.get(representative_id)
            )
            near = (
                similarity is not None
                and similarity >= condition_threshold
                and (membership_similarity is None or membership_similarity >= membership_threshold)
            )
            if exact or near:
                kind = "Exact duplicate" if exact else "Near duplicate"
                basis = "exact conditions" if exact else "conditions"
                if not exact and membership_similarity is not None:
                    basis += " and held-out membership"
                matches.append(BoxDuplicateMatch(
                    box_id=box_id,
                    representative_id=representative_id,
                    kind=kind,
                    condition_similarity=1.0 if exact else float(similarity or 0.0),
                    membership_jaccard=membership_similarity,
                    comparison_basis=basis,
                ))
                break
        else:
            prior.append((box_id, box))
    return matches


def rank_box_results(records: Sequence[Mapping[str, Any]]) -> dict[str, list[tuple[int | None, Mapping[str, Any]]]]:
    """Rank score-bearing records within each target; leave unscored rows unranked."""
    grouped: dict[str, list[Mapping[str, Any]]] = {}
    for record in records:
        grouped.setdefault(str(record.get("target", "")), []).append(record)

    ranked: dict[str, list[tuple[int | None, Mapping[str, Any]]]] = {}
    for target, target_records in grouped.items():
        ordered = sorted(
            target_records,
            key=lambda record: (
                record.get("score") is None,
                -(float(record["score"]) if record.get("score") is not None else -1.0),
                -(float(record["hits"]) if record.get("hits") is not None else -1.0),
                int(record.get("condition_count", 0)),
                str(record.get("algorithm", "")),
                int(record.get("index", 0)),
            ),
        )
        rank = 0
        ranked[target] = []
        for record in ordered:
            if record.get("score") is None:
                ranked[target].append((None, record))
            else:
                rank += 1
                ranked[target].append((rank, record))
    return ranked


def rank_box_results_globally(
    records: Sequence[Mapping[str, Any]],
) -> list[tuple[int | None, Mapping[str, Any]]]:
    """Rank score-bearing records across all targets; leave unscored rows unranked."""
    ordered = sorted(
        records,
        key=lambda record: (
            record.get("score") is None,
            -(float(record["score"]) if record.get("score") is not None else -1.0),
            -(float(record["hits"]) if record.get("hits") is not None else -1.0),
            int(record.get("condition_count", 0)),
            str(record.get("target", "")),
            str(record.get("algorithm", "")),
            int(record.get("index", 0)),
        ),
    )
    rank = 0
    result = []
    for record in ordered:
        if record.get("score") is None:
            result.append((None, record))
        else:
            rank += 1
            result.append((rank, record))
    return result


__all__ = [
    "BoxDuplicateMatch",
    "BoxFitness",
    "calculate_box_fitness",
    "identify_duplicate_boxes",
    "rank_box_results",
    "rank_box_results_globally",
]
