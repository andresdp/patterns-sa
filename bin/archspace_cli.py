#!/usr/bin/env python3
"""Minimal CLI to run a registered plugin on an input CSV and export reports."""
import argparse
import os
from archspaces.plugin_api import PluginRegistry
from archspaces.plugins.toy import ToyPlugin


def main():
    parser = argparse.ArgumentParser(description="Run ArchSpace plugin on input data")
    parser.add_argument("--plugin", default="toy", help="Plugin name to run")
    parser.add_argument("--input", required=True, help="Input CSV path")
    parser.add_argument("--outdir", default="out", help="Output directory for artifacts")
    args = parser.parse_args()

    reg = PluginRegistry()
    # register known plugins here
    reg.register(ToyPlugin())

    plugin = reg.get(args.plugin)
    if plugin is None:
        raise SystemExit(f"Unknown plugin: {args.plugin}. Available: {reg.list()}")

    os.makedirs(args.outdir, exist_ok=True)
    df = plugin.parse(args.input)
    metrics = plugin.compute_metrics(df)
    artifacts = plugin.export_report(metrics, args.outdir)
    print("Exported artifacts:")
    for k, v in artifacts.items():
        print(f" - {k}: {v}")


if __name__ == "__main__":
    main()
