import json
from pathlib import Path

from adept.core.models import SystemDefinition
from adept.utils.spec_summary import summarize_system

# Anchored to this file's location, not the process cwd: some other test
# modules in this repo (e.g. federatedlearning/test_manual_simple.py) chdir()
# without restoring, which corrupts a bare relative path depending on test
# collection order.
REPO_ROOT = Path(__file__).resolve().parent.parent


def test_summarize_cqrs_single_decision_no_coverage_line():
    with open(REPO_ROOT / "patterns/CQRS/CQRS.json") as f:
        sys_def = SystemDefinition.model_validate(json.load(f))

    summary = summarize_system(sys_def)

    assert isinstance(summary, str) and len(summary) > 0
    # Single-decision component: coverage is trivially 1-of-1, no line expected.
    assert "Configuration Coverage" not in summary


def test_summarize_multi_decision_reports_coverage_gap():
    # Synthetic 3-binary-decision component mirroring FL's shape: 4 of 8
    # combinations declared, matching this repo's real FLsystem_split.json case.
    sys_def_dict = {
        "system": {
            "name": "Synthetic Multi-Decision System",
            "components": {
                "c1": {
                    "name": "C1",
                    "parameters": {
                        "p1": {"level": "pattern", "type": "constraint"},
                    },
                    "decisions": {
                        "d1": {"policies": {"OFF": {}, "ON": {
                            "parameter_bindings": {"constraints": {"p1": 1.0}}
                        }}},
                        "d2": {"policies": {"OFF": {}, "ON": {}}},
                        "d3": {"policies": {"OFF": {}, "ON": {}}},
                    },
                }
            },
            "tradeoffs": [],
        },
        "dataspace": {
            "quality_objectives": [{"name": "obj1", "metric": "unit"}],
            "configuration_identification": {
                "from": "column",
                "column": "config_id",
                "configurations": {
                    "OFF,OFF,OFF": {
                        "name": "OFF,OFF,OFF",
                        "pattern_policy_references": [
                            {"component": "c1", "decision": "d1", "policy": "OFF"},
                            {"component": "c1", "decision": "d2", "policy": "OFF"},
                            {"component": "c1", "decision": "d3", "policy": "OFF"},
                        ],
                    },
                    "ON,OFF,OFF": {
                        "name": "ON,OFF,OFF",
                        "pattern_policy_references": [
                            {"component": "c1", "decision": "d1", "policy": "ON"},
                            {"component": "c1", "decision": "d2", "policy": "OFF"},
                            {"component": "c1", "decision": "d3", "policy": "OFF"},
                        ],
                    },
                    "OFF,ON,OFF": {
                        "name": "OFF,ON,OFF",
                        "pattern_policy_references": [
                            {"component": "c1", "decision": "d1", "policy": "OFF"},
                            {"component": "c1", "decision": "d2", "policy": "ON"},
                            {"component": "c1", "decision": "d3", "policy": "OFF"},
                        ],
                    },
                    "OFF,OFF,ON": {
                        "name": "OFF,OFF,ON",
                        "pattern_policy_references": [
                            {"component": "c1", "decision": "d1", "policy": "OFF"},
                            {"component": "c1", "decision": "d2", "policy": "OFF"},
                            {"component": "c1", "decision": "d3", "policy": "ON"},
                        ],
                    },
                },
            },
        },
    }
    sys_def = SystemDefinition.model_validate(sys_def_dict)

    summary = summarize_system(sys_def)

    assert "4 of 8" in summary
    assert "p1" in summary  # policy binding renders the actual parameter name


def test_summarize_system_does_not_raise_on_empty_system():
    sys_def = SystemDefinition.model_validate({
        "system": {"name": "Empty"},
        "dataspace": {
            "configuration_identification": {"from": "column", "configurations": {}},
        },
    })

    summary = summarize_system(sys_def)

    assert isinstance(summary, str) and len(summary) > 0
