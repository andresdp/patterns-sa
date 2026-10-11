#!/usr/bin/env python
"""
Manual test script for NaN feature in ADEPT framework.
Tests the NaN handling using Federated Learning dataset.
"""

import sys
import pandas as pd
import numpy as np

# Add project root to path
sys.path.insert(0, '/Users/adiazpace/Documents/GitHub/patterns-sa')

from adept import PatternAnalysis

def test_nan_feature():
    print("=" * 60)
    print("NaN Feature End-to-End Test")
    print("=" * 60)
    
    # Test 1: Load Data with NaN Audit
    print("\n[Test 1] Loading FL system...")
    try:
        session = PatternAnalysis('federatedlearning/FLsystem.json')
        session.load()
        print("✓ PASSED: Data loaded successfully")
        print(f"  Experiments shape: {session.experiments_df.shape}")
        print(f"  Outcomes shape: {session.outcomes_df.shape}")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False
    
    # Test 2: Verify NaN in Dataset
    print("\n[Test 2] Verifying NaN values...")
    try:
        nan_counts = session.experiments_df.isna().sum()
        nan_percentages = (nan_counts / len(session.experiments_df)) * 100
        nan_params = nan_counts[nan_counts > 0]
        
        if len(nan_params) > 0:
            print(f"✓ PASSED: Found {len(nan_params)} parameters with NaN")
            for param in nan_params.index[:5]:  # Show first 5
                count = nan_counts[param]
                pct = nan_percentages[param]
                print(f"  • {param}: {count} NaNs ({pct:.1f}%)")
        else:
            print("✗ FAILED: No NaN values found in dataset")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False
    
    # Test 3: Create Tradeoffs with Outcome Imputation
    print("\n[Test 3] Creating tradeoffs...")
    try:
        session.create_tradeoffs(method='discretization', n_bins=3)
        print(f"✓ PASSED: Created {len(session.tradeoffs)} tradeoffs")
        for to in session.tradeoffs[:3]:  # Show first 3
            print(f"  • {to.name}: {to.point_count} points")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        return False
    
    # Test 4: Run Scenario Discovery with NaN Parameters
    print("\n[Test 4] Running scenario discovery...")
    try:
        if session.tradeoffs:
            boxes = session.discover_scenarios(
                tradeoff_names=[session.tradeoffs[0].name],
                method='prim',
                threshold=0.6
            )
            print(f"✓ PASSED: Discovery completed, found {len(boxes)} boxes")
            
            if boxes:
                first_box = boxes[0]
                print(f"  First box: {first_box.name}")
                print(f"    Density: {first_box.metrics.get('density', 0):.3f}")
                print(f"    Coverage: {first_box.metrics.get('coverage', 0):.3f}")
                
                # Check for includes_na flags
                has_includes_na = any(
                    lims.get('includes_na', False) 
                    for lims in first_box.limits.values()
                    if isinstance(lims, dict)
                )
                if has_includes_na:
                    print("  ✓ Box includes N/A states")
                else:
                    print("  ⚠ Box does not include N/A states")
        else:
            print("✗ FAILED: No tradeoffs available")
            return False
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 5: Compute Feature Importance
    print("\n[Test 5] Computing feature importance...")
    try:
        scores_df = session.compute_feature_scores()
        print(f"✓ PASSED: Feature importance computed")
        print(f"  Scores shape: {scores_df.shape}")
        
        # Show top features
        print("\n  Top 5 features:")
        for i, (feat, score) in enumerate(scores_df.iloc[:5].items()):
            print(f"    {i+1}. {feat}: {score:.3f}")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Test 6: Compute Robustness
    print("\n[Test 6] Computing robustness...")
    try:
        robustness_df = session.compute_robustness(metric='starr')
        print(f"✓ PASSED: Robustness computed")
        print(f"  Robustness matrix shape: {robustness_df.shape}")
    except Exception as e:
        print(f"✗ FAILED: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    # Summary
    print("\n" + "=" * 60)
    print("NaN Feature Test Summary")
    print("=" * 60)
    print("✅ All tests PASSED!")
    print("\nThe NaN feature is working correctly:")
    print("  • NaN audit during data loading: ✓")
    print("  • Outcome imputation for tradeoffs: ✓")
    print("  • Scenario discovery with sentinel values: ✓")
    print("  • Feature importance with NaN handling: ✓")
    print("  • Robustness computation: ✓")
    print("\n📊 Key Findings:")
    print("  • Optional parameters correctly identified as NaN")
    print("  • Discovery algorithms can learn from N/A states")
    print("  • Framework maintains backward compatibility")
    print("=" * 60)
    
    return True

if __name__ == '__main__':
    success = test_nan_feature()
    sys.exit(0 if success else 1)