import unittest
import pandas as pd
import numpy as np

from adept.utils.nan_handler import SemanticNaNHandler
from adept.core.models import Parameter, QualityObjective, ParameterType, ParameterLevel


def make_param(name, optional=False):
    return Parameter(
        name=name,
        level=ParameterLevel.SYSTEM,
        type=ParameterType.UNCERTAINTY,
        optional=optional,
    )


def make_objective(name, maximize=True, nan_policy="worst_case", nan_value=None):
    return QualityObjective(
        name=name,
        maximize=maximize,
        nan_policy=nan_policy,
        nan_value=nan_value,
    )


class TestAuditNanProportions(unittest.TestCase):
    """R12: audit_nan_proportions overall and per-column percentages."""

    def test_overall_and_per_column_percentages_on_known_pattern(self):
        # 4 rows x 2 cols = 8 cells. col A has 2 NaNs (50%), col B has 0.
        # Overall: 2/8 = 25%.
        df = pd.DataFrame({
            "A": [1.0, np.nan, 3.0, np.nan],
            "B": [1.0, 2.0, 3.0, 4.0],
        })
        stats = SemanticNaNHandler.audit_nan_proportions(df)
        self.assertEqual(stats["total_cells"], 8)
        self.assertEqual(stats["total_nans"], 2)
        self.assertAlmostEqual(stats["overall_pct"], 25.0)
        self.assertAlmostEqual(stats["columns"]["A"], 50.0)
        self.assertAlmostEqual(stats["columns"]["B"], 0.0)

    def test_empty_dataframe_does_not_crash(self):
        stats = SemanticNaNHandler.audit_nan_proportions(pd.DataFrame())
        self.assertEqual(stats, {})

    def test_none_input_does_not_crash(self):
        stats = SemanticNaNHandler.audit_nan_proportions(None)
        self.assertEqual(stats, {})


