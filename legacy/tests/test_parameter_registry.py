
import unittest
from adept.core.models import Parameter, ParameterType, ParameterLevel
from adept.core.parameter_registry import ParameterRegistry

class TestParameterRegistry(unittest.TestCase):
    def setUp(self):
        self.registry = ParameterRegistry()

    def test_parameter_creation(self):
        p = Parameter(
            name="n_replicas",
            level=ParameterLevel.SYSTEM,
            type=ParameterType.LEVER,
            description="Total number of replicas",
            value=3
        )
        self.assertEqual(p.name, "n_replicas")
        self.assertEqual(p.level, ParameterLevel.SYSTEM)
        self.assertEqual(p.type, ParameterType.LEVER)

    def test_registry_registration(self):
        p = Parameter(
            name="offload_amount",
            level=ParameterLevel.PATTERN,
            type=ParameterType.LEVER,
            value=0.5
        )
        self.registry.register(p)
        self.assertEqual(self.registry.get("offload_amount"), p)

    def test_get_by_type(self):
        p1 = Parameter(name="p1", level=ParameterLevel.SYSTEM, type=ParameterType.LEVER)
        p2 = Parameter(name="p2", level=ParameterLevel.SYSTEM, type=ParameterType.UNCERTAINTY)
        self.registry.register(p1)
        self.registry.register(p2)
        
        levers = self.registry.get_by_type(ParameterType.LEVER)
        self.assertIn(p1, levers)
        self.assertNotIn(p2, levers)

    def test_get_by_level(self):
        p1 = Parameter(name="p1", level=ParameterLevel.SYSTEM, type=ParameterType.LEVER)
        p2 = Parameter(name="p2", level=ParameterLevel.PATTERN, type=ParameterType.LEVER)
        self.registry.register(p1)
        self.registry.register(p2)
        
        system_params = self.registry.get_by_level(ParameterLevel.SYSTEM)
        self.assertIn(p1, system_params)
        self.assertNotIn(p2, system_params)

if __name__ == '__main__':
    unittest.main()
