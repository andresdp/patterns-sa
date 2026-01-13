"""Plugin API for ArchSpace: separate Parser / Metrics / Report hooks.

This module defines the hook interfaces and a simple registry for plugins.
"""
from abc import ABC, abstractmethod
from typing import Dict, Any, Optional, List
import pandas as pd


class ParserHook(ABC):
    """Parse raw input (file/path/other) into a canonical pandas.DataFrame."""

    @abstractmethod
    def parse(self, input_source: str) -> pd.DataFrame:
        raise NotImplementedError()


class MetricsHook(ABC):
    """Compute domain-specific metrics from a canonical DataFrame."""

    @abstractmethod
    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        raise NotImplementedError()


class ReportHook(ABC):
    """Export metrics and produce report artifacts (CSV/JSON/plots)."""

    @abstractmethod
    def export_report(self, metrics: Dict[str, Any], outdir: str) -> Dict[str, str]:
        raise NotImplementedError()


class ArchSpacePlugin(ABC):
    """Convenience base: plugins implement three hooks as methods."""

    @abstractmethod
    def name(self) -> str:
        raise NotImplementedError()

    @abstractmethod
    def parse(self, input_source: str) -> pd.DataFrame:
        raise NotImplementedError()

    @abstractmethod
    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, Any]:
        raise NotImplementedError()

    @abstractmethod
    def export_report(self, metrics: Dict[str, Any], outdir: str) -> Dict[str, str]:
        raise NotImplementedError()


class PluginRegistry:
    """Simple in-memory registry for ArchSpace plugins."""

    def __init__(self) -> None:
        self._plugins: Dict[str, ArchSpacePlugin] = {}

    def register(self, plugin: ArchSpacePlugin) -> None:
        self._plugins[plugin.name()] = plugin

    def get(self, name: str) -> Optional[ArchSpacePlugin]:
        return self._plugins.get(name)

    def list(self) -> List[str]:
        return list(self._plugins.keys())


__all__ = [
    "ParserHook",
    "MetricsHook",
    "ReportHook",
    "ArchSpacePlugin",
    "PluginRegistry",
]
