import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data import TICKERS

COLORS = {
    "Banco do Brasil": "#FFD700",
    "Itaú": "#EC7000",
    "Vale": "#005CA9",
}


def chart_historico(close: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for name, ticker in TICKERS.items():
        col = close[ticker].dropna()
        fig.add_trace(go.Scatter(
            x=col.index,
            y=col.values,
            name=name,
            line=dict(color=COLORS[name], width=2),
            hovertemplate=f"<b>{name}</b><br>Data: %{{x|%d/%m/%Y}}<br>Preço: R$ %{{y:.2f}}<extra></extra>",
        ))
    fig.update_layout(
        title="Histórico de Preços — Fechamento Diário",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        template="plotly_dark",
    )
    return fig


def chart_performance(close: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for name, ticker in TICKERS.items():
        col = close[ticker].dropna()
        base = col.iloc[0]
        norm = (col / base) * 100
        fig.add_trace(go.Scatter(
            x=norm.index,
            y=norm.values,
            name=name,
            line=dict(color=COLORS[name], width=2),
            hovertemplate=f"<b>{name}</b><br>Data: %{{x|%d/%m/%Y}}<br>Base 100: %{{y:.2f}}<extra></extra>",
        ))
    fig.add_hline(y=100, line_dash="dash", line_color="gray", annotation_text="Base (01/01/2025)")
    fig.update_layout(
        title="Performance Comparada (Base 100 em 01/01/2025)",
        xaxis_title="Data",
        yaxis_title="Índice (Base 100)",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        hovermode="x unified",
        template="plotly_dark",
    )
    return fig


def chart_candlestick(open_: pd.DataFrame, high: pd.DataFrame, low: pd.DataFrame, close: pd.DataFrame, nome: str) -> go.Figure:
    ticker = TICKERS[nome]
    fig = go.Figure(data=[go.Candlestick(
        x=close.index,
        open=open_[ticker],
        high=high[ticker],
        low=low[ticker],
        close=close[ticker],
        increasing_line_color="#26A69A",
        decreasing_line_color="#EF5350",
        name=nome,
    )])
    fig.update_layout(
        title=f"Candlestick — {nome} ({ticker})",
        xaxis_title="Data",
        yaxis_title="Preço (R$)",
        xaxis_rangeslider_visible=False,
        template="plotly_dark",
    )
    return fig


def chart_volume(volume: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for name, ticker in TICKERS.items():
        col = volume[ticker].dropna()
        fig.add_trace(go.Bar(
            x=col.index,
            y=col.values,
            name=name,
            marker_color=COLORS[name],
            opacity=0.8,
            hovertemplate=f"<b>{name}</b><br>Data: %{{x|%d/%m/%Y}}<br>Volume: %{{y:,.0f}}<extra></extra>",
        ))
    fig.update_layout(
        title="Volume Negociado Diário",
        xaxis_title="Data",
        yaxis_title="Volume",
        barmode="group",
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        template="plotly_dark",
    )
    return fig
