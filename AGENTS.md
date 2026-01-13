# Agent Guidelines for patterns-sa

## Project Overview

**patterns-sa** is a toolkit for sensitivity analysis and explainability of architectural tradeoffs on design patterns. It consists of multiple modules, with ADEPT as the core framework.

## ADEPT Module Architecture

ADEPT (Architectural Design Exploration and Trade-off Planning Tool) follows a **Coordinator Pattern** with three main layers:

### Core Layer (`adept/core/`)

- **models.py**: Pydantic-based data models following EMA (Exploratory Modeling & Analysis) principles
  - `ParameterType` (LEVER, UNCERTAINTY, OUTCOME, CONSTRAINT)
  - `ParameterLevel` (SYSTEM, PATTERN, INFRASTRUCTURE)
  - `Parameter`, `ArchitecturalPattern`, `System`, `Dataspace`
  - `SystemDefinition`: Top-level declarative spec (typically from system.json)
  - `Tradeoff`: A multi-dimensional region in outcome space
  - `DiscretizationScheme`, `QualityBin`: Categorical bin definitions

- **coordinator.py**: `ArchSpaceCore` - Main orchestrator
  - Composes all components into a unified API
  - Delegates to specialized managers (not a thick class)
  - Provides entry points: `load_data()`, `discover_scenarios()`, `discretize()`, `compute_robustness()`, `explain()`

- **loader.py**: Data ingestion abstraction
  - `DataLoader` (ABC) - Abstract base
  - `PandasDataLoader` - Thin wrapper for simple CSV loading
  - `GenericDataLoader` - Metadata-driven loader (uses SystemDefinition)
  - Handles file discovery, policy identification, column renaming, data partitioning

- **parameter_registry.py**: Parameter management (currently minimal)

- **plugin_api.py**: Plugin infrastructure

- **plugins/**: Example implementations (toy.py)

### Analysis Layer (`adept/analysis/`)

- **discretization.py**: `DataProcessor`
  - Transforms continuous metrics to categorical bins
  - Static methods: `get_bins()`, `get_tradeoffs()`, `discretize()`

- **robustness.py**: `RobustnessAnalyzer`
  - Computes architectural robustness metrics

- **tradeoffs.py**: `TradeoffAnalyzer`
  - Finds similar tradeoffs using KNN (Euclidean distance on ordinal-encoded labels)
  - Method: `get_nearest_tradeoffs()`

- **discovery.py**: `ScenarioDiscoveryManager`
  - Identifies parameter regions driving specific outcomes

- **explainer.py**: `ExplanationManager`
  - Generates natural language explanations

- **metrics.py**: Supporting metrics utilities

### Utilities Layer (`adept/utils/`)

- **validation.py**: Schema validation
  - `SchemaValidator` (ABC)
  - `SimpleValidator` (basic implementation)

## Code Style & Patterns

### Model Design
- Use Pydantic `BaseModel` for all data structures
- Include `model_config = {"extra": "allow", "validate_assignment": True}` for flexibility
- Provide `.dict()` and `.from_dict()` methods for compatibility
- Add field validators with `@field_validator` (mode="before") for coercion

### Coordinator Pattern
- `ArchSpaceCore` should remain lightweight, delegating to specialized managers
- Use dependency injection in `__init__` for testability
- Each manager should have a single responsibility

### Data Processing
- Return tuples for multi-value results: `Tuple[DataFrame, List[Scheme]]`
- Use static methods in `DataProcessor` for stateless transformations
- Provide `**kwargs` for extensibility

### API Design
- High-level entry points on `ArchSpaceCore` (e.g., `discover_scenarios()`, `explain()`)
- Accept flexible source types (paths, DataFrames, etc.)
- Return intuitive types (DataFrames, dicts, lists)

## Module Interactions

```
ArchSpaceCore (Coordinator)
  ├─ Loads data via GenericDataLoader
  ├─ Validates via SchemaValidator
  ├─ Processes via DataProcessor (discretization)
  ├─ Analyzes via RobustnessAnalyzer, TradeoffAnalyzer
  ├─ Discovers via ScenarioDiscoveryManager
  └─ Explains via ExplanationManager
```

## Key Concepts

### SystemDefinition (system.json)
The declarative spec that ties everything together:
```json
{
  "mode": "static",
  "system": {
    "name": "...",
    "components": { "pattern_name": {...} },
    "tradeoffs": [...]
  },
  "dataspace": {
    "policy_identification": {...},
    "quality_objectives": [...]
  }
}
```

### Tradeoff
A named region in multi-dimensional outcome space. Defined by quality attribute treatments (e.g., {"latency": "fast", "throughput": "high"}).

### Discretization
Converting continuous metrics to categorical bins for intuitive solution exploration.

## Testing

Tests are in `tests/`. Follow existing patterns when adding new tests:
- Test models with various input types
- Mock external dependencies
- Validate error handling

## Other Modules

- **archspaces/**: Additional architectural space implementations
- **conductor/**: Orchestration logic
- **patterns/**: Pattern library
- **tools/**: Utility scripts
- **legacy/**: Deprecated code (reference only)

## Commands & Workflows

### Running Analysis
1. Create a `system.json` with your architectural model
2. Prepare CSV data aligned to the model
3. Use `ArchSpaceCore` to load, validate, and analyze

### Adding New Analysis
1. Create a new class in `adept/analysis/`
2. Follow the manager pattern (single responsibility)
3. Integrate via `ArchSpaceCore.__init__()` and expose via a high-level method
4. Update `adept/analysis/__init__.py` exports

### Adding New Models
1. Define Pydantic models in `adept/core/models.py`
2. Include field validators for robustness
3. Update `__all__` export list

