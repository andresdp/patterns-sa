from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import hashlib
import json


class IExplanationStrategy(ABC):
    @abstractmethod
    def explain(self, artifact: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        """Generates an explanation for the given artifact."""
        raise NotImplementedError()


class TemplateExplainerStrategy(IExplanationStrategy):
    """A lightweight explainer that produces textual summaries using templates."""

    def explain(self, artifact: Any, context: Optional[Dict[str, Any]] = None) -> Dict[str, str]:
        # Assuming artifact is a dict of metrics for now, as in the legacy code
        metrics = artifact if isinstance(artifact, dict) else {}
        
        lines = []
        lines.append("Analysis summary:")
        for k, v in metrics.items():
            lines.append(f" - {k}: {v}")
        text = "\n".join(lines)

        # simple deterministic id for caching
        try:
            uid = hashlib.sha1(json.dumps(metrics, sort_keys=True, default=str).encode()).hexdigest()[:8]
        except Exception:
            uid = "unknown"
            
        return {"text": text, "explain_id": uid}


class ExplanationManager:
    """Manages explanation strategies."""

    def __init__(self):
        self._strategies = {
            'template': TemplateExplainerStrategy
        }

    def get_strategy(self, method: Optional[str]) -> IExplanationStrategy:
        if method is None:
            method = 'template'
        
        strategy_class = self._strategies.get(method.lower())
        if strategy_class:
            return strategy_class()
        
        return TemplateExplainerStrategy()

    def explain(self, artifact: Any, method: Optional[str] = None, **kwargs) -> Dict[str, str]:
        strategy = self.get_strategy(method)
        return strategy.explain(artifact, **kwargs)


__all__ = ["IExplanationStrategy", "TemplateExplainerStrategy", "ExplanationManager"]
