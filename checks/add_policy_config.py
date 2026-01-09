import pandas as pd
import os

# Define file path
csv_path = 'patterns/Toy_Example/data/merged.csv'

# Check if file exists
if not os.path.exists(csv_path):
    print(f"Error: {csv_path} not found.")
else:
    # Load CSV
    df = pd.read_csv(csv_path)
    
    # Create 'policy_config' column
    # Ensure d1Services, d2Services, d3Services are treated as strings for concatenation
    # Handle potential float types if any NaNs exist (though unlikely in this context)
    df['policy_config'] = (
        df['d1Services'].astype(str) + "_" + 
        df['d2Services'].astype(str) + "_" + 
        df['d3Services'].astype(str)
    )
    
    # Save back to CSV
    df.to_csv(csv_path, index=False)
    
    print(f"Successfully added 'policy_config' to {csv_path}")
    print("\nFirst 5 rows:")
    print(df[['d1Services', 'd2Services', 'd3Services', 'policy_config']].head())