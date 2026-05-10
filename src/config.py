# =============================================================================
# config.py — Central Configuration for Stock Market Data Analyzer
# =============================================================================

import os

# ── Stocks to analyze ────────────────────────────────────────────────────────
TICKERS = ["AAPL", "TSLA", "GOOGL", "MSFT"]

# ── Date range (5 years: 2020 → 2025) ────────────────────────────────────────
START_DATE = "2020-01-01"
END_DATE   = "2025-01-01"

# ── Moving average windows ────────────────────────────────────────────────────
MA_SHORT = 20    # 20-day  (short-term trend)
MA_LONG  = 50    # 50-day  (medium-term trend)
MA_200   = 200   # 200-day (long-term trend)

# ── Paths ─────────────────────────────────────────────────────────────────────
# src/config.py lives inside /src/ — go one level up to reach project root
SRC_DIR  = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(SRC_DIR)          # project root

DATA_DIR    = os.path.join(BASE_DIR, "data")
OUTPUT_DIR  = os.path.join(BASE_DIR, "outputs", "charts")
REPORT_DIR  = os.path.join(BASE_DIR, "reports")

# Create directories if they don't exist
for _dir in [DATA_DIR, OUTPUT_DIR, REPORT_DIR]:
    os.makedirs(_dir, exist_ok=True)

# ── Chart style ───────────────────────────────────────────────────────────────
CHART_STYLE   = "dark_background"
CHART_DPI     = 150
CHART_FIGSIZE = (14, 6)

# ── Colors per ticker ─────────────────────────────────────────────────────────
TICKER_COLORS = {
    "AAPL":  "#00D4FF",
    "TSLA":  "#FF4B4B",
    "GOOGL": "#FFD700",
    "MSFT":  "#7FFF00",
}
