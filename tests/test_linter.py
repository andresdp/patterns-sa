
import os
import unittest
import pandas as pd
from adept.utils.linter import SystemLinter
from adept.core.models import SystemDefinition
from adept.core.loader import GenericDataLoader

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

class TestSystemLinter(unittest.TestCase):
    def setUp(self):
        self.linter = SystemLinter()
        
        # Valid Base System Definition
        self.base_sys_def = {
            "system": {
                "name": "Test",
                "components": {
                    "c1": {
                        "name": "C1",
                        "parameters": {"p1": {"level": "system", "type": "lever"}},
                        "decisions": {
                            "d1": {"policies": {"pol_a": {}, "pol_b": {}}}
                        }
                    }
                },
                "tradeoffs": [
                    {"name": "t1", "elements": {"obj1": "good"}}
                ]
            },
            "dataspace": {
                "quality_objectives": [{"name": "obj1", "metric": "unit"}],
                "policy_identification": {
                    "from": "column",
                    "column": "policy_col",
                    "policies": {
                        "1": {"name": "sys_pol_1", "component_policies": {"c1": "pol_a"}}
                    }
                }
            }
        }
        
        # Valid Base Data
        self.base_df = pd.DataFrame({
            "p1": [1, 2],
            "obj1": [0.1, 0.2],
            "policy_col": ["1", "1"]
        })

    def test_valid_system(self):
        sys_def = SystemDefinition.model_validate(self.base_sys_def)
        issues = self.linter.lint(sys_def, self.base_df)
        self.assertEqual(len(issues), 0, f"Expected no issues, got: {[str(i) for i in issues]}")

    def test_missing_objective_column(self):
        df = self.base_df.drop(columns=["obj1"])
        sys_def = SystemDefinition.model_validate(self.base_sys_def)
        issues = self.linter.lint(sys_def, df)
        self.assertTrue(any("Quality Objective 'obj1' not found" in str(i) for i in issues))

    def test_missing_parameter_column(self):
        df = self.base_df.drop(columns=["p1"])
        sys_def = SystemDefinition.model_validate(self.base_sys_def)
        issues = self.linter.lint(sys_def, df)
        self.assertTrue(any("Parameter 'p1'" in str(i) for i in issues))

    def test_invalid_tradeoff_objective(self):
        bad_def = self.base_sys_def.copy()
        bad_def["system"]["tradeoffs"] = [{"name": "t2", "elements": {"BAD_OBJ": "good"}}]
        sys_def = SystemDefinition.model_validate(bad_def)
        issues = self.linter.lint(sys_def, self.base_df)
        self.assertTrue(any("references undefined objective 'BAD_OBJ'" in str(i) for i in issues))

    def test_invalid_tradeoff_scheme(self):
        bad_def = self.base_sys_def.copy()
        bad_def["system"]["tradeoffs"] = [{"name": "t3", "scheme": "magic_scheme", "elements": {}}]
        sys_def = SystemDefinition.model_validate(bad_def)
        issues = self.linter.lint(sys_def, self.base_df)
        self.assertTrue(any("unsupported scheme 'magic_scheme'" in str(i) for i in issues))

    def test_invalid_component_policy(self):
        bad_def = self.base_sys_def.copy()
        bad_def["dataspace"]["policy_identification"]["policies"]["1"]["component_policies"]["c1"] = "INVALID_POL"
        sys_def = SystemDefinition.model_validate(bad_def)
        issues = self.linter.lint(sys_def, self.base_df)
        print(f"DEBUG ISSUES: {[str(i) for i in issues]}")
        self.assertTrue(any("references undefined policy 'INVALID_POL'" in str(i) for i in issues))

    def test_missing_policy_column(self):
        df = self.base_df.drop(columns=["policy_col"])
        sys_def = SystemDefinition.model_validate(self.base_sys_def)
        issues = self.linter.lint(sys_def, df)
        self.assertTrue(any("Configuration identification column 'policy_col' not found" in str(i) for i in issues))


