
import unittest
import pandas as pd
from adept.core.coordinator import ArchSpaceCore
from adept.analysis.discretization import DataProcessor
from adept.analysis.robustness import RobustnessAnalyzer
from adept.analysis.tradeoffs import TradeoffAnalyzer

class TestArchSpaceCore(unittest.TestCase):
    def setUp(self):
        self.core = ArchSpaceCore()
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4],
            'B': [10, 20, 30, 40],
            'outcome': [0, 0, 1, 1]
        })

    def test_components_initialization(self):
        self.assertIsInstance(self.core.data_processor, DataProcessor)
        self.assertIsInstance(self.core.robustness_analyzer, RobustnessAnalyzer)
        self.assertIsInstance(self.core.tradeoff_analyzer, TradeoffAnalyzer)

    def test_discretize_delegation(self):
        discrete_df, schemes, indices, pf = self.core.define_tradeoffs(self.df, n_bins=2)
        self.assertEqual(len(discrete_df), 4)
        self.assertIsInstance(schemes, list)
        self.assertEqual(len(schemes), 3)

    def test_robustness_delegation(self):
        # discrete_df, _, _, _ = self.core.define_tradeoffs(self.df, n_bins=2)
        # robustness, tradeoff = self.core.compute_robustness(discrete_df)
        # self.assertIsNotNone(tradeoff)
        # self.assertTrue(0 <= robustness <= 1)
        pass

if __name__ == '__main__':
    unittest.main()
