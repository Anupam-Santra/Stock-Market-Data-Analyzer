# =============================================================================
# visualizer.py — Save publication-quality charts to /outputs/charts/
# =============================================================================

import os
import matplotlib
matplotlib.use("Agg")   # non-interactive backend (safe for all Windows setups)
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import seaborn as sns
import pandas as pd
import numpy as np
from src.config import OUTPUT_DIR, CHART_DPI, CHART_FIGSIZE, TICKER_COLORS, MA_SHORT, MA_LONG, MA_200

# ── Global style ──────────────────────────────────────────────────────────────
plt.style.use("dark_background")
sns.set_context("talk")

ACCENT   = "#00D4FF"
GRID_CLR = "#1E2A3A"


def _save(fig, filename: str):
    path = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(path, dpi=CHART_DPI, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  [Chart saved] {path}")


def _fig(title: str, figsize=None):
    figsize = figsize or CHART_FIGSIZE
    fig, ax = plt.subplots(figsize=figsize, facecolor="#0A0E1A")
    ax.set_facecolor("#0D1117")
    ax.set_title(title, color="white", fontsize=14, fontweight="bold", pad=16)
    ax.tick_params(colors="white")
    ax.xaxis.label.set_color("white")
    ax.yaxis.label.set_color("white")
    for spine in ax.spines.values():
        spine.set_edgecolor(GRID_CLR)
    ax.grid(color=GRID_CLR, linewidth=0.6, linestyle="--")
    return fig, ax


# =============================================================================
# 1. Closing price — all tickers on one chart
# =============================================================================
def plot_all_closing_prices(results: dict):
    fig, ax = _fig("Closing Price History (2020 – 2025) — AAPL · TSLA · GOOGL · MSFT",
                   figsize=(16, 7))
    for ticker, df in results.items():
        if ticker.startswith("_"):
            continue
        color = TICKER_COLORS.get(ticker, ACCENT)
        ax.plot(df.index, df["Close"], label=ticker, color=color, linewidth=1.5)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%Y"))
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=11)
    _save(fig, "01_all_closing_prices.png")


# =============================================================================
# 2. Individual closing price + moving averages
# =============================================================================
def plot_moving_averages(ticker: str, df: pd.DataFrame):
    fig, ax = _fig(f"{ticker} — Close Price & Moving Averages")
    color = TICKER_COLORS.get(ticker, ACCENT)

    ax.plot(df.index, df["Close"],           color=color,    linewidth=1.4, label="Close",     alpha=0.9)
    ax.plot(df.index, df[f"SMA_{MA_SHORT}"], color="#FFD700", linewidth=1.2, label=f"SMA {MA_SHORT}")
    ax.plot(df.index, df[f"SMA_{MA_LONG}"],  color="#FF6B6B", linewidth=1.2, label=f"SMA {MA_LONG}")
    ax.plot(df.index, df[f"SMA_{MA_200}"],   color="#90EE90", linewidth=1.2, label=f"SMA {MA_200}")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=10)
    _save(fig, f"02_moving_avg_{ticker}.png")


# =============================================================================
# 3. Bollinger Bands
# =============================================================================
def plot_bollinger_bands(ticker: str, df: pd.DataFrame):
    fig, ax = _fig(f"{ticker} — Bollinger Bands (SMA-20 ± 2σ)")
    color = TICKER_COLORS.get(ticker, ACCENT)

    ax.plot(df.index, df["Close"],     color=color,    linewidth=1.4, label="Close")
    ax.plot(df.index, df["BB_Upper"],  color="#FF4B4B", linewidth=0.9, linestyle="--", label="Upper Band")
    ax.plot(df.index, df["BB_Middle"], color="#FFD700", linewidth=0.9, linestyle="--", label="SMA-20")
    ax.plot(df.index, df["BB_Lower"],  color="#4BFF91", linewidth=0.9, linestyle="--", label="Lower Band")
    ax.fill_between(df.index, df["BB_Upper"], df["BB_Lower"], alpha=0.08, color=color)

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (USD)")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=10)
    _save(fig, f"03_bollinger_{ticker}.png")


# =============================================================================
# 4. RSI
# =============================================================================
def plot_rsi(ticker: str, df: pd.DataFrame):
    fig, ax = _fig(f"{ticker} — RSI (14-day)")
    color = TICKER_COLORS.get(ticker, ACCENT)

    ax.plot(df.index, df["RSI_14"], color=color, linewidth=1.2, label="RSI 14")
    ax.axhline(70, color="#FF4B4B", linewidth=0.9, linestyle="--", label="Overbought (70)")
    ax.axhline(30, color="#4BFF91", linewidth=0.9, linestyle="--", label="Oversold (30)")
    ax.fill_between(df.index, df["RSI_14"], 70, where=(df["RSI_14"] >= 70),
                    alpha=0.15, color="#FF4B4B", interpolate=True)
    ax.fill_between(df.index, df["RSI_14"], 30, where=(df["RSI_14"] <= 30),
                    alpha=0.15, color="#4BFF91", interpolate=True)

    ax.set_ylim(0, 100)
    ax.set_xlabel("Date")
    ax.set_ylabel("RSI")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=10)
    _save(fig, f"04_rsi_{ticker}.png")