class TestMultiDecisionLinting(unittest.TestCase):
    """R1/R2/R5: multi-decision completeness, coverage, and the degenerate
    single-decision case."""

    def setUp(self):
        self.linter = SystemLinter()

    @staticmethod
    def _build_sys_def(configs: dict) -> SystemDefinition:
        """Builds a SystemDefinition with one component ('mc') that has two
        decisions (d1: A/B, d2: X/Y), and the given configurations dict."""
        data = {
            "system": {
                "name": "MultiDecisionTest",
                "components": {
                    "mc": {
                        "name": "MC",
                        "parameters": {},
                        "decisions": {
                            "d1": {"policies": {"A": {}, "B": {}}},
                            "d2": {"policies": {"X": {}, "Y": {}}},
                        },
                    }
                },
                "tradeoffs": [],
            },
            "dataspace": {
                "quality_objectives": [],
                "policy_identification": {
                    "from": "column",
                    "column": "config_id",
                    "policies": configs,
                },
            },
        }
        return SystemDefinition.model_validate(data)

    def test_missing_decision_reference_is_error(self):
        """AE1: a configuration referencing only 1 of 2 decisions -> ERROR
        naming the missing decision."""
        sys_def = self._build_sys_def({
            "cfg1": {
                "name": "cfg1",
                "pattern_policy_references": [
                    {"component": "mc", "decision": "d1", "policy": "A"},
                    # d2 intentionally not referenced
                ],
            }
        })
        issues = self.linter._validate_multi_decision_completeness(sys_def)
        errors = [i for i in issues if i.level == "ERROR"]
        self.assertTrue(
            any("does not reference decision 'd2'" in i.message for i in errors),
            f"Expected an ERROR naming missing decision 'd2', got: {[str(i) for i in issues]}"
        )

    def test_duplicate_decision_reference_is_error(self):
        """AE2: a configuration with two references to the same
        component/decision pair -> ERROR for the duplicate."""
        sys_def = self._build_sys_def({
            "cfg1": {
                "name": "cfg1",
                "pattern_policy_references": [
                    {"component": "mc", "decision": "d1", "policy": "A"},
                    {"component": "mc", "decision": "d1", "policy": "B"},  # duplicate decision
                    {"component": "mc", "decision": "d2", "policy": "X"},
                ],
            }
        })
        issues = self.linter._validate_multi_decision_completeness(sys_def)
        errors = [i for i in issues if i.level == "ERROR"]
        self.assertTrue(
            any("references decision 'd1'" in i.message and "more than once" in i.message for i in errors),
            f"Expected an ERROR for duplicate 'd1' reference, got: {[str(i) for i in issues]}"
        )

    def test_partial_coverage_warns_with_missing_combinations_named(self):
        """Partial policy-combination coverage -> WARNING naming exactly the
        missing combinations (2 of 4 declared here: A,X and B,Y; missing
        A,Y and B,X)."""
        sys_def = self._build_sys_def({
            "cfg_ax": {
                "name": "cfg_ax",
                "pattern_policy_references": [
                    {"component": "mc", "decision": "d1", "policy": "A"},
                    {"component": "mc", "decision": "d2", "policy": "X"},
                ],
            },
            "cfg_by": {
                "name": "cfg_by",
                "pattern_policy_references": [
                    {"component": "mc", "decision": "d1", "policy": "B"},
                    {"component": "mc", "decision": "d2", "policy": "Y"},
                ],
            },
        })
        issues = self.linter._validate_policy_combination_coverage(sys_def)
        warnings = [i for i in issues if i.level == "WARNING"]
        self.assertEqual(len(warnings), 1, f"Expected exactly 1 coverage warning, got: {[str(i) for i in issues]}")
        message = warnings[0].message
        self.assertIn("A,Y", message)
        self.assertIn("B,X", message)
        self.assertNotIn("A,X", message.split("Missing combinations:")[-1])
        self.assertNotIn("B,Y", message.split("Missing combinations:")[-1])

    def test_full_coverage_no_warning(self):
        """All 4 combinations declared -> no coverage warning."""
        sys_def = self._build_sys_def({
            "cfg_ax": {"name": "cfg_ax", "pattern_policy_references": [
                {"component": "mc", "decision": "d1", "policy": "A"},
                {"component": "mc", "decision": "d2", "policy": "X"},
            ]},
            "cfg_ay": {"name": "cfg_ay", "pattern_policy_references": [
                {"component": "mc", "decision": "d1", "policy": "A"},
                {"component": "mc", "decision": "d2", "policy": "Y"},
            ]},
            "cfg_bx": {"name": "cfg_bx", "pattern_policy_references": [
                {"component": "mc", "decision": "d1", "policy": "B"},
                {"component": "mc", "decision": "d2", "policy": "X"},
            ]},
            "cfg_by": {"name": "cfg_by", "pattern_policy_references": [
                {"component": "mc", "decision": "d1", "policy": "B"},
                {"component": "mc", "decision": "d2", "policy": "Y"},
            ]},
        })
        issues = self.linter._validate_policy_combination_coverage(sys_def)
        self.assertEqual(len(issues), 0, f"Expected no coverage warnings, got: {[str(i) for i in issues]}")

    def test_single_decision_component_no_coverage_warning(self):
        """AE5: a single-decision pattern's spec -> the coverage check
        reports no warning (1 of 1 combination trivially satisfied)."""
        data = {
            "system": {
                "name": "SingleDecisionTest",
                "components": {
                    "sc": {
                        "name": "SC",
                        "parameters": {},
                        "decisions": {"d1": {"policies": {"A": {}, "B": {}}}},
                    }
                },
                "tradeoffs": [],
            },
            "dataspace": {
                "quality_objectives": [],
                "policy_identification": {
                    "from": "column",
                    "column": "config_id",
                    "policies": {
                        "cfg_a": {
                            "name": "cfg_a",
                            "pattern_policy_references": [
                                {"component": "sc", "decision": "d1", "policy": "A"}
                            ],
                        }
                    },
                },
            },
        }
        sys_def = SystemDefinition.model_validate(data)
        coverage_issues = self.linter._validate_policy_combination_coverage(sys_def)
        completeness_issues = self.linter._validate_multi_decision_completeness(sys_def)
        self.assertEqual(len(coverage_issues), 0, f"Expected no coverage warnings, got: {[str(i) for i in coverage_issues]}")
        self.assertEqual(len(completeness_issues), 0, f"Expected no completeness errors, got: {[str(i) for i in completeness_issues]}")


