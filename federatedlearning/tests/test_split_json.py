#!/usr/bin/env python3
"""
Simple manual test for split JSON approach to NaN handling.
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from adept.core.session import PatternAnalysis

def test_split_json():
    """Test loading with split JSON and CSV."""
    
    print("=" * 60)
    print("Testing Split JSON Approach for NaN Handling")
    print("=" * 60)
    
    # Initialize session
    json_path = "FLsystem_split.json"
    print(f"\n1. Loading system definition from: {json_path}")
    
    session = PatternAnalysis(json_path)
    
    # Load data
    print("2. Loading data with NaN audit...")
    try:
        session.load(validate_integrity=True)
        print("   ✓ Data loaded successfully")
        
        # Print NaN audit results if available
        if hasattr(session, 'nan_audit_report'):
            print("\n3. NaN Audit Report:")
            print(session.nan_audit_report)
        
        # Print basic info
        print(f"\n4. Dataset Info:")
        print(f"   - Experiments shape: {session.experiments_df.shape}")
        print(f"   - Outcomes shape: {session.outcomes_df.shape}")
        print(f"   - Total columns: {len(session.experiments_df.columns)}")
        
        # Check for NaN values in experiments_df
        print(f"\n5. NaN Check in Experiments DF:")
        nan_counts = session.experiments_df.isnull().sum()
        nan_cols = nan_counts[nan_counts > 0]
        print(f"   - Columns with NaN: {len(nan_cols)}")
        if len(nan_cols) > 0:
            print(f"   - Examples:")
            for col, count in nan_cols.head(5).items():
                print(f"     * {col}: {count} NaN values")
        
        # Check pattern columns specifically
        pattern_cols = ['client_selector_pattern', 'message_compressor_pattern', 'hdh_pattern']
        print(f"\n6. Pattern Column Values:")
        for col in pattern_cols:
            if col in session.experiments_df.columns:
                values = session.experiments_df[col].unique()
                print(f"   - {col}: {list(values)}")
                nan_count = session.experiments_df[col].isnull().sum()
                print(f"     NaN count: {nan_count}")
        
        # Check config_id
        if 'config_id' in session.experiments_df.columns:
            print(f"\n7. Configuration IDs:")
            configs = session.experiments_df['config_id'].unique()
            print(f"   Unique configs: {list(configs)}")
            for config in configs:
                count = (session.experiments_df['config_id'] == config).sum()
                print(f"   - {config}: {count} rows")
        
        print("\n" + "=" * 60)
        print("Test completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n✗ Error during load: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    return True

if __name__ == '__main__':
    success = test_split_json()
    sys.exit(0 if success else 1)