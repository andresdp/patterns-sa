
import unittest
import pandas as pd
from archspaces.core import RobustnessAnalyzer, DataProcessor

class TestRobustnessAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = RobustnessAnalyzer()
        self.processor = DataProcessor()

    def test_compute_robustness_single_config(self):
        # Mocking ArchSpace.get_experiment/s behavior with pre-discretized data
        # In a real scenario, this would likely take the ArchSpace instance or DataFrames directly.
        
        # Let's assume we pass the discretized dataframe directly for now
        discrete_df = pd.DataFrame({
            'A': ['low', 'low', 'high', 'low'],
            'B': ['high', 'low', 'high', 'high']
        })
        
        # Tradeoffs: 
        # low,high: 2
        # low,low: 1
        # high,high: 1
        # Total: 4
        
        # Most common is low,high
        
        robustness, tradeoff = self.analyzer.compute_robustness(discrete_df)
        self.assertEqual(tradeoff, 'low,high')
        self.assertEqual(robustness, 0.5) # 2/4

    def test_compute_robustness_specific_tradeoff(self):
        discrete_df = pd.DataFrame({
            'A': ['low', 'low', 'high', 'low'],
            'B': ['high', 'low', 'high', 'high']
        })
        
        robustness, tradeoff = self.analyzer.compute_robustness(discrete_df, qa_tradeoff='low,low')
        self.assertEqual(tradeoff, 'low,low')
        self.assertEqual(robustness, 0.25) # 1/4

if __name__ == '__main__':
    unittest.main()
