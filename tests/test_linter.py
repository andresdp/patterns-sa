
import unittest
import pandas as pd
from adept.utils.linter import SystemLinter
from adept.core.models import SystemDefinition

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

if __name__ == '__main__':
    unittest.main()