class TestImputeOutcomes(unittest.TestCase):
    """R12: impute_outcomes' worst_case x maximize/minimize, fixed_value, drop."""

    def test_worst_case_maximize_fills_below_observed_minimum(self):
        obj = make_objective("obj1", maximize=True, nan_policy="worst_case")
        df = pd.DataFrame({"obj1": [1.0, 2.0, np.nan]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        filled = out["obj1"].iloc[2]
        self.assertFalse(pd.isna(filled))
        self.assertLess(filled, df["obj1"].min())
        # Matches the implementation's exact formula: min - 0.1 * range.
        self.assertAlmostEqual(filled, 1.0 - 0.1 * (2.0 - 1.0))

    def test_worst_case_minimize_fills_above_observed_maximum(self):
        obj = make_objective("obj1", maximize=False, nan_policy="worst_case")
        df = pd.DataFrame({"obj1": [1.0, 2.0, np.nan]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        filled = out["obj1"].iloc[2]
        self.assertFalse(pd.isna(filled))
        self.assertGreater(filled, df["obj1"].max())
        self.assertAlmostEqual(filled, 2.0 + 0.1 * (2.0 - 1.0))

    def test_fixed_value_policy_fills_with_specified_value(self):
        obj = make_objective("obj1", nan_policy="fixed_value", nan_value=42.0)
        df = pd.DataFrame({"obj1": [1.0, np.nan, 3.0]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        self.assertEqual(out["obj1"].iloc[1], 42.0)

    def test_drop_policy_leaves_nan_in_place(self):
        obj = make_objective("obj1", nan_policy="drop")
        df = pd.DataFrame({"obj1": [1.0, np.nan, 3.0]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        self.assertTrue(pd.isna(out["obj1"].iloc[1]))
        self.assertEqual(len(out), len(df))  # no rows dropped -- caller's job per source comment

    def test_column_with_zero_nans_is_noop(self):
        obj = make_objective("obj1", nan_policy="fixed_value", nan_value=99.0)
        df = pd.DataFrame({"obj1": [1.0, 2.0, 3.0]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        pd.testing.assert_series_equal(out["obj1"], df["obj1"])

    def test_objective_missing_from_dataframe_is_skipped(self):
        obj = make_objective("not_present", nan_policy="fixed_value", nan_value=99.0)
        df = pd.DataFrame({"obj1": [1.0, 2.0, 3.0]})
        out = SemanticNaNHandler.impute_outcomes(df, [obj])
        pd.testing.assert_frame_equal(out, df)


class TestApplySentinelTransformation(unittest.TestCase):
    """R12: apply_sentinel_transformation numeric/categorical/optional handling."""

    def test_numeric_optional_column_gets_sentinel_below_minimum(self):
        param = make_param("p_num", optional=True)
        df = pd.DataFrame({"p_num": [1.0, 2.0, np.nan]})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        self.assertFalse(out["p_num"].isnull().any())
        self.assertIn("p_num", sentinels)
        self.assertLess(sentinels["p_num"], df["p_num"].min())
        self.assertEqual(out["p_num"].iloc[2], sentinels["p_num"])

    def test_categorical_optional_column_becomes_binary_presence_flag(self):
        param = make_param("p_cat", optional=True)
        df = pd.DataFrame({"p_cat": ["x", None, "y"]})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        self.assertEqual(list(out["p_cat"]), [1.0, 0.0, 1.0])
        self.assertEqual(sentinels["p_cat"], 0.0)

    def test_non_optional_column_is_left_untouched(self):
        param = make_param("p_required", optional=False)
        df = pd.DataFrame({"p_required": [1.0, np.nan, 3.0]})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        self.assertTrue(out["p_required"].isnull().iloc[1])
        pd.testing.assert_series_equal(out["p_required"], df["p_required"])
        self.assertNotIn("p_required", sentinels)

    def test_mixed_columns_only_optional_ones_are_transformed(self):
        # Confirms optional-only scoping when both optional and non-optional
        # columns with NaNs are present in the same frame.
        opt_param = make_param("p_opt", optional=True)
        req_param = make_param("p_req", optional=False)
        df = pd.DataFrame({
            "p_opt": [1.0, np.nan, 3.0],
            "p_req": [1.0, np.nan, 3.0],
        })
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [opt_param, req_param])
        self.assertFalse(out["p_opt"].isnull().any())
        self.assertTrue(out["p_req"].isnull().any())
        self.assertIn("p_opt", sentinels)
        self.assertNotIn("p_req", sentinels)

    def test_numeric_optional_column_with_zero_nans_is_noop(self):
        param = make_param("p_num", optional=True)
        df = pd.DataFrame({"p_num": [1.0, 2.0, 3.0]})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        pd.testing.assert_series_equal(out["p_num"], df["p_num"])
        self.assertNotIn("p_num", sentinels)

    def test_fully_nan_categorical_optional_column_becomes_all_zero_flag(self):
        param = make_param("p_cat", optional=True)
        df = pd.DataFrame({"p_cat": pd.Series([None, None, None], dtype=object)})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        self.assertFalse(out["p_cat"].isnull().any())
        self.assertEqual(list(out["p_cat"]), [0.0, 0.0, 0.0])
        self.assertEqual(sentinels["p_cat"], 0.0)

    def test_fully_nan_numeric_optional_column_current_behavior(self):
        # Documents actual behavior of the unmodified implementation: with an
        # all-NaN numeric column, min()/max() are both NaN, so the computed
        # sentinel is NaN and fillna(NaN) is a no-op -- the column stays all
        # NaN. Unlike the categorical branch, this numeric edge case is NOT
        # transformed into a usable sentinel by the current code. This test
        # pins that real behavior rather than asserting an aspirational one.
        param = make_param("p_num", optional=True)
        df = pd.DataFrame({"p_num": pd.Series([np.nan, np.nan, np.nan])})
        out, sentinels = SemanticNaNHandler.apply_sentinel_transformation(df, [param])
        self.assertTrue(out["p_num"].isnull().all())


if __name__ == "__main__":
    unittest.main()
