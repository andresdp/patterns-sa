import os
import sys
import unittest

from adept import PatternAnalysis

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
FL_DIR = os.path.join(REPO_ROOT, "federatedlearning")
sys.path.insert(0, FL_DIR)

from preprocess_fl_clients import preprocess_fl  # noqa: E402

F1, TIME = "best_val_f1", "avg_total_time"


class TestObjectiveSelection(unittest.TestCase):
    """Creating tradeoffs over a subset of objectives narrows the whole session to it."""

    @classmethod
    def setUpClass(cls):
        cls.session = PatternAnalysis(os.path.join(FL_DIR, "FLsystem_split.json"))
        cls.session.load(preprocessor=preprocess_fl)
        cls.all_objectives = list(cls.session.outcomes_df.columns)

    def setUp(self):
        self.session.select_objectives(None)

    def assert_narrowed_to(self, objectives):
        s = self.session
        self.assertEqual(list(s.outcomes_df.columns), objectives)
        self.assertEqual(list(s.discrete_df.columns), objectives)
        self.assertEqual([sc.objective_name for sc in s.schemes], objectives)
        self.assertEqual([o.name for o in s.get_outcomes()], objectives)
        for key in s.tradeoff_indices:
            self.assertEqual(len(key.split(",")), len(objectives))

    def test_labels_keys_select_objectives(self):
        labels = {F1: ["S", "M", "L"], TIME: ["S", "M", "L"]}
        tradeoffs, _ = self.session.create_tradeoffs(method="discretization", labels=labels)
        self.assertEqual(len(tradeoffs), 9)
        self.assert_narrowed_to([F1, TIME])

    def test_explicit_objectives_select_objectives(self):
        tradeoffs, _ = self.session.create_tradeoffs(
            method="discretization", n_bins=3, objectives=[F1, TIME]
        )
        self.assertEqual(len(tradeoffs), 9)
        self.assert_narrowed_to([F1, TIME])

    def test_membership_counts_cover_all_rows(self):
        tradeoffs, _ = self.session.create_tradeoffs(method="discretization", objectives=[F1, TIME])
        counts = [len(self.session.get_indices_for_tradeoff(t)) for t in tradeoffs]
        self.assertEqual(sum(counts), len(self.session.outcomes_df))

    def test_reselection_starts_from_full_outcomes(self):
        self.session.create_tradeoffs(method="discretization", objectives=[F1])
        self.session.create_tradeoffs(method="discretization", objectives=[TIME, F1])
        self.assert_narrowed_to([TIME, F1])

        self.session.create_tradeoffs(method="discretization", n_bins=2)
        self.assertEqual(list(self.session.outcomes_df.columns), self.all_objectives)
        self.assertEqual(len(self.session.schemes), len(self.all_objectives))
        self.assertIsNone(self.session.active_objectives)

    def test_threshold_keys_select_objectives(self):
        tradeoffs, _ = self.session.create_tradeoffs(
            method="threshold", thresholds={F1: 0.3, TIME: 200}
        )
        self.assertEqual(len(tradeoffs), 4)
        self.assert_narrowed_to([F1, TIME])

    def test_split_and_feature_scores_follow_selection(self):
        self.session.create_tradeoffs(method="discretization", objectives=[F1, TIME])
        self.session.split_data(test_size=0.3, verbose=False)
        scores = self.session.compute_feature_scores(subset="train")
        self.assertEqual(sorted(scores.columns), sorted([F1, TIME]))

    def test_labels_outside_objectives_rejected(self):
        with self.assertRaises(ValueError):
            self.session.create_tradeoffs(
                method="discretization", objectives=[F1], labels={TIME: ["S", "M", "L"]}
            )

    def test_unknown_objective_rejected(self):
        with self.assertRaises(ValueError):
            self.session.create_tradeoffs(method="discretization", objectives=["not_an_objective"])


if __name__ == "__main__":
    unittest.main()
