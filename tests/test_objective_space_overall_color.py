import sys
from pathlib import Path
from types import SimpleNamespace

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adept.analysis.visualization import show_quality_objective_space
from adept.core.coordinator import ArchSpaceCore
from adept.core.session import PatternAnalysis


@pytest.mark.parametrize(
    ("overall_color", "expected"),
    [("gray", "gray"), ("steelblue", "steelblue")],
)
def test_objective_space_overall_color_is_applied(overall_color, expected):
    outcomes = pd.DataFrame({"x": [1.0, 2.0], "y": [3.0, 4.0]})

    fig = show_quality_objective_space(
        outcomes,
        "x",
        "y",
        schemes=[],
        show_overall=True,
        color_points=False,
        overall_color=overall_color,
    )

    try:
        collection = fig.axes[0].collections[0]
        actual = matplotlib.colors.to_rgba(collection.get_facecolors()[0])
        assert actual[:3] == matplotlib.colors.to_rgba(expected)[:3]
        assert actual[3] == pytest.approx(0.6)
    finally:
        plt.close(fig)


def test_objective_space_generic_category_color_order_and_labels():
    outcomes = pd.DataFrame({"x": [1.0, 2.0, 3.0], "y": [3.0, 2.0, 1.0]})
    groups = pd.Series([25, 50, 75], name="stress")
    palette = {"Low": "green", "Medium": "orange", "High": "red"}

    fig = show_quality_objective_space(
        outcomes,
        "x",
        "y",
        schemes=[],
        hue_series=groups,
        hue_order=[25, 50, 75],
        hue_labels={25: "Low", 50: "Medium", 75: "High"},
        hue_palette=palette,
        hue_legend_title="Stress level",
    )
    try:
        legend = fig.axes[0].get_legend()
        assert legend.get_title().get_text() == "Stress level"
        assert [text.get_text() for text in legend.get_texts()] == ["Low", "Medium", "High"]
        handles, labels = fig.axes[0].get_legend_handles_labels()
        assert labels == ["Low", "Medium", "High"]
        expected_colors = ["green", "orange", "red"]
        for handle, color in zip(handles, expected_colors):
            assert matplotlib.colors.to_rgba(handle.get_color()) == pytest.approx(matplotlib.colors.to_rgba(color))
    finally:
        plt.close(fig)


def test_objective_space_category_legend_column_count_is_configurable():
    outcomes = pd.DataFrame({"x": [1, 2, 3, 4, 5], "y": [5, 4, 3, 2, 1]})
    groups = pd.Series([0, 25, 50, 75, 100], name="stress")

    fig = show_quality_objective_space(
        outcomes,
        "x",
        "y",
        schemes=[],
        hue_series=groups,
        hue_order=[0, 25, 50, 75, 100],
        hue_legend_ncol=1,
    )
    try:
        legend_columns = fig.axes[0].get_legend()._legend_box.get_children()[-1].get_children()
        assert len(legend_columns) == 1
    finally:
        plt.close(fig)


def test_session_generic_color_feature_tracks_requested_partition():
    session = PatternAnalysis.__new__(PatternAnalysis)
    session.experiments_df = pd.DataFrame({"group": ["a", "b", "c", "d"]})
    session.outcomes_df = pd.DataFrame({"x": [1, 2, 3, 4], "y": [4, 3, 2, 1]})
    session.discrete_df = pd.DataFrame(index=range(4))
    session.schemes = [SimpleNamespace(objective_name="unused", bins=[])]
    session.train_indices = [0, 2]
    session.test_indices = [1, 3]
    session.coordinator = ArchSpaceCore()

    fig = session.show_quality_objective_space(
        "x",
        "y",
        color_by="group",
        color_order=["d", "b"],
        color_labels={"d": "D", "b": "B"},
        color_palette={"D": "purple", "B": "gold"},
        color_legend_title="Selected rows",
        subset="test",
    )
    try:
        legend = fig.axes[0].get_legend()
        assert legend.get_title().get_text() == "Selected rows"
        assert [text.get_text() for text in legend.get_texts()] == ["D", "B"]
    finally:
        plt.close(fig)


def test_session_generic_color_rejects_missing_or_conflicting_grouping():
    session = PatternAnalysis.__new__(PatternAnalysis)
    session.experiments_df = pd.DataFrame({"group": ["a"]})
    session.outcomes_df = pd.DataFrame({"x": [1], "y": [2]})
    session.discrete_df = pd.DataFrame(index=range(1))
    session.schemes = []
    session.train_indices = None
    session.test_indices = None
    session.coordinator = object()

    with pytest.raises(ValueError, match="not found"):
        session.show_quality_objective_space("x", "y", color_by="missing")
    with pytest.raises(ValueError, match="cannot be combined"):
        session.show_quality_objective_space("x", "y", color_by="group", highlight_policies=["a"])
