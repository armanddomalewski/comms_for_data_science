import matplotlib

matplotlib.use("Agg")  # no display in CI or a grading container

import pytest

import odyssey_viz as ov


@pytest.fixture(autouse=True)
def theme():
    ov.use_theme("ithaca", grain=False)


@pytest.fixture
def df():
    return ov.sample_voyage()


def test_sample_voyage_shape(df):
    assert len(df) == 14
    assert df["crew"].iloc[0] == 600
    assert df["crew"].iloc[-1] == 1


def test_palette_is_six_hex_colors():
    colors = ov.palette("ithaca")
    assert len(colors) == 6
    assert all(c.startswith("#") and len(c) == 7 for c in colors)


def test_unknown_palette_raises():
    with pytest.raises(ValueError):
        ov.palette("atlantis")


def test_use_theme_sets_the_color_cycle():
    ov.use_theme("aegean", grain=False)
    assert ov.current_palette() == ov.palette("aegean")
    assert matplotlib.rcParams["axes.prop_cycle"].by_key()["color"][0] == "#4E7C94"


def test_bars_draws_one_bar_per_row(df):
    ax = ov.bars(df, x="stop", y="days")
    assert len(ax.patches) == len(df)


def test_line_with_group_makes_one_line_per_level(df):
    ax = ov.line(df, x="leg", y="peril", group="realm")
    assert len(ax.lines) == df["realm"].nunique()


def test_scatter_returns_axes_with_points(df):
    ax = ov.scatter(df, x="distance_nm", y="peril", color="realm", size="crew")
    assert len(ax.collections) == df["realm"].nunique()


def test_histogram_bin_count(df):
    ax = ov.histogram(df, "peril", bins=5)
    assert len(ax.patches) == 5


def test_heatmap_is_square_over_numeric_columns(df):
    ax = ov.heatmap(df)
    numeric = df.select_dtypes(include="number").shape[1]
    assert ax.images[0].get_array().shape == (numeric, numeric)


def test_save_writes_a_file(df, tmp_path):
    ax = ov.bars(df, x="stop", y="crew")
    path = ov.save(ax, tmp_path / "bars.png")
    assert path.exists()
