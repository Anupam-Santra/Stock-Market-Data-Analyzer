# =============================================================================
# analyzer.py — Financial calculations for each stock
# =============================================================================

import numpy as np
import pandas as pd
from src.config import MA_SHORT, MA_LONG, MA_200


def add_moving_averages(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add SMA-20, SMA-50, SMA-200 and EMA-20, EMA-50 columns.
    """
    df = df.copy()
    df[f"SMA_{MA_SHORT}"]  = df["Close"].rolling(window=MA_SHORT).mean()
    df[f"SMA_{MA_LONG}"]   = df["Close"].rolling(window=MA_LONG).mean()
    df[f"SMA_{MA_200}"]    = df["Close"].rolling(window=MA_200).mean()
    df[f"EMA_{MA_SHORT}"]  = df["Close"].ewm(span=MA_SHORT, adjust=False).mean()
    df[f"EMA_{MA_LONG}"]   = df["Close"].ewm(span=MA_LONG, adjust=False).mean()
    return df


def add_daily_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add percentage daily return column.
    """
    df = df.copy()
    df["Daily_Return"] = df["Close"].pct_change() * 100   # in %
    return df


def add_cumulative_returns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Add cumulative return from the start of the series.
    """
    df = df.copy()
    # pct_change gives fractional change; cumprod gives growth factor
    df["Cumulative_Return"] = (1 + df["Close"].pct_change()).cumprod() - 1
    df["Cumulative_Return"] *= 100   # in %
    return df


def add_volatility(df: pd.DataFrame, window: int = 30) -> pd.DataFrame:
    """
    Add rolling 30-day annualised volatility (standard deviation of returns).
    """
    df = df.copy()
    daily_ret = df["Close"].pct_change()
    df["Volatility_30d"] = daily_ret.rolling(window=window).std() * np.sqrt(252) * 100
    return df


def add_bollinger_bands(df: pd.DataFrame, window: int = 20) -> pd.DataFrame:
    """
    Add Bollinger Bands: middle band (SMA-20), upper & lower bands.
    """
    df = df.copy()
    rolling_mean = df["Close"].rolling(window=window).mean()
    rolling_std  = df["Close"].rolling(window=window).std()
    df["BB_Middle"] = rolling_mean
    df["BB_Upper"]  = rolling_mean + 2 * rolling_std
    df["BB_Lower"]  = rolling_mean - 2 * rolling_std
    return df


def add_rsi(df: pd.DataFrame, window: int = 14) -> pd.DataFrame:
    """
    Add 14-day Relative Strength Index (RSI).
    RSI > 70 → overbought, RSI < 30 → oversold.
    """
    df = df.copy()
    delta = df["Close"].diff()
    gain  = delta.clip(lower=0)
    loss  = -delta.clip(upper=0)
    avg_gain = gain.ewm(com=window - 1, adjust=False).mean()
    avg_loss = loss.ewm(com=window - 1, adjust=False).mean()
    rs  = avg_gain / avg_loss
    df["RSI_14"] = 100 - (100 / (1 + rs))
    return df


def compute_summary(df: pd.DataFrame, ticker: str) -> dict:
    """
    Compute a one-row risk/return summary for a ticker.

    Returns a dict suitable for building a summary DataFrame.
    """
    close = df["Close"].dropna()
    daily_ret = close.pct_change().dropna()

    total_return   = ((close.iloc[-1] / close.iloc[0]) - 1) * 100
    annualised_ret = ((1 + total_return / 100) ** (1 / 5) - 1) * 100   # 5-year horizon
    volatility     = daily_ret.std() * np.sqrt(252) * 100
    sharpe_ratio   = (daily_ret.mean() * 252) / (daily_ret.std() * np.sqrt(252)) if daily_ret.std() != 0 else 0

    # Max drawdown
    rolling_max = close.cummax()
    drawdown     = (close - rolling_max) / rolling_max
    max_drawdown = drawdown.min() * 100

    return {
        "Ticker":             ticker,
        "Start Price ($)":    round(float(close.iloc[0]), 2),
        "End Price ($)":      round(float(close.iloc[-1]), 2),
        "Total Return (%)":   round(total_return, 2),
        "Ann. Return (%)":    round(annualised_ret, 2),
        "Volatility (%)":     round(volatility, 2),
        "Sharpe Ratio":       round(sharpe_ratio, 2),
        "Max Drawdown (%)":   round(max_drawdown, 2),
        "Highest Price ($)":  round(float(close.max()), 2),
        "Lowest Price ($)":   round(float(close.min()), 2),
        "Avg Volume":         int(df["Volume"].mean()),
    }


def run_full_analysis(clean_data: dict) -> dict:
    """
    Apply all indicators to every ticker.

    Returns
    -------
    {
        ticker: enriched DataFrame,
        ...
        "_summary": summary DataFrame with one row per ticker
    }
    """
    print("\n━━━ ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    results  = {}
    summaries = []

    for ticker, df in clean_data.items():
        print(f"  [{ticker}] Calculating indicators …")
        df = add_moving_averages(df)
        df = add_daily_returns(df)
        df = add_cumulative_returns(df)
        df = add_volatility(df)
        df = add_bollinger_bands(df)
        df = add_rsi(df)
        results[ticker]  = df
        summaries.append(compute_summary(df, ticker))

    results["_summary"] = pd.DataFrame(summaries).set_index("Ticker")
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    return results
