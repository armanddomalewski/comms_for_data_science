"""The public plotting API: five small matplotlib visualizations.

Design rules (mirroring the "one job per function" guidance):

* Every function takes an optional ``df`` (defaults to the bundled dataset)
  and returns a ``matplotlib.figure.Figure`` -- it never calls ``plt.show``
  and never saves to disk. The caller decides what to do with the figure,
  which keeps the functions easy to reuse and to test.
* ``The Odyssey`` is highlighted in every chart so the story of the library
  stays front and center.
"""

from __future__ import annotations

from .data import FEATURED_FILM, load_films

# A small, thematic palette (Aegean navy + bronze for the featured film).
_BASE = "#4a6b8a"      # muted slate-blue for the supporting films
_FEATURE = "#c8942b"   # bronze/gold for The Odyssey
_INK = "#1b2a3a"       # near-black for text and axes
_GRID = "#d6dde4"      # faint gridlines


def _bar_colors(titles):
    """Bronze for the featured film, slate-blue for everything else."""
    return [_FEATURE if t == FEATURED_FILM else _BASE for t in titles]


def _style_axes(ax):
    """Apply the shared minimalist look to an Axes."""
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    for spine in ("left", "bottom"):
        ax.spines[spine].set_color(_INK)
    ax.tick_params(colors=_INK, labelsize=9)
    ax.title.set_color(_INK)
    ax.xaxis.label.set_color(_INK)
    ax.yaxis.label.set_color(_INK)


def _resolve(df):
    return load_films() if df is None else df


