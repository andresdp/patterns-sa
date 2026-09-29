
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

    def test_transform_features_reuses_fitted_optional_encoding(self):
        params = self.sys_def_dict["system"]["components"]["c1"]["parameters"]
        params["alg"] = {"level": "system", "type": "constraint", "optional": True}
        params["rate"] = {"level": "system", "type": "constraint", "optional": True}
        analyzer = FeatureImportanceAnalyzer(SystemDefinition.model_validate(self.sys_def_dict))

        train = pd.DataFrame({
            "p1": [1.0, 2.0, 3.0, 4.0],
            "alg": ["zlib", None, "CPU", None],
            "rate": [0.5, np.nan, 0.7, np.nan],
        })
        test = pd.DataFrame({"p1": [2.0, 3.0], "alg": ["CPU", None], "rate": [np.nan, 0.6]})

        _, _, stats = analyzer.preprocess_features(train, standardize=True)
        encoder = stats["encoder"]
        self.assertEqual(encoder.categories, {"alg": ["CPU", "zlib"]})

        # Categorical optional values must not reach the scaler as raw strings
        X_test = FeatureImportanceAnalyzer.transform_features(test, stats)
        self.assertEqual(list(X_test.columns), stats["numeric_cols"])
        self.assertFalse(X_test.isnull().values.any())

        # Encoded exactly as the fitted train data: category code and train sentinel
        expected = test.copy()
        expected["alg"] = [1.0, 0.0]
        expected["rate"] = [encoder.sentinels["rate"], 0.6]
        scaled = stats["scaler"].transform(expected[stats["numeric_cols"]])
        np.testing.assert_allclose(X_test.values, scaled)

    def test_correlated_selection_breaks_exact_ties_alphabetically(self):
        # 'zeta' and 'alpha' are identical copies (e.g. two settings of one pattern), so
        # they perform exactly alike; the kept one must not depend on set/hash order.
        rng = np.random.default_rng(0)
        signal = rng.integers(0, 2, 40).astype(float)
        X = pd.DataFrame({"zeta": signal, "alpha": signal, "noise": rng.normal(size=40)})
        y = pd.Series(signal * 10 + rng.normal(scale=0.1, size=40))
        scores = self.analyzer.compute_importance(X, y, use_smart_correlation=True)
        self.assertGreater(scores["alpha"], 0.0)
        self.assertEqual(scores["zeta"], 0.0)

if __name__ == '__main__':
    unittest.main()
