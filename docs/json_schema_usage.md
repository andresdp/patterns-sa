
# JSON System Definition Schema

This document describes the structure and conventions for the JSON files used to define systems, their constituent architectural patterns, and their associated data for analysis.

## 1. Purpose

These JSON files provide a declarative and language-agnostic way to define a software system. This includes the architectural patterns that compose the system, their parameters and design decisions, and how to load the data associated with them. This approach separates the definition of a system from the Python code used to analyze it, making the framework extensible and maintainable.

A generic `DataLoader` in the analysis framework will parse these files to understand and load the system's data correctly.

## 2. Top-Level Structure

Each JSON definition file has the following top-level keys:

| Key         | Type   | Description                                                                                                   |
|-------------|--------|---------------------------------------------------------------------------------------------------------------|
| `mode`      | String | Optional. Can be `"static"` (default) or `"discovery"`. See Section 5 for details.                            |
| `system`    | Object | Defines the system itself, including its name and components. See Section 3.1.                                |
| `dataspace` | Object | Defines how to find, load, and interpret the data for the system. See Section 3.2.                              |
| `metadata`  | Object | Contains supplementary information like version, author, etc.                                                   |

---

## 3. Detailed Section Breakdown

### 3.1 The `system` Object

This object describes the system being analyzed. It is composed of one or more named **components**, where each component is an instance of an **architectural pattern**.

```json
"system": {
  "name": "E-commerce System",
  "description": "A composite system for processing orders.",
  "components": {
    "order_service": {
      "name": "CQRS",
      "description": "Handles order processing.",
      "parameters": {
        "N_read": { "type": "integer", "description": "Number of read users." }
      },
      "decisions": {
        "separation_strategy": {
          "description": "DB separation strategy.",
          "policies": {
            "sw": { "description": "Software separation." },
            "hw": { "description": "Hardware separation." }
          }
        }
      }
    },
    "api_gateway": {
       // ... definition for another component ...
    }
  }
}
```

*   **`name` / `description`**: The name and description of the overall system.
*   **`components`**: An object where each key is a unique, logical name for a component (e.g., `order_service`). The value is an `ArchitecturalPattern` object.
*   **`ArchitecturalPattern` Object**:
    *   `name`: The formal name of the pattern (e.g., "CQRS").
    *   `parameters`: An object defining the input parameters for this pattern component.
    *   `decisions`: An object defining the design decisions for this pattern. Each decision has a dictionary of possible `policies` that can be chosen for it.

### 3.2 The `dataspace` Object

This object links the abstract system definition to concrete data.

```json
"dataspace": {
  "policy_identification": { ... },
  "quality_objectives": [ ... ],
  "source_file": "path/to/data.csv", // Optional
  "column_renames": { ... } // Optional
}
```

*   **`quality_objectives`**: A list defining the quality metrics being measured.
*   **`policy_identification`**: A critical object that defines the system-level policies and maps them to the policies of the individual components. It has two main modes, specified by the `from` key.

#### 3.2.1 Policy Identification: `from: "column"`

Used when a single data file contains multiple system policies, distinguished by a column's value.

```json
"policy_identification": {
  "from": "column",
  "column": "system_configuration",
  "policies": {
    "base_config": {
      "name": "Base Configuration",
      "description": "SW-CQRS with no offloading.",
      "component_policies": {
        "order_service": "sw",
        "api_gateway": "no-offloading"
      }
    },
    "perf_config": { ... }
  }
}
```

*   **`column`**: The column in the `source_file` that identifies the system policy.
*   **`policies`**: An object where keys are the **raw values** from the `column`. The value defines the system policy, including its `name`, `description`, and the crucial `component_policies` map.
*   **`component_policies`**: This map links a component name (from `system.components`) to the name of the component-level policy chosen for it.

#### 3.2.2 Policy Identification: `from: "file"`

Used when each system policy's data is in a separate file.

```json
"policy_identification": {
  "from": "file",
  "policies": [
    {
      "name": "sw-system",
      "description": "System with software-separated CQRS.",
      "source_file": "sw_data.csv",
      "component_policies": { "cqrs_service": "sw" }
    },
    {
      "name": "hw-system",
      "description": "System with hardware-separated CQRS.",
      "source_file": "hw_data.csv",
      "component_policies": { "cqrs_service": "hw" }
    }
  ]
}
```

*   **`policies`**: A **list** of objects. Each object defines a system policy, its `source_file`, and the `component_policies` map.

---

## 4. Discovery Mode

