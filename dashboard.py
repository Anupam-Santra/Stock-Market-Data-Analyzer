# =============================================================================
# dashboard.py — Enterprise-grade Plotly Dash Dashboard
# =============================================================================
# Run:  python dashboard.py
# Then open: http://127.0.0.1:8050
#
# CSS is loaded automatically from /assets/dashboard.css
# (Dash serves everything in /assets/ automatically)
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import pandas as pd
import numpy as np
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc

from src.data_fetcher  import fetch_all
from src.data_cleaner  import clean_all
from src.analyzer      import run_full_analysis
from src.config        import TICKERS, TICKER_COLORS

# ─────────────────────────────────────────────────────────────────────────────
# Load data on startup
# ─────────────────────────────────────────────────────────────────────────────
print("\n[Dashboard] Loading stock data ...")
raw     = fetch_all()
clean   = clean_all(raw)
RESULTS = run_full_analysis(clean)
SUMMARY = RESULTS["_summary"]
print("[Dashboard] Data ready. Starting server ...\n")

# ─────────────────────────────────────────────────────────────────────────────
# Design tokens — used in Plotly figures only
# All page CSS lives in assets/dashboard.css (auto-loaded by Dash)
# ─────────────────────────────────────────────────────────────────────────────
BG_CARD  = "#0D1117"
BG_CARD2 = "#111827"
BORDER   = "#1E2D3D"
TEXT_PRI = "#E6EDF3"
TEXT_SEC = "#8B949E"
ACCENT   = "#00D4FF"
GREEN    = "#3FB950"
RED      = "#F85149"
YELLOW   = "#D29922"

PLOTLY_LAYOUT = dict(
    paper_bgcolor=BG_CARD,
    plot_bgcolor=BG_CARD,
    font=dict(color=TEXT_PRI, family="JetBrains Mono, monospace", size=12),
    xaxis=dict(gridcolor=BORDER, zeroline=False, showline=False),
    yaxis=dict(gridcolor=BORDER, zeroline=False, showline=False),
    legend=dict(bgcolor="rgba(0,0,0,0)", bordercolor=BORDER, borderwidth=1),
    margin=dict(l=16, r=16, t=40, b=16),
    hovermode="x unified",
)

def _fig(title="", height=400):
    fig = go.Figure()
    layout = {**PLOTLY_LAYOUT, "height": height}
    if title:
        layout["title"] = title
    fig.update_layout(**layout)
    return fig

def kpi_card(title, value, subtitle="", color=TEXT_PRI, icon=""):
    return html.Div(className="kpi-card", children=[
        html.Div((f"{icon}  " if icon else "") + title, className="kpi-label"),
        html.Div(value, className="kpi-value", style={"color": color}),
        html.Div(subtitle, className="kpi-sub"),
    ])

# ─────────────────────────────────────────────────────────────────────────────
# App — CSS auto-served from /assets/dashboard.css
# ─────────────────────────────────────────────────────────────────────────────
app = dash.Dash(
    __name__,
    external_stylesheets=[dbc.themes.CYBORG],
    title="Stock Market Analyzer",
    suppress_callback_exceptions=True,
)

