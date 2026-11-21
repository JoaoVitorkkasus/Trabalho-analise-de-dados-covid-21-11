
print("INICIANDO AUDITORIA...")

import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

brasil = df[(df["state"] == "TOTAL") & (df["city"] == "TOTAL")].copy()
sergipe = df[(df["state"] == "SE") & (df["city"] == "TOTAL")].copy()

colunas = [
    "newCases", "totalCases", "newDeaths", "deaths",
    "vaccinated", "vaccinated_second",
    "vaccinated_third", "vaccinated_single"
]

for nome, dados in [("BRASIL", brasil), ("SERGIPE", sergipe)]:

    print(f"\n========== {nome} ==========")

    dados = dados.sort_values("date").copy()

    # 1. Verificação de datas duplicadas
    print("Datas duplicadas:", dados["date"].duplicated().sum())

    # 2. Verificação de dias ausentes na série temporal
    intervalo_datas = pd.date_range(
        start=dados["date"].min(),
        end=dados["date"].max(),
        freq="D"
    )

    datas_existentes = pd.DatetimeIndex(dados["date"])

    datas_ausentes = intervalo_datas.difference(datas_existentes)

    print("Dias ausentes na série temporal:", len(datas_ausentes))

    if len(datas_ausentes) > 0:
        print("Exemplos de datas ausentes:")
        print(datas_ausentes[:10])

    # 3. Valores ausentes nas variáveis
    print("\nValores ausentes:")
    print(dados[colunas].isna().sum())

    # 4. Verificação de valores negativos
    print("\nValores negativos:")

    for coluna in colunas:
        negativos = (dados[coluna] < 0).sum()
        print(f"{coluna}: {negativos}")

    # 5. Verificação de redução em indicadores acumulados
    acumulados = [
        "totalCases",
        "deaths",
        "vaccinated",
        "vaccinated_second",
        "vaccinated_third",
        "vaccinated_single"
    ]

    print("\nReduções em indicadores acumulados:")

    for coluna in acumulados:

        variacao = dados[coluna].diff()

        reducoes = (variacao < 0).sum()

        print(f"{coluna}: {reducoes}")

    # 6. Últimos cinco registros
    print("\nÚltimos cinco registros:")

    print(
        dados[["date"] + colunas]
        .tail(5)
        .to_string(index=False)
    )

# ==========================================================
# INVESTIGAÇÃO DOS REGISTROS PROBLEMÁTICOS
# ==========================================================

print("\n\n===== INVESTIGAÇÃO: BRASIL E SERGIPE =====")

for nome, dados in [("BRASIL", brasil), ("SERGIPE", sergipe)]:

    dados = dados.sort_values("date").copy()

    print(f"\n========== {nome} ==========")

    # Valores negativos nos registros diários
    print("\n--- Casos diários negativos ---")

    print(
        dados.loc[dados["newCases"] < 0,
                  ["date", "newCases", "totalCases"]]
        .to_string(index=False)
    )

    print("\n--- Óbitos diários negativos ---")

    print(
        dados.loc[dados["newDeaths"] < 0,
                  ["date", "newDeaths", "deaths"]]
        .to_string(index=False)
    )

    # Reduções nos acumulados
    acumulados = [
        "totalCases",
        "deaths",
        "vaccinated",
        "vaccinated_second",
        "vaccinated_third",
        "vaccinated_single"
    ]

    for coluna in acumulados:

        variacao = dados[coluna].diff()

        reducoes = dados.loc[
            variacao < 0,
            ["date", coluna]
        ].copy()

        if not reducoes.empty:

            print(f"\n--- Reduções em {coluna} ---")

            print(reducoes.to_string(index=False))

print("\nINVESTIGAÇÃO CONCLUÍDA!")

# ==========================================================
# INVESTIGAÇÃO DOS DADOS AUSENTES DE VACINAÇÃO
# ==========================================================

print("\n\n===== DADOS AUSENTES NA VACINAÇÃO =====")

colunas_vacina = [
    "vaccinated",
    "vaccinated_second",
    "vaccinated_third",
    "vaccinated_single"
]

for nome, dados in [("BRASIL", brasil), ("SERGIPE", sergipe)]:

    dados = dados.sort_values("date").copy()

    print(f"\n========== {nome} ==========")

    for coluna in colunas_vacina:

        ausentes = dados.loc[
            dados[coluna].isna(),
            "date"
        ]

        print(f"\nVariável: {coluna}")
        print("Total de registros ausentes:", len(ausentes))

        if len(ausentes) > 0:

            print("Primeira data ausente:", ausentes.min().date())
            print("Última data ausente:", ausentes.max().date())

print("\nINVESTIGAÇÃO DE VACINAÇÃO CONCLUÍDA!")