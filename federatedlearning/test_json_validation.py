#!/usr/bin/env python3
"""Test script to diagnose JSON validation issues."""

import json
import sys
sys.path.insert(0, '/Users/adiazpace/Documents/GitHub/patterns-sa')

from adept.core.models import SystemDefinition

# Load JSON
json_path = '/Users/adiazpace/Documents/GitHub/patterns-sa/federatedlearning/FLsystem.json'

print("Loading JSON file...")
with open(json_path, 'r') as f:
    json_data = json.load(f)

print(f"JSON keys: {list(json_data.keys())}")
print(f"Dataspace keys: {list(json_data['dataspace'].keys())}")
print(f"Config identification keys: {list(json_data['dataspace']['configuration_identification'].keys())}")

# Try to validate
try:
    print("\nAttempting to validate SystemDefinition...")
    sys_def = SystemDefinition.model_validate(json_data)
    print("✓ Validation successful!")
    print(f"System name: {sys_def.system.name}")
    print(f"Quality objectives: {len(sys_def.dataspace.quality_objectives)}")
except Exception as e:
    print(f"✗ Validation failed!")
    print(f"Error type: {type(e).__name__}")
    print(f"Error: {e}")
    
    # Try to extract more details
    if hasattr(e, 'errors'):
        print(f"\nValidation errors:")
        for err in e.errors():
            print(f"  - Location: {' -> '.join(str(loc) for loc in err['loc'])}")
            print(f"    Type: {err['type']}")
            print(f"    Message: {err['msg']}")
            print(f"    Input: {err['input']}")