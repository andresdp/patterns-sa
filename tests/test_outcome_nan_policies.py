"""nan_policy of quality objectives during tradeoff definition, and NaN-semantics lint warnings."""
import unittest

import numpy as np
import pandas as pd

from adept.analysis.discretization import DataProcessor, FAILURE_LABEL
from adept.core.models import QualityObjective, SystemDefinition
from adept.utils.linter import SystemLinter


def discretize(df, objectives, n_bins=2):
    return DataProcessor.define_tradeoffs(df, method="discretization", objectives=objectives,
                                          n_bins=n_bins, all_labels=None, ranges=None)


class TestWorstCaseFailureBin(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"time": [10.0, 20.0, 30.0, np.nan], "f1": [0.1, 0.2, 0.3, 0.4]})
        self.objectives = [QualityObjective(name="time", maximize=False), QualityObjective(name="f1")]

    def test_failed_runs_get_a_dedicated_bin(self):
        labeled, schemes, indices, _ = discretize(self.df, self.objectives)
        self.assertEqual(labeled["time"].iloc[3], FAILURE_LABEL)
        time_scheme = next(s for s in schemes if s.objective_name == "time")
        self.assertEqual([b.label for b in time_scheme.bins], ["level_1", "level_2", FAILURE_LABEL])
        self.assertTrue(any(k.startswith(FAILURE_LABEL) for k in indices))

    def test_bins_are_computed_from_observed_values_only(self):
        _, schemes, _, _ = discretize(self.df, self.objectives)
        time_scheme = next(s for s in schemes if s.objective_name == "time")
        # Equal-width bins over the observed 10-30 range (padded by 0.1), not stretched by the failure
        self.assertAlmostEqual(time_scheme.bins[1].max_value, 30.1)
        self.assertGreater(time_scheme.bins[2].min_value, 30.1)

    def test_other_methods_keep_imputed_worst_values(self):
        labeled, _, _, _ = DataProcessor.define_tradeoffs(
            self.df, method="threshold", objectives=self.objectives,
            params={"thresholds": {"time": 25.0, "f1": 0.2}})
        self.assertEqual(labeled["time"].iloc[3], "unsatisfactory")


class TestDropPolicy(unittest.TestCase):
    def setUp(self):
        self.df = pd.DataFrame({"time": [10.0, 20.0, 30.0, np.nan], "f1": [0.1, 0.2, 0.3, 0.4]})
        self.objectives = [QualityObjective(name="time", maximize=False, nan_policy="drop"), QualityObjective(name="f1")]

    def test_dropped_runs_belong_to_no_tradeoff(self):
        for method, extra in (("discretization", {"n_bins": 2, "all_labels": None, "ranges": None}),
                              ("threshold", {"params": {"thresholds": {"time": 25.0, "f1": 0.2}}})):
            labeled, _, indices, _ = DataProcessor.define_tradeoffs(self.df, method=method, objectives=self.objectives, **extra)
            self.assertTrue(pd.isna(labeled["time"].iloc[3]), method)
            covered = set(np.concatenate(list(indices.values())))
            self.assertEqual(covered, {0, 1, 2}, method)


class TestNanSemanticsLint(unittest.TestCase):
    def make_sys_def(self, optional=False, nan_policy=None):
        objective = {"name": "o1", "maximize": False}
        if nan_policy:
            objective["nan_policy"] = nan_policy
        return SystemDefinition.model_validate({
            "system": {"name": "T", "components": {"c1": {"name": "C1", "parameters": {
                "p1": {"level": "system", "type": "lever", "optional": optional}}}}},
            "dataspace": {"configuration_identification": {"from": "column", "column": "pol", "configurations": {}},
                          "quality_objectives": [objective]},
        })

    def nan_warnings(self, sys_def, df):
        return [i for i in SystemLinter()._validate_nan_semantics(sys_def, df)]

    def test_mostly_nan_required_parameter_is_flagged(self):
        df = pd.DataFrame({"p1": [1.0, np.nan, np.nan], "o1": [1.0, 2.0, 3.0]})
        issues = self.nan_warnings(self.make_sys_def(), df)
        self.assertEqual(len(issues), 1)
        self.assertIn("not declared optional", issues[0].message)
        self.assertEqual(self.nan_warnings(self.make_sys_def(optional=True), df), [])

    def test_objective_nans_without_explicit_policy_are_flagged(self):
        df = pd.DataFrame({"p1": [1.0, 2.0, 3.0], "o1": [1.0, np.nan, 3.0]})
        issues = self.nan_warnings(self.make_sys_def(), df)
        self.assertEqual(len(issues), 1)
        self.assertIn("nan_policy", issues[0].message)
        self.assertEqual(self.nan_warnings(self.make_sys_def(nan_policy="worst_case"), df), [])


if __name__ == "__main__":
    unittest.main()
