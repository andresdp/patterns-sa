
import unittest
import os
import pandas as pd
from adept import PatternAnalysis

class TestAnalysisSession(unittest.TestCase):
    def setUp(self):
        self.json_path = "patterns/Toy_Example/ArchExample_Discretization.json"
        self.session = PatternAnalysis(self.json_path)

    def test_session_lifecycle(self):
        # 1. Load
        self.session.load(validate_integrity=False)
        self.assertIsNotNone(self.session.raw_df)
        
        # 2. Define Tradeoffs
        self.session.define_tradeoffs(n_bins=3)
        self.assertIsNotNone(self.session.discrete_df)
        
        # 3. Split
        self.session.split_data(test_size=0.2)
        self.assertIsNotNone(self.session.train_indices)
        self.assertIsNotNone(self.session.test_indices)
        
        # 4. Feature Scoring
        scores = self.session.compute_feature_scores()
        self.assertIsInstance(scores, pd.DataFrame)
        
        # 5. Discovery
        # Use first tradeoff
        tradeoff_name = self.session.get_tradeoffs()[0].name
        boxes = self.session.discover_scenarios(tradeoff_name, method='prim')
        self.assertIsInstance(boxes, list)

    def test_robustness_analysis(self):
        self.session.load(validate_integrity=False)
        self.session.define_tradeoffs(n_bins=3)
        
        policy_name = "one_device_low"
        tradeoff_name = self.session.get_tradeoffs()[0].name
        
        result = self.session.compute_robustness(policy_name, tradeoff_name, metric='starr')
        self.assertEqual(result['metric'], 'starr')
        self.assertIn('value', result)

if __name__ == '__main__':
    unittest.main()
