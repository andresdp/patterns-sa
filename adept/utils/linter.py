from typing import List, Dict, Set, Any
import pandas as pd
from ..core.models import SystemDefinition

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

        return issues

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
                # Logic mirrors GenericDataLoader: check exact name or prefixed name
                candidates = [param_name, f"{comp_name}_{param_name}"]
                if not any(c in df.columns for c in candidates):
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
        
        configs = sys_def.dataspace.configuration_identification.configurations
        config_iterator = configs.values() if isinstance(configs, dict) else configs

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

        return issues