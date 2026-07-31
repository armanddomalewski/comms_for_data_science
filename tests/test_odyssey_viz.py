import matplotlib

matplotlib.use("Agg")  # no display in CI or a grading container

import pytest

import odyssey_viz as ov


@pytest.fixture(autouse=True)
def theme():
    ov.use_theme("ithaca", grain=False)


@pytest.fixture
def df():
    return ov.sample_box_office()


def test_sample_box_office_shape(df):
    assert len(df) == 13
    assert df["title"].iloc[0] == "Following"
    assert df["title"].iloc[-1] == "The Odyssey"
    assert df["worldwide_musd"].max() > 1000  # The Dark Knight Rises


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
    ax = ov.bars(df, x="title", y="worldwide_musd")
    assert len(ax.patches) == len(df)


def test_line_with_group_makes_one_line_per_level(df):
    ax = ov.line(df, x="year", y="worldwide_musd", group="studio")
    assert len(ax.lines) == df["studio"].nunique()


def test_scatter_returns_axes_with_points(df):
    ax = ov.scatter(df, x="budget_musd", y="worldwide_musd", color="studio", size="runtime_min")
    assert len(ax.collections) == df["studio"].nunique()


def test_scatter_drops_rows_missing_a_used_column(df):
    df = df.copy()
    df.loc[df.index[-1], "worldwide_musd"] = None  # a film still in theaters
    ax = ov.scatter(df, x="budget_musd", y="worldwide_musd", size="runtime_min")
    assert ax.collections[0].get_offsets().shape[0] == len(df) - 1


def test_histogram_bin_count(df):
    ax = ov.histogram(df, "runtime_min", bins=5)
    assert len(ax.patches) == 5


def test_save_writes_a_file(df, tmp_path):
    ax = ov.bars(df, x="title", y="budget_musd")
    path = ov.save(ax, tmp_path / "bars.png")
    assert path.exists()
