# =============================================================================
# data_cleaner.py — Clean & validate raw stock DataFrames
# =============================================================================

import pandas as pd


def clean(df: pd.DataFrame, ticker: str = "") -> pd.DataFrame:
    """
    Perform all cleaning steps on a raw OHLCV DataFrame.

    Steps
    -----
    1. Drop rows where ALL OHLCV columns are NaN
    2. Forward-fill remaining NaN gaps (market holidays, weekends)
    3. Remove duplicate index entries
    4. Ensure chronological order
    5. Cast numeric columns to float64
    6. Add a 'Ticker' column for identification in multi-stock contexts

    Parameters
    ----------
    df     : raw DataFrame from data_fetcher
    ticker : stock symbol string (used for logging)

    Returns
    -------
    Cleaned pd.DataFrame
    """
    label = f"[{ticker}]" if ticker else ""
    original_len = len(df)

    required_cols = ["Open", "High", "Low", "Close", "Volume"]

    # ── 1. Keep only needed columns (ignore extras like Dividends, etc.) ──────
    existing = [c for c in required_cols if c in df.columns]
    df = df[existing].copy()

    # ── 2. Drop rows that are entirely NaN ────────────────────────────────────
    df.dropna(how="all", inplace=True)

    # ── 3. Forward-fill gaps (e.g. missing trading days) ─────────────────────
    df.ffill(inplace=True)
    df.bfill(inplace=True)   # Back-fill any leading NaNs at the start

    # ── 4. Remove duplicate dates ─────────────────────────────────────────────
    df = df[~df.index.duplicated(keep="first")]

    # ── 5. Sort chronologically ───────────────────────────────────────────────
    df.sort_index(inplace=True)

    # ── 6. Cast numeric columns to float ──────────────────────────────────────
    for col in ["Open", "High", "Low", "Close"]:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    if "Volume" in df.columns:
        df["Volume"] = pd.to_numeric(df["Volume"], errors="coerce").fillna(0).astype(int)

    # ── 7. Add ticker label ───────────────────────────────────────────────────
    if ticker:
        df["Ticker"] = ticker

    dropped = original_len - len(df)
    print(f"  {label} Cleaned — {len(df)} rows kept, {dropped} rows dropped.")
    return df


def clean_all(raw_data: dict) -> dict:
    """
    Clean every DataFrame in the raw_data dict.

    Parameters
    ----------
    raw_data : {ticker: DataFrame}

    Returns
    -------
    {ticker: cleaned DataFrame}
    """
    print("\n━━━ DATA CLEANING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    cleaned = {}
    for ticker, df in raw_data.items():
        cleaned[ticker] = clean(df, ticker)
    print("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")
    return cleaned
