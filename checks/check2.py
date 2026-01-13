from archspaces.core import ArchSpaceCore
import os

core = ArchSpaceCore()

# Verify Declarative Loading
json_path = 'tests/test_system.json'

# Re-create if missing
if not os.path.exists(json_path):

    import json
    import pandas as pd
    
    df = pd.DataFrame({'N_A': [10, 20], 'R0': [0.1, 0.2], 'U0': [0.5, 0.6], 'config': ['c1', 'c2']})
    
    df.to_csv('tests/test_data.csv', index=False)
    system_def = {
        "system": {
            "name": "TestSys", 
            "components": {
                "comp1": {
                    "name": "Patt1", 
                    "parameters": 
                    {
                        "N_A": { "type": "integer" }
                    }
                }    
            }
        }, 
        "dataspace": {
            "source_file": "test_data.csv", 
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
    
    with open(json_path, 'w') as f: 
        json.dump(system_def, f)
        
    raw_df, exps_df, outs_df = core.load_detailed_data(json_path)
    print("Experiments Columns:", exps_df.columns.tolist())
    print("Outcomes Columns:", outs_df.columns.tolist())
    
    # Verify Strategy Management (Explanations)
    explanation = core.explain({'robustness': 0.9}, method='template')
    print("Explanation Text:", explanation['text'])