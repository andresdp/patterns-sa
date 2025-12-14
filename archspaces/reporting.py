"""Reporting utilities: save metrics as CSV/JSON and produce a simple plot."""
from typing import Dict, Any
import os
import json
import csv

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


def save_metrics_csv(metrics: Dict[str, Any], outpath: str) -> str:
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["metric", "value"])
        for k, v in metrics.items():
            writer.writerow([k, v])
    return outpath


def save_metrics_json(metrics: Dict[str, Any], outpath: str) -> str:
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    with open(outpath, "w") as fh:
        json.dump(metrics, fh, indent=2)
    return outpath


def plot_metric_histogram(metric_name: str, values: list, outpath: str) -> str:
    os.makedirs(os.path.dirname(outpath), exist_ok=True)
    plt.figure()
    plt.hist(values, bins=20)
    plt.title(f"{metric_name} distribution")
    plt.xlabel(metric_name)
    plt.ylabel("count")
    plt.tight_layout()
    plt.savefig(outpath)
    plt.close()
    return outpath


__all__ = ["save_metrics_csv", "save_metrics_json", "plot_metric_histogram"]
