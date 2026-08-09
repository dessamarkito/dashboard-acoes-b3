import pandas as pd
from datetime import date

PROJETOS = [
    {
        "id": "PRJ-001",
        "nome": "Novo Produto Residencial",
        "area": "Danos",
        "gerente": "Andressa Marquito",
        "status": "verde",
        "conclusao_pct": 82,
        "inicio": "2025-01-10",
        "previsao_original": "2025-06-30",
        "forecast": "2025-07-10",
        "orcamento_total": 480000,
        "orcamento_consumido": 360000,
        "forecast_custo": 490000,
        "risco_nivel": "Baixo",
        "risco_descricao": "Nenhum blocker crítico identificado",
    },
    {
        "id": "PRJ-002",
        "nome": "Integração Gateway de Pagamento",
        "area": "Tecnologia",
        "gerente": "Andressa Marquito",
        "status": "amarelo",
        "conclusao_pct": 55,
        "inicio": "2025-02-03",
        "previsao_original": "2025-07-15",
        "forecast": "2025-08-20",
        "orcamento_total": 620000,
        "orcamento_consumido": 410000,
        "forecast_custo": 680000,
        "risco_nivel": "Alto",
        "risco_descricao": "Dependência de API do parceiro com atraso",
    },
    {
        "id": "PRJ-003",
        "nome": "Seguro Prestamista Digital",
        "area": "Vida / Prestamista",
        "gerente": "Andressa Marquito",
        "status": "verde",
        "conclusao_pct": 91,
        "inicio": "2024-11-01",
        "previsao_original": "2025-05-31",
        "forecast": "2025-06-05",
        "orcamento_total": 310000,
        "orcamento_consumido": 295000,
        "forecast_custo": 315000,
        "risco_nivel": "Baixo",
        "risco_descricao": "Aprovação SUSEP em fase final",
    },
    {
        "id": "PRJ-004",
        "nome": "Plataforma Seguro Rural Safra 2026",
        "area": "Rural",
        "gerente": "Andressa Marquito",
        "status": "vermelho",
        "conclusao_pct": 34,
        "inicio": "2025-03-01",
        "previsao_original": "2025-08-30",
        "forecast": "2025-11-15",
        "orcamento_total": 750000,
        "orcamento_consumido": 390000,
        "forecast_custo": 870000,
        "risco_nivel": "Alto",
        "risco_descricao": "Atraso na validação regulatória e turnover no time",
    },
    {
        "id": "PRJ-005",
        "nome": "Modernização VMO / PMO",
        "area": "Governança",
        "gerente": "Andressa Marquito",
        "status": "verde",
        "conclusao_pct": 68,
        "inicio": "2025-01-20",
        "previsao_original": "2025-09-30",
        "forecast": "2025-09-30",
        "orcamento_total": 200000,
        "orcamento_consumido": 128000,
        "forecast_custo": 205000,
        "risco_nivel": "Médio",
        "risco_descricao": "Resistência de algumas áreas à mudança de processo",
    },
    {
        "id": "PRJ-006",
        "nome": "App de Gestão de Apólices",
        "area": "Danos",
        "gerente": "Andressa Marquito",
        "status": "amarelo",
        "conclusao_pct": 47,
        "inicio": "2025-02-17",
        "previsao_original": "2025-09-01",
        "forecast": "2025-10-15",
        "orcamento_total": 530000,
        "orcamento_consumido": 265000,
        "forecast_custo": 570000,
        "risco_nivel": "Médio",
        "risco_descricao": "Escopo ampliado após alinhamento com diretoria",
    },
    {
        "id": "PRJ-007",
        "nome": "Migração de Dados Legado",
        "area": "Tecnologia",
        "gerente": "Andressa Marquito",
        "status": "verde",
        "conclusao_pct": 78,
        "inicio": "2024-12-01",
        "previsao_original": "2025-06-30",
        "forecast": "2025-07-01",
        "orcamento_total": 390000,
        "orcamento_consumido": 300000,
        "forecast_custo": 395000,
        "risco_nivel": "Médio",
        "risco_descricao": "Volume de dados maior que o estimado",
    },
    {
        "id": "PRJ-008",
        "nome": "Programa de Agilidade Corporativa",
        "area": "Governança",
        "gerente": "Andressa Marquito",
        "status": "amarelo",
        "conclusao_pct": 40,
        "inicio": "2025-03-10",
        "previsao_original": "2025-12-31",
        "forecast": "2025-12-31",
        "orcamento_total": 280000,
        "orcamento_consumido": 95000,
        "forecast_custo": 295000,
        "risco_nivel": "Médio",
        "risco_descricao": "Engajamento das lideranças abaixo do esperado",
    },
]

def get_dataframe():
    df = pd.DataFrame(PROJETOS)
    df["previsao_original"] = pd.to_datetime(df["previsao_original"])
    df["forecast"]          = pd.to_datetime(df["forecast"])
    df["inicio"]            = pd.to_datetime(df["inicio"])
    df["desvio_dias"]       = (df["forecast"] - df["previsao_original"]).dt.days
    df["desvio_custo"]      = df["forecast_custo"] - df["orcamento_total"]
    df["pct_orcamento"]     = (df["orcamento_consumido"] / df["orcamento_total"] * 100).round(1)
    return df

STATUS_COLOR = {
    "verde":    "#009A44",
    "amarelo":  "#FFC200",
    "vermelho": "#C0392B",
}

STATUS_LABEL = {
    "verde":    "🟢 No Prazo",
    "amarelo":  "🟡 Atenção",
    "vermelho": "🔴 Crítico",
}

RISCO_COLOR = {
    "Baixo":  "#009A44",
    "Médio":  "#FFC200",
    "Alto":   "#C0392B",
}
