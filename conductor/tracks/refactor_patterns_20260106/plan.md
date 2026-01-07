# Track Plan: ADEPT Framework Implementation

## Phase 1: Framework Decomposition (Refactoring Proposal Phase 1) [checkpoint: 1e475f2]
- [x] Task: Create `DataProcessor` class to handle data discretization and labeling logic extracted from `ArchSpace`.
- [x] Task: Create `RobustnessAnalyzer` class to isolate robustness calculation logic.
- [x] Task: Create `ScenarioDiscoverer` (or `ScenarioDiscoveryManager`) class to encapsulate PRIM and CART logic.
- [x] Task: Create `TradeoffAnalyzer` class for trade-off calculations.
- [x] Task: Refactor `ArchSpace` to become a coordinator that initializes these new components and delegates tasks to them.
- [x] Task: Conductor - User Manual Verification 'Phase 1: Framework Decomposition' (Protocol in workflow.md)

## Phase 2: Declarative Loading & Strategy Implementation (Refactoring Proposal Phase 2) [checkpoint: c4cdefb]
- [x] Task: Implement `ScenarioDiscoveryManager` with `IScenarioDiscoveryStrategy` (Strategies: `PrimStrategy`, `CartStrategy`).
- [x] Task: Implement `ExplanationManager` with `IExplanationStrategy` (Strategy: `TemplateExplainerStrategy`).
- [x] Task: Implement the generic `DataLoader` that parses `*.json` system definitions (as per `docs/json_schema_usage.md`).
- [x] Task: Update `ArchSpace` to integrate with the new Managers and Loader.
- [x] Task: Conductor - User Manual Verification 'Phase 2: Declarative Loading & Strategy Implementation' (Protocol in workflow.md)

## Phase 3: ADEPT Core & Advanced Data Modeling [checkpoint: c8eb00d]
- [x] Task: Reorganize `archspaces/` modules into the ADEPT modular structure (as per `docs/functional.md` section 3.1).
- [x] Task: Implement `ParameterRegistry` to handle Lever/Uncertainty/Outcome categorization and hierarchy.
- [x] Task: Extend `GenericDataLoader` to support `AdaptiveProcess` metadata and temporal `BehavioralTrace` loading.
- [x] Task: Conductor - User Manual Verification 'Phase 3: ADEPT Core' (Protocol in workflow.md)

## Phase 4: Enhanced Discretization-Based Exploration [checkpoint: 0b754c3]
- [x] Task: Formalize `QualityBin` and `DiscretizationScheme` entities within the `DataProcessor`.
- [x] Task: Update `ScenarioDiscoveryManager` to explicitly support the "Discretization" paradigm mode with multi-dimensional targets.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Exploration Paradigm' (Protocol in workflow.md)

## Phase 5: Static Pattern Migration (Microservices)
- [ ] Task: Migrate `Toy_Example` to the full ADEPT model as a proof-of-concept.
- [ ] Task: Migrate microservices patterns: `Gateway_Aggregation`, `Gateway_Offloading`, `CQRS`, and `Anti_Corruption_Layer`.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Static Migration' (Protocol in workflow.md)

## Phase 6: Adaptive Pattern Migration (Temporal Behavior)
- [ ] Task: Implement basic analysis logic for `BehavioralTrace` data (temporal sensitivity and convergence checks).
- [ ] Task: Migrate adaptive datasets: `Federated Learning` patterns and `AWS_Petshop`.
- [ ] Task: Conductor - User Manual Verification 'Phase 6: Adaptive Migration' (Protocol in workflow.md)

## Phase 7: Explainability & Documentation
- [ ] Task: Implement `LLMExplainerStrategy` for natural language rule translation.
- [ ] Task: Standardize all visualization functions into a unified ADEPT Plotting API.
- [ ] Task: Update `README.md` and `docs/` with final ADEPT branding and usage guidelines.
- [ ] Task: Conductor - User Manual Verification 'Phase 7: Final Polish' (Protocol in workflow.md)
