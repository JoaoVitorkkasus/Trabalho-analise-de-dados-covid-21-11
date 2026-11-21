import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

regioes = {
    "BRASIL": df[
        (df["state"] == "TOTAL") &
        (df["city"] == "TOTAL")
    ].copy(),

    "SERGIPE": df[
        (df["state"] == "SE") &
        (df["city"] == "TOTAL")
    ].copy()
}

for nome, dados in regioes.items():

    dados = dados.sort_values("date").copy()

    print(f"\n{'=' * 15} {nome} {'=' * 15}")

    print(
        "Período:",
        dados["date"].min().date(),
        "até",
        dados["date"].max().date()
    )

    print("\n--- Indicadores acumulados ---")

    print("Total de casos:", dados["totalCases"].max())
    print("Total de mortes:", dados["deaths"].max())

    print("\n--- Máximos diários ---")

    idx_casos = dados["newCases"].idxmax()
    idx_mortes = dados["newDeaths"].idxmax()

    print("Maior número de casos em um dia:",
          dados.loc[idx_casos, "newCases"])

    print("Data do maior número de casos:",
          dados.loc[idx_casos, "date"].date())

    print("Maior número de mortes em um dia:",
          dados.loc[idx_mortes, "newDeaths"])

    print("Data do maior número de mortes:",
          dados.loc[idx_mortes, "date"].date())

    print("\n--- Médias diárias ---")

    print("Média diária de casos:",
          round(dados["newCases"].mean(), 2))

    print("Média diária de mortes:",
          round(dados["newDeaths"].mean(), 2))

    print("\n--- Registros negativos ---")

    print("Dias com casos negativos:",
          (dados["newCases"] < 0).sum())

    print("Dias com mortes negativas:",
          (dados["newDeaths"] < 0).sum())

print("\nANÁLISE CONCLUÍDA!")