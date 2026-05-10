# =============================================================================
# main.py — Entry point for Stock Market Data Analyzer
# =============================================================================
# Run:  python main.py
# =============================================================================

import sys
import os

# Ensure project root is on the path (handles running from any working dir)
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.data_fetcher    import fetch_all
from src.data_cleaner    import clean_all
from src.analyzer        import run_full_analysis
from src.visualizer      import generate_all_charts
from src.report_generator import run_reports


def main():
    print("\n" + "═" * 68)
    print("   📈  STOCK MARKET DATA ANALYZER")
    print("   Tickers : AAPL · TSLA · GOOGL · MSFT")
    print("   Period  : 2020-01-01  →  2025-01-01")
    print("═" * 68 + "\n")

    # ── Step 1: Fetch ──────────────────────────────────────────────────────────
    raw_data = fetch_all()

    if not raw_data:
        print("[ERROR] No data could be fetched or loaded. Exiting.")
        sys.exit(1)

    # ── Step 2: Clean ──────────────────────────────────────────────────────────
    clean_data = clean_all(raw_data)

    # ── Step 3: Analyse ────────────────────────────────────────────────────────
    results = run_full_analysis(clean_data)

    # ── Step 4: Visualise ──────────────────────────────────────────────────────
    generate_all_charts(results)

    # ── Step 5: Report ─────────────────────────────────────────────────────────
    run_reports(results)

    print("\n" + "═" * 68)
    print("   ✅  Analysis complete!")
    print("   📂  Charts  → outputs/charts/")
    print("   📄  Reports → reports/")
    print("   💾  Data    → data/")
    print("═" * 68 + "\n")


if __name__ == "__main__":
    main()
