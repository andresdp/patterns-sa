"""Example usage of the ArchSpace plugin system.

This module demonstrates programmatic usage patterns for the core pieces we
added: the Toy plugin, ETL normalizer, reporting utilities and the local
explainer. Keep this file as a minimal, importable example for developers.

Example (in Python):

    from archspaces.example_archspace import run_toy_example
    run_toy_example("patterns/Toy_Example/sample.csv", "patterns/Toy_Example/out")

"""
from typing import Optional
import os
from archspaces.plugins.toy import ToyPlugin
from patterns.Toy_Example.etl import normalize
from archspaces import reporting
from archspaces.llm_explainers import LocalTemplateExplainer
from archspaces.frontend_adapter import assemble_payload


def run_toy_example(input_path: str, outdir: str, normalize_input: bool = True) -> dict:
    """Run the Toy example pipeline programmatically and return artifact paths.

    Args:
        input_path: path to raw CSV (or normalized CSV)
        outdir: directory to write artifacts
        normalize_input: if True, run the pandas ETL normalizer first

    Returns:
        A dict mapping artifact names to file paths.
    """
    os.makedirs(outdir, exist_ok=True)

    if normalize_input:
        df = normalize(input_path)
    else:
        # plugin.parse expects a CSV path; write df to a temp path if needed
        df = None

    plugin = ToyPlugin()
    # If we have a DataFrame already, compute metrics directly
    if df is not None:
        metrics = plugin.compute_metrics(df)
    else:
        df2 = plugin.parse(input_path)
        metrics = plugin.compute_metrics(df2)

    # Export CSV and JSON
    csv_path = os.path.join(outdir, "metrics.csv")
    json_path = os.path.join(outdir, "metrics.json")
    reporting.save_metrics_csv(metrics, csv_path)
    reporting.save_metrics_json(metrics, json_path)

    artifacts = {"metrics_csv": csv_path, "metrics_json": json_path}

    # Optional histogram
    if df is not None and "latency" in df.columns:
        hist_path = os.path.join(outdir, "latency_hist.png")
        reporting.plot_metric_histogram("latency", df["latency"].tolist(), hist_path)
        artifacts["latency_hist"] = hist_path

    # Explanation
    explainer = LocalTemplateExplainer()
    explanation = explainer.explain(metrics)
    explain_path = os.path.join(outdir, "explanation.json")
    import json
    with open(explain_path, "w") as fh:
        json.dump(explanation, fh, indent=2)
    artifacts["explanation"] = explain_path

    # Frontend payload
    payload = assemble_payload(metrics, charts=[{"name": "latency_hist", "path": artifacts.get("latency_hist")}])
    payload_path = os.path.join(outdir, "frontend_payload.json")
    with open(payload_path, "w") as fh:
        json.dump(payload, fh, indent=2)
    artifacts["frontend_payload"] = payload_path

    # Backwards-compatible report from plugin
    artifacts.update(plugin.export_report(metrics, outdir))

    return artifacts


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", required=True)
    parser.add_argument("--outdir", default="patterns/Toy_Example/out")
    args = parser.parse_args()
    art = run_toy_example(args.input, args.outdir)
    print("Artifacts:", art)