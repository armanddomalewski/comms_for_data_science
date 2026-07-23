# nolan-viz-armand

Tiny matplotlib visualizations of Christopher Nolan's box office, built around
his 2026 film **The Odyssey**.

The library ships a small dataset of Nolan's feature films (budget, worldwide
gross, opening weekend) and five plotting functions. Each function returns a
matplotlib `Figure` -- it never shows or saves on its own, so you decide what
to do with it.

## Install

```bash
pip install nolan-viz-armand
```

Or, from a local clone, in editable mode:

```bash
pip install -e .
```

## Use

```python
import nolan_viz as nv

fig = nv.opening_weekend_bar()   # The Odyssey set Nolan's opening record
fig.savefig("opening_weekend.png")

# Or grab the raw data as a pandas DataFrame:
df = nv.load_films()
print(df.head())
```

## The five visualizations

| Function | Chart |
|----------|-------|
| `opening_weekend_bar()` | Bar chart of domestic opening-weekend gross |
| `budget_vs_gross()` | Scatter of budget vs. worldwide gross, with a break-even line |
| `worldwide_gross_ranked()` | Horizontal bar ranking films by worldwide gross |
| `gross_over_time()` | Line chart of worldwide gross across Nolan's career |
| `return_on_budget()` | Horizontal bar of gross / budget (ROI multiple) |

Every chart highlights **The Odyssey** in bronze.

## Notes on the data

Figures are rounded from public box-office sources (Box Office Mojo /
The Numbers). *The Odyssey* released 2026-07-17, so its worldwide number is the
opening-weekend global total and is still growing -- read it as a floor, not a
final gross. Films still in release are flagged in the dataset and marked in
the charts.
