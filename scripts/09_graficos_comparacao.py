import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
resultados = pasta / "resultados"
logo_path = pasta / "imagens" / "orelha.png"

logo = mpimg.imread(logo_path)

regioes = {
    "Brasil": "brasil_vacinacao_mortes_mensal.csv",
    "Sergipe": "sergipe_vacinacao_mortes_mensal.csv"
}

for nome, arquivo_csv in regioes.items():

    arquivo = resultados / arquivo_csv

    tabela = pd.read_csv(arquivo, index_col=0)

    # Converter o índice mensal para datas
    datas = pd.PeriodIndex(tabela.index, freq="M").to_timestamp()

    fig, eixos = plt.subplots(
        2, 1,
        figsize=(13, 8),
        sharex=True
    )

    # Gráfico de mortes
    eixos[0].bar(
        datas,
        tabela["mortes_no_mes"],
        width=25
    )

    # Logotipo no gráfico superior
    ax_logo1 = fig.add_axes([0.02, 0.91, 0.07, 0.07])
    ax_logo1.imshow(logo)
    ax_logo1.axis("off")

    eixos[0].set_title(
        f"Mortes mensais por COVID-19 - {nome}"
    )

    eixos[0].set_ylabel("Número de mortes")
    eixos[0].grid(axis="y", alpha=0.3)

    # Gráfico de vacinação
    eixos[1].bar(
        datas,
        tabela["novas_segundas_doses"],
        width=25
    )

    eixos[1].set_title(
        "Novas pessoas registradas com segunda dose"
    )

    eixos[1].set_ylabel("Pessoas")
    eixos[1].set_xlabel("Mês")
    eixos[1].grid(axis="y", alpha=0.3)

    fig.tight_layout(rect=[0.02, 0.02, 0.98, 0.88])

    nome_arquivo = (
        nome.lower() +
        "_comparacao_vacinacao_mortes.png"
    )

    fig.savefig(
        resultados / nome_arquivo,
        dpi=300,
        facecolor="white"
    )

    plt.show()
    plt.close(fig)

    print(f"\nGráfico gerado: {nome_arquivo}")

print("\nGRÁFICOS COMPARATIVOS CONCLUÍDOS!")