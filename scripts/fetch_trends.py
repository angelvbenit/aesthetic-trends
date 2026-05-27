"""
fetch_trends.py
Pulls 5-year weekly interest data from Google Trends for all keywords.
Includes exponential backoff for rate limiting.
"""

import sys
import os
import time
import pandas as pd
from pytrends.request import TrendReq

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from data.keywords import ALL_KEYWORDS

# ── Config ─────────────────────────────────────────────────────────────────
TIMEFRAME  = "today 5-y"   
GEO        = ""            
BATCH_SIZE = 5             
SLEEP_SEC  = 10            # Increased to 10 seconds to avoid IP bans
OUTPUT_DIR = "outputs"
OUTPUT_FILE = os.path.join(OUTPUT_DIR, "raw_trends.csv")

# ── Init ────────────────────────────────────────────────────────────────────
os.makedirs(OUTPUT_DIR, exist_ok=True)
# Disguise the request as a standard Chrome browser
requests_args = {
    'headers': {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'
    }
}
pytrends = TrendReq(hl="en-US", tz=360, timeout=(10, 25), requests_args=requests_args)

# ── Fetch in batches with retries ───────────────────────────────────────────
def fetch_batch(keywords: list, retries=3) -> pd.DataFrame:
    for attempt in range(retries):
        try:
            pytrends.build_payload(keywords, timeframe=TIMEFRAME, geo=GEO)
            df = pytrends.interest_over_time()
            if df.empty:
                return pd.DataFrame()
            return df.drop(columns=["isPartial"], errors="ignore")
        except Exception as e:
            if "429" in str(e):
                wait = 60 * (attempt + 1)
                print(f"    ⚠ Rate limited (429). Pausing for {wait} seconds...")
                time.sleep(wait)
            else:
                print(f"    ✗ Error: {e}")
                break
    return pd.DataFrame()

all_frames = []
batches = [ALL_KEYWORDS[i:i+BATCH_SIZE] for i in range(0, len(ALL_KEYWORDS), BATCH_SIZE)]

print(f"Fetching {len(ALL_KEYWORDS)} keywords in {len(batches)} batches...\n")

for idx, batch in enumerate(batches):
    print(f"  Batch {idx+1}/{len(batches)}: {batch}")
    df = fetch_batch(batch)
    if not df.empty:
        all_frames.append(df)
    else:
        print(f"    ⚠ Empty/failed result for batch {idx+1}")
    time.sleep(SLEEP_SEC)

# ── Merge all batches ───────────────────────────────────────────────────────
if not all_frames:
    print("No data fetched. Check your internet connection or IP status.")
    sys.exit(1)

combined = pd.concat(all_frames, axis=1)
combined = combined.loc[:, ~combined.columns.duplicated()]  
combined.index.name = "date"
combined.reset_index(inplace=True)

combined.to_csv(OUTPUT_FILE, index=False)
print(f"\n✓ Saved {combined.shape[0]} weeks × {combined.shape[1]-1} keywords → {OUTPUT_FILE}")