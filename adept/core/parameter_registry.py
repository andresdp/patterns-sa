from typing import Dict, List, Optional
from .models import Parameter, ParameterType, ParameterLevel

class ParameterRegistry:
    """Registry for managing and categorized system/pattern/infrastructure parameters.
    
    The ParameterRegistry serves as a centralized metadata repository during an 
    analysis session. It allows the framework to reason about the role 
    (Lever, Uncertainty, etc.) and scope (System, Pattern, Infrastructure) of 
    different variables, facilitating structured sensitivity analysis and 
    automated experimental design.
    """

    def __init__(self):
        self._parameters: Dict[str, Parameter] = {}

    def register(self, parameter: Parameter) -> None:
        """Registers a new parameter in the registry.
        
        Args:
            parameter: The Parameter instance to register.
        """
        self._parameters[parameter.name] = parameter

    def get(self, name: str) -> Optional[Parameter]:
        """Retrieves a parameter by name.
        
        Args:
            name: The unique name of the parameter.
            
        Returns:
            The Parameter instance if found, else None.
        """
        return self._parameters.get(name)

    def get_by_type(self, param_type: ParameterType) -> List[Parameter]:
        """Retrieves all parameters of a specific type.
        
        This is used to identify all controllable 'Levers' or all measurable 
        'Outcomes' for targeted analysis.
        
        Args:
            param_type: The ParameterType enum value to filter by.
        """
        return [p for p in self._parameters.values() if p.type == param_type]

    def get_by_level(self, param_level: ParameterLevel) -> List[Parameter]:
        """Retrieves all parameters of a specific level.
        
        Allows focusing analysis on a specific architectural layer (e.g., only 
        Pattern-level decisions).
        
        Args:
            param_level: The ParameterLevel enum value to filter by.
        """
        return [p for p in self._parameters.values() if p.level == param_level]

    def all_parameters(self) -> List[Parameter]:
        """Returns a list of all registered parameters."""
        return list(self._parameters.values())