"""
clean_data.py
Cleans raw trends data: normalizes, adds metadata, handles missing values.
Input:  outputs/raw_trends.csv
Output: outputs/clean_trends.csv
"""

import sys, os
import pandas as pd

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.keywords import KEYWORD_CATEGORY

RAW_FILE   = "outputs/raw_trends.csv"
OUT_FILE   = "outputs/clean_trends.csv"

df = pd.read_csv(RAW_FILE, parse_dates=["date"])
df.sort_values("date", inplace=True)

# Fill missing weeks with 0 (keyword had no search interest that week)
df.fillna(0, inplace=True)

# Melt from wide → long (tidy format — Power BI loves this)
id_vars = ["date"]
value_vars = [c for c in df.columns if c != "date"]

long_df = df.melt(id_vars=id_vars, value_vars=value_vars,
                  var_name="keyword", value_name="interest_score")

# Add category column
long_df["category"] = long_df["keyword"].map(KEYWORD_CATEGORY).fillna("Uncategorized")

# Add rolling 4-week average (smooths noise)
long_df.sort_values(["keyword", "date"], inplace=True)
long_df["interest_4w_avg"] = (
    long_df.groupby("keyword")["interest_score"]
    .transform(lambda x: x.rolling(4, min_periods=1).mean())
    .round(2)
)

long_df.to_csv(OUT_FILE, index=False)
print(f"✓ Clean data saved → {OUT_FILE}")
print(f"  Shape: {long_df.shape[0]} rows × {long_df.shape[1]} columns")
print(f"  Date range: {long_df['date'].min().date()} to {long_df['date'].max().date()}")
print(f"  Keywords: {long_df['keyword'].nunique()}")
print(f"  Categories: {long_df['category'].unique().tolist()}")