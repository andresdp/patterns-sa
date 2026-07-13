#!/usr/bin/env python3
"""Simple manual test of NaN feature from scratch."""

import sys
import os

# Add parent directory to path
parent_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parent_dir)

# Change to federatedlearning directory
os.chdir('/Users/adiazpace/Documents/GitHub/patterns-sa/federatedlearning')

# Import
from adept import PatternAnalysis

print("=" * 60)
print("TEST 1: Load Data")
print("=" * 60)

try:
    session = PatternAnalysis('./FLsystem_split.json')
    print("✓ Session created")
except Exception as e:
    print(f"✗ Session creation failed: {e}")
    sys.exit(1)

try:
    session.load()
    print("✓ Data loaded")
    print(f"  Experiments shape: {session.experiments_df.shape}")
    print(f"  Outcomes shape: {session.outcomes_df.shape}")
except Exception as e:
    print(f"✗ Data loading failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TEST 2: Create Tradeoffs")
print("=" * 60)

try:
    session.create_tradeoffs(method='discretization', n_bins=3)
    print("✓ Tradeoffs created")
    print(f"  Number of schemes: {len(session.schemes)}")
except Exception as e:
    print(f"✗ Tradeoff creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TEST 3: Feature Importance")
print("=" * 60)

try:
    scores_df = session.compute_feature_scores()
    print("✓ Feature scores computed")
    print(f"  Scores shape: {scores_df.shape}")
    print("\nTop 5 features by importance (avg across outcomes):")
    top_features = scores_df.mean(axis=1).sort_values(ascending=False).head()
    print(top_features)
except Exception as e:
    print(f"✗ Feature scoring failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("TEST 4: Scenario Discovery (PRIM)")
print("=" * 60)

try:
    # Get first tradeoff scheme and its first tradeoff
    scheme = session.schemes[0]
    tradeoff_name = scheme.bins[0].label
    print(f"Discovering scenarios for tradeoff: {tradeoff_name}")
    
    boxes = session.discover_scenarios(tradeoff_names=[tradeoff_name], method='prim')
    print(f"✓ Discovered {len(boxes)} boxes")
    for box in boxes:
        print(f"  Box: {box.name}")
        print(f"    Density: {box.metrics.get('density', 'N/A'):.3f}")
        print(f"    Coverage: {box.metrics.get('coverage', 'N/A'):.3f}")
        print(f"    Limits: {box.limits}")
except Exception as e:
    print(f"✗ Scenario discovery failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("ALL TESTS PASSED!")
print("=" * 60)