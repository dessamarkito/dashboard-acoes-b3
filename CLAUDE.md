# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project

A Streamlit dashboard displaying Brazilian stock market (B3) data for three tickers — Banco do Brasil (BBAS3.SA), Itaú (ITUB4.SA), and Vale (VALE3.SA) — from 2025-01-01 onward. Data is fetched live from Yahoo Finance via `yfinance` with a 1-hour cache.

## Commands

```bash
# Install dependencies
pip install -r dashboard-acoes/requirements.txt

# Run the dashboard
streamlit run dashboard-acoes/app.py
```

## Architecture

All code lives in `dashboard-acoes/`:

- **`data.py`** — data layer. `TICKERS` dict maps display names to Yahoo Finance symbols. `get_stock_data()` downloads OHLCV data as separate DataFrames (cached 1h via `@st.cache_data`). `get_metrics()` computes current price, YTD % change, max, and min from the close DataFrame.
- **`charts.py`** — presentation layer. Four Plotly figure builders: `chart_historico` (line, daily close), `chart_performance` (base-100 normalized), `chart_candlestick` (per-ticker, selected via dropdown), `chart_volume` (grouped bar). All use `template="plotly_dark"`. Colors per ticker are defined in the `COLORS` dict.
- **`app.py`** — entry point. Assembles the Streamlit page: calls data functions, renders metric cards, then each chart in order. Ticker selection for the candlestick chart is done with `st.selectbox` keyed to `TICKERS.keys()`.

To add a new ticker, add it to `TICKERS` in `data.py` and `COLORS` in `charts.py`. No other files need changes.