class TestLowVarianceLinting(unittest.TestCase):
    """R3: low-variance WARNING for objectives and parameters."""

    def setUp(self):
        self.linter = SystemLinter()
        self.sys_def = SystemDefinition.model_validate({
            "system": {
                "name": "VarianceTest",
                "components": {
                    "c1": {
                        "name": "C1",
                        "parameters": {"p_low_var": {"level": "system", "type": "lever"}},
                        "decisions": {"d1": {"policies": {"A": {}}}},
                    }
                },
                "tradeoffs": [],
            },
            "dataspace": {
                "quality_objectives": [{"name": "obj_low_var", "metric": "unit"}],
                "policy_identification": {
                    "from": "column",
                    "column": "config_id",
                    "policies": {
                        "cfg_a": {
                            "name": "cfg_a",
                            "pattern_policy_references": [
                                {"component": "c1", "decision": "d1", "policy": "A"}
                            ],
                        }
                    },
                },
            },
        })

    def test_low_variance_objective_and_parameter_warn(self):
        # 8 of 10 rows share the same value -> 80% concentration, over threshold.
        df = pd.DataFrame({
            "config_id": ["cfg_a"] * 10,
            "obj_low_var": [1.0] * 8 + [2.0, 3.0],
            "p_low_var": [5] * 8 + [6, 7],
        })
        issues = self.linter._validate_low_variance(self.sys_def, df)
        self.assertTrue(any("Quality Objective 'obj_low_var' is low-variance" in i.message for i in issues))
        self.assertTrue(any("Parameter 'p_low_var'" in i.message and "low-variance" in i.message for i in issues))

    def test_high_variance_no_warning(self):
        df = pd.DataFrame({
            "config_id": ["cfg_a"] * 10,
            "obj_low_var": list(range(10)),
            "p_low_var": list(range(10, 20)),
        })
        issues = self.linter._validate_low_variance(self.sys_def, df)
        self.assertEqual(len(issues), 0, f"Expected no low-variance warnings, got: {[str(i) for i in issues]}")

    def test_missing_column_skipped(self):
        df = pd.DataFrame({"config_id": ["cfg_a"] * 3})
        # Neither obj_low_var nor p_low_var present -- mirrors
        # _validate_objectives's existing column-presence guard.
        issues = self.linter._validate_low_variance(self.sys_def, df)
        self.assertEqual(len(issues), 0)


