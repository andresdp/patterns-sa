
import unittest
import pandas as pd
from adept.core.models import Tradeoff, System
from adept.analysis.discovery import ScenarioDiscoveryManager

class TestTradeoffEntity(unittest.TestCase):
    def setUp(self):
        self.manager = ScenarioDiscoveryManager()
        self.experiments_df = pd.DataFrame({
            'L1': [0.1, 0.2, 0.3, 0.4, 0.5]
        })
        self.outcomes_df = pd.DataFrame({
            'Q1': [10, 20, 30, 40, 50]
        })
        self.discrete_df = pd.DataFrame({
            'Q1': ['bad', 'bad', 'avg', 'good', 'good']
        })

    def test_tradeoff_modeling(self):
        t = Tradeoff(
            name="EfficientGood",
            description="Good performance with high efficiency",
            elements={"Q1": "good"},
            paradigm="discretization"
        )
        self.assertEqual(t.name, "EfficientGood")
        self.assertEqual(t.elements["Q1"], "good")

    def test_discovery_with_tradeoff_object(self):
        t = Tradeoff(name="target", elements={"Q1": "good"})
        
        # Run discovery using the Tradeoff object
        result = self.manager.discover(
            self.experiments_df,
            self.outcomes_df,
            outcome='Q1',
            tradeoff=t,
            discrete_outcomes_df=self.discrete_df
        )
        self.assertIsNotNone(result)
        # result[1] contains the limits. L1 should be high.
        limits = result[1]
        self.assertIn('L1', limits)
        self.assertGreater(limits['L1']['min'], 0.2)

if __name__ == '__main__':
    unittest.main()
