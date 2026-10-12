"""Contingency analysis by policy grouping (composite vs. marginal decisions).

In a multi-decision system a decision policy (e.g. hdh_pattern=ON) pools every
configuration that contains it, so contingency is reported per configuration by default
(composite decisions) and per decision on request (marginal view).
"""
import contextlib
import io
import os
import sys
import unittest

from adept import PatternAnalysis

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
SPEC = os.path.join(FL_DIR, "compact", "FLsystem_compact_all.json")
sys.path.insert(0, FL_DIR)

import fl_slices  # noqa: E402

OBJECTIVES = {"final_val_accuracy": ["S", "M", "L"], "avg_total_time": ["S", "M", "L"]}
CONFIGS = ["OFF,OFF,OFF", "OFF,OFF,ON", "OFF,ON,OFF", "OFF,ON,ON",
           "ON,OFF,OFF", "ON,OFF,ON", "ON,ON,OFF", "ON,ON,ON"]
DECISIONS = ["client_selector_pattern", "message_compressor_pattern", "hdh_pattern"]


def load(**filters):
    session = PatternAnalysis(SPEC)
    with contextlib.redirect_stdout(io.StringIO()):
        session.load(preprocessor=fl_slices.slice_filter(**filters))
        session.create_tradeoffs(method="discretization", labels=OBJECTIVES)
    return session


def quiet(fn, *args, **kwargs):
    out = io.StringIO()
    with contextlib.redirect_stdout(out):
        result = fn(*args, **kwargs)
    return result, out.getvalue()


class TestCompositeContingency(unittest.TestCase):
    """All 8 configurations: 8 clients, image task, common environment (10 runs each)."""

    @classmethod
    def setUpClass(cls):
        cls.session = load(clients=8, task="image", environment="common")

    def test_default_rows_are_configurations(self):
        counts = self.session.get_policy_contingency_matrix(normalization_mode="none")
        self.assertEqual(list(counts.index), CONFIGS)
        self.assertTrue((counts.sum(axis=1) == 10).all())

    def test_marginal_rows_pool_their_configurations(self):
        s = self.session
        counts = s.get_policy_contingency_matrix(normalization_mode="none")
        for position, decision in enumerate(DECISIONS):
            marginal = s.get_policy_contingency_matrix(decision, normalization_mode="none")
            for policy in ("OFF", "ON"):
                with self.subTest(decision=decision, policy=policy):
                    rows = [c for c in CONFIGS if c.split(",")[position] == policy]
                    self.assertEqual(list(marginal.loc[policy]), list(counts.loc[rows].sum()))

    def test_decision_grouping_stacks_qualified_rows(self):
        stacked = self.session.get_policy_contingency_matrix(by="decision", normalization_mode="none")
        self.assertEqual(list(stacked.index), [f"{d}:{p}" for d in DECISIONS for p in ("OFF", "ON")])
        hdh = self.session.get_policy_contingency_matrix(by="hdh_pattern", normalization_mode="none")
        self.assertEqual(list(stacked.loc["hdh_pattern:ON"]), list(hdh.loc["ON"]))

    def test_decision_key_is_shorthand_for_by(self):
        s = self.session
        self.assertTrue(s.get_policy_contingency_matrix("hdh_pattern").equals(
            s.get_policy_contingency_matrix(by="hdh_pattern")))
        with self.assertRaises(ValueError):
            s.get_policy_contingency_matrix("hdh_pattern", by="configuration")

    def test_column_grouping(self):
        counts = self.session.get_policy_contingency_matrix(by="Pattern Types Active", normalization_mode="none")
        self.assertEqual(list(counts.index), [f"Pattern Types Active={k}" for k in range(4)])
        self.assertEqual(list(counts.sum(axis=1)), [10, 30, 30, 10])

    def test_marginal_exclusivity_can_come_from_a_combination(self):
        """A tradeoff reached only by configurations sharing two ON policies looks exclusive to
        each of those policies in the marginal view, but the composite view names the
        configurations that reach it."""
        s = self.session
        counts = s.get_policy_contingency_matrix(normalization_mode="none")
        for decision_pair, tradeoff in s.get_exclusive_tradeoffs(by="decision"):
            decision, policy = decision_pair.split(":")
            position = DECISIONS.index(decision)
            reaching = counts.index[counts[tradeoff] > 0]
            with self.subTest(pair=decision_pair, tradeoff=tradeoff):
                self.assertTrue(all(c.split(",")[position] == policy for c in reaching))

    def test_shares_are_fractions(self):
        s = self.session
        for policy, distribution in [(c, s.get_policy_tradeoff_distribution(policy_name=c)) for c in CONFIGS]:
            with self.subTest(policy=policy):
                self.assertAlmostEqual(sum(distribution.values()), 1.0)
        shares = s.get_policy_contingency_matrix()  # 'population': share of each group's runs
        self.assertTrue(((shares >= 0) & (shares <= 1)).all().all())
        self.assertTrue(((shares.sum(axis=1) - 1).abs() < 1e-9).all())
        # A threshold above every share finds no deterministic group
        self.assertEqual(s.get_deterministic_policies(threshold=1.01), [])

    def test_varying_decisions(self):
        self.assertEqual(self.session.get_varying_decisions(), DECISIONS)


