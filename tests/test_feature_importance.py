
import unittest
import pandas as pd
import numpy as np
from adept.analysis.feature_importance import FeatureImportanceAnalyzer
from adept.core.models import SystemDefinition

class TestFeatureImportance(unittest.TestCase):
    def setUp(self):
        # Mock System Definition
        self.sys_def_dict = {
            "system": {
                "name": "Test",
                "components": {
                    "c1": {
                        "name": "C1",
                        "parameters": {
                            "p1": {"level": "system", "type": "lever"},
                            "p2": {"level": "system", "type": "uncertainty"}
                        }
                    }
                }
            },
            "dataspace": {
                "configuration_identification": {"from": "column", "column": "pol", "configurations": {}},
                "quality_objectives": [{"name": "o1", "maximize": False}]
            }
        }
        self.sys_def = SystemDefinition.model_validate(self.sys_def_dict)
        self.analyzer = FeatureImportanceAnalyzer(self.sys_def)
        
        # Mock Data
        self.X = pd.DataFrame({
            "p1": [1, 2, 3, 4, 5],
            "p2": [10, 20, 10, 20, 10]
        })
        self.y = pd.Series([100, 200, 110, 210, 105]) # High correlation with p2

    def test_compute_importance(self):
        scores = self.analyzer.compute_importance(self.X, self.y)
        self.assertIn("p1", scores)
        self.assertIn("p2", scores)
        # p2 should have higher importance than p1 given the data
        self.assertGreater(scores["p2"], scores["p1"])

    def test_get_parameter_columns(self):
        cols = self.analyzer.get_parameter_columns(self.X)
        self.assertIn("p1", cols)
        self.assertIn("p2", cols)

if __name__ == '__main__':
    unittest.main()
