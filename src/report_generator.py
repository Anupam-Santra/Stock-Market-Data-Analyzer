# =============================================================================
# report_generator.py — Generate text + CSV summary reports
# =============================================================================

import os
import datetime
import pandas as pd
from src.config import REPORT_DIR, START_DATE, END_DATE


def _divider(char="━", width=70):
    return char * width


def generate_text_report(results: dict) -> str:
    """
    Build and save a human-readable .txt summary report.
    """
    summary: pd.DataFrame = results.get("_summary")
    if summary is None:
        print("  [Warning] No summary data found. Skipping text report.")
        return ""

    lines = []
    now   = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    lines += [
        _divider("═"),
        "   STOCK MARKET DATA ANALYZER — SUMMARY REPORT",
        f"   Generated : {now}",
        f"   Period    : {START_DATE}  →  {END_DATE}",
        f"   Stocks    : {', '.join(summary.index.tolist())}",
        _divider("═"),
        "",
    ]

    for ticker in summary.index:
        row = summary.loc[ticker]
        lines += [
            _divider(),
            f"  {ticker}",
            _divider(),
            f"  Start Price       : ${row['Start Price ($)']:>10,.2f}",
            f"  End Price         : ${row['End Price ($)']:>10,.2f}",
            f"  Total Return      : {row['Total Return (%)']:>+10.2f} %",
            f"  Annualised Return : {row['Ann. Return (%)']:>+10.2f} %",
            f"  Volatility (Ann.) : {row['Volatility (%)']:>10.2f} %",
            f"  Sharpe Ratio      : {row['Sharpe Ratio']:>10.2f}",
            f"  Max Drawdown      : {row['Max Drawdown (%)']:>+10.2f} %",
            f"  Highest Price     : ${row['Highest Price ($)']:>10,.2f}",
            f"  Lowest Price      : ${row['Lowest Price ($)']:>10,.2f}",
            f"  Avg Daily Volume  : {int(row['Avg Volume']):>15,}",
            "",
        ]

    # ── Best & worst performers ───────────────────────────────────────────────
    best   = summary["Total Return (%)"].idxmax()
    worst  = summary["Total Return (%)"].idxmin()
    stable = summary["Volatility (%)"].idxmin()

    lines += [
        _divider("═"),
        "  INSIGHTS",
        _divider("═"),
        f"  🏆 Best 5-Year Return  : {best}  ({summary.loc[best, 'Total Return (%)']:+.2f}%)",
        f"  📉 Worst 5-Year Return : {worst} ({summary.loc[worst, 'Total Return (%)']:+.2f}%)",
        f"  🛡️  Lowest Volatility  : {stable} ({summary.loc[stable, 'Volatility (%)']:.2f}%)",
        "",
        _divider("─"),
        "  ⚠️  DISCLAIMER",
        "  This report is generated for EDUCATIONAL PURPOSES ONLY.",
        "  It does NOT constitute financial advice.",
        "  Past performance is not indicative of future results.",
        _divider("─"),
    ]

    report_text = "\n".join(lines)

    path = os.path.join(REPORT_DIR, "summary_report.txt")
    with open(path, "w", encoding="utf-8") as f:
        f.write(report_text)
    print(f"  [Report saved] {path}")

    return report_text


def generate_csv_report(results: dict):
    """
    Save the summary DataFrame as a CSV file.
    """
    summary: pd.DataFrame = results.get("_summary")
    if summary is None:
        return

    path = os.path.join(REPORT_DIR, "summary_report.csv")
    summary.to_csv(path)
    print(f"  [CSV saved]    {path}")


def save_enriched_csvs(results: dict):
    """
    Save the full enriched DataFrame (with all indicators) for each ticker.
    """
    from src.config import DATA_DIR
    for ticker, df in results.items():
        if ticker.startswith("_"):
            continue
        path = os.path.join(DATA_DIR, f"{ticker}_enriched.csv")
        df.to_csv(path)
        print(f"  [Enriched CSV] {path}")


def run_reports(results: dict):
    print("\n━━━ GENERATING REPORTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    text = generate_text_report(results)
    generate_csv_report(results)
    save_enriched_csvs(results)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    print(text)
