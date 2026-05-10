# 🎯 Interview Preparation — Stock Market Data Analyzer

---

## ❓ Q1: Explain your project.

**HR Answer:**
"I built a Stock Market Data Analyzer — a Python-based tool that automatically collects, cleans, analyzes, and visualizes 5 years of real stock market data for Apple, Tesla, Google, and Microsoft. It includes an interactive enterprise-grade dashboard where you can explore price trends, risk metrics, and compare stocks side by side. The goal was to simulate how a financial analyst or data analyst would approach investment research using open data."

**Technical Answer:**
"The project has a modular architecture: a data fetcher using yfinance with a CSV fallback, a cleaning pipeline built with Pandas, an analyzer that computes SMA-20/50/200, EMA, Bollinger Bands, RSI-14, daily/cumulative returns, volatility, Sharpe ratio, and max drawdown. The visualizer generates 30+ charts with Matplotlib and Seaborn. The enterprise dashboard is built with Plotly Dash and has 6 pages — Overview, Price & MA, Indicators, Returns, All Stocks comparison, and Risk Matrix. All outputs are saved as CSVs, PNGs, and a text report."

---

## ❓ Q2: What is a moving average and why is it useful?

**Answer:**
A moving average smooths out short-term price fluctuations by averaging prices over a fixed window. The 20-day SMA shows short-term trend, the 50-day shows medium-term, and the 200-day shows long-term direction. A 'golden cross' — where the 50-day crosses above the 200-day — is a classic bullish signal. I implemented both SMA (Simple Moving Average) and EMA (Exponential Moving Average, which weights recent prices more heavily) in my analyzer.

---

## ❓ Q3: What is the Sharpe Ratio?

**Answer:**
The Sharpe Ratio measures risk-adjusted return. The formula is:
```
Sharpe = (Annualised Return − Risk-Free Rate) / Annualised Volatility
```
In my project I simplified it by using 0 as the risk-free rate since I'm comparing relative performance. A Sharpe Ratio above 1.0 is generally good, above 2.0 is excellent. It tells you how much return you earn per unit of risk taken.

---

## ❓ Q4: What is RSI and how did you use it?

**Answer:**
RSI (Relative Strength Index) is a momentum oscillator that ranges from 0 to 100. I used a 14-day window, which is the industry standard. RSI above 70 signals overbought — the stock may be due for a correction. RSI below 30 signals oversold — potential buying opportunity. I calculated it using the exponential moving average of gains vs losses. In the dashboard I highlighted overbought and oversold zones with color fills.

---

## ❓ Q5: How did you clean the data?

**Answer:**
My cleaning pipeline in `data_cleaner.py` does the following:
1. Drops rows where all OHLCV values are NaN
2. Forward-fills gaps caused by market holidays or weekends
3. Back-fills any leading NaN values at the start
4. Removes duplicate index entries
5. Sorts the index chronologically
6. Casts all price columns to float64 and volume to int
7. Adds a Ticker label column for multi-stock contexts

---

## ❓ Q6: What is Max Drawdown?

**Answer:**
Max Drawdown measures the largest peak-to-trough decline in price over the period. I calculate it as:
```python
rolling_max = close.cummax()
drawdown = (close - rolling_max) / rolling_max
max_drawdown = drawdown.min() * 100
```
For example, if TSLA fell from $400 to $100, the max drawdown would be -75%. It's one of the most important risk metrics for investors because it shows the worst-case scenario they could have experienced.

---

## ❓ Q7: Why did you use yfinance?

**Answer:**
yfinance provides free access to Yahoo Finance's historical OHLCV data, adjusted for splits and dividends. It's widely used in academic and personal projects. Since I'm a student without access to Bloomberg or Refinitiv, yfinance was the ideal choice. I also built a CSV fallback mechanism so the project works even without internet — it loads from a previously downloaded CSV file stored in the `/data/` folder.

---

## ❓ Q8: What is Bollinger Bands?

**Answer:**
Bollinger Bands consist of a middle band (SMA-20) and upper/lower bands at ±2 standard deviations from it. They adapt to volatility — the bands widen when volatility is high and narrow when it's low. When price touches the upper band, it may be overbought; when it touches the lower band, it may be oversold. I calculated them in Pandas and visualized them with a fill between the upper and lower bands.

---

## ❓ Q9: How is your project structured / how does it scale?

**Answer:**
The project follows a clean modular architecture:
- `config.py` — all settings in one place. Adding a new ticker is a single line change.
- `data_fetcher.py` — handles data acquisition (network + CSV fallback)
- `data_cleaner.py` — handles all data quality
- `analyzer.py` — all financial calculations
- `visualizer.py` — all chart generation
- `report_generator.py` — all output files
- `main.py` — orchestrates the pipeline
- `dashboard.py` — separate interactive layer

To add a new ticker, you only change `TICKERS` in `config.py` and add a color in `TICKER_COLORS`. Everything else runs automatically.

---

## ❓ Q10: What would you add if this were a production system?

**Answer:**
Several things:
1. **Real-time data** via a WebSocket connection to a market data provider
2. **Database layer** — PostgreSQL for historical storage and Redis for caching
3. **Alert system** — email/Slack notification when RSI crosses 70 or 30
4. **Backtesting engine** — simulate trading strategies on historical data
5. **Authentication** on the dashboard
6. **Automated scheduling** — run daily analysis using Airflow or cron
7. **CI/CD pipeline** on GitHub Actions with automated tests
8. **Docker containerization** for easy deployment

---

*Remember: When explaining the project, always start with the business problem, then the solution, then the technology. This shows business thinking, not just coding.*
