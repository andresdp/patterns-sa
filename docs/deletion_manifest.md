# ADEPT v3.0 Cleanup: Deletion Manifest

This manifest outlines the components to be removed or preserved to transition ADEPT into a clean **v3.0 "Core Analysis"** release. The goal is to remove superseded legacy code, unused structural placeholders, and developer-specific scripts to improve maintainability and usability.

## 1. Deletion Manifest (Items to be Removed)

| Component | Path | Action | Justification |
| :--- | :--- | :--- | :--- |
| **Legacy Framework** | `archspaces/` | **Delete** | Superseded by the modern `adept/` package. All core logic (loading, discovery, visualization) has been migrated and refined. |
| **Old CLI** | `bin/archspace_cli.py` | **Delete** | Hard-coded to work with the legacy `archspaces` classes; incompatible with the new `PatternAnalysis` API. |
| **Milestone Checks** | `checks/` | **Delete** | Temporary scripts used to verify development milestones (Phases 1–4). Replaced by the `tests/` suite. |
| **Redundant Registry** | `adept/core/parameter_registry.py` | **Delete** | Redundant logic. The Pydantic models in `adept/core/models.py` now handle parameter metadata and validation natively. |
| **Unused Extension API** | `adept/core/plugin_api.py` | **Delete** | Related to deferred Phase 7 work. Removing it simplifies the core package for initial release. |
| **Unused Extensions** | `adept/core/plugins/` | **Delete** | Empty/boilerplate directory for the deferred plugin system. |
| **Adaptive Experiment API** | `adept/experiment/` | **Delete** | Skeleton classes for temporal behavioral analysis (Phase 6). Since that work is deferred, this is currently dead code. |
| **Storage Placeholder** | `adept/storage/` | **Delete** | Placeholder for DB persistence. ADEPT v3.0 is entirely memory-resident (Pandas/Pydantic), making this unnecessary. |

---

## 2. Preservation Manifest (Items to be Kept)

| Component | Path | Reason for Staying |
| :--- | :--- | :--- |
| **Legacy Archive** | `legacy/` | **User Request.** Preserved as a historical reference for previous papers and original simulation results (JMT jars, etc.). |
| **Linter Utility** | `adept/utils/linter.py` | **User Request.** Useful utility for maintaining code quality during manual edits. |
| **Analysis Patterns** | `patterns/` | **Manual Review.** Currently held for manual inspection to decide which notebooks to prune or update to the v3.0 API. |
| **Core Framework** | `adept/analysis/`, `adept/core/` | The functional backbone of the new ADEPT architecture. |
| **Validation Utilities** | `adept/utils/` | Contains critical exception and validation logic used by the core framework. |
| **Unit Tests** | `tests/` | Essential for ensuring that cleanup or future work does not regress existing functionality. |

---

## 3. Post-Cleanup Project Structure

After executing this manifest, the project structure will align with the functional **"Analysis Journey"** workflow. The `adept/` package will contain only production-ready code, and the project root will be free of developer-specific "junk" files, signaling a stable v3.0 release.