app.layout = html.Div([
    # Top bar
    html.Div(className="topbar", children=[
        html.Div("◈ StockAnalyzer Pro", className="topbar-logo"),
        html.Div([
            html.Span("AAPL · TSLA · GOOGL · MSFT", className="topbar-meta"),
            html.Span("  |  ", style={"color": BORDER}),
            html.Span("2020 – 2025", className="topbar-meta"),
        ]),
        html.Div("Educational Use Only", className="topbar-badge"),
    ]),

    html.Div(className="main-wrap", children=[
        # Sidebar
        html.Div(className="sidebar", children=[
            html.Div("Analysis", className="sidebar-section"),
            html.Button("Overview",    id="nav-overview",   className="nav-btn", n_clicks=0),
            html.Button("Price & MA",  id="nav-price",      className="nav-btn", n_clicks=0),
            html.Button("Indicators",  id="nav-indicators", className="nav-btn", n_clicks=0),
            html.Button("Returns",     id="nav-returns",    className="nav-btn", n_clicks=0),
            html.Div("Comparison", className="sidebar-section"),
            html.Button("All Stocks",  id="nav-compare",   className="nav-btn", n_clicks=0),
            html.Button("Risk Matrix", id="nav-risk",       className="nav-btn", n_clicks=0),
        ]),

        # Content
        html.Div(className="content", children=[
            html.Div(className="ticker-row", children=[
                html.Div([
                    html.Label("SELECT TICKER", style={
                        "fontSize": "0.65rem", "color": TEXT_SEC,
                        "letterSpacing": "0.1em", "marginBottom": "4px", "display": "block",
                    }),
                    dcc.Dropdown(
                        id="ticker-select",
                        options=[{"label": t, "value": t} for t in TICKERS],
                        value=TICKERS[0], clearable=False,
                        style={"width": "180px", "backgroundColor": BG_CARD2,
                               "color": TEXT_PRI, "border": f"1px solid {BORDER}", "borderRadius": "6px"},
                    ),
                ]),
                html.Div([
                    html.Label("ACTIVE PAGE", style={
                        "fontSize": "0.65rem", "color": TEXT_SEC,
                        "letterSpacing": "0.1em", "marginBottom": "4px", "display": "block",
                    }),
                    html.Div(id="page-indicator", style={
                        "background": "rgba(0,212,255,0.1)", "color": ACCENT,
                        "border": f"1px solid {ACCENT}", "borderRadius": "6px",
                        "padding": "8px 18px", "fontSize": "0.78rem",
                        "letterSpacing": "0.08em", "height": "38px",
                        "display": "flex", "alignItems": "center",
                    }),
                ]),
            ]),
            html.Div(id="page-content"),
        ]),
    ]),
])

PAGES = {
    "nav-overview":   "Overview",
    "nav-price":      "Price & MA",
    "nav-indicators": "Indicators",
    "nav-returns":    "Returns",
    "nav-compare":    "All Stocks",
    "nav-risk":       "Risk Matrix",
}

@app.callback(
    Output("page-content",   "children"),
    Output("page-indicator", "children"),
    Input("nav-overview",    "n_clicks"),
    Input("nav-price",       "n_clicks"),
    Input("nav-indicators",  "n_clicks"),
    Input("nav-returns",     "n_clicks"),
    Input("nav-compare",     "n_clicks"),
    Input("nav-risk",        "n_clicks"),
    Input("ticker-select",   "value"),
)
def render_page(o, p, ind, r, c, risk, ticker):
    ctx = dash.callback_context
    page_id = "nav-overview"
    if ctx.triggered:
        fired = ctx.triggered[0]["prop_id"].split(".")[0]
        if fired != "ticker-select":
            page_id = fired
    df = RESULTS.get(ticker, pd.DataFrame())
    builders = {
        "nav-overview":   lambda: build_overview(ticker, df),
        "nav-price":      lambda: build_price_ma(ticker, df),
        "nav-indicators": lambda: build_indicators(ticker, df),
        "nav-returns":    lambda: build_returns(ticker, df),
        "nav-compare":    build_compare,
        "nav-risk":       build_risk,
    }
    return builders.get(page_id, lambda: build_overview(ticker, df))(), PAGES.get(page_id, "Overview")

