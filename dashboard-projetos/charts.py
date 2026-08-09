import plotly.express as px
import plotly.graph_objects as go
from data import STATUS_COLOR, RISCO_COLOR

TEMPLATE = "plotly_dark"
FONT     = dict(family="Calibri", size=13, color="#FFFFFF")

def chart_status_donut(df):
    counts = df["status"].value_counts().reset_index()
    counts.columns = ["status", "qtd"]
    labels = {"verde": "🟢 No Prazo", "amarelo": "🟡 Atenção", "vermelho": "🔴 Crítico"}
    counts["label"] = counts["status"].map(labels)
    fig = go.Figure(go.Pie(
        labels=counts["label"],
        values=counts["qtd"],
        hole=0.6,
        marker_colors=[STATUS_COLOR[s] for s in counts["status"]],
        textinfo="label+value",
        textfont=dict(size=13),
    ))
    fig.update_layout(
        title="Status do Portfólio",
        template=TEMPLATE, font=FONT,
        showlegend=False,
        height=300,
        margin=dict(t=40, b=10, l=10, r=10),
        annotations=[dict(text=f"<b>{len(df)}</b><br>projetos", x=0.5, y=0.5,
                          font_size=16, showarrow=False, font_color="#FFFFFF")]
    )
    return fig

def chart_conclusao(df):
    df_sorted = df.sort_values("conclusao_pct", ascending=True)
    cores = [STATUS_COLOR[s] for s in df_sorted["status"]]
    fig = go.Figure(go.Bar(
        x=df_sorted["conclusao_pct"],
        y=df_sorted["nome"],
        orientation="h",
        marker_color=cores,
        text=[f"{v}%" for v in df_sorted["conclusao_pct"]],
        textposition="outside",
        textfont=dict(color="#FFFFFF", size=12),
    ))
    fig.add_vline(x=50, line_dash="dot", line_color="#888888",
                  annotation_text="50%", annotation_font_color="#AAAAAA")
    fig.update_layout(
        title="% de Conclusão por Projeto",
        template=TEMPLATE, font=FONT,
        xaxis=dict(range=[0, 115], title="% Conclusão"),
        yaxis=dict(title=""),
        height=380,
        margin=dict(t=40, b=20, l=10, r=60),
    )
    return fig

def chart_orcamento(df):
    fig = go.Figure()
    fig.add_trace(go.Bar(
        name="Consumido", x=df["nome"],
        y=df["orcamento_consumido"] / 1000,
        marker_color="#0056A2",
        text=[f"R${v/1000:.0f}k" for v in df["orcamento_consumido"]],
        textposition="outside", textfont=dict(color="#FFFFFF", size=10),
    ))
    fig.add_trace(go.Bar(
        name="Forecast", x=df["nome"],
        y=(df["forecast_custo"] - df["orcamento_consumido"]) / 1000,
        marker_color="#FFC200",
        base=df["orcamento_consumido"] / 1000,
        text=[f"+R${(f-c)/1000:.0f}k" if f > c else ""
              for f, c in zip(df["forecast_custo"], df["orcamento_consumido"])],
        textposition="outside", textfont=dict(color="#FFC200", size=10),
    ))
    fig.add_trace(go.Scatter(
        name="Orçamento Total", x=df["nome"],
        y=df["orcamento_total"] / 1000,
        mode="markers", marker=dict(symbol="line-ew", size=20,
                                     color="#FFFFFF", line=dict(width=2, color="#FFFFFF")),
    ))
    fig.update_layout(
        title="Orçamento: Consumido vs. Forecast vs. Total (R$ mil)",
        template=TEMPLATE, font=FONT,
        barmode="stack",
        height=380,
        legend=dict(orientation="h", y=1.1),
        xaxis=dict(tickangle=-20),
        margin=dict(t=60, b=60, l=10, r=10),
    )
    return fig

def chart_timeline(df):
    df_sorted = df.sort_values("forecast")
    fig = go.Figure()
    for _, row in df_sorted.iterrows():
        cor = STATUS_COLOR[row["status"]]
        fig.add_trace(go.Scatter(
            x=[row["inicio"], row["previsao_original"]],
            y=[row["nome"], row["nome"]],
            mode="lines",
            line=dict(color="#555555", width=6),
            showlegend=False,
        ))
        fig.add_trace(go.Scatter(
            x=[row["previsao_original"]],
            y=[row["nome"]],
            mode="markers",
            marker=dict(symbol="diamond", size=10, color="#AAAAAA"),
            name="Previsão original" if row.name == df_sorted.index[0] else "",
            showlegend=(row.name == df_sorted.index[0]),
        ))
        fig.add_trace(go.Scatter(
            x=[row["forecast"]],
            y=[row["nome"]],
            mode="markers",
            marker=dict(symbol="circle", size=12, color=cor,
                        line=dict(width=2, color="#FFFFFF")),
            name="Forecast" if row.name == df_sorted.index[0] else "",
            showlegend=(row.name == df_sorted.index[0]),
        ))
    fig.update_layout(
        title="Timeline — Previsão Original vs. Forecast",
        template=TEMPLATE, font=FONT,
        height=380,
        xaxis=dict(title="", type="date"),
        yaxis=dict(title=""),
        legend=dict(orientation="h", y=1.1),
        margin=dict(t=60, b=20, l=10, r=10),
    )
    return fig

def chart_riscos(df):
    risco_map = {"Baixo": 1, "Médio": 2, "Alto": 3}
    df = df.copy()
    df["risco_num"] = df["risco_nivel"].map(risco_map)
    fig = px.scatter(
        df, x="conclusao_pct", y="risco_num",
        size="orcamento_total",
        color="risco_nivel",
        color_discrete_map=RISCO_COLOR,
        text="id",
        hover_name="nome",
        hover_data={"risco_descricao": True, "conclusao_pct": True,
                    "risco_num": False, "orcamento_total": False},
        labels={"conclusao_pct": "% Conclusão", "risco_num": "Nível de Risco"},
        title="Mapa de Risco vs. Avanço",
        template=TEMPLATE,
    )
    fig.update_traces(textposition="top center", textfont=dict(color="#FFFFFF", size=10))
    fig.update_yaxes(tickvals=[1, 2, 3], ticktext=["Baixo", "Médio", "Alto"])
    fig.update_layout(
        font=FONT, height=350,
        legend=dict(orientation="h", y=1.1, title=""),
        margin=dict(t=60, b=20, l=10, r=10),
    )
    return fig
