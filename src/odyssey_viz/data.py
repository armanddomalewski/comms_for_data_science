"""A small built-in dataset so the charts have something to draw.

Every feature Christopher Nolan has directed, with budget and box office in
millions of USD.

Sourced from public box office reporting (Box Office Mojo / The Numbers
figures as repeated by trade press), compiled 2026-07-31. Read the caveats
before you draw a conclusion from it:

  - Grosses are lifetime and include re-releases, which is why Interstellar
    reads 746.6 rather than the 677.5 it finished its original run on.
  - Budgets are the reported production budget. They exclude marketing, so
    "profit" is not budget subtracted from gross.
  - `studio` is the lead domestic distributor. Two are simplifications:
    The Prestige was Touchstone domestically and Warner Bros. abroad, and
    Interstellar was Paramount domestically and Warner Bros. abroad.
  - The Odyssey is still in theaters. Its row is a snapshot taken after two
    weekends of release and will be stale almost immediately.

Verify against a primary source before citing any of these numbers.
"""

import pandas as pd

_FILMS = [
    # title,                  year, studio,         runtime, budget, domestic, worldwide
    ("Following", 1998, "Zeitgeist", 69, 0.006, 0.05, 0.13),
    ("Memento", 2000, "Newmarket", 113, 9.0, 25.5, 39.7),
    ("Insomnia", 2002, "Warner Bros.", 118, 46.0, 67.4, 113.7),
    ("Batman Begins", 2005, "Warner Bros.", 140, 150.0, 206.9, 373.4),
    ("The Prestige", 2006, "Touchstone", 130, 40.0, 53.1, 109.7),
    ("The Dark Knight", 2008, "Warner Bros.", 152, 185.0, 535.2, 1008.0),
    ("Inception", 2010, "Warner Bros.", 148, 160.0, 292.6, 832.6),
    ("The Dark Knight Rises", 2012, "Warner Bros.", 164, 250.0, 448.1, 1081.0),
    ("Interstellar", 2014, "Paramount", 169, 165.0, 188.0, 746.6),
    ("Dunkirk", 2017, "Warner Bros.", 106, 100.0, 189.7, 549.1),
    ("Tenet", 2020, "Warner Bros.", 150, 200.0, 59.5, 366.3),
    ("Oppenheimer", 2023, "Universal", 180, 100.0, 330.1, 975.8),
    ("The Odyssey", 2026, "Universal", 172, 250.0, 289.0, 652.0),
]

_COLUMNS = [
    "title",
    "year",
    "studio",
    "runtime_min",
    "budget_musd",
    "domestic_musd",
    "worldwide_musd",
]


def sample_box_office():
    """Return the filmography as a DataFrame -- 13 rows, ready for every chart."""
    return pd.DataFrame(_FILMS, columns=_COLUMNS)
