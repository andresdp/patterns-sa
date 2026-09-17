"""Model spec summary generator (R4/R5).

Renders a validated ``SystemDefinition`` as a human-readable Markdown
summary: each component's decisions and policies together with exactly
which parameters each policy's ``parameter_bindings`` sets (read directly
from the bindings, not inferred); parameters grouped by level/type and
flagged optional, cross-referenced against which decisions/policies
actually bind them versus free-standing levers/uncertainties no policy
touches; multi-decision configuration coverage (the declared configurations
diffed against the full cross-product of policies across a component's
decisions); and the declared quality objectives and tradeoffs.

This is deliberately a standalone utility, not a wrapper around
``adept/utils/linter.py``. Per this repo's Key Decision (spec-checking and
description stay separate), the coverage computation below is written
independently of ``SystemLinter._validate_policy_combination_coverage`` even
though the two compute the same thing.
"""
from __future__ import annotations

import itertools
from typing import Any, Dict, Iterable, List, Optional, Tuple

from ..core.models import (
    ArchitecturalPattern,
    Decision,
    Parameter,
    SystemDefinition,
)


def _iter_configs(configs: Any) -> Iterable[Any]:
    """Yield SystemConfiguration-like objects from either the dict or list form."""
    if isinstance(configs, dict):
        return configs.values()
    return configs or []


def _binding_items(bindings: Any) -> List[Tuple[str, str, Any]]:
    """Flatten a ParameterBindings object into (kind, param_name, value) triples."""
    items: List[Tuple[str, str, Any]] = []
    for kind in ("levers", "uncertainties", "constraints"):
        group = getattr(bindings, kind, None) or {}
        for name, value in group.items():
            items.append((kind, name, value))
    return items


def _collect_component_bindings(comp: ArchitecturalPattern) -> Dict[str, List[str]]:
    """Map parameter name -> list of "decision.policy (kind)" labels that bind it.

    Scans every policy's parameter_bindings (levers, uncertainties, and
    constraints sub-blocks) in every decision of the component.
    """
    bound_by: Dict[str, List[str]] = {}
    for decision_key, decision in comp.decisions.items():
        for policy_key, policy in decision.policies.items():
            for kind, param_name, _value in _binding_items(policy.parameter_bindings):
                bound_by.setdefault(param_name, []).append(
                    f"{decision_key}.{policy_key} ({kind})"
                )
    return bound_by


def _format_value(value: Any) -> str:
    if isinstance(value, str):
        return value
    return str(value)


def _level_type(param: Parameter) -> Tuple[str, str]:
    level = getattr(param.level, "value", str(param.level))
    ptype = getattr(param.type, "value", str(param.type))
    return level, ptype


def _optional_flag(param: Parameter) -> str:
    return " (optional)" if bool(getattr(param, "optional", False)) else ""


def _render_decisions(comp: ArchitecturalPattern) -> List[str]:
    lines: List[str] = []
    if not comp.decisions:
        lines.append("")
        lines.append("_No decisions declared._")
        return lines

    for decision_key, decision in comp.decisions.items():
        lines.append("")
        header = f"#### Decision: `{decision_key}`"
        lines.append(header)
        if decision.description:
            lines.append("")
            lines.append(decision.description)

        if not decision.policies:
            lines.append("")
            lines.append("_No policies declared._")
            continue

        for policy_key, policy in decision.policies.items():
            lines.append("")
            policy_line = f"- Policy `{policy_key}`"
            if policy.description:
                policy_line += f": {policy.description}"
            lines.append(policy_line)

            binding_items = _binding_items(policy.parameter_bindings)
            if not binding_items:
                lines.append("  - No parameter bindings (no-op policy).")
            else:
                for kind, param_name, value in binding_items:
                    lines.append(
                        f"  - [{kind}] `{param_name}` = `{_format_value(value)}`"
                    )
    return lines


def _render_parameters(comp: ArchitecturalPattern, bound_by: Dict[str, List[str]]) -> List[str]:
    lines: List[str] = []
    lines.append("")
    lines.append("#### Parameters")

    if not comp.parameters:
        lines.append("")
        lines.append("_No parameters declared._")
        return lines

    # Group parameter names by (level, type).
    groups: Dict[Tuple[str, str], List[str]] = {}
    for name, param in comp.parameters.items():
        groups.setdefault(_level_type(param), []).append(name)

    for (level, ptype), names in sorted(groups.items()):
        lines.append("")
        lines.append(f"**{level} / {ptype}**")
        for name in sorted(names):
            param = comp.parameters[name]
            flags = _optional_flag(param)
            binders = bound_by.get(name)
            if binders:
                binding_note = "bound by " + ", ".join(binders)
            else:
                binding_note = "free-standing (no policy binds this parameter)"
            lines.append(f"- `{name}`{flags} — {binding_note}")

    return lines


