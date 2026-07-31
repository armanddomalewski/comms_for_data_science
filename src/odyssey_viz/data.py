"""A small built-in demo dataset so the charts have something to draw.

This is illustrative, not a source. Do not analyze it and expect to learn
anything about the poem:

  crew         follows the text -- twelve ships out of Troy, six men lost at
               Ismaros per ship, six to the Cyclops, eleven ships to the
               Laestrygonians, six to Scylla, one man onto the beach at Ithaca
  days         the long stays are textual (a month with Aeolus, a year with
               Circe, seven years on Ogygia); the short ones are approximate
  distance_nm  invented. The voyage has no agreed geography
  peril        invented. A subjective 1-10 rating
  realm        my own grouping of each stop
"""

import pandas as pd

# The ten-year voyage home, one row per landfall.
_VOYAGE = [
    # leg, stop,                 realm,        days, crew, distance_nm, peril
    (1, "Troy", "mortal", 1, 600, 0, 3),
    (2, "Ismaros", "mortal", 6, 528, 110, 6),
    (3, "Lotus-Eaters", "divine", 10, 528, 640, 4),
    (4, "Cyclops", "monster", 3, 522, 320, 9),
    (5, "Aeolus", "divine", 30, 522, 210, 5),
    (6, "Laestrygonians", "monster", 2, 46, 480, 10),
    (7, "Aiaia", "divine", 365, 44, 300, 7),
    (8, "Underworld", "underworld", 2, 44, 520, 8),
    (9, "Sirens", "monster", 1, 44, 260, 7),
    (10, "Scylla", "monster", 1, 38, 90, 10),
    (11, "Thrinacia", "divine", 31, 38, 150, 6),
    (12, "Ogygia", "divine", 2555, 1, 400, 4),
    (13, "Scheria", "mortal", 18, 1, 900, 3),
    (14, "Ithaca", "mortal", 41, 1, 320, 9),
]

_COLUMNS = ["leg", "stop", "realm", "days", "crew", "distance_nm", "peril"]


def sample_voyage():
    """Return the voyage as a DataFrame -- 14 rows, ready for every chart."""
    return pd.DataFrame(_VOYAGE, columns=_COLUMNS)
