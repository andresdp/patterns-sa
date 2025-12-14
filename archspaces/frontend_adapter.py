"""Frontend adapter: convert analysis outputs to UI-friendly JSON payloads.

This module provides helpers to prepare chart-ready payloads and summaries
that a frontend can consume without re-running heavy analyses.
"""
from typing import Dict, Any, List


def metrics_to_summary_payload(metrics: Dict[str, Any]) -> Dict[str, Any]:
    """Convert metrics dict into a concise summary payload for UI display."""
    return {
        "summary": [{"name": k, "value": v} for k, v in metrics.items()],
        "metrics_count": len(metrics),
    }


def timeseries_to_chart_payload(name: str, series: List[float]) -> Dict[str, Any]:
    return {"type": "line", "name": name, "data": series}


def assemble_payload(metrics: Dict[str, Any], charts: List[Dict[str, Any]] = None) -> Dict[str, Any]:
    return {"metrics": metrics_to_summary_payload(metrics), "charts": charts or []}


__all__ = ["metrics_to_summary_payload", "timeseries_to_chart_payload", "assemble_payload"]
