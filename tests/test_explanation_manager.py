
import unittest
from archspaces.explanations import ExplanationManager, TemplateExplainerStrategy

class TestExplanationManager(unittest.TestCase):
    def setUp(self):
        self.manager = ExplanationManager()
        self.metrics = {'robustness': 0.8}

    def test_get_strategy(self):
        self.assertIsInstance(self.manager.get_strategy('template'), TemplateExplainerStrategy)
        self.assertIsInstance(self.manager.get_strategy(None), TemplateExplainerStrategy)

    def test_explain_delegation(self):
        explanation = self.manager.explain(self.metrics, method='template')
        self.assertIn('Analysis summary', explanation['text'])
        self.assertIn('robustness: 0.8', explanation['text'])

if __name__ == '__main__':
    unittest.main()
