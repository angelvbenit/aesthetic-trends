# Aesthetic Trends Intelligence Dashboard

## Project Overview
This project is an automated, end-to-end Business Intelligence solution designed to track, classify, and visualize the lifecycle of 74 distinct "Aesthetics" and micro-trends using Google Search volume data. 

Built for retail, fashion, and marketing strategy, this pipeline replaces expensive agency trend reports by programmatically identifying which cultural aesthetics are emerging, which are highly profitable "goldmines," and which are statistically dead.

## Tech Stack & Architecture
* **Data Engineering (Python):** `pandas`, `pytrends`, `numpy`
* **Pipeline Automation:** Exponential backoff scripts to bypass API rate limiting.
* **Data Visualization (Power BI):** Cross-filtering Matrix visuals, Top N dynamic filtering, and custom UI/UX design via transparent layered containers.

---

## Exact Findings & Strategic Insights

Based on the 2025-2026 data window, the algorithm analyzed 74 active micro-trends and yielded the following macro-market insights:

### 1. High Market Volatility & Inventory Risk
The data proves the aesthetic trend cycle is rapidly accelerating. Out of the 74 aesthetics tracked, over **35% (26 trends) are classified as statistically "Dead"**. Brands holding physical inventory tied to aesthetics like *Tumblr Aesthetic*, *Coastal Granddaughter*, or *Apocalypse Chic* face severe markdown risks, as these trends currently occupy the "Saturated/Dead" quadrant of the matrix.

### 2. The "Goldmine" Opportunities
The Macro Opportunity Matrix successfully identified a specific cluster of trends possessing both high baseline search volume and strong positive momentum. The primary targets for immediate product development and marketing spend are:
* **Clean Girl Aesthetic**
* **Frutiger Aero**
* **Old Money Aesthetic**
* **Dark Academia**

### 3. The "Social Media vs. Search Intent" Discrepancy
The model identified **20 Emerging** trends and **12 Rising** trends. Crucially, the data revealed a massive discrepancy between "TikTok virality" and actual consumer search intent. Several aesthetics manually categorized by human assumption as "Currently Exploding" (e.g., *Tomato Girl Summer*) failed the objective mathematical threshold for high search volume. This indicates that while a trend may generate impressions on social media algorithms, it does not necessarily translate to the active consumer search behavior required to drive retail sales.

---

## Methodology & Lifecycle Logic

The Python backend classifies trends into 6 distinct stages based on a trailing 52-week vs. previous 52-week mathematical comparison:
1. **Emerging:** Low absolute volume, but extreme growth (>50% YoY).
2. **Rising:** Consistent, steady growth (>15% YoY) but not at peak.
3. **Peaking:** Current 8-week volume is within 80% of its all-time historical high.
4. **Declining:** Past its peak, with negative growth (<-20% YoY).
5. **Stable:** Moderate volume with flat growth patterns.
6. **Dead:** Consistently flatlined near a score of 0-5 with zero recent growth.

---

## Analytical Limitations
* **Proxy Data Limitations:** The project analyzes Google Search intent as a proxy for Pinterest mood-board behavior. Search indicates "intent to buy/learn," which generally lags behind initial social media visual discovery.
* **Relative Scaling Index:** Google Trends standardizes data on a 0-100 scale per batch, obfuscating absolute search query volumes. Therefore, the matrix measures *relative momentum* against peer trends, not exact market cap.
* **Short-Term Viral Noise:** Despite utilizing a 4-week moving average to smooth the data, micro-trends are highly susceptible to short-term spikes driven by single viral weekends, which can occasionally result in a false-positive "Emerging" flag.

---

## How to Run the Pipeline Locally

**1. Clone the repository:**
```bash
git clone [https://github.com/angelvbenit/aesthetic-trends.git](https://github.com/angelvbenit/aesthetic-trends.git)
cd pinterest-trends
```
**2. Set up the virtual environment & install dependencies:**

```bash
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```
**3. Run the Data Engine:**
Note: This script includes automatic delays to prevent IP bans from the Google API.

```bash
python run_pipeline.py
```
***4. View the Dashboard:***
Open outputs/dashboard.pbix in Power BI Desktop and click Refresh to load the newly generated datasets into the front-end layout.
