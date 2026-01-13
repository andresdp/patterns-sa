from __future__ import annotations

from typing import List, Dict, Any, Optional, Union

from pydantic import BaseModel, Field, field_validator


class ArchitecturalPattern(BaseModel):
    name: str
    description: str = ""
    parameters: Dict[str, Any] = Field(default_factory=dict)
    decisions: Dict[str, Any] = Field(default_factory=dict) # Added for new schema

    model_config = {"extra": "allow", "validate_assignment": True}

    @field_validator("parameters", mode="before")
    def _coerce_parameters(cls, v):
        if v is None:
            return {}
        return dict(v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls.model_validate(data)

    def dict(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)


class ConfigurationSpace(BaseModel):
    # mapping parameter name -> list of possible values
    parameters: Dict[str, List[Any]] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}

    @field_validator("parameters", mode="before")
    def _coerce_parameters(cls, v):
        if v is None:
            return {}
        return dict(v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls.model_validate(data)

    def dict(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)


class QualityObjective(BaseModel):
    name: str
    description: str = "" # Added
    metric: str = "" # Optional/Default
    maximize: bool = True
    threshold: Optional[float] = None

    model_config = {"extra": "allow", "validate_assignment": True}

    @field_validator("threshold", mode="before")
    def _coerce_threshold(cls, v):
        if v is None:
            return None
        try:
            return float(v)
        except Exception:
            return v

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls.model_validate(data)

    def dict(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)


class ArchitectureSpace(BaseModel):
    pattern: ArchitecturalPattern
    configuration_space: ConfigurationSpace
    quality_objectives: List[QualityObjective] = Field(default_factory=list)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}

    @field_validator("quality_objectives", mode="before")
    def _coerce_quality_objectives(cls, v):
        if v is None:
            return []
        return list(v)

    @field_validator("metadata", mode="before")
    def _coerce_metadata(cls, v):
        if v is None:
            return {}
        return dict(v)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls.model_validate(data)

    def dict(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)

# --- New Schema Models ---

class System(BaseModel):
    name: str
    description: str = ""
    components: Dict[str, ArchitecturalPattern] = Field(default_factory=dict)

class Policy(BaseModel):
    name: str
    description: str = ""
    component_policies: Dict[str, str] = Field(default_factory=dict)
    source_file: Optional[str] = None

class PolicyIdentification(BaseModel):
    from_: str = Field(alias="from")
    column: Optional[str] = None
    policies: Union[Dict[str, Policy], List[Policy]]

class Dataspace(BaseModel):
    policy_identification: PolicyIdentification
    quality_objectives: List[QualityObjective] = Field(default_factory=list)
    source_file: Optional[str] = None
    column_renames: Dict[str, str] = Field(default_factory=dict)
    discovery_options: Dict[str, Any] = Field(default_factory=dict)

class SystemDefinition(BaseModel):
    mode: str = "static"
    system: System
    dataspace: Dataspace
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str):
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.model_validate(data)


__all__ = [
    "ArchitecturalPattern",
    "ConfigurationSpace",
    "QualityObjective",
    "ArchitectureSpace",
    "SystemDefinition",
    "System",
    "Dataspace",
    "PolicyIdentification",
    "Policy"
]
