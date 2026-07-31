"""The look: dark IMAX frame, thin rules, uppercase titles, optional film grain."""

import matplotlib as mpl
import matplotlib.pyplot as plt
import numpy as np

from .palettes import DEFAULT_PALETTE, INK, palette

# Module state, set by use_theme() and read by the chart functions.
_STATE = {"palette": DEFAULT_PALETTE, "grain": True}


def use_theme(name=DEFAULT_PALETTE, grain=True):
    """Apply the Odyssey style to matplotlib. Call once, before plotting.

    name  -- categorical palette: "ithaca", "aegean", or "underworld".
    grain -- overlay faint 70mm film grain on each figure.
    """
    colors = palette(name)
    _STATE["palette"] = name
    _STATE["grain"] = grain

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
            "xtick.direction": "out",
            "ytick.direction": "out",
            "legend.frameon": False,
            "legend.fontsize": 8,
            "lines.linewidth": 1.8,
            "lines.solid_capstyle": "round",
            "font.family": "sans-serif",
            "font.size": 9,
        }
    )
    return name


def current_palette():
    """Colors of the palette currently in use."""
    return palette(_STATE["palette"])


def _new_axes(ax, figsize=None):
    """Return the axes to draw on, making a figure if the caller passed none."""
    if ax is not None:
        return ax
    return plt.subplots(figsize=figsize)[1]


def _spaced(text):
    """Wide letter-spacing, faked with thin spaces. Title-card typography."""
    return " ".join(text.upper())


def _label(text):
    """Column name to axis label: distance_nm -> DISTANCE NM."""
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
    for side in ("left", "bottom"):
        ax.spines[side].set_linewidth(0.8)

    ax.tick_params(length=3, width=0.6)
    if xlabel:
        ax.set_xlabel(_label(xlabel), labelpad=8, color=INK["ash"])
    if ylabel:
        ax.set_ylabel(_label(ylabel), labelpad=8, color=INK["ash"])

    if title:
        ax.set_title(
            _spaced(title),
            loc="left",
            pad=26 if subtitle else 14,
            color=INK["bone"],
        )
    if subtitle:
        ax.text(
            0,
            1.02,
            subtitle,
            transform=ax.transAxes,
            fontsize=8.5,
            color=INK["ash"],
            va="bottom",
        )

    if _STATE["grain"]:
        _add_grain(ax.figure)
    return ax


def _add_grain(fig, amount=0.05, seed=70):
    """Lay a single faint noise field over the whole figure. Once per figure."""
    if getattr(fig, "_odyssey_grain", False):
        return
    rng = np.random.default_rng(seed)
    noise = rng.random((360, 640))
    layer = fig.add_axes([0, 0, 1, 1], zorder=1000)
    layer.imshow(noise, cmap="gray", alpha=amount, aspect="auto", interpolation="nearest")
    layer.set_axis_off()
    layer.set_navigate(False)
    layer.patch.set_alpha(0)
    fig._odyssey_grain = True


def save(ax, path, dpi=200):
    """Write the chart holding `ax` to disk at presentation resolution."""
    ax.figure.savefig(path, dpi=dpi, facecolor=INK["background"])
    return path
