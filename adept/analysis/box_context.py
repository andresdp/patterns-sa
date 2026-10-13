"""Specification-only architectural context for decoded scenario-discovery boxes."""

from __future__ import annotations

from typing import Any, Dict, List, Mapping, Optional, Tuple

from ..core.models import Box, SystemConfiguration, SystemDefinition


def _value(value: Any) -> Any:
    return getattr(value, "value", value)


def _configs(sys_def: SystemDefinition) -> List[Tuple[str, SystemConfiguration]]:
    configs = sys_def.dataspace.configuration_identification.configurations
    if isinstance(configs, dict):
        return list(configs.items())
    return [(config.name, config) for config in configs]


def _policy_bindings(policy: Any) -> Dict[str, Any]:
    groups = policy.parameter_bindings
    result: Dict[str, Any] = {}
    for group in (groups.levers, groups.uncertainties, groups.constraints):
        result.update(group)
    return result


def _matches(value: Any, condition: Mapping[str, Any]) -> Optional[bool]:
    """Check a policy binding against a decoded categorical or numeric condition."""
    if value is None or str(value).strip().lower() in {"nan", "none", "(not selected)"}:
        return bool(condition.get("includes_na")) or "(not selected)" in condition.get("in", [])
    if "in" in condition:
        return str(value) in {str(choice) for choice in condition["in"]}
    if not isinstance(value, (int, float)):
        return None
    try:
        low = float(condition.get("min", float("-inf")))
        high = float(condition.get("max", float("inf")))
        return low <= float(value) <= high
    except (TypeError, ValueError):
        return None


def _decision_label(decision: str) -> str:
    known = {
        "client_selector_pattern": "Client Selector",
        "message_compressor_pattern": "Message Compressor",
        "hdh_pattern": "HDH",
    }
    name = decision[:-8] if decision.endswith("_pattern") else decision
    return known.get(decision, name.replace("_", " ").title())


def _parameter_label(name: str) -> str:
    return {
        "Client Selector Strategy": "Strategy",
        "Client Selector Criteria": "Criteria",
        "Client Selector Value": "Value",
        "Message Compressor Alg": "Algorithm",
        "non_iid_percentage": "non-IID percentage",
        "delay_percentage": "delay percentage",
        "low_spec_percentage": "low-spec percentage",
    }.get(name, name.replace("_", " "))


def _format_value(value: Any) -> str:
    if isinstance(value, float):
        return f"{value:.1f}" if value.is_integer() else f"{value:g}"
    return str(value)


