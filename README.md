# 📈 Stock Market Data Analyzer

> **An enterprise-grade Python project for fetching, analyzing, visualizing, and reporting on stock market data.**  
> Built for Python · Data Analysis · FinTech · Financial Analyst · Business Analyst portfolios.

---

## 🚀 Live Demo

| Module | What it does |
|---|---|
| `python main.py` | Full CLI pipeline — fetch → clean → analyze → charts → report |
| `python dashboard.py` | Enterprise Plotly Dash interactive dashboard at `http://127.0.0.1:8050` |
| `notebooks/EDA.ipynb` | Step-by-step Jupyter notebook exploration |

---

## 📌 Problem Statement

Investors, analysts, and traders need to quickly understand:
- How a stock has performed over time
- What the risk exposure looks like
- Whether a stock is trending up or down
- How different stocks compare in terms of risk and return

This project solves that by building a **complete automated analysis pipeline** using Python and public stock data — no paid terminals required.

---

## 🏭 Industry Relevance

| Role | How this project helps |
|---|---|
| Python Developer | Modular, production-style project architecture |
| Data Analyst | Full ETL pipeline — fetch, clean, transform, visualize |
| Financial Analyst | Moving averages, RSI, Bollinger Bands, Sharpe Ratio |
| Business Analyst | KPI summaries, trend insights, executive-style reports |
| FinTech Developer | Real API usage (yfinance), dashboard (Plotly Dash) |

---

## ✨ Features

- ✅ **Real stock data** via `yfinance` (AAPL, TSLA, GOOGL, MSFT)
- ✅ **CSV fallback** if network is unavailable
- ✅ **Data cleaning** — NaN handling, deduplication, type casting
- ✅ **Technical indicators** — SMA-20/50/200, EMA-20/50, Bollinger Bands, RSI-14
- ✅ **Return analysis** — daily, cumulative, annualised returns
- ✅ **Risk analysis** — volatility, Sharpe ratio, max drawdown
- ✅ **10+ publication-quality charts** saved to `/outputs/charts/`
- ✅ **Text + CSV reports** saved to `/reports/`
- ✅ **Enterprise Plotly Dash dashboard** — 6 interactive pages
- ✅ **Jupyter notebook** for EDA
- ✅ **Windows one-click setup** via `.bat` files

---

## 🛠️ Tech Stack

| Category | Tool |
|---|---|
| Language | Python 3.10+ |
| Data Fetching | yfinance |
| Data Processing | Pandas, NumPy |
| Static Charts | Matplotlib, Seaborn |
| Interactive Charts | Plotly |
| Dashboard | Plotly Dash + Dash Bootstrap Components |
| Notebook | Jupyter |
| Environment | venv |

---

## 📂 Folder Structure

```
Stock-Market-Data-Analyzer/
│
├── data/                    # Raw + enriched CSVs (auto-created)
├── notebooks/
│   └── EDA.ipynb            # Jupyter EDA notebook
├── src/
│   ├── __init__.py
│   ├── config.py            # Central config (tickers, dates, paths)
│   ├── data_fetcher.py      # yfinance + CSV fallback
│   ├── data_cleaner.py      # Cleaning pipeline
│   ├── analyzer.py          # All financial indicators
│   ├── visualizer.py        # Matplotlib/Seaborn charts
│   └── report_generator.py  # Text + CSV reports
├── outputs/
│   └── charts/              # All saved chart PNGs
├── reports/                 # summary_report.txt + .csv
├── images/                  # Screenshots for GitHub README
├── docs/                    # Additional documentation
│
├── main.py                  # CLI entry point
├── dashboard.py             # Enterprise Dash dashboard
├── setup.bat                # Windows one-click setup
├── run_analysis.bat         # Windows: run analysis
├── run_dashboard.bat        # Windows: run dashboard
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ How to Run (Windows)

### Step 1 — Clone the repo
```bash
git clone https://github.com/YOUR_USERNAME/Stock-Market-Data-Analyzer.git
cd Stock-Market-Data-Analyzer
```

### Step 2 — One-click setup
```
Double-click setup.bat
```
This creates a virtual environment and installs all dependencies.

### Step 3 — Run the analysis
```
Double-click run_analysis.bat
```
OR from terminal:
```bash
venv\Scripts\activate
python main.py
```

### Step 4 — Launch the dashboard
```
Double-click run_dashboard.bat
```
OR:
```bash
venv\Scripts\activate
python dashboard.py
```
Then open **http://127.0.0.1:8050** in your browser.

### Step 5 — Jupyter Notebook
```bash
venv\Scripts\activate
pip install jupyter
jupyter notebook notebooks/EDA.ipynb
```

---

## 📊 Sample Output

### Terminal
```
════════════════════════════════════════════════════════════════════
   📈  STOCK MARKET DATA ANALYZER
   Tickers : AAPL · TSLA · GOOGL · MSFT
   Period  : 2020-01-01  →  2025-01-01
