"""Bundled dataset: Christopher Nolan feature films and their box office.

The data is stored inline (a plain list of dicts) so the installed package
never has to hunt for a data file on disk. ``load_films`` turns it into a
pandas DataFrame, which is what every plotting function consumes.

Figures are rounded from public box-office sources (Box Office Mojo /
The Numbers). ``The Odyssey`` released 2026-07-17; its worldwide number is
its opening-weekend global total and is still growing, so it is flagged with
``in_release=True`` and should be read as a floor, not a final gross.
"""

from __future__ import annotations

# name, year, budget, worldwide gross, domestic opening weekend  (USD millions)
_FILMS = [
    ("Memento",               2000,   9,     40,   0.03, False),
    ("Insomnia",              2002,  46,    113,  20.9,  False),
    ("Batman Begins",         2005, 150,    375,  48.7,  False),
    ("The Prestige",          2006,  40,    110,  14.8,  False),
    ("The Dark Knight",       2008, 185,   1006, 158.4,  False),
    ("Inception",             2010, 160,    837,  62.8,  False),
    ("The Dark Knight Rises", 2012, 250,   1081, 160.9,  False),
    ("Interstellar",          2014, 165,    731,  47.5,  False),
    ("Dunkirk",               2017, 100,    527,  50.5,  False),
    ("Tenet",                 2020, 200,    365,   9.4,  False),
    ("Oppenheimer",           2023, 100,    976,  82.5,  False),
    ("The Odyssey",           2026, 250,    264, 124.5,  True),
]

#: The film the library is built to celebrate. Plotting functions highlight it.
FEATURED_FILM = "The Odyssey"


def load_films():
    """Return the bundled Nolan filmography as a pandas DataFrame.

    Columns:
        title           str    film title
        year            int    theatrical release year
        budget_musd     float  production budget, USD millions
        worldwide_musd  float  worldwide gross, USD millions
        opening_musd    float  domestic opening-weekend gross, USD millions
        in_release      bool   True if still in theaters (gross not final)
        roi             float  worldwide gross / budget (return multiple)

    Importing pandas lazily keeps ``import nolan_viz`` cheap and makes the
    dependency obvious.
    """
    import pandas as pd

    df = pd.DataFrame(
        _FILMS,
        columns=[
            "title",
            "year",
            "budget_musd",
            "worldwide_musd",
            "opening_musd",
            "in_release",
        ],
    )
    df["roi"] = df["worldwide_musd"] / df["budget_musd"]
    return df
