
import unittest
import os
import pandas as pd
from adept import PatternAnalysis

class TestPatternMigration(unittest.TestCase):
    def setUp(self):
        self.patterns = [
            "patterns/Gateway_Aggregation/Gateway_Aggregation.json",
            "patterns/Gateway_Offloading/Gateway_Offloading.json",
            "patterns/CQRS/CQRS.json",
            "patterns/Anti_Corruption_Layer/Anti_Corruption_Layer.json"
        ]

    def test_load_and_validate_migrated_patterns(self):
        """Verifies that all migrated JSON definitions can be loaded and validated."""
        for json_path in self.patterns:
            print(f"\nTesting migration for: {json_path}")
            session = PatternAnalysis(json_path)
            
            # This should load both system definition and CSV data
            # validate_integrity=True will catch column mismatches
            try:
                session.load(validate_integrity=True)
                
                # Check data presence
                self.assertIsNotNone(session.experiments_df)
                self.assertIsNotNone(session.outcomes_df)
                self.assertFalse(session.experiments_df.empty)
                
                # Verify objectives were correctly mapped/renamed
                for obj in session.sys_def.dataspace.quality_objectives:
                    self.assertIn(obj.name, session.outcomes_df.columns)
                
                print(f"SUCCESS: {json_path} loaded correctly.")
                
            except Exception as e:
                print(f"FAILURE: {json_path} failed to load: {e}")
                raise e

if __name__ == '__main__':
    unittest.main()
