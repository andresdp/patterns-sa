from __future__ import annotations

from typing import List, Dict, Any, Optional, Union, Tuple
from enum import Enum
import pandas as pd
import numpy as np

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
    name: str = Field(default="", description="Unique name of the parameter.")
    level: ParameterLevel = Field(..., description="The scope where the parameter is defined (System, Pattern, Infrastructure).")
    type: ParameterType = Field(..., description="The role of the parameter (Lever, Uncertainty, Outcome, Constraint).")
    data_type: str = Field(default="float", description="Python data type (float, int, str).")
    description: str = Field(default="", description="Human-readable description of the parameter's meaning.")
    value: Any = Field(default=None, description="Current value assigned to the parameter.")
    bounds: Optional[Tuple[float, float]] = Field(default=None, description="Numeric range (min, max) for exploration.")

    model_config = {"extra": "allow", "validate_assignment": True}


class ParameterBindings(BaseModel):
    """Binds architectural decisions to specific parameter values.
    
    Groups values by parameter type (levers, uncertainties, constraints).
    """
    levers: Dict[str, Any] = Field(default_factory=dict, description="Assignments for design decisions.")
    uncertainties: Dict[str, Any] = Field(default_factory=dict, description="Assignments for external factors.")
    constraints: Dict[str, Any] = Field(default_factory=dict, description="Assignments for fixed parameters.")

    model_config = {"extra": "allow", "validate_assignment": True}


class PatternPolicy(BaseModel):
    """A concrete implementation choice for a design decision within a pattern."""
    description: str = Field(default="", description="Summary of what this policy does.")
    parameter_bindings: ParameterBindings = Field(default_factory=ParameterBindings, description="The specific values this choice sets.")

    model_config = {"extra": "allow", "validate_assignment": True}


class Decision(BaseModel):
    """A variation point within an architectural pattern."""
    description: str = Field(default="", description="Description of the architectural variation point.")
    policies: Dict[str, PatternPolicy] = Field(default_factory=dict, description="Mapping of policy IDs to their concrete definitions.")

    model_config = {"extra": "allow", "validate_assignment": True}


class ArchitecturalPattern(BaseModel):
    """Template for a reusable design solution.
    
    Instances of this class represent concrete applications of patterns like 
    'CQRS' or 'Gateway Offloading' within a system.
    """
    name: str = Field(..., description="The pattern identifier (e.g., 'Gateway_Offloading').")
    description: str = Field(default="", description="Overall description of the pattern's role.")
    parameters: Dict[str, Parameter] = Field(default_factory=dict, description="Parameters specific to this pattern.")
    decisions: Dict[str, Decision] = Field(default_factory=dict, description="Design decisions associated with this pattern.")

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
    parameters: Dict[str, List[Any]] = Field(default_factory=dict, description="Allowed values for each parameter.")

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
    name: str = Field(..., description="The outcome identifier (e.g., 'response_time').")
    description: str = Field(default="", description="Meaning of the metric.")
    metric: str = Field(default="", description="Unit of measurement (e.g., 'ms', '%').")
    maximize: bool = Field(default=True, description="Whether higher values are better.")
    threshold: Optional[float] = Field(default=None, description="Optional target value for baseline compliance.")

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
    process_id: str = Field(..., description="Unique ID for the process type.")
    instance_id: str = Field(..., description="Unique ID for the specific trace.")
    process_type: str = Field(..., description="Type: Iterative, Stateful, or Adaptive.")
    cycle_definition: Dict[str, Any] = Field(default_factory=dict, description="Config for individual iterations.")
    initial_state: Dict[str, Any] = Field(default_factory=dict, description="Values at cycle 0.")
    termination_logic: str = Field(default="", description="Condition to stop the process.")

    model_config = {"extra": "allow", "validate_assignment": True}


class BehavioralTrace(BaseModel):
    """A time-series of outcomes produced by an AdaptiveProcess.
    
    Stored as a DataFrame where each row typically represents a process cycle.
    """
    trace_id: str
    scenario_id: str
    outcomes: pd.DataFrame
    
    model_config = {
        "arbitrary_types_allowed": True,
        "validate_assignment": True
    }


class QualityBin(BaseModel):
    """Represents a categorical region in outcome space.
    
    E.g., label='fast', range=(0.0, 0.5).
    """
    label: str = Field(..., description="The category name (e.g., 'low').")
    min_value: float = Field(..., description="Lower bound of the bin.")
    max_value: float = Field(..., description="Upper bound of the bin.")


class DiscretizationScheme(BaseModel):
    """The mapping from continuous metric values to categorical bins for an objective."""
    objective_name: str = Field(..., description="Target outcome name.")
    bins: List[QualityBin] = Field(default_factory=list, description="Categorical segments.")
    method: str = Field(default="equal_width", description="Method used to calculate boundaries.")


