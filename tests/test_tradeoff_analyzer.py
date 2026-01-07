
import unittest
import pandas as pd
import numpy as np
from adept.analysis.tradeoffs import TradeoffAnalyzer

class TestTradeoffAnalyzer(unittest.TestCase):
    def setUp(self):
        self.analyzer = TradeoffAnalyzer()
        self.all_labels = {
            'R': ['fast', 'average', 'slow'],
            'U': ['low', 'average', 'high']
        }
        self.available_tradeoffs = [
            'fast,low', 'fast,average', 'average,low', 'slow,high'
        ]
        self.outputs = ['R', 'U']

    def test_get_nearest_tradeoffs(self):
        # Target: 'fast,high'. Nearest should be 'fast,average' (1 step away)
        # Note: encoding assumes ordinal order
        
        nearest = self.analyzer.get_nearest_tradeoffs(
            'fast,high', 
            self.available_tradeoffs, 
            self.all_labels, 
            self.outputs, 
            k=1
        )
        self.assertEqual(nearest[0], 'fast,average')

if __name__ == '__main__':
    unittest.main()
