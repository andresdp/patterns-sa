
import unittest
import pandas as pd
import json
import os
from adept.core.loader import GenericDataLoader
from adept.core.models import SystemDefinition

class TestGenericDataLoader(unittest.TestCase):
    def setUp(self):
        self.csv_path = 'tests/test_data.csv'
        self.json_path = 'tests/test_system.json'
        
        # Create dummy CSV
        df = pd.DataFrame({
            'N_A': [10, 20],
            'R0': [0.1, 0.2],
            'U0': [0.5, 0.6],
            'config': ['c1', 'c2']
        })
        df.to_csv(self.csv_path, index=False)
        
        # Create dummy JSON
        system_def = {
            "system": {
                "name": "TestSys",
                "components": {
                    "comp1": {
                        "name": "Patt1",
                        "parameters": {"N_A": {"type": "integer"}}
                    }
                }
            },
            "dataspace": {
                "source_file": os.path.basename(self.csv_path),
                "quality_objectives": [{"name": "R0", "metric": "response_time"}],
                "policy_identification": {
                    "from": "column",
                    "column": "config",
                    "policies": {
                        "c1": {"name": "Config 1"},
                        "c2": {"name": "Config 2"}
                    }
                }
            }
        }
        with open(self.json_path, 'w') as f:
            json.dump(system_def, f)

    def tearDown(self):
        if os.path.exists(self.csv_path):
            os.remove(self.csv_path)
        if os.path.exists(self.json_path):
            os.remove(self.json_path)

    def test_load_system_definition(self):
        loader = GenericDataLoader()
        sys_def = loader.load_system_definition(self.json_path)
        self.assertIsInstance(sys_def, SystemDefinition)
        self.assertEqual(sys_def.system.name, "TestSys")

    def test_load_data(self):
        loader = GenericDataLoader()
        # In this simplified test, we just check if it loads and returns a dataframe
        # The actual splitting into experiments/outcomes depends on logic I need to implement
        df, experiments, outcomes = loader.load_data(self.json_path)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(len(df), 2)
        # Check if experiments/outcomes splitting worked (basic check)
        self.assertIn('N_A', experiments.columns)
        self.assertIn('R0', outcomes.columns)

if __name__ == '__main__':
    unittest.main()