# ─────────────────────────────────────────────────────────────────────────────
# Page builders
# ─────────────────────────────────────────────────────────────────────────────
def build_overview(ticker, df):
    row = SUMMARY.loc[ticker]
    ret = row["Total Return (%)"]
    color = TICKER_COLORS.get(ticker, ACCENT)

    close_fig = _fig(f"{ticker} — Closing Price", height=340)
    close_fig.add_trace(go.Scatter(x=df.index, y=df["Close"],
        line=dict(color=color, width=1.8), fill="tozeroy",
        fillcolor="rgba(0,212,255,0.05)", name="Close",
        hovertemplate="$%{y:.2f}<extra></extra>"))

    vol_fig = _fig(f"{ticker} — Daily Volume", height=220)
    vol_fig.add_trace(go.Bar(x=df.index, y=df["Volume"],
        marker_color=color, opacity=0.5, name="Volume"))

    return html.Div([
        html.Div(className="kpi-row", children=[
            kpi_card("Total Return",  f"{ret:+.1f}%",
                     f"${row['Start Price ($)']:.2f} to ${row['End Price ($)']:.2f}",
                     GREEN if ret >= 0 else RED, "▲" if ret >= 0 else "▼"),
            kpi_card("Ann. Return",   f"{row['Ann. Return (%)']:+.1f}%",  "5-year CAGR",
                     GREEN if row["Ann. Return (%)"] >= 0 else RED),
            kpi_card("Volatility",    f"{row['Volatility (%)']:.1f}%",   "Ann. std dev", YELLOW),
            kpi_card("Sharpe Ratio",  f"{row['Sharpe Ratio']:.2f}",      "Risk-adj. return",
                     GREEN if row["Sharpe Ratio"] >= 1 else YELLOW),
        ]),
        html.Div(className="kpi-row", children=[
            kpi_card("Max Drawdown",  f"{row['Max Drawdown (%)']:.1f}%", "Peak-to-trough", RED),
            kpi_card("Highest Price", f"${row['Highest Price ($)']:.2f}", "5-year high",   GREEN),
            kpi_card("Lowest Price",  f"${row['Lowest Price ($)']:.2f}", "5-year low",     RED),
            kpi_card("Avg Volume",    f"{int(row['Avg Volume']):,}",      "Daily avg",      ACCENT),
        ]),
        html.Div(className="chart-card", children=[
            html.H4(f"{ticker} — CLOSING PRICE 2020–2025"),
            dcc.Graph(figure=close_fig, config={"displayModeBar": False}),
        ]),
        html.Div(className="chart-card", children=[
            html.H4("TRADING VOLUME"),
            dcc.Graph(figure=vol_fig, config={"displayModeBar": False}),
        ]),
    ])


def build_price_ma(ticker, df):
    color = TICKER_COLORS.get(ticker, ACCENT)
    ma_fig = _fig(f"{ticker} — Price & Moving Averages", height=480)
    ma_fig.add_trace(go.Scatter(x=df.index, y=df["Close"],   name="Close",   line=dict(color=color,     width=1.8)))
    ma_fig.add_trace(go.Scatter(x=df.index, y=df["SMA_20"],  name="SMA 20",  line=dict(color="#FFD700", width=1.2, dash="dot")))
    ma_fig.add_trace(go.Scatter(x=df.index, y=df["SMA_50"],  name="SMA 50",  line=dict(color="#FF6B6B", width=1.2, dash="dot")))
    ma_fig.add_trace(go.Scatter(x=df.index, y=df["SMA_200"], name="SMA 200", line=dict(color="#90EE90", width=1.4)))
    ma_fig.add_trace(go.Scatter(x=df.index, y=df["EMA_20"],  name="EMA 20",  line=dict(color="#FF8C00", width=1.0, dash="dash")))

    bb_fig = _fig(f"{ticker} — Bollinger Bands", height=360)
    bb_fig.add_trace(go.Scatter(x=df.index, y=df["BB_Upper"], name="Upper Band",
                                line=dict(color="#FF4B4B", width=1, dash="dash")))
    bb_fig.add_trace(go.Scatter(x=df.index, y=df["BB_Lower"], name="Lower Band",
                                line=dict(color="#4BFF91", width=1, dash="dash"),
                                fill="tonexty", fillcolor="rgba(255,75,75,0.06)"))
    bb_fig.add_trace(go.Scatter(x=df.index, y=df["Close"],    name="Close",
                                line=dict(color=color, width=1.5)))
    bb_fig.add_trace(go.Scatter(x=df.index, y=df["BB_Middle"], name="SMA 20",
                                line=dict(color="#FFD700", width=1, dash="dot")))

    return html.Div([
        html.Div(className="chart-card", children=[html.H4("MOVING AVERAGES"),
            dcc.Graph(figure=ma_fig, config={"displayModeBar": False})]),
        html.Div(className="chart-card", children=[html.H4("BOLLINGER BANDS (SMA-20 ± 2σ)"),
            dcc.Graph(figure=bb_fig, config={"displayModeBar": False})]),
    ])


