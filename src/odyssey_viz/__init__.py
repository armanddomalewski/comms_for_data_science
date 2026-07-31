"""odyssey-viz: four matplotlib charts in one dark, Bronze Age house style.

    import odyssey_viz as ov

    df = ov.sample_box_office()
    ov.use_theme()
    ax = ov.bars(df, x="title", y="worldwide_musd", title="Worldwide gross")
    ov.save(ax, "gross.png")
"""

from .core import bars, histogram, line, scatter
from .data import sample_box_office
from .theme import current_palette, palette, save, use_theme

__version__ = "0.3.2"

__all__ = [
    "bars",
    "line",
    "scatter",
    "histogram",
    "use_theme",
    "palette",
    "current_palette",
    "save",
    "sample_box_office",
    "__version__",
]
