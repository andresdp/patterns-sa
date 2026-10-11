import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import pandas as pd
import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from adept.analysis.visualization import show_quality_objective_space


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