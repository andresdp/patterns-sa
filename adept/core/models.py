from __future__ import annotations

from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum
import pandas as pd

from pydantic import BaseModel, Field, field_validator, model_validator


class ParameterType(str, Enum):
    """Categorization of parameters following EMA (Exploratory Modeling and Analysis) principles.
    
    Levers: Controllable design decisions.
    Uncertainties: External factors beyond direct control.
    Outcomes: Performance or quality metrics being measured.
    Constraints: Fixed bounds or requirements.
    """
    LEVER = "lever"
    UNCERTAINTY = "uncertainty"
    OUTCOME = "outcome"
    CONSTRAINT = "constraint"


class ParameterLevel(str, Enum):
    """The scope or layer where a parameter is defined.
    
    System: Global parameters affecting the entire architecture.
    Pattern: Parameters specific to an architectural pattern instance.
    Infrastructure: Physical or resource-level constraints (e.g., VM size).
    """
    SYSTEM = "system"
    PATTERN = "pattern"
    INFRASTRUCTURE = "infrastructure"


class Parameter(BaseModel):
    """Represents a single architectural variable or outcome.
    
    This model encapsulates the metadata and current state of a parameter,
    including its role (type) and scope (level).
    """
    name: str = "" # Default empty, will be populated by parent
    level: ParameterLevel
    type: ParameterType
    data_type: str = "float" # e.g., float, integer, string
    description: str = ""
    value: Any = None
    bounds: Optional[Tuple[float, float]] = None

    model_config = {"extra": "allow", "validate_assignment": True}


class ParameterBindings(BaseModel):
    """Binds architectural decisions to specific parameter values.
    
    Groups values by parameter type (levers, uncertainties, constraints).
    """
    levers: Dict[str, Any] = Field(default_factory=dict)
    uncertainties: Dict[str, Any] = Field(default_factory=dict)
    constraints: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}


class PatternPolicy(BaseModel):
    """A concrete implementation choice for a design decision within a pattern."""
    description: str = ""
    parameter_bindings: ParameterBindings = Field(default_factory=ParameterBindings)

    model_config = {"extra": "allow", "validate_assignment": True}


class Decision(BaseModel):
    """A variation point within an architectural pattern."""
    description: str = ""
    policies: Dict[str, PatternPolicy] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}


class ArchitecturalPattern(BaseModel):
    """Template for a reusable design solution.
    
    Instances of this class represent concrete applications of patterns like 
    'CQRS' or 'Gateway Offloading' within a system.
    """
    name: str
    description: str = ""
    parameters: Dict[str, Parameter] = Field(default_factory=dict)
    decisions: Dict[str, Decision] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}

    @model_validator(mode="after")
    def _sync_parameter_names(self) -> ArchitecturalPattern:
        for name, param in self.parameters.items():
            if not param.name:
                param.name = name
        return self

    @classmethod
    def from_dict(cls, data: Dict[str, Any]):
        return cls.model_validate(data)

    def dict(self, *args, **kwargs):
        return self.model_dump(*args, **kwargs)


class ConfigurationSpace(BaseModel):
    """Defines the set of all possible parameter assignments for a pattern or system.
    
    Used primarily during experimental design to bound the exploration space.
    """
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
    """A target performance or quality metric (Outcome).
    
    Defines what constitutes 'success' for an architecture, including thresholds
    and optimization direction.
    """
    name: str
    description: str = ""
    metric: str = ""
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
    """A legacy container for a single pattern's analysis scope.
    
    Replaced by SystemDefinition in newer ADEPT workflows.
    """
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


class AdaptiveProcess(BaseModel):
    """Models temporal, iterative behavior within a pattern (e.g., FL training).
    
    Captures how system state evolves over cycles, enabling analysis of 
    adaptive systems.
    """
    process_id: str
    instance_id: str
    process_type: str  # Iterative, Stateful, Adaptive
    cycle_definition: Dict[str, Any] = Field(default_factory=dict)
    initial_state: Dict[str, Any] = Field(default_factory=dict)
    termination_logic: str = ""

    model_config = {"extra": "allow", "validate_assignment": True}


class BehavioralTrace(BaseModel):
    """A time-series of outcomes produced by an AdaptiveProcess.
    
    Stored as a DataFrame where each row typically represents a process cycle.
    """
    trace_id: str
    scenario_id: str
    outcomes: pd.DataFrame
    
    model_config = {"arbitrary_types_allowed": True}


class QualityBin(BaseModel):
    """Represents a categorical region in outcome space.
    
    E.g., label='fast', range=(0.0, 0.5).
    """
    label: str
    min_value: float
    max_value: float


class DiscretizationScheme(BaseModel):
    """The mapping from continuous metric values to categorical bins for an objective."""
    objective_name: str
    bins: List[QualityBin]
    method: str = "equal_width"


