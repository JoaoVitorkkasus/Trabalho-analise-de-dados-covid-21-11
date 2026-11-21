
import pandas as pd
from pathlib import Path

# Localizar o arquivo CSV
pasta_projeto = Path(__file__).resolve().parent.parent
arquivo = pasta_projeto / "dados" / "cases-brazil-states.csv"

# Ler os dados
df = pd.read_csv(arquivo)

# Converter a coluna de data
df["date"] = pd.to_datetime(df["date"])

print("ARQUIVO CARREGADO COM SUCESSO!")
print("-" * 40)

# Informações gerais
print("Quantidade de registros:", len(df))
print("Quantidade de colunas:", len(df.columns))
print("Período:", df["date"].min().date(), "até", df["date"].max().date())

# Separar Brasil e Sergipe
brasil = df[(df["state"] == "TOTAL") & (df["city"] == "TOTAL")]
sergipe = df[(df["state"] == "SE") & (df["city"] == "TOTAL")]

print("-" * 40)
print("Registros do Brasil:", len(brasil))
print("Registros de Sergipe:", len(sergipe))

# Mostrar algumas informações
print("\nDADOS DO BRASIL:")
print(brasil[["date", "newCases", "newDeaths", "vaccinated"]].head())

print("\nDADOS DE SERGIPE:")
print(sergipe[["date", "newCases", "newDeaths", "vaccinated"]].head())
