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

    def lint(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        
        # 1. Validate Quality Objectives against Data
        issues.extend(self._validate_objectives(sys_def, df))

        # 2. Validate Parameters against Data
        issues.extend(self._validate_parameters(sys_def, df))

        # 3. Validate Policy Identification against Data
        issues.extend(self._validate_policy_column(sys_def, df))

        # 4. Validate Tradeoffs against Objectives
        issues.extend(self._validate_tradeoffs(sys_def))

        # 5. Validate System Policies against Components
        issues.extend(self._validate_component_policies(sys_def))

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

    def _validate_policy_column(self, sys_def: SystemDefinition, df: pd.DataFrame) -> List[LintIssue]:
        issues = []
        ident = sys_def.dataspace.policy_identification
        if ident.from_ == "column":
            if ident.column and ident.column not in df.columns:
                issues.append(LintIssue(
                    "ERROR",
                    f"Policy identification column '{ident.column}' not found in data.",
                    "Dataspace.PolicyIdentification"
                ))
            
            # Check if policies defined in JSON match values in Data
            if ident.column in df.columns and isinstance(ident.policies, dict):
                json_policies = set(ident.policies.keys())
                # Convert data values to string to ensure matching (e.g. "1" vs 1)
                data_policies = set(df[ident.column].astype(str).unique())
                
                missing_in_data = json_policies - data_policies
                if missing_in_data:
                    issues.append(LintIssue(
                        "WARNING",
                        f"Policies defined in JSON but missing in Data: {missing_in_data}",
                        "Dataspace.PolicyIdentification"
                    ))
        return issues

    def _validate_tradeoffs(self, sys_def: SystemDefinition) -> List[LintIssue]:
        issues = []
        defined_objectives = {obj.name for obj in sys_def.dataspace.quality_objectives}
        
        for tradeoff in sys_def.system.tradeoffs:
            for element_key in tradeoff.elements.keys():
                if element_key not in defined_objectives:
                    issues.append(LintIssue(
                        "ERROR",
                        f"Tradeoff '{tradeoff.name}' references undefined objective '{element_key}'.",
                        "System.Tradeoffs"
                    ))
        return issues

    def _validate_component_policies(self, sys_def: SystemDefinition) -> List[LintIssue]:
        issues = []
        defined_components = set(sys_def.system.components.keys())
        
        # Helper to extract available policies from a component definition
        # Assumes component.decisions structure: { "decision_name": { "policies": { "policy_name": ... } } }
        component_valid_policies = {}
        for c_name, comp in sys_def.system.components.items():
            valid = set()
            for dec_name, dec_body in comp.decisions.items():
                if isinstance(dec_body, dict) and "policies" in dec_body:
                    valid.update(dec_body["policies"].keys())
            component_valid_policies[c_name] = valid

        policies = sys_def.dataspace.policy_identification.policies
        policy_iterator = policies.values() if isinstance(policies, dict) else policies

        for sys_policy in policy_iterator:
            for comp_ref, comp_pol_ref in sys_policy.component_policies.items():
                # Check 1: Component existence
                if comp_ref not in defined_components:
                    issues.append(LintIssue(
                        "ERROR",
                        f"System Policy '{sys_policy.name}' references undefined component '{comp_ref}'.",
                        "Dataspace.Policies"
                    ))
                    continue # Skip next check if component doesn't exist

                # Check 2: Component Policy existence (if decisions are defined)
                # If the component has decisions defined, we should validate against them.
                valid_pols = component_valid_policies.get(comp_ref, set())
                if valid_pols and comp_pol_ref not in valid_pols:
                     issues.append(LintIssue(
                        "WARNING",
                        f"System Policy '{sys_policy.name}' assigns policy '{comp_pol_ref}' to component '{comp_ref}', but this policy is not defined in the component decisions.",
                        "Dataspace.Policies"
                    ))

        return issues