class Tradeoff(BaseModel):
    """Represents a specific combination of quality attribute treatments.
    
    A tradeoff is a first-class element that defines a region of interest 
    in the multi-dimensional outcome space. It serves as a bridge between 
    raw performance data and architectural requirements.
    """
    name: str
    label: str = "" # Human-readable display label
    description: str = ""
    # Mapping of objective names to their respective treatment values
    elements: Dict[str, Any] = Field(default_factory=dict)
    scheme: str = "discretization"
    params: Dict[str, Any] = Field(default_factory=dict)
    
    # Membership info (populated during analysis)
    has_points: bool = False
    point_count: int = 0

    model_config = {"extra": "allow", "validate_assignment": True}

    @model_validator(mode="after")
    def _ensure_label(self) -> Tradeoff:
        if not self.label:
            self.label = self.name
        return self


# --- ADEPT Schema Models ---

class System(BaseModel):
    """The root container for an architectural model.
    
    Composes pattern instances, adaptive processes, and tradeoff definitions 
    into a unified system.
    """
    name: str
    description: str = ""
    parameters: Dict[str, Parameter] = Field(default_factory=dict)
    components: Dict[str, ArchitecturalPattern] = Field(default_factory=dict)
    adaptive_processes: List[AdaptiveProcess] = Field(default_factory=list)
    tradeoffs: List[Tradeoff] = Field(default_factory=list)

    @model_validator(mode="after")
    def _sync_parameter_names(self) -> System:
        for name, param in self.parameters.items():
            if not param.name:
                param.name = name
        return self


class PatternPolicyReference(BaseModel):
    """Points to a specific policy within an architectural pattern."""
    component: str
    decision: str
    policy: str

    model_config = {"extra": "allow", "validate_assignment": True}


class SystemConfiguration(BaseModel):
    """A high-level configuration or 'strategy' for the entire system.
    
    Maps specific pattern-level choices into a named system configuration.
    Was previously named 'Policy'.
    """
    name: str
    description: str = ""
    pattern_policy_references: List[PatternPolicyReference] = Field(default_factory=list)
    source_file: Optional[str] = None
    # Backward compatibility for 'component_policies' map {component_name: policy_name}
    # This is handled during ingestion but storing it might be useful if we want to preserve old structure
    component_policies: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}
    
    @model_validator(mode="before")
    def _convert_component_policies(cls, values):
        # Allow old style 'component_policies' dict and convert to references where possible
        # However, 'component_policies' is usually {comp: policy}, missing 'decision'. 
        # Without schema knowledge we can't infer decision easily.
        # So we keep 'component_policies' as a field for backward compat usage in loader.
        return values


class ConfigurationIdentification(BaseModel):
    """Describes how to identify system configurations from simulation data.
    
    Supports distinguishing configurations either by a specific column in a single CSV
    or by separating them into multiple files.
    Was previously named 'PolicyIdentification'.
    """
    from_: str = Field(alias="from")
    column: Optional[str] = None
    configurations: Union[Dict[str, SystemConfiguration], List[SystemConfiguration]]

    model_config = {"extra": "allow", "validate_assignment": True}
    
    @model_validator(mode="before")
    def _rename_policies_to_configurations(cls, values):
        if "policies" in values:
            values["configurations"] = values.pop("policies")
        return values


class DataSpace(BaseModel):
    """Configuration for data loading and interpretation.
    
    Links the abstract System model to concrete CSV files or Behavioral Traces.
    """
    configuration_identification: ConfigurationIdentification
    quality_objectives: List[QualityObjective] = Field(default_factory=list)
    source_file: Optional[str] = None
    traces_path: Optional[str] = None
    column_renames: Dict[str, str] = Field(default_factory=dict)
    discovery_options: Dict[str, Any] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}
    
    @model_validator(mode="before")
    def _rename_policy_id_to_config_id(cls, values):
        if "policy_identification" in values:
            values["configuration_identification"] = values.pop("policy_identification")
        return values


class SystemDefinition(BaseModel):
    """The top-level ADEPT declarative specification.
    
    Typically loaded from a 'system.json' file to configure the entire 
    analysis pipeline.
    """
    mode: str = "static"
    system: System
    dataspace: DataSpace
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @classmethod
    def from_json(cls, path: str):
        """Loads a SystemDefinition from a JSON file."""
        import json
        with open(path, 'r') as f:
            data = json.load(f)
        return cls.model_validate(data)


# Backward compatibility aliases
Policy = SystemConfiguration
PolicyIdentification = ConfigurationIdentification


__all__ = [
    "ParameterType",
    "ParameterLevel",
    "Parameter",
    "ParameterBindings",
    "PatternPolicy",
    "Decision",
    "ArchitecturalPattern",
    "ConfigurationSpace",
    "QualityObjective",
    "ArchitectureSpace",
    "AdaptiveProcess",
    "BehavioralTrace",
    "QualityBin",
    "DiscretizationScheme",
    "Tradeoff",
    "SystemDefinition",
    "System",
    "DataSpace",
    "ConfigurationIdentification",
    "SystemConfiguration",
    "PatternPolicyReference",
    "Policy",
    "PolicyIdentification"
]