def build_indicators(ticker, df):
    color = TICKER_COLORS.get(ticker, ACCENT)
    rsi_fig = _fig(f"{ticker} — RSI 14", height=320)
    rsi_fig.add_trace(go.Scatter(x=df.index, y=df["RSI_14"], name="RSI 14",
                                  line=dict(color=color, width=1.4)))
    rsi_fig.add_hline(y=70, line=dict(color=RED,   width=1, dash="dash"),
                      annotation_text="Overbought (70)", annotation_font_color=RED)
    rsi_fig.add_hline(y=30, line=dict(color=GREEN, width=1, dash="dash"),
                      annotation_text="Oversold (30)",   annotation_font_color=GREEN)
    rsi_fig.add_hrect(y0=70, y1=100, fillcolor=RED,   opacity=0.04, line_width=0)
    rsi_fig.add_hrect(y0=0,  y1=30,  fillcolor=GREEN, opacity=0.04, line_width=0)
    rsi_fig.update_yaxes(range=[0, 100])

    vf = _fig(f"{ticker} — Rolling 30-Day Volatility (%)", height=300)
    vf.add_trace(go.Scatter(x=df.index, y=df["Volatility_30d"], name="Volatility",
                             line=dict(color=YELLOW, width=1.4),
                             fill="tozeroy", fillcolor="rgba(210,153,34,0.08)"))

    return html.Div([
        html.Div(className="chart-card", children=[html.H4("RSI (14-DAY)"),
            dcc.Graph(figure=rsi_fig, config={"displayModeBar": False})]),
        html.Div(className="chart-card", children=[html.H4("ANNUALISED ROLLING VOLATILITY"),
            dcc.Graph(figure=vf, config={"displayModeBar": False})]),
    ])


def build_returns(ticker, df):
    color = TICKER_COLORS.get(ticker, ACCENT)
    ret   = df["Daily_Return"].dropna()

    cum_fig = _fig(f"{ticker} — Cumulative Return (%)", height=320)
    cum_fig.add_trace(go.Scatter(x=df.index, y=df["Cumulative_Return"], name="Cum. Return",
                                  line=dict(color=color, width=1.8),
                                  fill="tozeroy", fillcolor="rgba(0,212,255,0.07)"))
    cum_fig.add_hline(y=0, line=dict(color=TEXT_SEC, width=0.7, dash="dot"))

    hist_fig = _fig(f"{ticker} — Daily Return Distribution", height=320)
    hist_fig.add_trace(go.Histogram(x=ret, nbinsx=80, marker_color=color, opacity=0.75, name="Return"))
    hist_fig.add_vline(x=ret.mean(), line=dict(color=YELLOW, width=1.5, dash="dash"),
                       annotation_text=f"Mean={ret.mean():.2f}%", annotation_font_color=YELLOW)

    stats = {
        "Mean Return": f"{ret.mean():.3f}%", "Median Return": f"{ret.median():.3f}%",
        "Std Dev": f"{ret.std():.3f}%",      "Skewness": f"{ret.skew():.3f}",
        "Kurtosis": f"{ret.kurt():.3f}",     "Best Day": f"{ret.max():.2f}%",
        "Worst Day": f"{ret.min():.2f}%",    "Positive Days": f"{(ret>0).sum()} ({(ret>0).mean()*100:.1f}%)",
    }
    rows = [html.Tr([
        html.Td(k, style={"color": TEXT_SEC, "padding": "8px 14px", "fontSize": "0.78rem"}),
        html.Td(v, style={"color": TEXT_PRI, "padding": "8px 14px", "fontWeight": "600",
                           "textAlign": "right", "fontSize": "0.82rem"}),
    ]) for k, v in stats.items()]

    return html.Div([
        html.Div(className="two-col", children=[
            html.Div(className="chart-card", children=[html.H4("CUMULATIVE RETURN"),
                dcc.Graph(figure=cum_fig, config={"displayModeBar": False})]),
            html.Div(className="chart-card", children=[html.H4("DAILY RETURN DISTRIBUTION"),
                dcc.Graph(figure=hist_fig, config={"displayModeBar": False})]),
        ]),
        html.Div(className="chart-card", children=[
            html.H4("DAILY RETURN STATISTICS"),
            html.Table(rows, style={"width": "100%", "borderCollapse": "collapse"}),
        ]),
    ])


