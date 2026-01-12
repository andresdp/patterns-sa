import unittest
import pandas as pd
from adept.analysis.robustness import RobustnessAnalyzer

class TestRobustnessAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = RobustnessAnalyzer()

    def test_compute_starr(self):
        # Data setup
        discrete_df = pd.DataFrame({
            'A': ['low', 'low', 'high', 'low'],
            'B': ['high', 'low', 'high', 'high']
        })
        
        # Target: A=low, B=high
        # Indices: 0 (True), 1 (False), 2 (False), 3 (True) -> 2 successes
        target_mask = (discrete_df['A'] == 'low') & (discrete_df['B'] == 'high')
        
        result = self.analyzer.compute_starr(target_mask)
        
        self.assertEqual(result['metric'], 'starr')
        self.assertEqual(result['value'], 0.5) # 2/4
        self.assertEqual(result['details']['success_count'], 2)
        self.assertEqual(result['details']['total_count'], 4)

    def test_compute_starr_specific_tradeoff(self):
        discrete_df = pd.DataFrame({
            'A': ['low', 'low', 'high', 'low'],
            'B': ['high', 'low', 'high', 'high']
        })
        
        # Target: A=low, B=low
        # Indices: 1 (True) -> 1 success
        target_mask = (discrete_df['A'] == 'low') & (discrete_df['B'] == 'low')
        
        result = self.analyzer.compute_starr(target_mask)
        
        self.assertEqual(result['value'], 0.25) # 1/4
        self.assertEqual(result['details']['success_count'], 1)

if __name__ == '__main__':
    unittest.main()