def _compute_coverage(
    comp_key: str, comp: ArchitecturalPattern, configs: Any
) -> Optional[Tuple[int, int, List[Tuple[str, ...]]]]:
    """Return (declared_count, total_count, missing_combinations) or None.

    None is returned for single-decision (or zero-decision) components,
    where coverage is trivially 1-of-1 and not worth reporting.
    """
    decision_keys = list(comp.decisions.keys())
    if len(decision_keys) <= 1:
        return None

    policy_lists = [list(comp.decisions[d].policies.keys()) for d in decision_keys]
    if any(len(policies) == 0 for policies in policy_lists):
        return None

    all_combos = list(itertools.product(*policy_lists))
    total = len(all_combos)

    declared: set = set()
    for config in _iter_configs(configs):
        refs = {
            ref.decision: ref.policy
            for ref in getattr(config, "pattern_policy_references", [])
            if ref.component == comp_key
        }
        if set(refs.keys()) != set(decision_keys):
            # Doesn't fully (or uniquely) cover this component's decisions;
            # not a valid combination to count (completeness is R1's job).
            continue
        declared.add(tuple(refs[d] for d in decision_keys))

    missing = [combo for combo in all_combos if combo not in declared]
    return len(declared), total, missing


def _render_coverage(comp_key: str, comp: ArchitecturalPattern, sys_def: SystemDefinition) -> List[str]:
    configs = sys_def.dataspace.configuration_identification.configurations
    result = _compute_coverage(comp_key, comp, configs)
    if result is None:
        return []

    declared_count, total, missing = result
    lines: List[str] = []
    lines.append("")
    lines.append("#### Configuration Coverage")
    lines.append("")
    lines.append(
        f"{declared_count} of {total} possible decision-policy combinations are declared."
    )
    if missing:
        missing_str = "; ".join(",".join(combo) for combo in missing)
        lines.append(f"Missing combinations: {missing_str}")
    return lines


def _render_component(comp_key: str, comp: ArchitecturalPattern, sys_def: SystemDefinition) -> List[str]:
    lines: List[str] = []
    lines.append("")
    lines.append(f"### Component: `{comp_key}` ({comp.name})")
    if comp.description:
        lines.append("")
        lines.append(comp.description)

    lines.extend(_render_decisions(comp))

    bound_by = _collect_component_bindings(comp)
    lines.extend(_render_parameters(comp, bound_by))
    lines.extend(_render_coverage(comp_key, comp, sys_def))

    return lines


def _render_quality_objectives(sys_def: SystemDefinition) -> List[str]:
    lines: List[str] = []
    lines.append("")
    lines.append("## Quality Objectives")

    objectives = sys_def.dataspace.quality_objectives
    if not objectives:
        lines.append("")
        lines.append("_No quality objectives declared._")
        return lines

    for obj in objectives:
        direction = "maximize" if obj.maximize else "minimize"
        detail = direction
        if obj.metric:
            detail += f", metric: {obj.metric}"
        line = f"- `{obj.name}` ({detail})"
        if obj.threshold is not None:
            line += f", threshold: {obj.threshold}"
        lines.append(line)
        if obj.description:
            lines.append(f"  - {obj.description}")

    return lines


def _render_tradeoffs(sys_def: SystemDefinition) -> List[str]:
    lines: List[str] = []
    lines.append("")
    lines.append("## Tradeoffs")

    tradeoffs = sys_def.system.tradeoffs
    if not tradeoffs:
        lines.append("")
        lines.append("_No tradeoffs declared._")
        return lines

    for tradeoff in tradeoffs:
        lines.append(f"- `{tradeoff.name}` ({tradeoff.scheme}): {tradeoff.label}")
        if tradeoff.description:
            lines.append(f"  - {tradeoff.description}")
        if tradeoff.elements:
            elements_str = ", ".join(f"{k}={v}" for k, v in tradeoff.elements.items())
            lines.append(f"  - Elements: {elements_str}")

    return lines


def summarize_system(sys_def: SystemDefinition) -> str:
    """Render a Markdown summary of a validated ``SystemDefinition``.

    Order: for each component -- name/description, decisions/policies with
    exactly which parameters each policy binds, parameters grouped by
    level/type/optional and cross-referenced against which policies bind
    them, and (for multi-decision components) configuration coverage;
    followed by the system's declared quality objectives and tradeoffs.
    """
    system = sys_def.system
    lines: List[str] = []

    lines.append(f"# {system.name}")
    if system.description:
        lines.append("")
        lines.append(system.description)

    lines.append("")
    lines.append("## Components")

    if not system.components:
        lines.append("")
        lines.append("_No components declared._")
    else:
        for comp_key, comp in system.components.items():
            lines.extend(_render_component(comp_key, comp, sys_def))

    if system.parameters:
        lines.append("")
        lines.append("## System-Level Parameters")
        for name, param in system.parameters.items():
            level, ptype = _level_type(param)
            flags = _optional_flag(param)
            lines.append(f"- `{name}`{flags} — {level} / {ptype}")

    lines.extend(_render_quality_objectives(sys_def))
    lines.extend(_render_tradeoffs(sys_def))

    return "\n".join(lines) + "\n"
