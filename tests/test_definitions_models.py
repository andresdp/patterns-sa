from adept.core.models import (
    ArchitecturalPattern,
    ConfigurationSpace,
    QualityObjective,
    ArchitectureSpace,
)


def test_architectural_pattern_from_dict_and_dump():
    data = {"name": "Toy", "description": "desc", "parameters": {"a": 1}}
    p = ArchitecturalPattern.from_dict(data)
    assert isinstance(p, ArchitecturalPattern)
    assert p.name == "Toy"
    assert p.parameters["a"] == 1
    assert p.dict() == p.model_dump()


def test_architecture_space_nested_validation():
    data = {
        "pattern": {"name": "Toy"},
        "configuration_space": {"parameters": {"p": [1, 2]}},
        "quality_objectives": [{"name": "q", "metric": "m"}],
        "metadata": {"k": "v"},
    }
    a = ArchitectureSpace.from_dict(data)
    assert a.pattern.name == "Toy"
    assert a.configuration_space.parameters["p"] == [1, 2]
    assert len(a.quality_objectives) == 1


def test_quality_objective_threshold_coercion():
    q = QualityObjective.from_dict({"name": "q", "metric": "m", "threshold": "0.5"})
    assert isinstance(q.threshold, float)
    assert q.threshold == 0.5


def test_extra_fields_allowed_on_input():
    p = ArchitecturalPattern.from_dict({"name": "X", "extra_field": 123})
    assert getattr(p, "extra_field") == 123