class Box(BaseModel):
    """Represents a discovered region in parameter space."""
    name: str = Field(default="", description="Human-readable name for the box.")
    limits: Dict[str, Dict[str, float]] = Field(..., description="Parameter bounds {param: {min, max}}.")
    dataset_bounds: Dict[str, Dict[str, float]] = Field(default_factory=dict, description="Original data ranges.")
    metrics: Dict[str, float] = Field(default_factory=dict, description="Discovery performance (density, coverage).")
    target_tradeoff: Optional[str] = Field(default=None, description="ID of the targeted tradeoff.")
    target_tradeoff_labels: Optional[str] = Field(default=None, description="Labels associated with the tradeoff.")
    method: str = Field(default="prim", description="Algorithm used (prim, cart).")
    population_prevalence: float = Field(default=0.0, description="Baseline prevalence of target in dataset.")
    
    model_config = {"extra": "allow", "validate_assignment": True}

    @property
    def actual_limits(self) -> Dict[str, Dict[str, float]]:
        # If any limit is 'inf', substitute it for the dataset bounds
        if not self.dataset_bounds:
            return self.limits
        
        actual_limits = self.limits.copy()
        for param, limits in self.limits.items():
            if param in self.dataset_bounds:
                for key, value in limits.items():
                    if value == np.inf:
                        actual_limits[param]['max'] = self.dataset_bounds[param]['max']
                    elif value == -np.inf:
                        actual_limits[param]['min'] = self.dataset_bounds[param]['min']
        return actual_limits
    
    # @property
    def is_empty(self) -> bool:
        if self.metrics.get('targets_in_box', 0) < 1:
            return True
        if len(self.limits.keys()) == 0:
            return True
        return False


class Tradeoff(BaseModel):
    """Represents a specific combination of quality attribute treatments.
    
    A tradeoff is a first-class element that defines a region of interest 
    in the multi-dimensional outcome space. It serves as a bridge between 
    raw performance data and architectural requirements.
    """
    name: str = Field(..., description="Internal unique ID for the tradeoff.")
    label: str = Field(default="", description="Human-readable display label.")
    description: str = Field(default="", description="Summary of what this performance region represents.")
    # Mapping of objective names to their respective treatment values
    elements: Dict[str, Any] = Field(default_factory=dict, description="Mapping of {objective: bin_label}.")
    scheme: str = Field(default="discretization", description="Logical scheme used (discretization, pareto, threshold).")
    params: Dict[str, Any] = Field(default_factory=dict, description="Arguments for the specific scheme (e.g., epsilon).")
    
    # Membership info (populated during analysis)
    has_points: bool = Field(default=False, description="Whether any data points fall into this region.")
    point_count: int = Field(default=0, description="Total number of data points found in this region.")

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
    name: str = Field(..., description="Name of the software system.")
    description: str = Field(default="", description="Overview of the architecture.")
    parameters: Dict[str, Parameter] = Field(default_factory=dict, description="System-level parameters.")
    components: Dict[str, ArchitecturalPattern] = Field(default_factory=dict, description="Pattern instances within the system.")
    adaptive_processes: List[AdaptiveProcess] = Field(default_factory=list, description="Temporal models.")
    tradeoffs: List[Tradeoff] = Field(default_factory=list, description="Performance regions of interest.")

    @model_validator(mode="after")
    def _sync_parameter_names(self) -> System:
        for name, param in self.parameters.items():
            if not param.name:
                param.name = name
        return self


class PatternPolicyReference(BaseModel):
    """Points to a specific policy within an architectural pattern."""
    component: str = Field(..., description="ID of the pattern instance.")
    decision: str = Field(..., description="ID of the variation point.")
    policy: str = Field(..., description="ID of the chosen policy.")

    model_config = {"extra": "allow", "validate_assignment": True}


class SystemConfiguration(BaseModel):
    """A high-level configuration or 'strategy' for the entire system.
    
    Maps specific pattern-level choices into a named system configuration.
    Was previously named 'Policy'.
    """
    name: str = Field(..., description="Unique ID for this system configuration.")
    description: str = Field(default="", description="Description of the configuration's design intent.")
    pattern_policy_references: List[PatternPolicyReference] = Field(default_factory=list, description="Detailed pattern-level choices.")
    source_file: Optional[str] = Field(default=None, description="Optional path to simulation results for this config.")
    # Backward compatibility for 'component_policies' map {component_name: policy_name}
    component_policies: Dict[str, str] = Field(default_factory=dict)

    model_config = {"extra": "allow", "validate_assignment": True}
    
    @model_validator(mode="before")
    def _convert_component_policies(cls, values):
        return values


class ConfigurationIdentification(BaseModel):
    """Describes how to identify system configurations from simulation data.
    
    Supports distinguishing configurations either by a specific column in a single CSV
    or by separating them into multiple files.
    Was previously named 'PolicyIdentification'.
    """
    from_: str = Field(alias="from", description="Source: 'column' or 'file'.")
    column: Optional[str] = Field(default=None, description="Name of CSV column containing configuration IDs.")
    configurations: Union[Dict[str, SystemConfiguration], List[SystemConfiguration]] = Field(..., description="Available config mappings.")

    model_config = {
        "extra": "allow", 
        "validate_assignment": True,
        "populate_by_name": True
    }
    
    @model_validator(mode="before")
    def _rename_policies_to_configurations(cls, values):
        if "policies" in values:
            values["configurations"] = values.pop("policies")
        return values


class DataSpace(BaseModel):
    """Configuration for data loading and interpretation.
    
    Links the abstract System model to concrete CSV files or Behavioral Traces.
    """
    configuration_identification: ConfigurationIdentification = Field(..., description="Logic for policy mapping.")
    quality_objectives: List[QualityObjective] = Field(default_factory=list, description="Target metrics.")
    source_file: Optional[str] = Field(default=None, description="Primary CSV data file.")
    traces_path: Optional[str] = Field(default=None, description="Path to behavioral trace datasets.")
    column_renames: Dict[str, str] = Field(default_factory=dict, description="Mapping of CSV names to internal IDs.")
    discovery_options: Dict[str, Any] = Field(default_factory=dict, description="Global defaults for scenario discovery.")

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
    mode: str = Field(default="static", description="'static' or 'adaptive'.")
    system: System = Field(..., description="The architectural structure.")
    dataspace: DataSpace = Field(..., description="The data mapping config.")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Optional analysis properties.")

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
