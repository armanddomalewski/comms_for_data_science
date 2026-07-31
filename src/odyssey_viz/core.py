"""The four charts. Each takes a pandas DataFrame and returns a matplotlib Axes."""

import pandas as pd
from matplotlib.ticker import MaxNLocator

from .theme import INK, _finish, _legend, _new_axes, current_palette


def bars(df, x, y, title=None, subtitle=None, sort=True, ax=None):
    """Ranked horizontal bars -- one bar per row, longest at the top.

    df    -- DataFrame
    x     -- column of labels
    y     -- column of numbers
    sort  -- order bars by value instead of row order
    """
    data = df[[x, y]].dropna()
    if sort:
        data = data.sort_values(y)

    colors = current_palette()
    ax = _new_axes(ax)
    bar = ax.barh(
        data[x].astype(str),
        data[y],
        height=0.62,
        color=colors[0],
        edgecolor=INK["background"],
        linewidth=0.8,
    )
    # The top-ranked bar carries the story; cool the rest of them down.
    for patch in bar[:-1]:
        patch.set_alpha(0.72)

    ax.xaxis.grid(True)
    ax.yaxis.grid(False)
    ax.margins(x=0.08)
    return _finish(ax, title, subtitle, xlabel=y, ylabel=None)


def line(df, x, y, group=None, title=None, subtitle=None, ax=None):
    """A line over an ordered column -- time, distance, book number.

    group -- optional column; draws one labelled line per category
    """
    colors = current_palette()
    ax = _new_axes(ax)

    if group is None:
        data = df[[x, y]].dropna().sort_values(x)
        ax.plot(data[x], data[y], color=colors[0], marker="o", markersize=3.5)
        ax.fill_between(data[x], data[y], data[y].min(), color=colors[0], alpha=0.10)
    else:
        for i, (name, part) in enumerate(df.groupby(group, sort=False)):
            part = part[[x, y]].dropna().sort_values(x)
            ax.plot(part[x], part[y], color=colors[i % len(colors)], label=str(name),
                    marker="o", markersize=3.5)
        _legend(ax)

    ax.margins(x=0.02)
    return _finish(ax, title, subtitle, xlabel=x, ylabel=y)


def scatter(df, x, y, color=None, size=None, title=None, subtitle=None, ax=None):
    """Two numeric columns as points.

    color -- optional categorical column, one color per level
    size  -- optional numeric column, scaled to point area
    """
    used = [c for c in (x, y, color, size) if c is not None]
    df = df.dropna(subset=used)
    colors = current_palette()
    ax = _new_axes(ax)

    area = pd.Series(45.0, index=df.index)
    if size is not None:
        s = df[size].astype(float)
        span = s.max() - s.min()
        area = 25 + 260 * ((s - s.min()) / span if span else 0.5)

    if color is None:
        ax.scatter(df[x], df[y], s=area, color=colors[0], alpha=0.85,
                   edgecolor=INK["background"], linewidth=0.7)
    else:
        for i, (name, part) in enumerate(df.groupby(color, sort=False)):
            ax.scatter(part[x], part[y], s=area.loc[part.index], label=str(name),
                       color=colors[i % len(colors)], alpha=0.85,
                       edgecolor=INK["background"], linewidth=0.7)
        _legend(ax)

    return _finish(ax, title, subtitle, xlabel=x, ylabel=y)


def histogram(df, column, bins=12, title=None, subtitle=None, ax=None):
    """Distribution of one numeric column, with the mean marked."""
    values = df[column].dropna().astype(float)
    colors = current_palette()
    ax = _new_axes(ax)

    ax.hist(values, bins=bins, color=colors[0], alpha=0.85,
            edgecolor=INK["background"], linewidth=0.9)
    ax.axvline(values.mean(), color=INK["bone"], linewidth=1.0, linestyle=(0, (4, 3)))
    ax.text(values.mean(), ax.get_ylim()[1], f"  mean {values.mean():.1f}",
            color=INK["bone"], fontsize=8, va="top")

    # Counts are whole things; never offer the reader half a row.
    ax.yaxis.set_major_locator(MaxNLocator(integer=True))
    ax.xaxis.grid(False)
    return _finish(ax, title, subtitle, xlabel=column, ylabel="count")
