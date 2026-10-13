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
        self.assertIn("Pattern activation among training discovery rows matching this box", result["text"])

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


if __name__ == "__main__":
    unittest.main()
