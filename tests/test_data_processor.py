
import unittest
import pandas as pd
import numpy as np
from adept.analysis.discretization import DataProcessor

class TestDataProcessor(unittest.TestCase):
    def setUp(self):
        self.data = pd.DataFrame({
            'A': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
            'B': [10, 20, 30, 40, 50, 60, 70, 80, 90, 100]
        })
        self.processor = DataProcessor()

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
        discrete_df, tradeoffs = self.processor.discretize(self.data, n_bins=2, all_labels=all_labels)
        self.assertEqual(len(discrete_df), 10)
        self.assertIn('low', discrete_df['A'].values)
        self.assertIn('high', discrete_df['A'].values)

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
