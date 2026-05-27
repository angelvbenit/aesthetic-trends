"""
analyze_trends.py
Classifies each aesthetic keyword into a trend lifecycle stage.
Uses last 52 weeks vs previous 52 weeks comparison + current peak proximity.

Lifecycle stages:
  Emerging  — low absolute score but growing fast (>50% YoY)
  Rising    — growing, not yet at peak
  Peaking   — currently at or near all-time high
  Declining — past peak, falling
  Dead      — consistently low, no recent growth
"""

import sys, os
import pandas as pd
import numpy as np

CLEAN_FILE  = "outputs/clean_trends.csv"
SUMMARY_OUT = "outputs/trend_summary.csv"
CATEGORY_OUT = "outputs/category_report.csv"

df = pd.read_csv(CLEAN_FILE, parse_dates=["date"])

# ── Per-keyword stats ───────────────────────────────────────────────────────
results = []

for keyword, grp in df.groupby("keyword"):
    grp = grp.sort_values("date")
    scores = grp["interest_score"].values

    if len(scores) < 8:
        continue

    all_time_max  = scores.max()
    recent_52     = scores[-52:]   if len(scores) >= 52  else scores
    prev_52       = scores[-104:-52] if len(scores) >= 104 else scores[:max(1, len(scores)//2)]
    recent_mean   = recent_52.mean()
    prev_mean     = prev_52.mean() if prev_52.mean() > 0 else 0.01
    yoy_growth    = (recent_mean - prev_mean) / prev_mean * 100
    last_8_mean   = scores[-8:].mean()
    peak_proximity = (last_8_mean / all_time_max * 100) if all_time_max > 0 else 0

    # Lifecycle classification logic
    if all_time_max < 5:
        stage = "Dead"
    elif peak_proximity >= 80:
        stage = "Peaking"
    elif yoy_growth >= 50 and recent_mean < 20:
        stage = "Emerging"
    elif yoy_growth >= 15:
        stage = "Rising"
    elif yoy_growth <= -20:
        stage = "Declining"
    else:
        stage = "Stable"

    results.append({
        "keyword":        keyword,
        "category":       grp["category"].iloc[0],
        "all_time_max":   round(float(all_time_max), 1),
        "recent_avg":     round(float(recent_mean), 1),
        "prev_avg":       round(float(prev_mean), 1),
        "yoy_growth_pct": round(float(yoy_growth), 1),
        "peak_proximity": round(float(peak_proximity), 1),
        "lifecycle_stage": stage,
    })

summary_df = pd.DataFrame(results)
summary_df.sort_values(["category", "lifecycle_stage", "recent_avg"],
                        ascending=[True, True, False], inplace=True)
summary_df.to_csv(SUMMARY_OUT, index=False)
print(f"✓ Trend summary saved → {SUMMARY_OUT}")
print(summary_df["lifecycle_stage"].value_counts().to_string())

# ── Category-level report ───────────────────────────────────────────────────
cat_df = (
    summary_df.groupby("category")
    .agg(
        avg_interest   = ("recent_avg",     "mean"),
        avg_yoy_growth = ("yoy_growth_pct", "mean"),
        peaking_count  = ("lifecycle_stage", lambda x: (x == "Peaking").sum()),
        rising_count   = ("lifecycle_stage", lambda x: (x == "Rising").sum()),
        emerging_count = ("lifecycle_stage", lambda x: (x == "Emerging").sum()),
        total_keywords = ("keyword",         "count"),
    )
    .round(2)
    .reset_index()
)
cat_df.sort_values("avg_interest", ascending=False, inplace=True)
cat_df.to_csv(CATEGORY_OUT, index=False)
print(f"\n✓ Category report saved → {CATEGORY_OUT}")
print(cat_df.to_string(index=False))