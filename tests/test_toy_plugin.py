import os
from tools.mock_generator import generate_toy_csv
from archspaces.plugins.toy import ToyPlugin


def test_toy_plugin_end_to_end(tmp_path):
    csv_path = tmp_path / "sample.csv"
    generate_toy_csv(str(csv_path), n=10)

    plugin = ToyPlugin()
    df = plugin.parse(str(csv_path))
    metrics = plugin.compute_metrics(df)

    assert metrics.get("n_samples") == 10
    assert "mean_latency" in metrics
    assert "mean_availability" in metrics

    outdir = tmp_path / "out"
    artifacts = plugin.export_report(metrics, str(outdir))
    assert "summary" in artifacts
    assert os.path.exists(artifacts["summary"]) is True
