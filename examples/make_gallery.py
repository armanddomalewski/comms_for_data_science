"""Render one PNG per chart into examples/. Run: python examples/make_gallery.py"""

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import odyssey_viz as ov

OUT = Path(__file__).parent
DPI = 140  # grain is noise and does not compress; keep the repo copies light

ov.use_theme("ithaca")
df = ov.sample_voyage()

ov.save(
    ov.bars(df, x="stop", y="days", title="Ten years, one landfall at a time",
            subtitle="Days spent at each stop between Troy and Ithaca"),
    OUT / "01_bars.png", dpi=DPI,
)

ov.save(
    ov.line(df, x="leg", y="crew", title="The crew count",
            subtitle="600 men leave Troy. One man reaches Ithaca."),
    OUT / "02_line.png", dpi=DPI,
)

ov.save(
    ov.scatter(df, x="distance_nm", y="peril", color="realm", size="days",
               title="Distance against danger",
               subtitle="Point size is time lost; color is the realm of the stop"),
    OUT / "03_scatter.png", dpi=DPI,
)

ov.save(
    ov.histogram(df, "peril", bins=6, title="How dangerous was a landfall?",
                 subtitle="Peril rating, 1-10, across all fourteen stops"),
    OUT / "04_histogram.png", dpi=DPI,
)

ov.save(
    ov.heatmap(df, title="What travels together",
               subtitle="Correlation across the numeric log"),
    OUT / "05_heatmap.png", dpi=DPI,
)

print(f"wrote 5 charts to {OUT}")
