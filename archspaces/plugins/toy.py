"""Toy plugin: minimal parser, metrics and reporting for the Toy example."""
from typing import Dict
import os
import pandas as pd
from archspaces.plugin_api import ArchSpacePlugin


class ToyPlugin(ArchSpacePlugin):
    def name(self) -> str:
        return "toy"

    def parse(self, input_source: str) -> pd.DataFrame:
        # simple CSV reader; ETL can normalize before passing here
        df = pd.read_csv(input_source)
        return df

    def compute_metrics(self, df: pd.DataFrame) -> Dict[str, object]:
        metrics: Dict[str, object] = {}
        if "latency" in df.columns:
            metrics["mean_latency"] = float(df["latency"].mean())
        else:
            metrics["mean_latency"] = None

        if "availability" in df.columns:
            metrics["mean_availability"] = float(df["availability"].mean())
        else:
            metrics["mean_availability"] = None

        metrics["n_samples"] = int(len(df))
        return metrics

    def export_report(self, metrics: Dict[str, object], outdir: str) -> Dict[str, str]:
        os.makedirs(outdir, exist_ok=True)
        summary_txt = os.path.join(outdir, "toy_summary.txt")
        with open(summary_txt, "w") as fh:
            for k, v in metrics.items():
                fh.write(f"{k}: {v}\n")
        return {"summary": summary_txt}


def get_plugin() -> ToyPlugin:
    return ToyPlugin()