def build_compare():
    cum_fig = _fig("Cumulative Return Comparison — All Stocks", height=380)
    norm_fig = _fig("Normalised Price (Base 100 = Jan 2020)", height=360)
    for t in TICKERS:
        df = RESULTS[t]
        c  = TICKER_COLORS[t]
        cum_fig.add_trace(go.Scatter(x=df.index, y=df["Cumulative_Return"],
                                      name=t, line=dict(color=c, width=1.8)))
        norm_fig.add_trace(go.Scatter(x=df.index, y=df["Close"]/df["Close"].iloc[0]*100,
                                       name=t, line=dict(color=c, width=1.6)))
    cum_fig.add_hline(y=0, line=dict(color=TEXT_SEC, width=0.6, dash="dot"))

    cols = ["Total Return (%)", "Ann. Return (%)", "Volatility (%)",
            "Sharpe Ratio", "Max Drawdown (%)", "Highest Price ($)", "Lowest Price ($)"]
    header = html.Tr([html.Th("Ticker")] + [html.Th(c) for c in cols])
    rows = []
    for t in TICKERS:
        r = SUMMARY.loc[t]
        cells = [html.Td(t)]
        for c in cols:
            v   = r[c]
            clr = GREEN if ("Return" in c or "Sharpe" in c) and float(v) >= 0 else RED if "Drawdown" in c else TEXT_PRI
            cells.append(html.Td(f"{v:+.2f}" if isinstance(v, float) else str(v), style={"color": clr}))
        rows.append(html.Tr(cells))

    return html.Div([
        html.Div(className="chart-card", children=[html.H4("CUMULATIVE RETURN"),
            dcc.Graph(figure=cum_fig, config={"displayModeBar": False})]),
        html.Div(className="chart-card", children=[html.H4("NORMALISED PRICE (BASE 100)"),
            dcc.Graph(figure=norm_fig, config={"displayModeBar": False})]),
        html.Div(className="chart-card", children=[
            html.H4("5-YEAR PERFORMANCE SUMMARY"),
            html.Table(className="summary-table",
                       children=[html.Thead(header), html.Tbody(rows)]),
        ]),
    ])


def build_risk():
    scatter_fig = _fig("Risk vs Return — Volatility vs Ann. Return", height=420)
    for t in TICKERS:
        r = SUMMARY.loc[t]
        scatter_fig.add_trace(go.Scatter(
            x=[r["Volatility (%)"]], y=[r["Ann. Return (%)"]],
            mode="markers+text", text=[t], textposition="top center",
            textfont=dict(color=TICKER_COLORS[t], size=13),
            marker=dict(size=22, color=TICKER_COLORS[t], line=dict(color="white", width=1.5)),
            name=t,
            hovertemplate=f"<b>{t}</b><br>Vol: %{{x:.1f}}%<br>Ret: %{{y:.1f}}%<extra></extra>",
        ))
    scatter_fig.update_layout(xaxis_title="Volatility (%)", yaxis_title="Ann. Return (%)", showlegend=False)

    closes = pd.DataFrame({t: RESULTS[t]["Close"] for t in TICKERS})
    corr   = closes.pct_change().corr().round(3)
    heat_fig = go.Figure(go.Heatmap(
        z=corr.values, x=list(corr.columns), y=list(corr.index),
        colorscale="RdBu_r", zmid=0,
        text=corr.values, texttemplate="%{text:.2f}",
        hovertemplate="Corr(%{x},%{y})=%{z:.3f}<extra></extra>",
    ))
    heat_fig.update_layout(**PLOTLY_LAYOUT, title="Return Correlation Matrix", height=380)

    dd_fig = _fig("Drawdown Over Time (%)", height=320)
    for t in TICKERS:
        df  = RESULTS[t]
        drw = (df["Close"] - df["Close"].cummax()) / df["Close"].cummax() * 100
        dd_fig.add_trace(go.Scatter(x=df.index, y=drw, name=t,
                                     line=dict(color=TICKER_COLORS[t], width=1.2)))

    return html.Div([
        html.Div(className="two-col", children=[
            html.Div(className="chart-card", children=[html.H4("RISK vs RETURN SCATTER"),
                dcc.Graph(figure=scatter_fig, config={"displayModeBar": False})]),
            html.Div(className="chart-card", children=[html.H4("CORRELATION MATRIX"),
                dcc.Graph(figure=heat_fig, config={"displayModeBar": False})]),
        ]),
        html.Div(className="chart-card", children=[html.H4("DRAWDOWN OVER TIME"),
            dcc.Graph(figure=dd_fig, config={"displayModeBar": False})]),
    ])


if __name__ == "__main__":
    app.run(debug=False, host="127.0.0.1", port=8050)
