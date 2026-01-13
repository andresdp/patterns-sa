
import unittest
import pandas as pd
import numpy as np
from adept.analysis.contingency import ContingencyAnalyzer
from adept.core.models import SystemDefinition

class TestContingency(unittest.TestCase):
    def setUp(self):
        # Mock System Definition
        self.sys_def_dict = {
            "system": {
                "name": "Test",
                "components": {
                    "c1": {
                        "name": "C1",
                        "decisions": {
                            "d1": {
                                "policies": {
                                    "pol_a": {},
                                    "pol_b": {}
                                }
                            }
                        }
                    }
                }
            },
            "dataspace": {
                "configuration_identification": {
                    "from": "column", 
                    "column": "policy_col", 
                    "configurations": {
                        "A": {"name": "config_a", "pattern_policy_references": [{"component": "c1", "decision": "d1", "policy": "pol_a"}]},
                        "B": {"name": "config_b", "pattern_policy_references": [{"component": "c1", "decision": "d1", "policy": "pol_b"}]}
                    }
                },
                "quality_objectives": [{"name": "o1"}]
            }
        }
        self.sys_def = SystemDefinition.model_validate(self.sys_def_dict)
        self.analyzer = ContingencyAnalyzer(self.sys_def)

    def test_get_decision_policy_map(self):
        df = pd.DataFrame({"policy_col": ["A", "B", "A"]})
        policy_map = self.analyzer.get_decision_policy_map(df, "policy_col")
        self.assertIn("c1:d1", policy_map.columns)
        self.assertEqual(policy_map["c1:d1"].iloc[0], "pol_a")
        self.assertEqual(policy_map["c1:d1"].iloc[1], "pol_b")

    def test_compute_contingency(self):
        policy_df = pd.DataFrame({"c1:d1": ["pol_a", "pol_b", "pol_a", "pol_a"]})
        tradeoff_mask = pd.DataFrame({"t1": [True, False, True, False]})
        
        # Result should show pol_a hitting t1 in 2/3 cases (66.6%), pol_b in 0/1 cases
        result = self.analyzer.compute_contingency(policy_df, tradeoff_mask, "c1:d1", normalization_mode='population')
        
        self.assertAlmostEqual(result.loc["pol_a", "t1"], 66.66666666666666)
        self.assertEqual(result.loc["pol_b", "t1"], 0.0)

if __name__ == '__main__':
    unittest.main()
