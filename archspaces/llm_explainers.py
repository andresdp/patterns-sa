"""LLM explainers: pluggable interface and simple prompt templates.

This module provides a small, dependency-light explainer interface that can be
extended to call external LLM services. The implementation below is a stub
that formats explanations locally; calling an external API should be done via
an adapter that implements `LLMClient`.
"""
from typing import Dict, Any, Optional
from abc import ABC, abstractmethod
import hashlib
import json


class Explainer(ABC):
    @abstractmethod
    def explain(self, metrics: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        raise NotImplementedError()


class LocalTemplateExplainer(Explainer):
    """A lightweight explainer that produces textual summaries using templates.

    This is deterministic and safe for CI/testing; later you can add an
    `OpenAIExplainer` or similar that calls a remote LLM.
    """

    def explain(self, metrics: Dict[str, Any], context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        lines = []
        lines.append("Analysis summary:")
        for k, v in metrics.items():
            lines.append(f" - {k}: {v}")
        text = "\n".join(lines)

        # simple deterministic id for caching
        uid = hashlib.sha1(json.dumps(metrics, sort_keys=True).encode()).hexdigest()[:8]
        return {"text": text, "explain_id": uid}


class LLMClient(ABC):
    """Adapter interface for external LLM providers.

    Concrete implementations should handle API keys, rate limiting, and
    safety checks. Not implemented here.
    """

    @abstractmethod
    def call(self, prompt: str) -> str:
        raise NotImplementedError()


__all__ = ["Explainer", "LocalTemplateExplainer", "LLMClient"]
