import streamlit as st
import pandas as pd
from datetime import date
from data import get_dataframe, STATUS_COLOR, STATUS_LABEL, RISCO_COLOR
from charts import (chart_status_donut, chart_conclusao,
                    chart_orcamento, chart_timeline, chart_riscos)

st.set_page_config(
    page_title="Dashboard de Projetos | Andressa Marquito",
    page_icon="📊",
    layout="wide",
)

st.markdown("""
<style>
    .main { background-color: #0E1117; }
    .block-container { padding-top: 1.5rem; }
    .kpi-card {
        background: #1C2333;
        border-radius: 10px;
        padding: 18px 20px;
        text-align: center;
    }
    .kpi-value { font-size: 2rem; font-weight: 700; margin: 4px 0; }
    .kpi-label { font-size: 0.85rem; color: #AAAAAA; }
    .section-title {
        font-size: 1.1rem; font-weight: 600;
        color: #CCDDFF; margin: 20px 0 8px 0;
        border-left: 4px solid #0056A2;
        padding-left: 10px;
    }
    .tag {
        display: inline-block;
        padding: 3px 10px;
        border-radius: 12px;
        font-size: 0.78rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# ── Header ──────────────────────────────────────────────────────────
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.markdown("## 📊 Dashboard de Portfólio de Projetos")
    st.markdown("**Responsável:** Andressa Marquito &nbsp;|&nbsp; **Atualização:** semanal")
with col_h2:
    st.markdown(f"<div style='text-align:right; color:#AAAAAA; padding-top:20px'>"
                f"🗓️ {date.today().strftime('%d/%m/%Y')}</div>", unsafe_allow_html=True)

st.divider()

# ── Dados ────────────────────────────────────────────────────────────
df = get_dataframe()

# ── Filtros ──────────────────────────────────────────────────────────
col_f1, col_f2, col_f3 = st.columns(3)
with col_f1:
    areas = ["Todos"] + sorted(df["area"].unique().tolist())
    area_sel = st.selectbox("Área", areas)
with col_f2:
    status_opts = {"Todos": None, "🟢 No Prazo": "verde",
                   "🟡 Atenção": "amarelo", "🔴 Crítico": "vermelho"}
    status_sel = st.selectbox("Status", list(status_opts.keys()))
with col_f3:
    risco_opts = ["Todos", "Alto", "Médio", "Baixo"]
    risco_sel = st.selectbox("Risco", risco_opts)

df_f = df.copy()
if area_sel != "Todos":
    df_f = df_f[df_f["area"] == area_sel]
if status_opts[status_sel]:
    df_f = df_f[df_f["status"] == status_opts[status_sel]]
if risco_sel != "Todos":
    df_f = df_f[df_f["risco_nivel"] == risco_sel]

# ── KPIs ─────────────────────────────────────────────────────────────
st.markdown('<div class="section-title">Visão Geral do Portfólio</div>',
            unsafe_allow_html=True)

total          = len(df_f)
no_prazo       = len(df_f[df_f["status"] == "verde"])
atencao        = len(df_f[df_f["status"] == "amarelo"])
critico        = len(df_f[df_f["status"] == "vermelho"])
avg_conclusao  = df_f["conclusao_pct"].mean()
orc_total      = df_f["orcamento_total"].sum()
orc_consumido  = df_f["orcamento_consumido"].sum()
orc_forecast   = df_f["forecast_custo"].sum()
desvio_orc     = orc_forecast - orc_total
projetos_risco = len(df_f[df_f["risco_nivel"] == "Alto"])

k1, k2, k3, k4, k5, k6, k7, k8 = st.columns(8)

def kpi(col, label, value, color="#FFFFFF", sub=None):
    sub_html = f"<div style='font-size:0.72rem;color:#AAAAAA'>{sub}</div>" if sub else ""
    col.markdown(
        f"<div class='kpi-card'>"
        f"<div class='kpi-label'>{label}</div>"
        f"<div class='kpi-value' style='color:{color}'>{value}</div>"
        f"{sub_html}</div>", unsafe_allow_html=True)

kpi(k1, "Total de Projetos", total)
kpi(k2, "🟢 No Prazo",  no_prazo,  "#009A44")
kpi(k3, "🟡 Atenção",   atencao,   "#FFC200")
kpi(k4, "🔴 Crítico",   critico,   "#C0392B")
kpi(k5, "Avanço Médio", f"{avg_conclusao:.0f}%", "#7EB8F7")
kpi(k6, "Orçamento Total", f"R${orc_total/1e6:.1f}M", "#FFFFFF")
kpi(k7, "Consumido", f"R${orc_consumido/1e6:.1f}M",
    "#009A44" if orc_consumido <= orc_total else "#C0392B",
    sub=f"{orc_consumido/orc_total*100:.0f}% do total")
kpi(k8, "Forecast Custo",
    f"R${orc_forecast/1e6:.1f}M",
    "#C0392B" if desvio_orc > 0 else "#009A44",
    sub=f"+R${desvio_orc/1000:.0f}k vs. orçado" if desvio_orc > 0 else "Dentro do orçamento")

st.markdown("<br>", unsafe_allow_html=True)

# ── Gráficos Linha 1 ────────────────────────────────────────────────
st.markdown('<div class="section-title">Análise Visual</div>', unsafe_allow_html=True)

g1, g2, g3 = st.columns([1, 2, 2])
with g1:
    st.plotly_chart(chart_status_donut(df_f), use_container_width=True)
with g2:
    st.plotly_chart(chart_conclusao(df_f), use_container_width=True)
with g3:
    st.plotly_chart(chart_orcamento(df_f), use_container_width=True)

# ── Gráficos Linha 2 ────────────────────────────────────────────────
g4, g5 = st.columns([2, 2])
with g4:
    st.plotly_chart(chart_timeline(df_f), use_container_width=True)
with g5:
    st.plotly_chart(chart_riscos(df_f), use_container_width=True)

# ── Tabela detalhada ─────────────────────────────────────────────────
st.markdown('<div class="section-title">Tabela de Projetos</div>', unsafe_allow_html=True)

def fmt_status(s):
    icons = {"verde": "🟢", "amarelo": "🟡", "vermelho": "🔴"}
    labels = {"verde": "No Prazo", "amarelo": "Atenção", "vermelho": "Crítico"}
    return f"{icons[s]} {labels[s]}"

def fmt_risco(r):
    icons = {"Baixo": "🟢", "Médio": "🟡", "Alto": "🔴"}
    return f"{icons[r]} {r}"

df_display = df_f[[
    "id", "nome", "area", "status", "conclusao_pct",
    "previsao_original", "forecast", "desvio_dias",
    "orcamento_total", "orcamento_consumido", "forecast_custo", "desvio_custo",
    "risco_nivel", "risco_descricao"
]].copy()

df_display["status"]           = df_display["status"].map(fmt_status)
df_display["risco_nivel"]      = df_display["risco_nivel"].map(fmt_risco)
df_display["conclusao_pct"]    = df_display["conclusao_pct"].map(lambda x: f"{x}%")
df_display["previsao_original"]= df_display["previsao_original"].dt.strftime("%d/%m/%Y")
df_display["forecast"]         = df_display["forecast"].dt.strftime("%d/%m/%Y")
df_display["desvio_dias"]      = df_display["desvio_dias"].map(
    lambda x: f"+{x}d" if x > 0 else (f"{x}d" if x < 0 else "—"))
df_display["orcamento_total"]  = df_display["orcamento_total"].map(lambda x: f"R${x:,.0f}")
df_display["orcamento_consumido"] = df_display["orcamento_consumido"].map(lambda x: f"R${x:,.0f}")
df_display["forecast_custo"]   = df_display["forecast_custo"].map(lambda x: f"R${x:,.0f}")
df_display["desvio_custo"]     = df_display["desvio_custo"].map(
    lambda x: f"+R${x:,.0f}" if x > 0 else (f"-R${abs(x):,.0f}" if x < 0 else "—"))

df_display.columns = [
    "ID", "Projeto", "Área", "Status", "Avanço",
    "Previsão Original", "Forecast", "Desvio Prazo",
    "Orçamento Total", "Consumido", "Forecast Custo", "Desvio Custo",
    "Risco", "Descrição do Risco"
]

st.dataframe(df_display, use_container_width=True, hide_index=True,
             column_config={"Avanço": st.column_config.TextColumn(width="small"),
                            "Status": st.column_config.TextColumn(width="medium")})

# ── Alertas ──────────────────────────────────────────────────────────
criticos_df = df_f[df_f["status"] == "vermelho"]
if not criticos_df.empty:
    st.markdown('<div class="section-title">🚨 Projetos Críticos — Atenção Imediata</div>',
                unsafe_allow_html=True)
    for _, row in criticos_df.iterrows():
        st.error(
            f"**{row['id']} — {row['nome']}** ({row['area']})  \n"
            f"Avanço: {row['conclusao_pct']}%  |  "
            f"Forecast: {row['forecast'].strftime('%d/%m/%Y')}  |  "
            f"Desvio: +{row['desvio_dias']} dias  |  "
            f"Risco: {row['risco_nivel']}  \n"
            f"⚠️ {row['risco_descricao']}"
        )

# ── Rodapé ───────────────────────────────────────────────────────────
st.divider()
st.markdown(
    "<div style='text-align:center; color:#555; font-size:0.8rem'>"
    "Dashboard de Portfólio · Andressa Marquito · dessajf@gmail.com · "
    "Atualização semanal</div>",
    unsafe_allow_html=True
)