class TestRealSpecRegression(unittest.TestCase):
    """Regression coverage against the real FL spec (AE3) and CQRS as the
    single-decision degenerate case (R5)."""

    def setUp(self):
        self.linter = SystemLinter()

    def test_fl_system_split_lints_clean_on_completeness_with_expected_coverage_warning(self):
        json_path = os.path.join(REPO_ROOT, "federatedlearning", "FLsystem_split.json")
        loader = GenericDataLoader()
        sys_def = loader.load_system_definition(json_path)
        raw_df, _experiments_df, _outcomes_df = loader.load_data(json_path, validate_integrity=False)

        issues = self.linter.lint(sys_def, raw_df)

        errors = [i for i in issues if i.level == "ERROR"]
        self.assertEqual(len(errors), 0, f"Expected zero ERRORs, got: {[str(i) for i in errors]}")

        coverage_warnings = [i for i in issues if "incomplete policy-combination coverage" in i.message]
        self.assertEqual(
            len(coverage_warnings), 1,
            f"Expected exactly 1 coverage WARNING, got: {[str(i) for i in coverage_warnings]}"
        )
        message = coverage_warnings[0].message
        for combo in ["ON,ON,OFF", "ON,OFF,ON", "OFF,ON,ON", "ON,ON,ON"]:
            self.assertIn(combo, message, f"Expected missing combination '{combo}' named in: {message}")

        # NOTE: U3 (a parallel unit) is responsible for adding the 6
        # aggregated client-heterogeneity parameters (e.g. "Client CPU Mean")
        # to FLsystem_split.json. As of this test, they are not yet present,
        # so we do not assert low-variance warnings on them here -- only that
        # today's declared parameters/objectives don't produce completeness
        # errors and the coverage warning is exactly as expected. If U3 lands
        # first, those aggregated parameters would additionally appear as
        # low-variance WARNINGs, which this test does not contradict.
        aggregated_param_names = [
            "Client CPU Mean", "Client RAM Mean", "Client Alpha Dirichlet Mean",
            "Client JSD Mean", "Client Data Distribution Diversity",
            "Client Data Persistence Diversity",
        ]
        if all(name in sys_def.system.components["fl_system"].parameters for name in aggregated_param_names):
            low_variance_warnings = [i for i in issues if "is low-variance" in i.message]
            for name in aggregated_param_names:
                self.assertTrue(
                    any(f"Parameter '{name}'" in i.message for i in low_variance_warnings),
                    f"Expected low-variance WARNING for aggregated parameter '{name}'"
                )

    def test_cqrs_single_decision_lints_clean_on_completeness_and_coverage(self):
        json_path = os.path.join(REPO_ROOT, "patterns", "CQRS", "CQRS.json")
        loader = GenericDataLoader()
        sys_def = loader.load_system_definition(json_path)

        completeness_issues = self.linter._validate_multi_decision_completeness(sys_def)
        coverage_issues = self.linter._validate_policy_combination_coverage(sys_def)

        self.assertEqual(len(completeness_issues), 0, f"Expected 0 completeness findings, got: {[str(i) for i in completeness_issues]}")
        self.assertEqual(len(coverage_issues), 0, f"Expected 0 coverage findings, got: {[str(i) for i in coverage_issues]}")


if __name__ == '__main__':
    unittest.main()
