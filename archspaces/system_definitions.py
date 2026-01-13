# archspaces/system_definitions.py

from typing import Any, Dict, List, Literal, Optional, Union

from pydantic import BaseModel, Field


# #############################################################################
# Core Building Blocks for Patterns and Systems
# #############################################################################


class Parameter(BaseModel):
    """Defines a single input parameter for an architectural pattern."""

    type: str = Field(
        description="The data type of the parameter (e.g., 'integer', 'float')."
    )
    description: str = Field(
        default="", description="A human-readable description of the parameter."
    )
    min: Optional[float] = Field(
        default=None, description="The minimum allowed value for a numeric parameter."
    )
    max: Optional[float] = Field(
        default=None, description="The maximum allowed value for a numeric parameter."
    )


class Policy(BaseModel):
    """Defines a single, selectable policy for a design decision."""

    description: str = Field(description="A human-readable description of the policy.")


class Decision(BaseModel):
    """Defines a design decision within an architectural pattern."""

    description: str = Field(
        description="A human-readable description of the design decision."
    )
    policies: Dict[str, Policy] = Field(
        default_factory=dict,
        description="A dictionary of possible policies for this decision, where the key is the policy name.",
    )


class ArchitecturalPattern(BaseModel):
    """Defines the abstract structure of a single architectural pattern."""

    name: str = Field(description="The formal name of the architectural pattern.")
    description: str = Field(
        default="", description="A human-readable description of the pattern."
    )
    parameters: Dict[str, Parameter] = Field(
        default_factory=dict,
        description="A dictionary of input parameters for this pattern, where the key is the parameter name.",
    )
    decisions: Dict[str, Decision] = Field(
        default_factory=dict,
        description="A dictionary of design decisions available for this pattern.",
    )


class System(BaseModel):
    """Defines a system composed of one or more architectural patterns."""

    name: str = Field(description="The name of the overall system being defined.")
    description: str = Field(
        default="", description="A human-readable description of the system."
    )
    components: Dict[str, ArchitecturalPattern] = Field(
        default_factory=dict,
        description="A dictionary of components that make up the system, where the key is the component's logical name.",
    )


# #############################################################################
# Models for Dataspace, Policy Identification, and Discovery
# #############################################################################


class QualityObjective(BaseModel):
    """Defines a single quality objective to be measured from the data."""

    name: str = Field(
        description="The name of the quality objective, corresponding to a column in the final dataframe."
    )
    metric: str = Field(
        description="The unit of measurement for this objective (e.g., 'ms', 'percentage')."
    )
    description: str = Field(
        default="", description="A human-readable description of the quality objective."
    )
    maximize: bool = Field(
        description="Whether this objective should be maximized (true) or minimized (false)."
    )


class SystemPolicy(BaseModel):
    """Defines a single, system-level policy."""

    name: str = Field(description="The formal name for this system-level policy.")
    description: str = Field(
        default="", description="A human-readable description of the system policy."
    )
    component_policies: Dict[str, str] = Field(
        description="A map linking component names (from system.components) to the name of the policy chosen for it."
    )


class FileBasedPolicy(SystemPolicy):
    """A system policy whose data is contained in a single, dedicated file."""

    source_file: str = Field(
        description="The path to the data file that implements this policy."
    )
    column_renames: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Optional column renames specific to this data file.",
    )


class PolicyIdentificationFromFile(BaseModel):
    """Defines policy identification when each policy is in its own file."""

    from_type: Literal["file"] = Field(
        "file",
        description="Specifies that policies are identified by their source file.",
    )
    policies: List[FileBasedPolicy] = Field(
        description="A list of policy definitions, each linked to a file."
    )


class PolicyIdentificationFromColumn(BaseModel):
    """Defines policy identification when policies are distinguished by a column value."""

    from_type: Literal["column"] = Field(
        "column",
        description="Specifies that policies are identified by a column's value.",
    )
    column: str = Field(
        description="The name of the column in the source file that distinguishes policies."
    )
    policies: Dict[str, SystemPolicy] = Field(
        description="A dictionary where the key is the raw value from the 'column' and the value is the system policy definition."
    )


class QANamingConvention(BaseModel):
    """Rule for discovering quality objective columns in discovery mode."""

    type: Literal["suffix"] = Field(
        description="The type of naming convention used (e.g., searching for a suffix)."
    )
    separator: str = Field(
        default="#", description="The separator used before the suffix."
    )


class ParameterIdentification(BaseModel):
    """Rule for discovering parameter columns in discovery mode."""

    type: Literal["all_except"] = Field(
        description="The rule for identifying parameter columns (e.g., all columns except a few)."
    )
    exclude_columns: List[str] = Field(
        default_factory=list,
        description="A list of columns to exclude from being treated as parameters.",
    )


class DiscoveryOptions(BaseModel):
    """Container for all discovery-mode configurations."""

    qa_naming_convention: QANamingConvention = Field(
        description="Rules for discovering Quality Objective columns."
    )
    parameter_identification: ParameterIdentification = Field(
        description="Rules for discovering Parameter columns."
    )


class DataSpace(BaseModel):
    """Defines how to find, load, and interpret the data for the system."""

    policy_identification: Union[
        PolicyIdentificationFromFile, PolicyIdentificationFromColumn
    ] = Field(description="Defines how system policies are identified in the data.")
    quality_objectives: Optional[List[QualityObjective]] = Field(
        default=None,
        description="A list of quality objectives being measured. Not used in 'discovery' mode.",
    )
    source_file: Optional[str] = Field(
        default=None,
        description="The single source file to use when policy identification is 'from: column'.",
    )
    column_renames: Optional[Dict[str, str]] = Field(
        default_factory=dict,
        description="Global column renames applied to all sources if not overridden locally.",
    )
    discovery_options: Optional[DiscoveryOptions] = Field(
        default=None, description="Configuration for 'discovery' mode."
    )


# #############################################################################
# Top-Level Root Model
# #############################################################################


class SystemDefinition(BaseModel):
    """The root model for a complete system definition JSON file."""

    mode: Literal["static", "discovery"] = Field(
        default="static",
        description="The operational mode for the data loader ('static' for explicit definitions, 'discovery' for dynamic).",
    )
    system: System = Field(
        description="The definition of the system and its components."
    )
    dataspace: DataSpace = Field(
        description="The definition of the data sources and how to interpret them."
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="A dictionary for storing supplementary metadata (e.g., version, author).",
    )