════════════════════════════════════════════════════════════════════

━━━ DATA FETCHING ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [Fetching] AAPL from Yahoo Finance …
  [Saved]   AAPL → data/AAPL.csv
  ...

━━━ ANALYSIS ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  [AAPL] Calculating indicators …
  ...

✅  Analysis complete!
📂  Charts  → outputs/charts/
📄  Reports → reports/
```

### Charts Generated
| File | Description |
|---|---|
| `01_all_closing_prices.png` | All 4 stocks on one chart |
| `02_moving_avg_TICKER.png` | SMA-20/50/200 per stock |
| `03_bollinger_TICKER.png` | Bollinger Bands per stock |
| `04_rsi_TICKER.png` | RSI 14-day per stock |
| `05_return_dist_TICKER.png` | Daily return histogram |
| `06_cumulative_returns.png` | 5-year cumulative return comparison |
| `07_volatility.png` | Rolling 30-day volatility |
| `08_correlation_heatmap.png` | Return correlation matrix |
| `09_volume_TICKER.png` | Daily volume per stock |

---

## 🎥 System Demo GIF

<p align="center">
  <img src="./images/Stock Market.gif" alt="System Demo GIF" width="100%">
</p>

---


## 🎓 Learning Outcomes

By building this project you will learn:
- How to use `yfinance` to fetch real stock data
- How to build a clean ETL pipeline with Pandas
- How to calculate financial indicators (SMA, EMA, RSI, Bollinger Bands)
- How to interpret risk metrics (Sharpe Ratio, Max Drawdown, Volatility)
- How to build professional charts with Matplotlib and Plotly
- How to build an enterprise-grade interactive dashboard with Plotly Dash
- How to structure a Python project for GitHub

---

## 🔖 Interview Preparation

**1. Explain your project.**  
This is a Stock Market Data Analyzer built with Python. It fetches 5 years of historical stock data for AAPL, TSLA, GOOGL, and MSFT using yfinance, cleans it with Pandas, calculates technical indicators like moving averages, RSI, Bollinger Bands, and risk metrics like Sharpe ratio and max drawdown. It produces 30+ charts and a summary report, and includes an enterprise Plotly Dash dashboard with 6 interactive analysis pages.

**2. What is a moving average and why is it useful?**  
A moving average smooths out price fluctuations over a given window (e.g. 20 days), making it easier to identify trends. A crossover of short-term and long-term MAs is often used as a buy/sell signal.

**3. What is the Sharpe Ratio?**  
Sharpe Ratio = (annualised return − risk-free rate) / annualised volatility. It measures how much return you get per unit of risk. A ratio above 1.0 is generally considered good.

**4. What is RSI?**  
Relative Strength Index (RSI) is a momentum indicator that measures the speed and magnitude of price changes. RSI > 70 indicates overbought conditions; RSI < 30 indicates oversold conditions.

**5. How did you clean the data?**  
I dropped rows with all-NaN values, forward-filled gaps caused by market holidays, removed duplicate index entries, sorted chronologically, and cast all numeric columns to float64.

**6. What is max drawdown?**  
Max drawdown is the largest peak-to-trough decline in portfolio value. It measures the worst-case loss an investor would have experienced if they bought at the peak and sold at the trough.

**7. Why yfinance instead of a paid API?**  
yfinance provides free access to Yahoo Finance's historical OHLCV data, which is sufficient for educational analysis. Paid APIs like Bloomberg provide real-time, tick-level data for professional use.

**8. How does your project scale?**  
Adding a new ticker is a one-line change in `config.py`. The modular architecture (fetcher → cleaner → analyzer → visualizer → reporter) means each component is independently maintainable.

**9. What is volatility and how did you calculate it?**  
Volatility is the standard deviation of daily returns, annualised by multiplying by √252 (trading days per year). It measures how much a stock's price fluctuates — higher volatility = higher risk.

**10. What would you add if this were a production system?**  
Real-time data streaming, a PostgreSQL database for historical storage, alerting on RSI overbought/oversold signals, a backtesting engine, and authentication for the dashboard.

---

## ⚠️ Disclaimer

> This project is developed **entirely for educational and learning purposes**.  
> It does **NOT** constitute financial advice.  
> Past performance is **not** indicative of future results.  
> Always consult a qualified financial advisor before making investment decisions.

---

## 🏷️ GitHub Tags

`python` `stock-market` `data-analysis` `pandas` `yfinance` `plotly-dash` `financial-analysis` `portfolio-project` `fintech` `matplotlib` `data-visualization` `moving-averages` `rsi` `bollinger-bands`

---

*Built with ❤️ for learning Python and Financial Analysis*