def opening_weekend_bar(df=None):
    """Bar chart: domestic opening-weekend gross for every film.

    Tells the headline story -- ``The Odyssey`` set Nolan's opening record.
    """
    import matplotlib.pyplot as plt

    data = _resolve(df).sort_values("opening_musd", ascending=False)

    fig, ax = plt.subplots(figsize=(9, 5))
    bars = ax.bar(data["title"], data["opening_musd"],
                  color=_bar_colors(data["title"]))
    ax.bar_label(bars, fmt="$%.0fM", padding=3, fontsize=8, color=_INK)

    ax.set_title("Christopher Nolan films by domestic opening weekend",
                 fontsize=13, fontweight="bold")
    ax.set_ylabel("Opening weekend (USD millions)")
    ax.set_ylim(0, data["opening_musd"].max() * 1.15)
    ax.set_axisbelow(True)
    ax.yaxis.grid(True, color=_GRID)
    plt.setp(ax.get_xticklabels(), rotation=40, ha="right")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def budget_vs_gross(df=None):
    """Scatter: production budget vs. worldwide gross, with a break-even line.

    Points above the dashed line made more than they cost. Films still in
    release are drawn as hollow markers because their gross is not final.
    """
    import matplotlib.pyplot as plt

    data = _resolve(df)

    fig, ax = plt.subplots(figsize=(8, 6))

    # Break-even reference: worldwide gross == budget.
    lim = max(data["budget_musd"].max(), data["worldwide_musd"].max()) * 1.1
    ax.plot([0, lim], [0, lim], linestyle="--", color="#9aa7b4",
            linewidth=1, label="break-even (gross = budget)")

    for _, row in data.iterrows():
        featured = row["title"] == FEATURED_FILM
        ax.scatter(
            row["budget_musd"], row["worldwide_musd"],
            s=140 if featured else 80,
            color=_FEATURE if featured else _BASE,
            edgecolor=_INK,
            facecolor="none" if row["in_release"] else None,
            linewidth=1.5 if row["in_release"] else 0.5,
            zorder=3,
        )
        ax.annotate(row["title"], (row["budget_musd"], row["worldwide_musd"]),
                    xytext=(6, 4), textcoords="offset points",
                    fontsize=8, color=_INK)

    ax.set_title("Budget vs. worldwide gross",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Production budget (USD millions)")
    ax.set_ylabel("Worldwide gross (USD millions)")
    ax.set_xlim(0, lim)
    ax.set_ylim(0, lim)
    ax.set_axisbelow(True)
    ax.grid(True, color=_GRID)
    ax.legend(frameon=False, fontsize=8, loc="upper left")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def worldwide_gross_ranked(df=None):
    """Horizontal bar chart: films ranked by worldwide gross.

    ``The Odyssey`` carries a ``*`` because it is still in theaters.
    """
    import matplotlib.pyplot as plt

    data = _resolve(df).sort_values("worldwide_musd")
    labels = [f"{t} *" if r else t
              for t, r in zip(data["title"], data["in_release"])]

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(labels, data["worldwide_musd"],
                   color=_bar_colors(data["title"]))
    ax.bar_label(bars, fmt="$%.0fM", padding=3, fontsize=8, color=_INK)

    ax.set_title("Christopher Nolan films by worldwide gross",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Worldwide gross (USD millions)")
    ax.set_xlim(0, data["worldwide_musd"].max() * 1.18)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=_GRID)
    ax.text(0.99, 0.02, "* still in theaters -- gross not final",
            transform=ax.transAxes, ha="right", va="bottom",
            fontsize=7.5, color="#6b7885", style="italic")
    _style_axes(ax)
    fig.tight_layout()
    return fig


def gross_over_time(df=None):
    """Line chart: worldwide gross across Nolan's career, by release year."""
    import matplotlib.pyplot as plt

    data = _resolve(df).sort_values("year")

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.plot(data["year"], data["worldwide_musd"],
            marker="o", color=_BASE, linewidth=2, zorder=2)

    # Highlight the featured film's point.
    feat = data[data["title"] == FEATURED_FILM]
    ax.scatter(feat["year"], feat["worldwide_musd"],
               s=150, color=_FEATURE, edgecolor=_INK, zorder=3)

    for _, row in data.iterrows():
        ax.annotate(row["title"], (row["year"], row["worldwide_musd"]),
                    xytext=(0, 8), textcoords="offset points",
                    fontsize=7.5, color=_INK, ha="center")

    ax.set_title("Worldwide gross across Nolan's career",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Release year")
    ax.set_ylabel("Worldwide gross (USD millions)")
    ax.set_ylim(0, data["worldwide_musd"].max() * 1.2)
    ax.set_axisbelow(True)
    ax.grid(True, color=_GRID)
    _style_axes(ax)
    fig.tight_layout()
    return fig


def return_on_budget(df=None):
    """Horizontal bar chart: worldwide gross as a multiple of budget (ROI).

    A value of 5x means the film earned five times its production budget.
    """
    import matplotlib.pyplot as plt

    data = _resolve(df).sort_values("roi")

    fig, ax = plt.subplots(figsize=(9, 5.5))
    bars = ax.barh(data["title"], data["roi"],
                   color=_bar_colors(data["title"]))
    ax.bar_label(bars, fmt="%.1fx", padding=3, fontsize=8, color=_INK)

    ax.set_title("Return on budget (worldwide gross / budget)",
                 fontsize=13, fontweight="bold")
    ax.set_xlabel("Return multiple")
    ax.set_xlim(0, data["roi"].max() * 1.15)
    ax.set_axisbelow(True)
    ax.xaxis.grid(True, color=_GRID)
    _style_axes(ax)
    fig.tight_layout()
    return fig


def save_all(outdir="reports/figures", df=None, dpi=150):
    """Render every chart to ``outdir`` and return the list of file paths.

    A small convenience for producing all five PNGs at once.
    """
    import os

    os.makedirs(outdir, exist_ok=True)
    data = _resolve(df)

    builders = {
        "opening_weekend": opening_weekend_bar,
        "budget_vs_gross": budget_vs_gross,
        "worldwide_gross_ranked": worldwide_gross_ranked,
        "gross_over_time": gross_over_time,
        "return_on_budget": return_on_budget,
    }

    paths = []
    for name, builder in builders.items():
        fig = builder(data)
        path = os.path.join(outdir, f"{name}.png")
        fig.savefig(path, dpi=dpi, bbox_inches="tight")
        paths.append(path)
    return paths
