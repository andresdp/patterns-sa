"""Tests for the generic per-client column aggregator (R7, R8, R15).

Covers:
  - Happy path: aggregation against the real FL CSV produces the 8
    documented columns.
  - Generality (R15): a synthetic DataFrame with a different client count
    and field names that appear nowhere in the real FL dataset is
    correctly aggregated, proving the mechanism doesn't hardcode `5` or
    any real FL field name.
  - Edge case: a DataFrame with zero `Client <N> <field>`-shaped columns
    is a no-op.
"""

import os

import pandas as pd
import pytest

from preprocess_fl_clients import aggregate_per_client_columns

FL_CSV_PATH = os.path.join(os.path.dirname(__file__), "FLwithAP_MLdata_split.csv")

# The 8 columns this dataset's aggregation is documented to produce.
EXPECTED_FL_COLUMNS = {
    "CPU Mean",
    "RAM Mean",
    "Alpha Dirichlet Mean",
    "JSD Mean",
    "Data Distribution Diversity",
    "Data Persistence Diversity",
    "CPU Usage Avg Mean",
    "RAM Usage Avg Mean",
}


def test_happy_path_real_fl_csv_produces_documented_columns():
    """aggregate_per_client_columns on the real FL CSV yields the 8 documented columns."""
    df = pd.read_csv(FL_CSV_PATH)
    original_cols = set(df.columns)

    out = aggregate_per_client_columns(df)

    new_cols = set(out.columns) - original_cols
    # All 8 documented columns must be present (checked by name).
    assert EXPECTED_FL_COLUMNS.issubset(new_cols), (
        f"Missing expected columns: {EXPECTED_FL_COLUMNS - new_cols}"
    )
    # Original columns/data are preserved.
    assert original_cols.issubset(set(out.columns))
    pd.testing.assert_frame_equal(out[list(original_cols)], df[list(original_cols)])


def test_generality_different_client_count_and_novel_field_names():
    """Covers R15: a 3-client synthetic frame with field names absent from the real FL
    dataset is detected and aggregated correctly, proving no hardcoded client count
    or field-name list.
    """
    synthetic = pd.DataFrame({
        "Client 1 Foo": [10.0, 20.0, 30.0],
        "Client 2 Foo": [30.0, 40.0, 90.0],
        "Client 3 Foo": [50.0, 60.0, 150.0],
        "Client 1 Bar": ["a", "x", "p"],
        "Client 2 Bar": ["a", "y", "p"],
        "Client 3 Bar": ["b", "y", "p"],
        "Unrelated Column": [1, 2, 3],
    })

    out = aggregate_per_client_columns(synthetic)

    assert "Foo Mean" in out.columns
    assert "Bar Diversity" in out.columns

    expected_foo_mean = [(10.0 + 30.0 + 50.0) / 3, (20.0 + 40.0 + 60.0) / 3, (30.0 + 90.0 + 150.0) / 3]
    assert list(out["Foo Mean"]) == expected_foo_mean

    expected_bar_diversity = [2, 2, 1]  # row0: {a,a,b}=2, row1: {x,y,y}=2, row2: {p,p,p}=1
    assert list(out["Bar Diversity"]) == expected_bar_diversity

    # Original columns preserved unchanged.
    assert "Unrelated Column" in out.columns
    assert list(out["Unrelated Column"]) == [1, 2, 3]

    # No FL-specific field names leaked into this unrelated synthetic case.
    assert "CPU Mean" not in out.columns
    assert "RAM Mean" not in out.columns


def test_no_client_columns_is_noop():
    """A DataFrame shaped like a non-FL pattern (e.g. CQRS-style) with no
    `Client <N> <field>` columns is returned unchanged.
    """
    non_fl = pd.DataFrame({
        "d1Services": [0, 1, 2],
        "d2Services": [1, 1, 0],
        "lbExecTime": [12.3, 15.6, 9.8],
        "policy": ["one_device_low", "balanced_low", "high_availability"],
    })

    out = aggregate_per_client_columns(non_fl)

    pd.testing.assert_frame_equal(out, non_fl)
