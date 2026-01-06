# Track Plan: Refactor and Standardize Pattern Analysis Scripts

## Phase 1: Framework Decomposition (Refactoring Proposal Phase 1)
- [ ] Task: Create `DataProcessor` class to handle data discretization and labeling logic extracted from `ArchSpace`.
- [ ] Task: Create `RobustnessAnalyzer` class to isolate robustness calculation logic.
- [ ] Task: Create `ScenarioDiscoverer` (or `ScenarioDiscoveryManager`) class to encapsulate PRIM and CART logic.
- [ ] Task: Create `TradeoffAnalyzer` class for trade-off calculations.
- [ ] Task: Refactor `ArchSpace` to become a coordinator that initializes these new components and delegates tasks to them.
- [ ] Task: Conductor - User Manual Verification 'Phase 1: Framework Decomposition' (Protocol in workflow.md)

## Phase 2: Declarative Loading & Strategy Implementation (Refactoring Proposal Phase 2)
- [ ] Task: Implement `ScenarioDiscoveryManager` with `IScenarioDiscoveryStrategy` (Strategies: `PrimStrategy`, `CartStrategy`).
- [ ] Task: Implement `ExplanationManager` with `IExplanationStrategy` (Strategy: `TemplateExplainerStrategy`).
- [ ] Task: Implement the generic `DataLoader` that parses `*.json` system definitions (as per `docs/json_schema_usage.md`).
- [ ] Task: Update `ArchSpace` to integrate with the new Managers and Loader.
- [ ] Task: Conductor - User Manual Verification 'Phase 2: Declarative Loading & Strategy Implementation' (Protocol in workflow.md)

## Phase 3: Toy Example Migration (Proof of Concept)
- [ ] Task: Create `patterns/Toy_Example/ToyExample.json` conforming to the JSON schema.
- [ ] Task: Refactor `patterns/Toy_Example/analysis.py` to use the new `DataLoader` and refactored `ArchSpace` coordinator.
- [ ] Task: Verify `Toy_Example` output matches legacy results.
- [ ] Task: Conductor - User Manual Verification 'Phase 3: Toy Example Migration' (Protocol in workflow.md)

## Phase 4: Gateway & Structural Patterns Migration
- [ ] Task: Migrate `Gateway_Aggregation`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Migrate `Gateway_Offloading`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Migrate `Anti_Corruption_Layer`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Migrate `Backends_for_Frontends`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Conductor - User Manual Verification 'Phase 4: Gateway & Structural Patterns Migration' (Protocol in workflow.md)

## Phase 5: Data/Compute Patterns Migration & Final Polish
- [ ] Task: Migrate `CQRS`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Migrate `Pipes_and_Filters`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Migrate `Static_Content_Hosting`: Create JSON and refactor to `analysis.py`.
- [ ] Task: Run full regression test suite across all patterns.
- [ ] Task: Update `README.md` and `docs/` to reflect the completed refactoring and new usage patterns.
- [ ] Task: Conductor - User Manual Verification 'Phase 5: Data/Compute Patterns Migration & Final Polish' (Protocol in workflow.md)