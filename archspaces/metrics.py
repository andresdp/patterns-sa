from abc import ABC, abstractmethod
from typing import Dict, Iterable, Optional
import pandas as pd
import numpy as np


class MetricsEngine(ABC):
    @abstractmethod
    def compute(self, df: pd.DataFrame) -> Dict[str, object]:
        """Compute and return metrics for `df`."""


class ToyMetricsEngine(MetricsEngine):
    """Simple reference implementation that returns basic numeric summaries."""
    def compute(self, df: pd.DataFrame) -> Dict[str, object]:
        numeric = df.select_dtypes(include=[np.number])
        return {
            "count": int(len(df)),
            "numeric_cols": list(numeric.columns),
            "means": numeric.mean().to_dict(),
            "stds": numeric.std().to_dict(),
        }


# Lightweight clustering helper with optional sklearn usage
class ClusteringEngine:
    def __init__(self):
        try:
            from sklearn.cluster import KMeans
            self._KMeans = KMeans
        except Exception:
            self._KMeans = None

    def kmeans(self, df: pd.DataFrame, features: Optional[Iterable[str]] = None, n_clusters: int = 3, random_state: int = 42):
        X = df[list(features)] if features is not None else df.select_dtypes(include=[float, int])
        if X.shape[0] == 0:
            return []
        if self._KMeans is not None:
            model = self._KMeans(n_clusters=n_clusters, random_state=random_state)
            labels = model.fit_predict(X.values)
            return labels.tolist()
        # fallback simple kmeans-like partition (by sorted value on first column)
        col = X.columns[0]
        order = X[col].sort_values().index
        sizes = [len(order) // n_clusters + (1 if i < (len(order) % n_clusters) else 0) for i in range(n_clusters)]
        labels = [None] * len(order)
        idx = 0
        for k, s in enumerate(sizes):
            for _ in range(s):
                labels[order[idx]] = k
                idx += 1
        # reorder to original index order
        return [labels[i] for i in range(len(labels))]


__all__ = ["MetricsEngine", "ToyMetricsEngine", "ClusteringEngine"]
