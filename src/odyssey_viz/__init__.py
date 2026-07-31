"""odyssey-viz: five matplotlib charts in one dark, Bronze Age house style.

    import odyssey_viz as ov

    df = ov.sample_box_office()
    ov.use_theme()
    ax = ov.bars(df, x="title", y="worldwide_musd", title="Worldwide gross")
    ov.save(ax, "gross.png")
"""

from .core import bars, heatmap, histogram, line, scatter
from .data import sample_box_office
from .palettes import palette
from .theme import current_palette, save, use_theme

__version__ = "0.2.0"

__all__ = [
    "bars",
    "line",
    "scatter",
    "histogram",
    "heatmap",
    "use_theme",
    "palette",
    "current_palette",
    "save",
    "sample_box_office",
    "__version__",
]
