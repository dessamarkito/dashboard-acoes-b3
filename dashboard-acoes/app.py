import streamlit as st
from data import get_stock_data, get_metrics, TICKERS
from charts import chart_historico, chart_performance, chart_candlestick, chart_volume

st.set_page_config(
    page_title="Dashboard de Ações B3 — 2025",
    page_icon="📈",
    layout="wide",
)

st.title("📈 Dashboard de Ações B3 — 2025")
st.caption("Cotação e performance de Banco do Brasil (BBAS3), Itaú (ITUB4) e Vale (VALE3)")

with st.spinner("Carregando dados do mercado..."):
    close, open_, high, low, volume = get_stock_data()
    metrics = get_metrics(close)

# --- Cards de métricas ---
st.subheader("Visão Geral")
cols = st.columns(3)
for i, (name, m) in enumerate(metrics.items()):
    with cols[i]:
        delta_str = f"{m['variacao_pct']:+.2f}% desde 01/01/2025"
        st.metric(
            label=f"{name} ({m['ticker']})",
            value=f"R$ {m['preco_atual']:.2f}",
            delta=delta_str,
        )
        st.caption(f"Máx: R$ {m['maxima']:.2f}  |  Mín: R$ {m['minima']:.2f}")

st.divider()

# --- Gráfico de linha ---
st.plotly_chart(chart_historico(close), use_container_width=True)

# --- Gráfico de performance ---
st.plotly_chart(chart_performance(close), use_container_width=True)

st.divider()

# --- Candlestick ---
st.subheader("Candlestick por Ação")
acao_selecionada = st.selectbox("Selecione a ação:", list(TICKERS.keys()))
st.plotly_chart(chart_candlestick(open_, high, low, close, acao_selecionada), use_container_width=True)

st.divider()

# --- Volume ---
st.plotly_chart(chart_volume(volume), use_container_width=True)

st.caption("Dados fornecidos por Yahoo Finance via yfinance. Atualização automática a cada 1 hora.")
