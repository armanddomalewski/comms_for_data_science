"""nolan_viz -- tiny matplotlib visualizations of Christopher Nolan's box office.

This file is what makes ``src/nolan_viz`` an importable package. It also sets
the public API: the names below are everything a user is meant to call.

    >>> import nolan_viz as nv
    >>> fig = nv.opening_weekend_bar()   # returns a matplotlib Figure
    >>> fig.savefig("opening.png")
"""

from .core import (
    load_films,
    opening_weekend_bar,
    budget_vs_gross,
    gross_over_time,
    return_on_budget,
)

__all__ = [
    "load_films",
    "opening_weekend_bar",
    "budget_vs_gross",
    "gross_over_time",
    "return_on_budget",
]

__version__ = "0.1.0"
