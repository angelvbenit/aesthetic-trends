"""
export_for_powerbi.py
Produces final clean Excel workbook with multiple sheets, ready for Power BI.
Output: outputs/powerbi_dataset.xlsx
"""

import os
import pandas as pd

files = {
    "TimeSeries":    "outputs/clean_trends.csv",
    "TrendSummary":  "outputs/trend_summary.csv",
    "CategoryReport":"outputs/category_report.csv",
}

out_path = "outputs/powerbi_dataset.xlsx"
os.makedirs("outputs", exist_ok=True)

with pd.ExcelWriter(out_path, engine="openpyxl") as writer:
    for sheet_name, path in files.items():
        if not os.path.exists(path):
            print(f"  ⚠ Missing: {path} — run previous scripts first")
            continue
        pd.read_csv(path, parse_dates=["date"] if "date" in pd.read_csv(path, nrows=0).columns else []).to_excel(
            writer, sheet_name=sheet_name, index=False
        )
        print(f"  ✓ Sheet '{sheet_name}' written from {path}")

print(f"\n✓ Power BI dataset saved → {out_path}")