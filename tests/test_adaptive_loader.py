
import unittest
import pandas as pd
import json
import os
import shutil
from adept.core.loader import GenericDataLoader
from adept.core.models import SystemDefinition, BehavioralTrace

class TestAdaptiveLoader(unittest.TestCase):
    def setUp(self):
        self.test_dir = 'tests/test_adept'
        os.makedirs(self.test_dir, exist_ok=True)
        self.csv_path = os.path.join(self.test_dir, 'data.csv')
        self.json_path = os.path.join(self.test_dir, 'system.json')
        self.traces_dir = os.path.join(self.test_dir, 'traces')
        os.makedirs(self.traces_dir, exist_ok=True)
        
        # Create dummy CSV
        df = pd.DataFrame({
            'lever1': [1, 2],
            'outcome1': [0.1, 0.2]
        })
        df.to_csv(self.csv_path, index=False)
        
        # Create dummy trace
        trace_df = pd.DataFrame({
            'cycle': [1, 2, 3],
            'metric': [0.5, 0.6, 0.7]
        })
        trace_df.to_csv(os.path.join(self.traces_dir, 'scenario_0.csv'), index=False)
        
        # Create dummy JSON
        system_def = {
            "system": {
                "name": "AdaptiveSys",
                "components": {
                    "comp1": {
                        "name": "Patt1",
                        "parameters": {"lever1": {"type": "integer"}}
                    }
                },
                "adaptive_processes": [
                    {
                        "process_id": "proc1",
                        "instance_id": "comp1",
                        "process_type": "Iterative"
                    }
                ]
            },
            "dataspace": {
                "source_file": "data.csv",
                "traces_path": "traces",
                "quality_objectives": [{"name": "outcome1", "metric": "unit"}],
                "policy_identification": {
                    "from": "column",
                    "column": "none",
                    "policies": {}
                }
            }
        }
        with open(self.json_path, 'w') as f:
            json.dump(system_def, f)

    def tearDown(self):
        if os.path.exists(self.test_dir):
            shutil.rmtree(self.test_dir)

    def test_load_adaptive_metadata(self):
        loader = GenericDataLoader()
        sys_def = loader.load_system_definition(self.json_path)
        self.assertEqual(len(sys_def.system.adaptive_processes), 1)
        self.assertEqual(sys_def.system.adaptive_processes[0].process_id, "proc1")

    def test_load_behavioral_traces(self):
        loader = GenericDataLoader()
        traces = loader.load_behavioral_traces(self.json_path)
        self.assertEqual(len(traces), 1)
        self.assertEqual(traces[0].scenario_id, "scenario_0")
        self.assertIsInstance(traces[0].outcomes, pd.DataFrame)

if __name__ == '__main__':
    unittest.main()
