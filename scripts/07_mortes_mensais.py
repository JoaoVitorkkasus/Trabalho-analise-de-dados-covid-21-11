import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"
resultados = pasta / "resultados"
logo_path = pasta / "imagens" / "orelha.png"

resultados.mkdir(exist_ok=True)

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

logo = mpimg.imread(logo_path)

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

    mensal = (
        dados.set_index("date")["newDeaths"]
        .resample("MS")
        .sum()
    )

    # Criar gráfico
    fig, ax = plt.subplots(figsize=(12, 6))

    ax.bar(
        mensal.index,
        mensal.values,
        width=25
    )

    # Inserir logotipo
    ax_logo = fig.add_axes([0.02, 0.82, 0.10, 0.12])
    ax_logo.imshow(logo)
    ax_logo.axis("off")

    # Configurar gráfico
    ax.set_title(f"Mortes por COVID-19 por mês - {nome}")
    ax.set_xlabel("Mês")
    ax.set_ylabel("Número de mortes")

    ax.grid(axis="y", alpha=0.3)

    fig.tight_layout()

    # Nome do arquivo
    nome_arquivo = nome.lower() + "_mortes_mensais.png"

    # Salvar gráfico
    fig.savefig(
        resultados / nome_arquivo,
        dpi=300,
        facecolor="white"
    )

    plt.show()
    plt.close(fig)

    # Resultados estatísticos
    print(f"\n{'=' * 15} {nome} {'=' * 15}")

    print("Mês com mais mortes:",
          mensal.idxmax().strftime("%m/%Y"))

    print("Maior número de mortes em um mês:",
          mensal.max())

    print("Meses com total negativo:",
          (mensal < 0).sum())

print("\nANÁLISE MENSAL CONCLUÍDA!")