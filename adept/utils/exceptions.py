from typing import Any, Optional


class ADEPTError(Exception):
    """Base exception class for all ADEPT-related errors."""
    def __init__(self, message: str, details: Optional[dict] = None):
        super().__init__(message)
        self.message = message
        self.details = details or {}
    
    def __str__(self) -> str:
        if self.details:
            return f"{self.message} - Details: {self.details}"
        return self.message


class DataLoadingError(ADEPTError):
    """Exception raised for errors during data loading."""
    pass


class ValidationError(ADEPTError):
    """Exception raised for data validation failures."""
    pass


class DiscoveryError(ADEPTError):
    """Exception raised for scenario discovery failures."""
    pass


class ConfigurationError(ADEPTError):
    """Exception raised for configuration issues."""
    pass


class AnalysisError(ADEPTError):
    """Exception raised for analysis computation failures."""
    pass


class MissingDependencyError(ADEPTError):
    """Exception raised when required dependencies are missing."""
    def __init__(self, dependency: str, message: str = ""):
        full_message = f"Missing required dependency: {dependency}"
        if message:
            full_message += f" - {message}"
        super().__init__(full_message)
        self.dependency = dependency


class TradeoffDefinitionError(ADEPTError):
    """Exception raised for issues with tradeoff definitions."""
    pass


class VisualizationError(ADEPTError):
    """Exception raised for visualization-related errors."""
    pass


__all__ = [
    "ADEPTError",
    "DataLoadingError",
    "ValidationError", 
    "DiscoveryError",
    "ConfigurationError",
    "AnalysisError",
    "MissingDependencyError",
    "TradeoffDefinitionError",
    "VisualizationError"
]