class TestDecisionContrasts(unittest.TestCase):
    """Matched one-factor contrasts: a pattern ON vs. OFF within comparable settings."""

    MATCH_ON = ["Dataset", "Total Clients", *fl_slices.ENVIRONMENT_COLUMNS]
    OBJECTIVES = ["final_val_accuracy", "avg_total_time"]

    @classmethod
    def setUpClass(cls):
        cls.session = load()
        cls.raw = cls.session.raw_df

    def test_pattern_alone_vs_baseline(self):
        settings, summary = self.session.get_decision_contrasts(
            "hdh_pattern", self.MATCH_ON, objectives=self.OBJECTIVES, tradeoffs=["M-S"])
        self.assertEqual(list(summary.index), ["client_selector_pattern=OFF, message_compressor_pattern=OFF"])
        # Recompute one setting by hand from the raw runs
        row = settings.iloc[0]
        same = (self.raw[self.MATCH_ON] == row[self.MATCH_ON]).all(axis=1)
        ref = self.raw[same & (self.raw["config_id"] == "OFF,OFF,OFF")]
        treat = self.raw[same & (self.raw["config_id"] == "OFF,OFF,ON")]
        self.assertEqual((row["runs ref"], row["runs treat"]), (len(ref), len(treat)))
        expected = treat["final_val_accuracy"].mean() - ref["final_val_accuracy"].mean()
        self.assertAlmostEqual(row["final_val_accuracy diff"], expected)
        self.assertIn("M-S diff", settings.columns)
        # Equal weights: the summary mean is the plain mean over settings
        self.assertAlmostEqual(summary["avg_total_time diff mean"].iloc[0], settings["avg_total_time diff"].mean())
        self.assertEqual(summary["settings"].iloc[0], len(settings))

    def test_only_settings_with_both_configurations(self):
        settings, _ = self.session.get_decision_contrasts("client_selector_pattern", self.MATCH_ON,
                                                          objectives=self.OBJECTIVES)
        self.assertTrue(((settings["runs ref"] > 0) & (settings["runs treat"] > 0)).all())
        baseline_points = self.raw[self.raw["config_id"] == "OFF,OFF,OFF"].groupby(self.MATCH_ON).ngroups
        self.assertLess(len(settings), baseline_points)

    def test_every_context_of_the_other_decisions(self):
        _, summary = self.session.get_decision_contrasts("hdh_pattern", self.MATCH_ON, others="all",
                                                         objectives=self.OBJECTIVES)
        self.assertEqual(len(summary), 4)  # 2 x 2 policies of the other two decisions

    def test_single_configuration_has_no_contrast(self):
        baseline = load(name="baseline")
        out = io.StringIO()
        with contextlib.redirect_stdout(out):
            settings, summary = baseline.get_decision_contrasts("hdh_pattern", self.MATCH_ON)
        self.assertTrue(settings.empty and summary.empty)
        self.assertIn("no setting", out.getvalue())


class TestSingleConfigurationSlice(unittest.TestCase):
    """The baseline slice: every decision has a single policy (OFF)."""

    @classmethod
    def setUpClass(cls):
        cls.session = load(name="baseline", clients=8, task="image")

    def test_no_decision_varies(self):
        self.assertEqual(self.session.get_varying_decisions(), [])

    def test_exclusivity_needs_two_groups(self):
        for by in ("configuration", "hdh_pattern", "decision"):
            with self.subTest(by=by):
                pairs, printed = quiet(self.session.get_exclusive_tradeoffs, by=by)
                self.assertEqual(pairs, [])
                self.assertIn("single policy group", printed)

    def test_context_grouping_still_compares(self):
        pairs, printed = quiet(self.session.get_exclusive_tradeoffs, by="delay_percentage")
        self.assertNotIn("single policy group", printed)
        counts = self.session.get_policy_contingency_matrix(by="delay_percentage", normalization_mode="none")
        self.assertGreater(len(counts.index), 1)


if __name__ == "__main__":
    unittest.main()
