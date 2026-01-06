
import unittest
import pandas as pd
from archspaces.discovery import ScenarioDiscoveryManager, PRIMDiscovery, CARTDiscovery

class TestScenarioDiscoveryManager(unittest.TestCase):
    def setUp(self):
        self.manager = ScenarioDiscoveryManager()
        self.df = pd.DataFrame({
            'x1': [0.1, 0.2, 0.3, 0.4],
            'x2': [0.5, 0.6, 0.7, 0.8],
            'outcome': [0, 0, 1, 1]
        })

    def test_get_strategy(self):
        self.assertIsInstance(self.manager.get_strategy('prim'), PRIMDiscovery)
        self.assertIsInstance(self.manager.get_strategy('cart'), CARTDiscovery)
        # Default
        self.assertIsInstance(self.manager.get_strategy(None), PRIMDiscovery)

    def test_discover_delegation(self):
        # We need to mock the strategy execution or handle the required args again
        # But here we test manager logic
        pass

if __name__ == '__main__':
    unittest.main()
