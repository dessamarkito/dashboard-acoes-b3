import yfinance as yf
import pandas as pd
import streamlit as st

TICKERS = {
    "Banco do Brasil": "BBAS3.SA",
    "Itaú": "ITUB4.SA",
    "Vale": "VALE3.SA",
}

START_DATE = "2025-01-01"


@st.cache_data(ttl=3600)
def get_stock_data():
    tickers = list(TICKERS.values())
    raw = yf.download(tickers, start=START_DATE, auto_adjust=True)

    close = raw["Close"].copy()
    open_ = raw["Open"].copy()
    high = raw["High"].copy()
    low = raw["Low"].copy()
    volume = raw["Volume"].copy()

    close.index = pd.to_datetime(close.index)
    return close, open_, high, low, volume


def get_metrics(close: pd.DataFrame):
    metrics = {}
    for name, ticker in TICKERS.items():
        col = close[ticker].dropna()
        if col.empty:
            continue
        price_now = col.iloc[-1]
        price_start = col.iloc[0]
        perf = ((price_now - price_start) / price_start) * 100
        metrics[name] = {
            "ticker": ticker,
            "preco_atual": price_now,
            "variacao_pct": perf,
            "maxima": col.max(),
            "minima": col.min(),
        }
    return metrics
