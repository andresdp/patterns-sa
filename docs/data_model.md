# ADEPT Data Model

This document describes the core entities and relationships within the ADEPT framework, as defined by the Pydantic models in `adept/core/models.py`.

## Entity Relationship Diagram

```mermaid
classDiagram
    class SystemDefinition {
        +String mode
        +System system
        +DataSpace dataspace
        +Dict metadata
    }

    class System {
        +String name
        +String description
        +Dict~str, Parameter~ parameters
        +Dict~str, ArchitecturalPattern~ components
        +List~AdaptiveProcess~ adaptive_processes
        +List~Tradeoff~ tradeoffs
    }

    class DataSpace {
        +ConfigurationIdentification configuration_identification
        +List~QualityObjective~ quality_objectives
        +String source_file
        +String traces_path
        +Dict column_renames
        +Dict discovery_options
    }

    class ArchitecturalPattern {
        +String name
        +String description
        +Dict~str, Parameter~ parameters
        +Dict~str, Decision~ decisions
    }

    class Parameter {
        +String name
        +ParameterLevel level
        +ParameterType type
        +String data_type
        +Any value
        +Tuple bounds
    }

    class Decision {
        +String description
        +Dict~str, PatternPolicy~ policies
    }

    class PatternPolicy {
        +String description
        +ParameterBindings parameter_bindings
    }

    class ParameterBindings {
        +Dict levers
        +Dict uncertainties
        +Dict constraints
    }

    class ConfigurationIdentification {
        +String from_
        +String column
        +Dict~str, SystemConfiguration~ configurations
    }

    class SystemConfiguration {
        +String name
        +String description
        +List~PatternPolicyReference~ pattern_policy_references
        +String source_file
    }

    class PatternPolicyReference {
        +String component
        +String decision
        +String policy
    }

    class QualityObjective {
        +String name
        +String metric
        +Boolean maximize
        +Float threshold
    }

    class Tradeoff {
        +String name
        +String label
        +Dict elements
        +String scheme
        +Dict params
        +Boolean has_points
        +Integer point_count
    }

    class DiscretizationScheme {
        +String objective_name
        +List~QualityBin~ bins
        +String method
    }

    class QualityBin {
        +String label
        +Float min_value
        +Float max_value
    }

    class Box {
        +String name
        +Dict limits
        +Dict metrics
        +String target_tradeoff
        +String method
    }

    %% Relationships
    SystemDefinition *-- System : contains
    SystemDefinition *-- DataSpace : contains
    
    System *-- ArchitecturalPattern : composes
    System *-- Tradeoff : defines
    
    ArchitecturalPattern *-- Parameter : has
    ArchitecturalPattern *-- Decision : variation point
    
    Decision *-- PatternPolicy : options
    PatternPolicy *-- ParameterBindings : sets
    
    DataSpace *-- ConfigurationIdentification : maps
    DataSpace *-- QualityObjective : targets
    
    ConfigurationIdentification *-- SystemConfiguration : identifies
    SystemConfiguration *-- PatternPolicyReference : resolves
    
    DiscretizationScheme *-- QualityBin : segments
```

## Key Entities

### SystemDefinition
The root declarative specification for an ADEPT analysis. It links the architectural structure (`System`) to the experimental data configuration (`DataSpace`).

### System
The architectural model of the software under study. It acts as a container for pattern instances, global parameters, and the desired performance tradeoffs.

### ArchitecturalPattern
A reusable design template (e.g., CQRS, Gateway Offloading) containing specific parameters and architectural decisions.

### Tradeoff
A first-class element defining a region of interest in the multi-dimensional outcome space (e.g., "Fast and Cheap").

### Box
A discovered region in the parameter space (usually via PRIM or CART) that reliably leads to a specific tradeoff.
