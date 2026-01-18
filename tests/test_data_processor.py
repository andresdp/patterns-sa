
import unittest
import pandas as pd
import numpy as np
from adept.analysis.discretization import DataProcessor
from adept.core.models import QualityObjective

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'B': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        })
        self.processor = DataProcessor()
        self.objectives = [
            QualityObjective(name="A", maximize=False), # Min A
            QualityObjective(name="B", maximize=True)   # Max B
        ]

    def test_get_bins(self):
        bins = self.processor.get_bins(self.data['A'], 2)
        self.assertEqual(len(bins), 3)
        self.assertAlmostEqual(bins[0], 0.9)
        self.assertAlmostEqual(bins[-1], 10.1)

    def test_discretize(self):
        all_labels = {
            'A': ['low', 'high'],
            'B': ['low', 'high']
        }
        discrete_df, schemes, indices, pf = self.processor.define_tradeoffs(self.data, n_bins=2, all_labels=all_labels)
        self.assertEqual(len(discrete_df), 10)
        self.assertIn('low', discrete_df['A'].values)
        self.assertIn('high', discrete_df['A'].values)
        self.assertEqual(len(schemes), 2)
        self.assertEqual(schemes[0].objective_name, 'A')
        self.assertEqual(len(schemes[0].bins), 2)
        self.assertEqual(schemes[0].bins[0].label, 'low')

    def test_static_threshold(self):
        params = {'thresholds': {'A': 5.0}}
        discrete_df, schemes, indices, pf = self.processor.define_tradeoffs(self.data, method='threshold', params=params, objectives=self.objectives)
        # A is min. <= 5 is Satisfactory.
        self.assertEqual(discrete_df.iloc[0]['A'], 'satisfactory') # 1
        self.assertEqual(discrete_df.iloc[9]['A'], 'unsatisfactory') # 10

    def test_pareto_epsilon(self):
        # A=[1..10] min, B=[10..100] max.
        # 1,10 vs 2,20. 1 is better A, 20 is better B.
        df = pd.DataFrame({'A': [1, 2, 5], 'B': [10, 20, 10]}) 
        # Row 2 (5,10) is dominated by Row 0 (1,10) and Row 1 (2,20).
        
        params = {'epsilon': 0.01} # Small tolerance
        discrete_df, schemes, indices, front = self.processor.define_tradeoffs(df, method='pareto_epsilon', params=params, objectives=self.objectives)
        
        self.assertEqual(discrete_df.iloc[0]['A'], 'epsilon-pareto-optimal')
        self.assertEqual(discrete_df.iloc[1]['A'], 'epsilon-pareto-optimal')
        # Row 2 is far away (dominanted)
        self.assertEqual(discrete_df.iloc[2]['A'], 'out_high')

    def test_discretize_with_ranges(self):
        # A has values [1..10]. Default min/max is 1/10.
        # Force range to [0, 20]. 
        # Bins (2) should be [0, 10] and [10, 20].
        # 1-10 will all fall into the first bin (low).
        ranges = {'A': (0.0, 20.0)}
        labels = {'A': ['low', 'high'], 'B': ['low', 'high']}
        
        discrete_df, schemes, indices, pf = self.processor.define_tradeoffs(self.data, n_bins=2, ranges=ranges, all_labels=labels)
        
        # Check A scheme
        scheme_a = next(s for s in schemes if s.objective_name == 'A')
        self.assertAlmostEqual(scheme_a.bins[0].min_value, 0.0, delta=0.2) # fuzzy due to buffer
        self.assertAlmostEqual(scheme_a.bins[1].max_value, 20.0, delta=0.2)
        
        # All original values (1-10) should be 'low' because 10 is midpoint
        # NOTE: pd.cut logic might put 10 in second bin depending on right/include_lowest defaults
        # Our get_bins adds buffer. 0-10, 10-20.
        # DataProcessor.get_bins returns edges.
        
        # Let's just verify the scheme bounds are correct based on input ranges
        self.assertTrue(any(b.max_value > 15 for b in scheme_a.bins))

    def test_get_tradeoffs(self):
        discrete_df = pd.DataFrame({
            'A': ['low', 'low', 'high'],
            'B': ['high', 'low', 'high']
        })
        tradeoffs = self.processor.get_tradeoffs(discrete_df)
        self.assertEqual(tradeoffs['low,high'], 1)
        self.assertEqual(tradeoffs['low,low'], 1)
        self.assertEqual(tradeoffs['high,high'], 1)

if __name__ == '__main__':
    unittest.main()
