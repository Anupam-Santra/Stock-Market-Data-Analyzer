# =============================================================================
# data_fetcher.py — Fetch & cache stock data using yfinance
# Multiple fetch strategies with automatic CSV fallback
# =============================================================================

import os
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
from src.config import TICKERS, START_DATE, END_DATE, DATA_DIR


def _flatten_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Flatten MultiIndex columns produced by newer yfinance versions."""
    if isinstance(df.columns, pd.MultiIndex):
        # e.g. ('Close', 'AAPL') → 'Close'
        df.columns = df.columns.get_level_values(0)
    return df


def _try_yf_download(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Strategy 1: yf.download() — works on most systems."""
    import yfinance as yf
    df = yf.download(ticker, start=start, end=end, progress=False,
                     auto_adjust=True, threads=False)
    df = _flatten_columns(df)
    return df


def _try_yf_ticker_history(ticker: str, start: str, end: str) -> pd.DataFrame:
    """Strategy 2: yf.Ticker().history() — more resilient to API changes."""
    import yfinance as yf
    t = yf.Ticker(ticker)
    df = t.history(start=start, end=end, auto_adjust=True)
    df = _flatten_columns(df)
    # history() adds Dividends & Stock Splits — drop them
    df = df[[c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]]
    return df


def fetch_stock_data(ticker: str, start: str = START_DATE, end: str = END_DATE) -> pd.DataFrame:
    """
    Download historical OHLCV data for a single ticker.

    Tries two yfinance strategies first, then falls back to a
    pre-bundled CSV in /data/ (included with this project).

    Parameters
    ----------
    ticker : str   e.g. "AAPL"
    start  : str   "YYYY-MM-DD"
    end    : str   "YYYY-MM-DD"

    Returns
    -------
    pd.DataFrame with columns: Open, High, Low, Close, Volume
    """
    csv_path = os.path.join(DATA_DIR, f"{ticker}.csv")

    # ── Strategy 1: yf.download() ────────────────────────────────────────────
    try:
        print(f"  [Fetching] {ticker} via yf.download() …")
        df = _try_yf_download(ticker, start, end)
        if not df.empty and len(df) > 10:
            df.index = pd.to_datetime(df.index)
            df.to_csv(csv_path)
            print(f"  [Saved]    {ticker} → {csv_path}  ({len(df)} rows)")
            return df
    except Exception as e:
        print(f"  [Info]     yf.download() failed: {type(e).__name__}")

    # ── Strategy 2: yf.Ticker().history() ────────────────────────────────────
    try:
        print(f"  [Fetching] {ticker} via Ticker.history() …")
        df = _try_yf_ticker_history(ticker, start, end)
        if not df.empty and len(df) > 10:
            df.index = pd.to_datetime(df.index)
            df.to_csv(csv_path)
            print(f"  [Saved]    {ticker} → {csv_path}  ({len(df)} rows)")
            return df
    except Exception as e:
        print(f"  [Info]     Ticker.history() failed: {type(e).__name__}")

    # ── Strategy 3: Load from bundled/cached CSV ──────────────────────────────
    if os.path.exists(csv_path):
        print(f"  [Fallback] Loading {ticker} from bundled CSV …")
        df = pd.read_csv(csv_path, index_col=0, parse_dates=True)
        # Keep only OHLCV columns
        ohlcv = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in df.columns]
        df = df[ohlcv]
        print(f"  [Loaded]   {ticker}  ({len(df)} rows from CSV)")
        return df

    raise FileNotFoundError(
        f"No data available for {ticker}.\n"
        f"  • Check your internet connection, OR\n"
        f"  • Place a '{ticker}.csv' file in the /data/ folder.\n"
        f"    CSV must have columns: Date, Open, High, Low, Close, Volume"
    )


def fetch_all(tickers: list = TICKERS) -> dict:
    """
    Fetch data for every ticker and return a dict  {{ticker: DataFrame}}.
    """
    all_data = {}
    print("\n" + "━" * 64)
    print("  DATA FETCHING")
    print("━" * 64)
    for ticker in tickers:
        try:
            all_data[ticker] = fetch_stock_data(ticker)
        except FileNotFoundError as err:
            print(f"  [SKIPPED] {err}")
    print("━" * 64 + "\n")
    return all_data
