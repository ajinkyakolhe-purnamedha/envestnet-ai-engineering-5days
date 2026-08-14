"""Reading and processing data.

Run:
    uv run --project ../CODE-ALONGS \
        python m0/data_csv.py

pandas for thousands of rows.
"""

import pandas as pd

prices = pd.read_csv("data/prices.csv")

# Filter, group, aggregate. Three chained operations
# replace the nested loop you'd write elsewhere.
summary = (
    prices[prices["date"] >= "2020-03-01"]
    .groupby("symbol")["close"]
    .agg(["count", "mean", "max"])
    .sort_values("mean", ascending=False)
)

print(summary)

# Billions of rows? Change the import, keep the logic:
#   import polars as pl
#   prices = pl.scan_csv("data/prices.csv")
