# Refactoring Proposal for the `ArchSpace` Class

This document outlines a proposal to refactor the `ArchSpace` class and related components. The current implementation is a large "God Class" that mixes data loading, analysis, and configuration, making it difficult to maintain and extend.

The goal of this refactoring is to create a modular, decoupled, and extensible architecture that aligns with modern software design principles.

## Analysis Summary

1.  **`ArchSpace` as a "God Class"**: The base class contains numerous distinct responsibilities, including data loading, preprocessing, multiple types of analysis (Robustness, PRIM, CART), and trade-off calculations.
2.  **Subclass Role**: The subclasses (`GatewayOffloading`, `CQRS`, etc.) primarily act as **data loaders and configurators**. They implement `load_results` to handle specific CSV formats but inherit a vast number of analysis methods they don't use, creating tight coupling.
3.  **Unused Pydantic Models**: The `archspaces/definitions.py` file contains Pydantic models that provide a formal, declarative structure for defining architectural patterns. These are currently unused, and their logic is instead hardcoded within the subclasses.
4.  **Extensibility Gaps**: The current design makes it difficult to add new analysis algorithms (alternatives to PRIM/CART) or new explanation methods (like using LLMs) without modifying the core `ArchSpace` class.

## The Refactoring Plan

I propose a phased approach to refactor the system into a clean, composition-based architecture that leverages the **Strategy Design Pattern**.

### Phase 1: Separate Analysis from Data Loading

This phase addresses the immediate "God Class" problem and separates concerns.

1.  **Create Specialized Analyzer Classes**: Extract the analysis logic from `ArchSpace` into new, single-responsibility classes:
    *   `DataProcessor`: For data discretization and labeling.
    *   `RobustnessAnalyzer`: For all robustness-related calculations.
    *   `ScenarioDiscoverer`: For running PRIM and CART algorithms.
    *   `TradeoffAnalyzer`: For calculating and analyzing trade-offs.

2.  **Slim Down `ArchSpace`**: The `ArchSpace` class will become a lean coordinator. It will be initialized with experiment data and will delegate analysis tasks to instances of the new analyzer classes.

3.  **Refactor Subclasses into `PatternLoaders`**: The existing subclasses (`GatewayOffloading`, etc.) will **no longer inherit from `ArchSpace`**. They will become simple loader classes whose sole purpose is to read a CSV and return the `experiments_df` and `outcomes_df`.

### Phase 2: Adopt a Declarative, Strategy-Based Architecture

This phase modernizes the architecture, making it truly pluggable and extensible.

1.  **Implement a Pluggable Subsystem**: We will introduce manager classes that execute different "strategies" for analysis and explanation.
    *   **`ScenarioDiscoveryManager`**: Will manage and run scenario discovery algorithms.
        *   **Interface**: `discover(strategy: IScenarioDiscoveryStrategy, ...)`
        *   **Strategies**: `PrimStrategy`, `CartStrategy`. New algorithms can be added as new strategy classes.
    *   **`ExplanationManager`**: Will manage generating explanations for various artifacts (tables, plots, etc.).
        *   **Interface**: `explain(artifact, strategy: IExplanationStrategy, ...)`
        *   **Strategies**: `TemplateExplainerStrategy` (using existing logic) and a future `LLMExplainerStrategy`.

2.  **Adopt Declarative Definitions**: We will replace the hardcoded `PatternLoader` classes from Phase 1 with a generic system.
    *   **`pattern.json` files**: The logic for each pattern will be moved to a declarative JSON file that conforms to the Pydantic models in `definitions.py`.
    *   **Generic `DataLoader`**: A single, reusable data loader will read any pattern's CSV by using its corresponding JSON definition file.

## Proposed Future Architecture

```
+-------------------+       +--------------------+       +----------------------+
| pattern.json      |----->| PatternDefinition  |----->|     DataLoader       |
| (declarative)     |       | (from definitions.py)|       | (generic)            |
+-------------------+       +--------------------+       +----------------------+
                                                                    |
                                                                    | (creates dataframes)
                                                                    v
+-----------------------------------------------------------------------------------------+
|                                    ArchSpace (Coordinator)                              |
|-----------------------------------------------------------------------------------------|
| - experiments_df, outcomes_df                                                           |
| - data_processor: DataProcessor                                                         |
| - discovery_manager: ScenarioDiscoveryManager                                           |
| - explanation_manager: ExplanationManager                                               |
| - robustness_analyzer: RobustnessAnalyzer                                               |
| - tradeoff_analyzer: TradeoffAnalyzer                                                   |
+-----------------------------------------------------------------------------------------+
     |        |                    |                          |
     |        |                    |                          +--------------->+-----------------------+
     |        |                    |                                           | RobustnessAnalyzer    |
     |        |                    +------------------------------------------>+-----------------------+
     |        |                                                                | TradeoffAnalyzer      |
     |        +-------------------------------------------------------------->+-----------------------+
     |                                                                        | DataProcessor         |
     +------------------------------------------------------------------------+-----------------------+
          |
          v
+---------------------------+      +---------------------------------+
| ScenarioDiscoveryManager  |----->|   IScenarioDiscoveryStrategy    |
|                           |      |---------------------------------|
| discover(strategy, ...)   |      | + PrimStrategy                  |
+---------------------------+      | + CartStrategy                  |
                                   | + ... (future algorithms)       |
                                   +---------------------------------+

          v
+---------------------------+      +---------------------------------+
| ExplanationManager        |----->|      IExplanationStrategy       |
|                           |      |---------------------------------|
| explain(artifact, ...)    |      | + TemplateExplainerStrategy     |
+---------------------------+      | + LLMExplainerStrategy (future) |
                                   +---------------------------------+
```

## Benefits of This Approach

*   **Decoupled**: Data loading, data processing, and different analyses are completely separate.
*   **Extensible**: New analysis algorithms or explanation methods can be added simply by creating new "strategy" classes, without changing any existing code.
*   **Cohesive**: Each class will have a single, well-defined responsibility.
*   **Maintainable**: The code will be easier to understand, test, and debug.
