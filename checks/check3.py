from adept.core.models import Parameter, ParameterLevel, ParameterType
from adept.core.parameter_registry import ParameterRegistry
from adept.core.loader import GenericDataLoader
import os
import pandas as pd
import json

# 1. Verify Parameter Registry
registry = ParameterRegistry()
p = Parameter(name="replicas", level=ParameterLevel.SYSTEM, type=ParameterType.LEVER, value=5)
registry.register(p)
print(f"Registered parameter: {registry.get('replicas').name}, Type: {registry.get('replicas').type}")
 
# 2. Verify Adaptive Loading
# Create a temporary system.json with adaptive process
test_json = 'manual_test_system.json'
test_csv = 'manual_test_data.csv'
pd.DataFrame({'x': [1, 2], 'y': [0.1, 0.2]}).to_csv(test_csv, index=False)
     
system_def = {
    "system": {
        "name": "ManualTest",
        "components": {"c1": {"name": "P1"}},
        "adaptive_processes": [{"process_id": "p1", "instance_id": "c1", "process_type": "Iterative"}]
    },
    "dataspace": {
        "source_file": test_csv,
        "quality_objectives": [ {"name": "y", "metric": "unit"} ],
        "policy_identification": {
            "from": "column", 
            "policies": {}
        }
    }
}

with open(test_json, 'w') as f: 
    json.dump(system_def, f)

loader = GenericDataLoader()
sys_def = loader.load_system_definition(test_json)
print(f"Loaded System: {sys_def.system.name}")
print(f"Adaptive Processes: {[p.process_id for p in sys_def.system.adaptive_processes]}")

# Cleanup
os.remove(test_json)
os.remove(test_csv)