class BoxContextExplainer:
    """Trace decoded conditions through relationships declared by a system JSON."""

    def explain(
        self,
        box: Box,
        sys_def: SystemDefinition,
        digits: int = 3,
        observed_configuration_counts: Optional[Mapping[str, int]] = None,
        observed_scope: Optional[str] = None,
        observed_row_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        params: Dict[str, Dict[str, Any]] = {}
        aliases: Dict[str, List[str]] = {}

        def add_parameter(name: str, parameter: Any, component: Optional[str]) -> None:
            canonical = parameter.name or name
            params[canonical] = {
                "name": canonical,
                "role": str(_value(parameter.type)),
                "level": str(_value(parameter.level)),
                "description": parameter.description,
                "component": component,
                "optional": bool(parameter.optional),
            }
            for alias in {name, canonical}:
                aliases.setdefault(alias, []).append(canonical)

        for name, parameter in sys_def.system.parameters.items():
            add_parameter(name, parameter, None)
        for component_id, component in sys_def.system.components.items():
            for name, parameter in component.parameters.items():
                add_parameter(name, parameter, component_id)
        for source, target in sys_def.dataspace.column_renames.items():
            if target in params:
                aliases.setdefault(source, []).append(target)
            if source in params:
                aliases.setdefault(target, []).append(source)

        conditions: List[Dict[str, Any]] = []
        for source_name, decoded in box.readable_limits().items():
            candidates = list(dict.fromkeys(aliases.get(source_name, [])))
            if not candidates and source_name in params:
                candidates = [source_name]
            if len(candidates) != 1:
                conditions.append({
                    "parameter": source_name,
                    "condition": decoded,
                    "status": "unresolved" if not candidates else "ambiguous",
                    "declarations": candidates,
                })
                continue
            info = params[candidates[0]]
            conditions.append({
                "parameter": candidates[0],
                "condition": decoded,
                "role": info["role"],
                "level": info["level"],
                "component": info["component"],
                "description": info["description"],
                "status": "resolved",
            })

        policies: Dict[Tuple[str, str, str], Dict[str, Any]] = {}
        decisions_by_parameter: Dict[str, set[Tuple[str, str]]] = {}
        for component_id, component in sys_def.system.components.items():
            for decision_id, decision in component.decisions.items():
                for policy_id, policy in decision.policies.items():
                    values = _policy_bindings(policy)
                    policies[(component_id, decision_id, policy_id)] = values
                    for parameter in values:
                        decisions_by_parameter.setdefault(parameter, set()).add((component_id, decision_id))

        configs = _configs(sys_def)
        policy_traces: List[Dict[str, Any]] = []
        for (component_id, decision_id, policy_id), values in policies.items():
            selected_by = [
                config_id for config_id, config in configs
                if any((ref.component, ref.decision, ref.policy) == (component_id, decision_id, policy_id)
                       for ref in config.pattern_policy_references)
            ]
            for parameter, value in values.items():
                policy_traces.append({
                    "component": component_id,
                    "decision": decision_id,
                    "policy": policy_id,
                    "parameter": parameter,
                    "value": value,
                    "configurations": selected_by,
                })

        for condition in conditions:
            condition["bindings"] = []
            if condition["status"] != "resolved":
                continue
            for trace in policy_traces:
                if trace["parameter"] == condition["parameter"]:
                    condition["bindings"].append({
                        **trace,
                        "matches_box": _matches(trace["value"], condition["condition"]),
                    })

        configurations: List[Dict[str, Any]] = []
        for config_id, config in configs:
            tests: List[str] = []
            traces: List[Dict[str, Any]] = []
            for condition in conditions:
                if condition["status"] != "resolved":
                    tests.append("unresolved")
                    continue
                parameter = condition["parameter"]
                relevant = decisions_by_parameter.get(parameter, set())
                if not relevant:
                    # Independent levers and uncertainties remain free for a configuration.
                    continue
                observed_values: List[Any] = []
                unknown = False
                for ref in config.pattern_policy_references:
                    if (ref.component, ref.decision) not in relevant:
                        continue
                    policy_values = policies.get((ref.component, ref.decision, ref.policy), {})
                    if parameter in policy_values:
                        value = policy_values[parameter]
                    elif params[parameter]["optional"] and params[parameter]["component"] == ref.component:
                        # An optional pattern setting's absent binding is its declared
                        # not-selected state for this selected pattern policy.
                        value = "(not selected)"
                    else:
                        unknown = True
                        continue
                    observed_values.append(value)
                    traces.append({
                        "parameter": parameter,
                        "component": ref.component,
                        "decision": ref.decision,
                        "policy": ref.policy,
                        "value": value,
                    })
                if unknown and not observed_values:
                    tests.append("unresolved")
                elif observed_values:
                    matches = [_matches(value, condition["condition"]) for value in observed_values]
                    tests.append("conflict" if False in matches else "unresolved" if None in matches else "match")

            if "conflict" in tests:
                status = "conflicts_with_box_conditions"
            elif "unresolved" in tests:
                status = "not_determined_by_specification"
            elif "match" in tests:
                status = "matches_box_conditions"
            else:
                status = "not_restricted_by_policy_bindings"
            configurations.append({"id": config_id, "name": config.name, "status": status, "binding_traces": traces})

        eligible = [c for c in configurations if c["status"] in {
            "matches_box_conditions", "not_restricted_by_policy_bindings"
        }]
        box_compatible = [c for c in configurations if c["status"] != "conflicts_with_box_conditions"]
        unresolved = any(c["status"] == "not_determined_by_specification" for c in configurations)
        decision_keys = {key for values in decisions_by_parameter.values() for key in values}
        prescriptions: List[Dict[str, Any]] = []
        if eligible and not unresolved:
            configs_by_id = dict(configs)
            for component_id, decision_id in sorted(decision_keys):
                choices = set()
                for candidate in eligible:
                    for ref in configs_by_id[candidate["id"]].pattern_policy_references:
                        if (ref.component, ref.decision) == (component_id, decision_id):
                            choices.add(ref.policy)
                if len(choices) != 1:
                    continue
                policy_id = next(iter(choices))
                values = policies.get((component_id, decision_id, policy_id), {})
                constrained = {
                    condition["parameter"] for condition in conditions
                    if condition.get("status") == "resolved"
                    and any(b["decision"] == decision_id and b["matches_box"] is True
                            for b in condition.get("bindings", []))
                }
                prescriptions.append({
                    "component": component_id,
                    "decision": decision_id,
                    "decision_label": _decision_label(decision_id),
                    "policy": policy_id,
                    "bindings": [
                        {"parameter": name, "value": value, "constrained_by_box": name in constrained}
                        for name, value in values.items()
                    ],
                })

        activation: List[Dict[str, Any]] = []
        configs_by_id = dict(configs)
        observed_counts = {
            str(config_id): max(0, int(count))
            for config_id, count in (observed_configuration_counts or {}).items()
        }
        for component_id, decision_id in sorted(decision_keys):
            policy_counts: Dict[str, int] = {}
            if observed_configuration_counts is not None:
                for config_id, count in observed_counts.items():
                    config = configs_by_id.get(config_id)
                    if config is None:
                        continue
                    for ref in config.pattern_policy_references:
                        if (ref.component, ref.decision) == (component_id, decision_id):
                            policy_counts[ref.policy] = policy_counts.get(ref.policy, 0) + count
                            break
                activation.append({
                    "component": component_id,
                    "decision": decision_id,
                    "decision_label": _decision_label(decision_id),
                    "policy_counts": policy_counts,
                    "source": "observed_box_rows",
                })
                continue

            possible_policies = set()
            for candidate in box_compatible:
                config = configs_by_id.get(candidate["id"])
                if config is None:
                    continue
                possible_policies.update(
                    ref.policy for ref in config.pattern_policy_references
                    if (ref.component, ref.decision) == (component_id, decision_id)
                )
            activation.append({
                "component": component_id,
                "decision": decision_id,
                "decision_label": _decision_label(decision_id),
                "possible_policies": sorted(possible_policies),
                "source": "specification_compatibility",
            })

        return {
            "box": {
                "target": box.target_tradeoff,
                "labels": box.target_tradeoff_labels,
                "method": box.method,
                "conditions": conditions,
            },
            "configurations": configurations,
            "design_prescriptions": prescriptions,
            "pattern_activation": activation,
            "observed_scope": observed_scope,
            "observed_row_count": observed_row_count,
            "prescription_status": "undetermined" if unresolved else "resolved_from_declared_configurations",
            "digits": max(0, int(digits)),
            "scope": "Specification-declared relationships only; no causal or empirical parent links inferred.",
        }

    @staticmethod
    def render(result: Mapping[str, Any], output_format: str = "plain") -> str:
        output_format = output_format.lower()
        if output_format not in {"plain", "markdown"}:
            raise ValueError("output_format must be 'plain' or 'markdown'")

        def label(text: str) -> str:
            return f"**{text}**" if output_format == "markdown" else text

        box = result["box"]
        bullet = "- " if output_format == "markdown" else "• "
        sub_bullet = "  - " if output_format == "markdown" else "  ◦ "
        lines = [label("Architectural interpretation"), f"{bullet}{label('Design prescription')}:"]
        if result["design_prescriptions"]:
            for prescription in result["design_prescriptions"]:
                settings = []
                for binding in prescription["bindings"]:
                    settings.append(f"{_parameter_label(binding['parameter'])} = {_format_value(binding['value'])}")
                detail = f" ({'; '.join(settings)})" if settings else ""
                lines.append(f"{sub_bullet}{prescription['decision_label']} = {prescription['policy']}{detail}")
        elif result["prescription_status"] == "undetermined":
            lines.append(f"{sub_bullet}Required pattern policy cannot be determined from the specification")
        else:
            lines.append(f"{sub_bullet}No pattern policy is required by the box conditions")

        activation = result.get("pattern_activation", [])
        if activation:
            if activation[0].get("source") == "observed_box_rows":
                scope = result.get("observed_scope") or "observed rows"
                heading = f"Pattern activation among {scope} matching this box"
                lines.append(f"{bullet}{label(heading)}:")
                row_count = result.get("observed_row_count")
                if not row_count:
                    lines.append(f"{sub_bullet}No matching discovery rows; activation cannot be summarized")
                else:
                    for item in activation:
                        states = item.get("policy_counts", {})
                        if not states:
                            lines.append(f"{sub_bullet}{item['decision_label']}: not resolved from the observed configuration IDs")
                            continue
                        summary = ", ".join(
                            f"{policy} ({count}/{row_count})"
                            for policy, count in sorted(states.items())
                        )
                        lines.append(f"{sub_bullet}{item['decision_label']}: {summary}")
            else:
                lines.append(f"{bullet}{label('Pattern activation allowed by declared configurations')}:")
                for item in activation:
                    policies = item.get("possible_policies", [])
                    if not policies:
                        value = "not determined from the specification"
                    elif len(policies) == 1:
                        value = f"{policies[0]} only (box-compatible configurations)"
                    else:
                        value = f"{', '.join(policies)} (not fixed by the box)"
                    lines.append(f"{sub_bullet}{item['decision_label']} = {value}")

        uncertainties = [c for c in box["conditions"] if c.get("role") == "uncertainty"]
        levers = [c for c in box["conditions"] if c.get("role") == "lever"]
        prescribed_parameters = {
            binding["parameter"]
            for prescription in result["design_prescriptions"]
            for binding in prescription["bindings"]
            if binding["constrained_by_box"]
        }
        other = [
            c for c in box["conditions"]
            if c.get("role") not in {"uncertainty", "lever"}
            and c["parameter"] not in prescribed_parameters
        ]
        lines.append(f"{bullet}{label('Operating envelope')}:")
        digits = result.get("digits", 3)
        lines.extend(f"{sub_bullet}{_parameter_label(c['parameter'])} {_format_condition(c['parameter'], c['condition'], digits)}" for c in uncertainties)
        if not uncertainties:
            lines.append(f"{sub_bullet}No uncertainty conditions in this box")
        if levers:
            lines.append(f"{bullet}{label('Other design conditions')}:")
            lines.extend(f"{sub_bullet}{_parameter_label(c['parameter'])} {_format_condition(c['parameter'], c['condition'], digits)}" for c in levers)
        if other:
            lines.append(f"{bullet}{label('Other parameter conditions')}:")
            lines.extend(f"{sub_bullet}{_parameter_label(c['parameter'])} {_format_condition(c['parameter'], c['condition'], digits)}" for c in other)

        return "\n".join(lines)


def _format_condition(parameter: str, condition: Any, digits: int = 3) -> str:
    if not isinstance(condition, Mapping):
        return str(condition)
    if "in" in condition:
        return "{" + ", ".join(str(value) for value in condition["in"]) + "}"
    low, high = condition.get("min"), condition.get("max")
    suffix = " (%)" if "percentage" in parameter.lower() else ""
    if low is None and high is None:
        return str(condition)
    if low is None:
        return f"<= {high:.{digits}g}{suffix}"
    if high is None:
        return f">= {low:.{digits}g}{suffix}"
    return f"[{low:.{digits}g}, {high:.{digits}g}]{suffix}"


__all__ = ["BoxContextExplainer"]
