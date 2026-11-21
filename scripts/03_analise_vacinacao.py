
import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

colunas = [
    "vaccinated",
    "vaccinated_second",
    "vaccinated_third",
    "vaccinated_single"
]

for nome, dados in [
    ("BRASIL", df[(df["state"] == "TOTAL") & (df["city"] == "TOTAL")]),
    ("SERGIPE", df[(df["state"] == "SE") & (df["city"] == "TOTAL")])
]:
    print(f"\n{'=' * 15} {nome} {'=' * 15}")

    for coluna in colunas:
        validos = dados.dropna(subset=[coluna])

        if not validos.empty:
            primeiro = validos.iloc[0]
            ultimo = validos.iloc[-1]

            print(f"\nIndicador: {coluna}")
            print("Primeiro registro:", primeiro["date"].date())
            print("Último registro:", ultimo["date"].date())
            print("Registros válidos:", len(validos))
            print("Valor final:", ultimo[coluna])
        else:
            print(f"\n{coluna}: sem registros válidos")
