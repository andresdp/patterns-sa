
import unittest
import pandas as pd
from adept.analysis.discovery import ScenarioDiscoveryManager

class TestScenarioDiscoveryParadigms(unittest.TestCase):
    def setUp(self):
        self.manager = ScenarioDiscoveryManager()
        self.experiments_df = pd.DataFrame({
            'lever1': [0.1, 0.2, 0.3, 0.4],
            'lever2': [10, 20, 30, 40]
        })
        self.outcomes_df = pd.DataFrame({
            'metric1': [0.5, 0.6, 0.7, 0.8]
        })
        self.discrete_df = pd.DataFrame({
            'metric1': ['low', 'low', 'high', 'high']
        })

    def test_discretization_paradigm_prim(self):
        # Targeting 'high' bin
        target_spec = {
            'paradigm': 'discretization',
            'target_bin': 'high'
        }
        # This should call PRIM by default
        result = self.manager.discover(
            self.experiments_df, 
            self.outcomes_df, 
            outcome='metric1',
            target_spec=target_spec,
            discrete_outcomes_df=self.discrete_df
        )
        self.assertIsNotNone(result)
        # result is a tuple (box, limits, alg)
        # box limits should contain info about which levers lead to 'high'
        # In our case, lever1 > 0.2 leading to 'high'

if __name__ == '__main__':
    unittest.main()