For high-dimensional datasets where explicitly listing parameters is not feasible, the schema supports a `"discovery"` mode.

```json
{
  "mode": "discovery",
  "system": { ... },
  "dataspace": {
    "discovery_options": { ... },
    "policy_identification": { ... }
  }
}
```

*   **`mode`**: When set to `"discovery"`, the loader will ignore `parameters` and `quality_objectives` defined in the file.
*   **`discovery_options`**: This new object guides the loader on how to find parameters and QAs dynamically from the data file, for instance by using naming conventions or exclusion rules.

This flexible, system-centric schema allows the framework to handle both simple, single-pattern analyses and complex, multi-pattern systems, as well as both statically-defined and discovery-driven datasets.

---

## 5. Compatibility with External Tools (e.g., PandasAI)

A key advantage of this declarative JSON schema is that it makes the data self-describing. This semantic information is highly compatible with external analysis tools like PandasAI that leverage Large Language Models (LLMs) to enable natural language querying of data.

### 5.1 Mapping to a Semantic Layer

The metadata required to create a "semantic layer" in PandasAI maps directly to the information captured in our JSON definition files.

| PandasAI Semantic Layer | Our JSON Structure (`system.json`) | Compatibility |
| :--- | :--- | :--- |
| **Dataset Name** (`name`) | `system.name` | **High** |
| **Dataset Description** (`description`) | `system.description` | **High** |
| **Column Name** (`columns[].name`) | The keys from `parameters` and the `name` from `quality_objectives`. | **High** |
| **Column Type** (`columns[].type`) | `parameters.<param_name>.type` (e.g., "integer", "float"). | **High** |
| **Column Description** (`columns[].description`) | `parameters.<param_name>.description` and `quality_objectives.<qa_name>.description`. | **High** |

As the table demonstrates, the core metadata is fully aligned. The rich `description` fields for parameters and quality objectives provide the essential context that LLMs need to understand user questions accurately.

### 5.2 Conceptual Conversion Guide

A Python function can be written to parse a system definition JSON file and programmatically generate the input required for PandasAI's `pai.create()` function.

The following conceptual code shows how this conversion would work:

```python
import json
# Assume 'SystemDefinition' is the Pydantic model for our JSON file
# Assume 'pai' is the imported pandas-ai library

def convert_to_pandasai_semantic_layer(system_def: SystemDefinition, dataframe):
    """
    Converts a SystemDefinition object into the metadata format required
    by PandasAI's semantic layer.
    """
    
    # 1. Extract dataset-level metadata
    dataset_name = system_def.system.name
    dataset_description = system_def.system.description
    
    # 2. Extract column-level metadata
    columns_metadata = []
    
    # Process parameters from all components
    # Note: Assumes a convention where dataframe columns are prefixed, e.g., 'order_service_N_read'
    for component_name, component in system_def.system.components.items():
        for param_name, param_details in component.parameters.items():
            full_column_name = f"{component_name}_{param_name}"
            if full_column_name in dataframe.columns:
                columns_metadata.append({
                    "name": full_column_name,
                    "type": param_details.type,
                    "description": param_details.description
                })

    # Process quality objectives
    for qa in system_def.dataspace.quality_objectives:
        if qa.name in dataframe.columns:
            columns_metadata.append({
                "name": qa.name,
                "type": "float", # Or infer from data; QAs are often numeric
                "description": qa.description
            })
    
    # 3. Create the PandasAI dataset object
    # The actual call to the library would look something like this:
    #
    # pandas_ai_dataset = pai.create(
    #     path=f"organization/{dataset_name.replace(' ', '_').lower()}",
    #     name=dataset_name,
    #     description=dataset_description,
    #     df=dataframe,
    #     columns=columns_metadata
    # )
    #
    # return pandas_ai_dataset

    # For demonstration, we just return the dictionary
    return {
        "name": dataset_name,
        "description": dataset_description,
        "df": dataframe,
        "columns": columns_metadata
    }

# --- Example Usage ---
#
# with open("patterns/CQRS/CQRS.json") as f:
#     data = json.load(f)
#     system_definition = SystemDefinition.model_validate(data)
# 
# # Assume 'my_dataframe' is the loaded and prepared pandas DataFrame
# semantic_layer_metadata = convert_to_pandasai_semantic_layer(system_definition, my_dataframe)
# print(semantic_layer_metadata)
```

This demonstrates that our JSON structure is not just a definition format but a practical, machine-readable specification that can be used to bootstrap other powerful analysis tools with minimal effort.