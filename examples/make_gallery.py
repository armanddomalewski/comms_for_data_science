"""Render one PNG per chart into examples/. Run: python examples/make_gallery.py"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import odyssey_viz as ov

OUT = Path(__file__).parent
DPI = 140  # grain is noise and does not compress; keep the repo copies light

ov.use_theme("ithaca")
df = ov.sample_box_office()

ov.save(
    ov.bars(df, x="title", y="worldwide_musd", title="Two films past a billion",
            subtitle="Lifetime worldwide gross, $M. The Odyssey is still in theaters."),
    OUT / "01_bars.png", dpi=DPI,
)

# Two measures on one pair of axes, which is what group= is for.
spend = df.melt(
    id_vars="year",
    value_vars=["budget_musd", "worldwide_musd"],
    var_name="measure",
    value_name="musd",
)
spend["measure"] = spend["measure"].map(
    {"budget_musd": "budget", "worldwide_musd": "worldwide gross"}
)
ov.save(
    ov.line(spend, x="year", y="musd", group="measure",
            title="Budgets rose. Grosses rose faster.",
            subtitle="$M per film, 1998 to 2026"),
    OUT / "02_line.png", dpi=DPI,
)

ov.save(
    ov.scatter(df, x="budget_musd", y="worldwide_musd", color="studio",
               size="runtime_min", title="What the money bought",
               subtitle="Budget against worldwide gross; point size is runtime"),
    OUT / "03_scatter.png", dpi=DPI,
)

ov.save(
    ov.histogram(df, "runtime_min", bins=6, title="Nolan does not make short films",
                 subtitle="How many of his thirteen films fall in each runtime band"),
    OUT / "04_histogram.png", dpi=DPI,
)

print(f"wrote 4 charts to {OUT}")
