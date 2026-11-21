
import pandas as pd
import matplotlib.pyplot as plt
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
    ],
    "Sergipe": df[
        (df["state"] == "SE") &
        (df["city"] == "TOTAL")
    ]
}

for nome, dados in regioes.items():

    plt.figure(figsize=(12, 6))

    plt.plot(
        dados["date"],
        dados["deaths"]
    )

    plt.title(f"Evolução das mortes acumuladas por COVID-19 - {nome}")
    plt.xlabel("Data")
    plt.ylabel("Mortes acumuladas")
    plt.grid(True, alpha=0.3)

    plt.tight_layout()

    nome_arquivo = nome.lower() + "_mortes_acumuladas.png"

    plt.savefig(
        resultados / nome_arquivo,
        dpi=300,
        facecolor='white',
        transparent=False
    )

    plt.show()
    plt.close()
