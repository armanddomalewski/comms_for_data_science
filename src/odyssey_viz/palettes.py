"""Colors for the library: cold Nolan blacks, Bronze Age metals, Aegean water."""

from matplotlib.colors import LinearSegmentedColormap

# Neutrals used by every chart. Deep, cold, film-stock black -- never pure #000.
INK = {
    "background": "#0B0E12",  # figure black, slightly blue
    "panel": "#11161C",  # plot area, one step lighter
    "grid": "#1E262F",
    "bone": "#DED7C8",  # primary text
    "ash": "#7C8794",  # secondary text
    "bronze": "#C8752A",  # accent for single-series charts
}

# Categorical palettes. Order matters: the first color is the "hero" series.
PALETTES = {
    # Default. Warm bronze against cold sea metal.
    "ithaca": ["#C8752A", "#4E7C94", "#6E8F7C", "#98A3AE", "#8E5A3B", "#D9B26A"],
    # Sea and sky. Good for anything that reads as water, distance, or time.
    "aegean": ["#4E7C94", "#7FA9B8", "#2F5464", "#A8C4CC", "#3E6E6B", "#95B3A6"],
    # Bone, ash, and rust. For grim subjects.
    "underworld": ["#9AA0A6", "#DED7C8", "#5C646D", "#B0654A", "#3F464E", "#7E6A57"],
}

DEFAULT_PALETTE = "ithaca"

# Sequential ramp: night water -> bronze -> bone.
CMAP_BRONZE = LinearSegmentedColormap.from_list(
    "odyssey_bronze", ["#0B0E12", "#2B4250", "#8E5A3B", "#C8752A", "#EBD9B8"]
)

# Diverging ramp for correlations: Aegean blue <- black -> bronze.
CMAP_TIDE = LinearSegmentedColormap.from_list(
    "odyssey_tide", ["#6FA3B8", "#33566A", "#11161C", "#8E5A3B", "#D98E3A"]
)


def palette(name=DEFAULT_PALETTE):
    """Return the list of hex colors for a named palette.

    >>> palette("ithaca")[0]
    '#C8752A'
    """
    if name not in PALETTES:
        raise ValueError(f"unknown palette {name!r}; try one of {list(PALETTES)}")
    return list(PALETTES[name])
