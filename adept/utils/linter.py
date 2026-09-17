import itertools
from typing import List, Dict, Optional, Set, Tuple, Any
import pandas as pd
from ..core.models import SystemDefinition

# Concentration (most-common-value share) at or above which a declared quality
# objective or parameter is flagged as low-variance (R3). Calibrated against
# the observed 78%-concentrated `RAM Usage Avg Mean` case in FL's aggregated
# telemetry data (AE4) -- not derived from any broader statistical analysis,
# so a future pattern with different data characteristics may need a
# different cutoff.
LOW_VARIANCE_THRESHOLD = 0.70

class LintIssue:
    def __init__(self, level: str, message: str, context: str):
        self.level = level  # ERROR, WARNING
        self.message = message
        self.context = context

    def __str__(self):
        return f"[{self.level}] {self.context}: {self.message}"

class SystemLinter:
    """Validates the semantic integrity of a SystemDefinition and its data."""
    
    SUPPORTED_SCHEMES = {'discretization', 'pareto', 'threshold', 'pareto_epsilon', 'pareto_knee'}

    def lint(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        
        # 1. Validate Quality Objectives against Data
        issues.extend(self._validate_objectives(sys_def, df))

        # 2. Validate Parameters against Data
        # Note: With parameter injection, parameters might not be in raw data but added later.
        # However, lint is typically called after load/injection in GenericDataLoader.
        issues.extend(self._validate_parameters(sys_def, df))

        # 3. Validate Configuration Identification against Data
        issues.extend(self._validate_configuration_column(sys_def, df))

        # 4. Validate Tradeoffs against Objectives
        issues.extend(self._validate_tradeoffs(sys_def))

        # 5. Validate System Configurations against Patterns
        issues.extend(self._validate_configuration_references(sys_def))

        # 6. Validate multi-decision configuration completeness (R1)
        issues.extend(self._validate_multi_decision_completeness(sys_def))

        # 7. Validate policy-combination coverage (R2)
        issues.extend(self._validate_policy_combination_coverage(sys_def))

        # 8. Validate low-variance objectives/parameters (R3)
        issues.extend(self._validate_low_variance(sys_def, df))

        return issues

    def _iter_configs(self, sys_def: SystemDefinition):
        """Normalize `configuration_identification.configurations` -- a dict
        keyed by config id, or (legacy) a plain list -- into an iterable of
        SystemConfiguration objects. Shared by every check below that walks
        declared configurations."""
        configs = sys_def.dataspace.configuration_identification.configurations
        return configs.values() if isinstance(configs, dict) else configs

    def _resolve_column(self, param_name: str, comp_name: str, df: pd.DataFrame) -> Optional[str]:
        """Resolve a component parameter to its actual data column: mirrors
        GenericDataLoader, checking the bare name first and the
        component-prefixed name second. Returns None if neither is present."""
        candidates = [param_name, f"{comp_name}_{param_name}"]
        return next((c for c in candidates if c in df.columns), None)

    def _validate_objectives(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        for obj in sys_def.dataspace.quality_objectives:
            if obj.name not in df.columns:
                issues.append(LintIssue(
                    "ERROR", 
                    f"Quality Objective '{obj.name}' not found in data columns.", 
                    "Dataspace.QualityObjectives"
                ))
        return issues

    def _validate_parameters(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        for comp_name, comp in sys_def.system.components.items():
            for param_name, param in comp.parameters.items():
                if self._resolve_column(param_name, comp_name, df) is None:
                    candidates = [param_name, f"{comp_name}_{param_name}"]
                    issues.append(LintIssue(
                        "WARNING",
                        f"Parameter '{param_name}' (Component: {comp_name}) not found in data columns. Checked: {candidates}",
                        "System.Components"
                    ))
        return issues

    def _validate_configuration_column(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        ident = sys_def.dataspace.configuration_identification
        if ident.from_ == "column":
            if ident.column and ident.column not in df.columns:
                issues.append(LintIssue(
                    "ERROR",
                    f"Configuration identification column '{ident.column}' not found in data.",
                    "Dataspace.ConfigurationIdentification"
                ))
            
            # Check if configurations defined in JSON match values in Data
            if ident.column in df.columns and isinstance(ident.configurations, dict):
                json_configs = set(ident.configurations.keys())
                # Convert data values to string to ensure matching (e.g. "1" vs 1)
                data_configs = set(df[ident.column].astype(str).unique())
                
                missing_in_data = json_configs - data_configs
                if missing_in_data:
                    issues.append(LintIssue(
                        "WARNING",
                        f"Configurations defined in JSON but missing in Data: {missing_in_data}",
                        "Dataspace.ConfigurationIdentification"
                    ))
        return issues

    def _validate_tradeoffs(self, sys_def: SystemDefinition) -> List[LintIssue]:
        issues = []
        defined_objectives = {obj.name for obj in sys_def.dataspace.quality_objectives}
        
        for tradeoff in sys_def.system.tradeoffs:
            if tradeoff.scheme not in self.SUPPORTED_SCHEMES:
                issues.append(LintIssue(
                    "ERROR",
                    f"Tradeoff '{tradeoff.name}' uses unsupported scheme '{tradeoff.scheme}'. Supported: {self.SUPPORTED_SCHEMES}",
                    "System.Tradeoffs"
                ))

            for element_key in tradeoff.elements.keys():
                if element_key not in defined_objectives:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Tradeoff '{tradeoff.name}' references undefined objective '{element_key}'.",
                        "System.Tradeoffs"
                    ))
        return issues

    def _validate_configuration_references(self, sys_def: SystemDefinition) -> List[LintIssue]:
        issues = []
        
        config_iterator = self._iter_configs(sys_def)

        for config in config_iterator:
            for ref in config.pattern_policy_references:
                # Check 1: Component existence
                comp = sys_def.system.components.get(ref.component)
                if not comp:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Configuration '{config.name}' references undefined component '{ref.component}'.",
                        "Dataspace.Configurations"
                    ))
                    continue

                # Check 2: Decision existence
                decision = comp.decisions.get(ref.decision)
                if not decision:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Configuration '{config.name}' references undefined decision '{ref.decision}' in component '{ref.component}'.",
                        "Dataspace.Configurations"
                    ))
                    continue

                # Check 3: Policy existence
                if ref.policy not in decision.policies:
                     issues.append(LintIssue(
                        "ERROR",
                        f"Configuration '{config.name}' references undefined policy '{ref.policy}' for decision '{ref.decision}' in component '{ref.component}'.",
                        "Dataspace.Configurations"
                    ))

            # Legacy Support: Check component_policies dict
            if hasattr(config, 'component_policies') and config.component_policies:
                for comp_name, pol_name in config.component_policies.items():
                    comp = sys_def.system.components.get(comp_name)
                    if not comp:
                        issues.append(LintIssue(
                            "ERROR", 
                            f"Configuration '{config.name}' references undefined component '{comp_name}'.", 
                            "Dataspace.Configurations"
                        ))
                        continue
                    
                    # Check if policy exists in ANY decision of the component
                    found = False
                    for decision in comp.decisions.values():
                        if pol_name in decision.policies:
                            found = True
                            break
                    
                    if not found:
                        issues.append(LintIssue(
                            "ERROR",
                            f"Configuration '{config.name}' references undefined policy '{pol_name}' in component '{comp_name}'.",
                            "Dataspace.Configurations"
                        ))

        return issues

    def _validate_multi_decision_completeness(self, sys_def: SystemDefinition) -> List[LintIssue]:
        """R1: every declared configuration must reference every decision of a
        multi-decision component exactly once. A component with a single
        decision is exempt -- there is nothing to check, it is trivially
        complete."""
        issues = []

        config_iterator = self._iter_configs(sys_def)

        for comp_name, comp in sys_def.system.components.items():
            decision_names = list(comp.decisions.keys())
            if len(decision_names) <= 1:
                continue

            for config in config_iterator:
                ref_counts: Dict[str, int] = {}
                for ref in config.pattern_policy_references:
                    if ref.component != comp_name:
                        continue
                    ref_counts[ref.decision] = ref_counts.get(ref.decision, 0) + 1

                missing = [d for d in decision_names if ref_counts.get(d, 0) == 0]
                duplicated = [d for d, count in ref_counts.items() if count > 1]

                for decision_name in missing:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Configuration '{config.name}' does not reference decision "
                        f"'{decision_name}' of multi-decision component '{comp_name}'.",
                        "Dataspace.Configurations"
                    ))

                for decision_name in duplicated:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Configuration '{config.name}' references decision '{decision_name}' "
                        f"of component '{comp_name}' more than once "
                        f"({ref_counts[decision_name]} times).",
                        "Dataspace.Configurations"
                    ))

        return issues

    def _validate_policy_combination_coverage(self, sys_def: SystemDefinition) -> List[LintIssue]:
        """R2: for each multi-decision component, compare the declared
        configurations' decision->policy combinations against the theoretical
        cross-product of policies across its decisions, and WARN naming any
        undeclared combinations. A single-decision component's cross-product
        is trivially 1-of-1 (its one decision's policies each form their own
        size-1 "combination"), so this never fires for one (R5)."""
        issues = []

        config_iterator = self._iter_configs(sys_def)

        for comp_name, comp in sys_def.system.components.items():
            decision_names = list(comp.decisions.keys())
            if len(decision_names) <= 1:
                continue

            policy_lists = [list(comp.decisions[d].policies.keys()) for d in decision_names]
            all_combos: Set[Tuple[str, ...]] = set(itertools.product(*policy_lists))

            declared_combos: Set[Tuple[str, ...]] = set()
            for config in config_iterator:
                per_decision: Dict[str, str] = {}
                is_well_formed = True
                for ref in config.pattern_policy_references:
                    if ref.component != comp_name:
                        continue
                    if ref.decision in per_decision:
                        # Duplicate reference -- already reported by the
                        # completeness check; skip this config for coverage
                        # purposes since its combination is ambiguous.
                        is_well_formed = False
                        break
                    per_decision[ref.decision] = ref.policy

                if is_well_formed and all(d in per_decision for d in decision_names):
                    declared_combos.add(tuple(per_decision[d] for d in decision_names))

            missing_combos = all_combos - declared_combos
            if missing_combos:
                missing_strs = sorted(",".join(combo) for combo in missing_combos)
                issues.append(LintIssue(
                    "WARNING",
                    f"Component '{comp_name}' has incomplete policy-combination coverage: "
                    f"{len(declared_combos)} of {len(all_combos)} combinations declared "
                    f"(decisions: {', '.join(decision_names)}). "
                    f"Missing combinations: {', '.join(missing_strs)}.",
                    "Dataspace.Configurations"
                ))

        return issues

    def _validate_low_variance(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        """R3: flag declared quality objectives and parameters whose data is
        near-constant/low-variance, so an architect decides whether to keep
        them declared rather than the pipeline silently deciding upfront."""
        issues = []

        def _concentration(col: str) -> float:
            # NaN is treated as its own distinct value for concentration
            # purposes (dropna=False): a column that is NaN-dominated (e.g.
            # an optional pattern parameter that is absent whenever its
            # pattern is OFF) is just as low-signal/near-constant as one
            # dominated by a single non-null value, so it should surface the
            # same way rather than being silently excluded from the count.
            counts = df[col].value_counts(normalize=True, dropna=False)
            return float(counts.max()) if not counts.empty else 0.0

        def _check(label: str, column: str, context: str) -> None:
            concentration = _concentration(column)
            if concentration >= LOW_VARIANCE_THRESHOLD:
                issues.append(LintIssue(
                    "WARNING",
                    f"{label} is low-variance: "
                    f"{concentration:.1%} of values are concentrated on a single value "
                    f"(threshold {LOW_VARIANCE_THRESHOLD:.0%}).",
                    context
                ))

        # Quality objectives
        for obj in sys_def.dataspace.quality_objectives:
            if obj.name in df.columns:
                _check(f"Quality Objective '{obj.name}'", obj.name, "Dataspace.QualityObjectives")

        # System-level parameters
        for param_name in sys_def.system.parameters.keys():
            if param_name in df.columns:
                _check(f"Parameter '{param_name}' (System)", param_name, "System.Parameters")

        # Component (pattern) parameters
        for comp_name, comp in sys_def.system.components.items():
            for param_name in comp.parameters.keys():
                col = self._resolve_column(param_name, comp_name, df)
                if col is not None:
                    _check(f"Parameter '{param_name}' (Component: {comp_name})", col, "System.Components")

        return issues
