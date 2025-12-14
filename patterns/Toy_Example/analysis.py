"""Runnable analysis for the Toy Example using the Toy plugin.

This runner uses the Toy ETL to normalize inputs, the Toy plugin to
compute metrics, the reporting utilities to export CSV/JSON/plots and the
LocalTemplateExplainer to produce a textual explanation. It also assembles
a small frontend payload.

Usage:
    python patterns/Toy_Example/analysis.py --input patterns/Toy_Example/sample.csv --outdir patterns/Toy_Example/out
"""
import argparse
import os
import json
from archspaces.plugin_api import PluginRegistry
from archspaces.plugins.toy import ToyPlugin
from patterns.Toy_Example.etl import normalize
from archspaces import reporting
from archspaces.llm_explainers import LocalTemplateExplainer
from archspaces.frontend_adapter import assemble_payload


def run(input_path: str, outdir: str) -> None:
    os.makedirs(outdir, exist_ok=True)

    # Normalize input with lightweight ETL
    df = normalize(input_path)

    # Use plugin directly on DataFrame
    plugin = ToyPlugin()
    metrics = plugin.compute_metrics(df)

    # Export standard reports
    csv_path = os.path.join(outdir, "metrics.csv")
    json_path = os.path.join(outdir, "metrics.json")
    reporting.save_metrics_csv(metrics, csv_path)
    reporting.save_metrics_json(metrics, json_path)

    artifacts = {"metrics_csv": csv_path, "metrics_json": json_path}

    # If latency series exists, produce a histogram
    if "latency" in df.columns:
        hist_path = os.path.join(outdir, "latency_hist.png")
        reporting.plot_metric_histogram("latency", df["latency"].tolist(), hist_path)
        artifacts["latency_hist"] = hist_path

    # Produce a lightweight explanation via LocalTemplateExplainer
    explainer = LocalTemplateExplainer()
    explanation = explainer.explain(metrics)
    explain_path = os.path.join(outdir, "explanation.json")
    with open(explain_path, "w") as fh:
        json.dump(explanation, fh, indent=2)
    artifacts["explanation"] = explain_path

    # Assemble frontend payload and write it
    payload = assemble_payload(metrics, charts=[{"name": "latency_hist", "path": artifacts.get("latency_hist")}])
    payload_path = os.path.join(outdir, "frontend_payload.json")
    with open(payload_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    artifacts["frontend_payload"] = payload_path

    # Also call plugin.export_report for backward compatibility artifacts
    artifacts.update(plugin.export_report(metrics, outdir))

    print("Artifacts:", artifacts)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="patterns/Toy_Example/out")
    args = parser.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    run(args.input, args.outdir)


if __name__ == "__main__":
    main()
