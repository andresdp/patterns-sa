import json
from pathlib import Path
import unittest

from adept.analysis.explainer import ExplanationManager
from adept.core.models import Box, SystemDefinition


class TestBoxContextPatternActivation(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        spec_path = Path(__file__).parents[1] / "federatedlearning" / "compact" / "FLsystem_compact_all.json"
        with spec_path.open() as source:
            cls.sys_def = SystemDefinition.model_validate(json.load(source))
        cls.manager = ExplanationManager()

    def test_observed_single_pattern_slice_reports_all_three_activations(self):
        box = Box(
            limits={"Client Selector Criteria": {"min": 1, "max": 1}},
            categorical_levels={"Client Selector Criteria": ["CPU"]},
        )

        result = self.manager.explain_box_context(
            box,
            self.sys_def,
            observed_configuration_counts={"ON,OFF,OFF": 8},
            observed_scope="training discovery rows",
            observed_row_count=8,
        )

        self.assertIn("Client Selector = ON", result["text"])
        self.assertIn("Message Compressor: OFF (8/8)", result["text"])
        self.assertIn("HDH: OFF (8/8)", result["text"])
        self.assertIn("Observed pattern activation — training discovery rows", result["text"])

    def test_baseline_scope_explicitly_shows_all_patterns_off(self):
        box = Box(limits={"Alpha Dirichlet Mean": {"min": 0.6, "max": 0.8}})

        result = self.manager.explain_box_context(
            box,
            self.sys_def,
            observed_configuration_counts={"OFF,OFF,OFF": 4},
            observed_scope="training discovery rows",
            observed_row_count=4,
        )

        self.assertIn("Client Selector: OFF (4/4)", result["text"])
        self.assertIn("Message Compressor: OFF (4/4)", result["text"])
        self.assertIn("HDH: OFF (4/4)", result["text"])

    def test_without_observations_reports_specification_alternatives_not_actual_usage(self):
        box = Box(limits={"Alpha Dirichlet Mean": {"min": 0.6, "max": 0.8}})

        result = self.manager.explain_box_context(box, self.sys_def)

        self.assertIn("OFF, ON (not fixed by the box)", result["text"])
        self.assertIn("Pattern activation allowed by declared configurations", result["text"])

    def test_activation_observations_can_compare_training_and_held_out_partitions(self):
        box = Box(limits={"Alpha Dirichlet Mean": {"min": 0.6, "max": 0.8}})

        result = self.manager.explain_box_context(
            box,
            self.sys_def,
            observed_partitions={
                "training partition": {
                    "configuration_counts": {"ON,OFF,OFF": 5},
                    "row_count": 5,
                },
                "held-out partition": {
                    "configuration_counts": {"OFF,OFF,OFF": 3, "ON,OFF,OFF": 1},
                    "row_count": 4,
                },
            },
        )

        self.assertIn("Observed pattern activation — training partition", result["text"])
        self.assertIn("Observed pattern activation — held-out partition", result["text"])
        self.assertIn("Client Selector: ON (5/5)", result["text"])
        self.assertIn("Client Selector: OFF (3/4), ON (1/4)", result["text"])


if __name__ == "__main__":
    unittest.main()
