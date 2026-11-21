
import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"
resultados = pasta / "resultados"

resultados.mkdir(exist_ok=True)

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

regioes = {
    "Brasil": df[
        (df["state"] == "TOTAL") &
        (df["city"] == "TOTAL")
    ].copy(),

    "Sergipe": df[
        (df["state"] == "SE") &
        (df["city"] == "TOTAL")
    ].copy()
}

for nome, dados in regioes.items():

    dados = dados.sort_values("date")
    dados["mes"] = dados["date"].dt.to_period("M")

    # Mortes notificadas por mês
    mortes = (
        dados.groupby("mes")["newDeaths"]
        .sum()
    )

    # Último registro disponível da segunda dose em cada mês
    vacinacao = (
        dados.dropna(subset=["vaccinated_second"])
        .groupby("mes")["vaccinated_second"]
        .last()
    )

    tabela = pd.concat(
        [mortes, vacinacao],
        axis=1
    )

    tabela.columns = [
        "mortes_no_mes",
        "pessoas_com_segunda_dose"
    ]

    # Quantidade de novas pessoas registradas com segunda dose
    tabela["novas_segundas_doses"] = (
        tabela["pessoas_com_segunda_dose"].diff()
    )

    tabela = tabela.dropna()

    tabela.to_csv(
        resultados / f"{nome.lower()}_vacinacao_mortes_mensal.csv",
        index=True
    )

    print(f"\n{'=' * 15} {nome} {'=' * 15}")

    print("\nPrimeiros registros:")
    print(tabela.head(10).to_string())

    print("\nÚltimos registros:")
    print(tabela.tail(10).to_string())

    print("\nMês com mais mortes:")
    print(tabela["mortes_no_mes"].idxmax())

    print("\nMês com mais segundas doses:")
    print(tabela["novas_segundas_doses"].idxmax())
