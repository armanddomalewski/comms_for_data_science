"""The look: cold Nolan blacks, Bronze Age metals, Aegean water, film grain."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Neutrals used by every chart. Deep, cold, film-stock black -- never pure #000.
INK = {
    "background": "#0B0E12",  # figure black, slightly blue
    "panel": "#11161C",  # plot area, one step lighter
    "grid": "#1E262F",
    "bone": "#DED7C8",  # primary text
    "ash": "#7C8794",  # secondary text
}

# Categorical palettes. The first color is the "hero" series.
PALETTES = {
    "ithaca": ["#C8752A", "#4E7C94", "#6E8F7C", "#98A3AE", "#8E5A3B", "#D9B26A"],
    "aegean": ["#4E7C94", "#7FA9B8", "#2F5464", "#A8C4CC", "#3E6E6B", "#95B3A6"],
    "underworld": ["#9AA0A6", "#DED7C8", "#5C646D", "#B0654A", "#3F464E", "#7E6A57"],
}

# Diverging ramp for correlations: Aegean blue <- black -> bronze.
CMAP_TIDE = LinearSegmentedColormap.from_list(
    "odyssey_tide", ["#6FA3B8", "#33566A", "#11161C", "#8E5A3B", "#D98E3A"]
)

# Set by use_theme(), read by the chart functions.
_STATE = {"palette": "ithaca", "grain": True}


def palette(name="ithaca"):
    """Return the list of hex colors for a named palette."""
    if name not in PALETTES:
        raise ValueError(f"unknown palette {name!r}; try one of {list(PALETTES)}")
    return list(PALETTES[name])


def current_palette():
    """Colors of the palette currently in use."""
    return palette(_STATE["palette"])


def use_theme(name="ithaca", grain=True):
    """Apply the Odyssey style to matplotlib. Call once, before plotting.

    name  -- categorical palette: "ithaca", "aegean", or "underworld".
    grain -- overlay faint 70mm film grain on each figure.
    """
    colors = palette(name)
    _STATE.update(palette=name, grain=grain)
    mpl.rcParams.update(
        {
            "figure.facecolor": INK["background"],
            "figure.figsize": (9, 5.0625),  # 16:9, the projection ratio
            "figure.dpi": 120,
            "savefig.facecolor": INK["background"],
            "savefig.bbox": "tight",
            "axes.facecolor": INK["panel"],
            "axes.edgecolor": INK["grid"],
            "axes.labelcolor": INK["ash"],
            "axes.labelsize": 8,
            "axes.titlesize": 13,
            "axes.titlecolor": INK["bone"],
            "axes.grid": True,
            "axes.axisbelow": True,
            "axes.prop_cycle": mpl.cycler(color=colors),
            "grid.color": INK["grid"],
            "grid.linewidth": 0.6,
            "text.color": INK["bone"],
            "xtick.color": INK["ash"],
            "ytick.color": INK["ash"],
            "xtick.labelsize": 8,
            "ytick.labelsize": 8,
            "legend.frameon": False,
            "legend.fontsize": 8,
            "lines.linewidth": 1.8,
            "font.size": 9,
        }
    )
    return name


def save(ax, path, dpi=200):
    """Write the chart holding `ax` to disk at presentation resolution."""
    ax.figure.savefig(path, dpi=dpi, facecolor=INK["background"])
    return path


def _new_axes(ax):
    """The axes to draw on, making a figure if the caller passed none."""
    return ax if ax is not None else plt.subplots()[1]


def _label(text):
    """Column name to axis label: budget_musd -> BUDGET MUSD."""
    return str(text).replace("_", " ").upper()


def _legend(ax):
    """Legend in the house style, with markers at a readable fixed size."""
    legend = ax.legend(loc="best", labelcolor=INK["ash"])
    for handle in legend.legend_handles:
        if hasattr(handle, "set_sizes"):
            handle.set_sizes([40])
    return legend


def _finish(ax, title=None, subtitle=None, xlabel=None, ylabel=None):
    """Apply the shared frame: open spines, uppercase title, grain. Returns ax."""
    for side in ("top", "right"):
        ax.spines[side].set_visible(False)
    ax.tick_params(length=3, width=0.6)

    if xlabel:
        ax.set_xlabel(_label(xlabel), labelpad=8)
    if ylabel:
        ax.set_ylabel(_label(ylabel), labelpad=8)
    if title:
        # Thin spaces between letters: title-card typography.
        ax.set_title(" ".join(title.upper()), loc="left",
                     pad=26 if subtitle else 14)
    if subtitle:
        ax.text(0, 1.02, subtitle, transform=ax.transAxes, fontsize=8.5,
                color=INK["ash"], va="bottom")

    if _STATE["grain"]:
        _add_grain(ax.figure)
    return ax


def _add_grain(fig, amount=0.05, seed=70):
    """Lay a single faint noise field over the whole figure. Once per figure."""
    if getattr(fig, "_odyssey_grain", False):
        return
    noise = np.random.default_rng(seed).random((360, 640))
    layer = fig.add_axes([0, 0, 1, 1], zorder=1000)
    layer.imshow(noise, cmap="gray", alpha=amount, aspect="auto")
    layer.set_axis_off()
    layer.patch.set_alpha(0)
    fig._odyssey_grain = True