# =============================================================================
# 5. Daily Returns histogram
# =============================================================================
def plot_return_distribution(ticker: str, df: pd.DataFrame):
    fig, ax = _fig(f"{ticker} — Daily Return Distribution")
    color = TICKER_COLORS.get(ticker, ACCENT)

    returns = df["Daily_Return"].dropna()
    ax.hist(returns, bins=80, color=color, alpha=0.75, edgecolor="none")
    ax.axvline(returns.mean(),   color="#FFD700", linewidth=1.5, linestyle="--", label=f"Mean: {returns.mean():.2f}%")
    ax.axvline(returns.median(), color="#FF6B6B", linewidth=1.5, linestyle=":",  label=f"Median: {returns.median():.2f}%")

    ax.set_xlabel("Daily Return (%)")
    ax.set_ylabel("Frequency")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=10)
    _save(fig, f"05_return_dist_{ticker}.png")


# =============================================================================
# 6. Cumulative returns — all tickers
# =============================================================================
def plot_cumulative_returns(results: dict):
    fig, ax = _fig("Cumulative Return (%) — 5-Year Comparison", figsize=(16, 7))
    for ticker, df in results.items():
        if ticker.startswith("_"):
            continue
        color = TICKER_COLORS.get(ticker, ACCENT)
        ax.plot(df.index, df["Cumulative_Return"], color=color, linewidth=1.5, label=ticker)

    ax.axhline(0, color="white", linewidth=0.5, linestyle="--")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative Return (%)")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=11)
    _save(fig, "06_cumulative_returns.png")


# =============================================================================
# 7. Rolling 30-day volatility
# =============================================================================
def plot_volatility(results: dict):
    fig, ax = _fig("Rolling 30-Day Annualised Volatility (%)", figsize=(16, 7))
    for ticker, df in results.items():
        if ticker.startswith("_"):
            continue
        color = TICKER_COLORS.get(ticker, ACCENT)
        ax.plot(df.index, df["Volatility_30d"], color=color, linewidth=1.2, label=ticker, alpha=0.85)

    ax.set_xlabel("Date")
    ax.set_ylabel("Volatility (% Annualised)")
    ax.legend(facecolor="#0D1117", edgecolor=GRID_CLR, labelcolor="white", fontsize=11)
    _save(fig, "07_volatility.png")


# =============================================================================
# 8. Correlation heatmap
# =============================================================================
def plot_correlation_heatmap(results: dict):
    closes = pd.DataFrame(
        {t: df["Close"] for t, df in results.items() if not t.startswith("_")}
    )
    corr = closes.pct_change().corr()

    fig, ax = plt.subplots(figsize=(7, 5), facecolor="#0A0E1A")
    ax.set_facecolor("#0D1117")
    ax.set_title("Return Correlation Heatmap", color="white", fontsize=14, fontweight="bold", pad=14)

    sns.heatmap(
        corr, annot=True, fmt=".2f", cmap="coolwarm",
        linewidths=0.5, linecolor=GRID_CLR,
        ax=ax, annot_kws={"size": 12, "color": "white"},
        cbar_kws={"shrink": 0.8}
    )
    ax.tick_params(colors="white")
    _save(fig, "08_correlation_heatmap.png")


# =============================================================================
# 9. Volume bar chart (individual)
# =============================================================================
def plot_volume(ticker: str, df: pd.DataFrame):
    fig, ax = _fig(f"{ticker} — Trading Volume", figsize=(16, 5))
    color = TICKER_COLORS.get(ticker, ACCENT)

    ax.bar(df.index, df["Volume"], color=color, alpha=0.5, width=1.5)
    ax.set_xlabel("Date")
    ax.set_ylabel("Volume")
    _save(fig, f"09_volume_{ticker}.png")


# =============================================================================
# Master runner
# =============================================================================
def generate_all_charts(results: dict):
    print("\n━━━ GENERATING CHARTS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    plot_all_closing_prices(results)
    plot_cumulative_returns(results)
    plot_volatility(results)
    plot_correlation_heatmap(results)

    for ticker, df in results.items():
        if ticker.startswith("_"):
            continue
        plot_moving_averages(ticker, df)
        plot_bollinger_bands(ticker, df)
        plot_rsi(ticker, df)
        plot_return_distribution(ticker, df)
        plot_volume(ticker, df)

    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
