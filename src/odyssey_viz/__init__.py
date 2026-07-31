"""odyssey-viz: five matplotlib charts in one dark, Bronze Age house style.

    import odyssey_viz as ov

    df = ov.sample_voyage()
    ov.use_theme()
    ax = ov.bars(df, x="stop", y="days", title="Time lost by landfall")
    ov.save(ax, "days.png")
"""

from .core import bars, heatmap, histogram, line, scatter
from .data import sample_voyage
from .palettes import palette
from .theme import current_palette, save, use_theme

__version__ = "0.1.0"

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
    "sample_voyage",
    "__version__",
]
