#!/usr/bin/env python3
"""
Pre-processing script to split AP List column into separate pattern columns.

This transforms FL CSV from a combined pattern representation:
  AP List (client_selector,message_compressor,heterogeneous_data_handler): {OFF,OFF,OFF}

To separate columns for each pattern:
  client_selector_pattern: OFF
  message_compressor_pattern: OFF
  hdh_pattern: OFF

Also converts to standard comma-delimited CSV format.
"""

import pandas as pd
import sys
import os

def split_ap_list(input_csv: str, output_csv: str = None) -> None:
    """
    Splits AP List column into separate pattern columns.
    
    Args:
        input_csv: Path to input CSV file
        output_csv: Path to output CSV file (if None, overwrites input)
    """
    # Read CSV with semicolon delimiter
    print(f"Reading input file: {input_csv}")
    df = pd.read_csv(input_csv, delimiter=';')
    
    # Replace decimal commas with dots (European format to standard)
    # Only do this for string/object columns that look like numbers
    for col in df.select_dtypes(include=['object']).columns:
        # Replace comma with dot for decimal values
        # Pattern: "3,5" -> "3.5"
        df[col] = df[col].astype(str).str.replace(r',(?=\d)', '.', regex=True)
    
    # Find AP List column (might have suffix)
    ap_list_col = None
    for col in df.columns:
        if 'AP List' in col:
            ap_list_col = col
            print(f"Found AP List column: '{ap_list_col}'")
            break
    
    if ap_list_col is None:
        print("ERROR: 'AP List' column not found in CSV")
        print(f"Available columns: {list(df.columns)}")
        sys.exit(1)
    
    # Parse AP List column
    print(f"Parsing AP List column with {len(df)} rows...")
    
    # Remove braces and split by comma
    # Format: {OFF,OFF,OFF} -> [OFF, OFF, OFF]
    df[ap_list_col] = df[ap_list_col].astype(str)
    df[ap_list_col] = df[ap_list_col].str.replace('{', '', regex=False)
    df[ap_list_col] = df[ap_list_col].str.replace('}', '', regex=False)
    
    # Split into three parts
    ap_split = df[ap_list_col].str.split(',', expand=True)
    
    # Create three new columns
    df['client_selector_pattern'] = ap_split[0].str.strip()
    df['message_compressor_pattern'] = ap_split[1].str.strip()
    df['hdh_pattern'] = ap_split[2].str.strip()
    
    # Create configuration_id column for JSON mapping
    df['config_id'] = df['client_selector_pattern'] + ',' + df['message_compressor_pattern'] + ',' + df['hdh_pattern']
    
    # Verify unique values
    print("\nPattern value distributions:")
    print(f"  client_selector_pattern: {df['client_selector_pattern'].unique().tolist()}")
    print(f"  message_compressor_pattern: {df['message_compressor_pattern'].unique().tolist()}")
    print(f"  hdh_pattern: {df['hdh_pattern'].unique().tolist()}")
    print(f"\nConfiguration IDs: {df['config_id'].unique().tolist()}")
    
    # Drop old AP List column
    df = df.drop(columns=[ap_list_col])
    
    # Determine output path
    if output_csv is None:
        output_csv = input_csv
        print(f"\nOverwriting input file: {output_csv}")
    else:
        print(f"\nWriting output file: {output_csv}")
    
    # Write back with comma delimiter (standard format)
    df.to_csv(output_csv, index=False)
    print(f"Successfully wrote {len(df)} rows with {len(df.columns)} columns")
    print(f"Output format: comma-delimited CSV")
    
    # Print some sample data
    print("\nSample rows (first 3):")
    print(df[['config_id', 'client_selector_pattern', 'message_compressor_pattern', 'hdh_pattern', 
              'Model', 'Dataset', 'Total Clients']].head(3).to_string(index=False))

if __name__ == '__main__':
    # Default paths
    input_csv = 'FLwithAP_MLdata.csv'
    output_csv = 'FLwithAP_MLdata_split.csv'
    
    # Allow command line arguments
    if len(sys.argv) > 1:
        input_csv = sys.argv[1]
    if len(sys.argv) > 2:
        output_csv = sys.argv[2]
    
    # Run preprocessing
    split_ap_list(input_csv, output_csv)