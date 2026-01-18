
import unittest
import pandas as pd
import numpy as np
from adept.core.models import BehavioralTrace
from adept.analysis.behavioral import BehavioralAnalyzer

class TestBehavioralAnalysis(unittest.TestCase):
    def setUp(self):
        # Mock trace: Converges to 100 after 5 steps
        data = {
            "cycle": range(10),
            "performance": [10, 50, 80, 95, 99, 100, 100, 100, 100, 100],
            "cost": [10, 10, 10, 10, 10, 10, 10, 10, 10, 10]
        }
        self.df = pd.DataFrame(data)
        self.trace = BehavioralTrace(trace_id="t1", scenario_id="s1", outcomes=self.df)
        self.analyzer = BehavioralAnalyzer()

    def test_convergence_time(self):
        # Should converge when value stays within 1% of final value
        # Final value is 100.
        # cycle 4: 99 (within 1%) -> Convergence at cycle 4?
        # Let's see the logic. Usually it's when it enters and stays.
        ct = self.analyzer.compute_convergence_time(self.trace, "performance", threshold=0.01)
        self.assertEqual(ct, 4)

    def test_stability_score(self):
        # Stable trace (variance of tail)
        stability = self.analyzer.compute_stability(self.trace, "performance", window=3)
        self.assertEqual(stability, 0.0) # Last 3 are identical

        # Unstable trace
        unstable_df = pd.DataFrame({"cycle": range(5), "val": [10, 90, 10, 90, 10]})
        unstable_trace = BehavioralTrace(trace_id="t2", scenario_id="s2", outcomes=unstable_df)
        stab = self.analyzer.compute_stability(unstable_trace, "val", window=3)
        self.assertGreater(stab, 0.0)

    def test_performance_integral(self):
        # Area under curve
        # Cost is constant 10. For 10 cycles (0-9), integral roughly 10 * 9? 
        # Using trapezoidal rule
        integral = self.analyzer.compute_integral(self.trace, "cost")
        self.assertTrue(80 <= integral <= 100) # depending on implementation

if __name__ == '__main__':
    unittest.main()
