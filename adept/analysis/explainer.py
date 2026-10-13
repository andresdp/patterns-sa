from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from .box_context import BoxContextExplainer
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
        metrics = artifact if isinstance(artifact, dict) else {}
        
        lines = []
        lines.append("Analysis summary:")
        for k, v in metrics.items():
            lines.append(f" - {k}: {v}")
        text = "\n".join(lines)

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
        self._box_context_explainer = BoxContextExplainer()

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

    def explain_box_context(
        self,
        box: Any,
        system_definition: Any,
        digits: int = 3,
        output_format: str = "plain",
        observed_configuration_counts: Optional[Dict[str, int]] = None,
        observed_scope: Optional[str] = None,
        observed_row_count: Optional[int] = None,
    ) -> Dict[str, Any]:
        """Explain a box from declared links and optional observed configuration counts."""
        result = self._box_context_explainer.explain(
            box,
            system_definition,
            digits=digits,
            observed_configuration_counts=observed_configuration_counts,
            observed_scope=observed_scope,
            observed_row_count=observed_row_count,
        )
        result["text"] = self._box_context_explainer.render(result, output_format=output_format)
        result["output_format"] = output_format
        return result


__all__ = ["IExplanationStrategy", "TemplateExplainerStrategy", "ExplanationManager"]
