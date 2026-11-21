import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
resultados = pasta / "resultados"
logo_path = pasta / "imagens" / "orelha.png"

logo = mpimg.imread(logo_path)

for regiao in ["brasil", "sergipe"]:

    arquivo = resultados / f"{regiao}_taxas_proporcionais.csv"

    dados = pd.read_csv(arquivo, index_col=0)

    datas = pd.PeriodIndex(
        dados.index, freq="M"
    ).to_timestamp()

    fig, eixos = plt.subplots(
        2, 1,
        figsize=(13, 8),
        sharex=True
    )

    # Gráfico de mortalidade proporcional mensal
    eixos[0].plot(
        datas,
        dados["mortes_por_100mil_no_mes"],
        marker="o"
    )

    eixos[0].set_title(
        f"Mortes mensais por 100 mil habitantes - {regiao.title()}"
    )

    eixos[0].set_ylabel("Mortes por 100 mil habitantes")
    eixos[0].grid(alpha=0.3)

    # Gráfico de cobertura vacinal
    eixos[1].plot(
        datas,
        dados["cobertura_segunda_dose"],
        marker="o"
    )

    eixos[1].set_title(
        "Cobertura acumulada da segunda dose"
    )

    eixos[1].set_ylabel("Cobertura (%)")
    eixos[1].set_xlabel("Mês")
    eixos[1].grid(alpha=0.3)

    # Inserir logotipo no cabeçalho
    ax_logo = fig.add_axes([0.02, 0.91, 0.07, 0.07])
    ax_logo.imshow(logo)
    ax_logo.axis("off")

    # Reservar espaço para o cabeçalho
    fig.tight_layout(
        rect=[0.02, 0.02, 0.98, 0.88]
    )

    nome_arquivo = (
        f"{regiao}_taxas_vacinacao_mortes.png"
    )

    fig.savefig(
        resultados / nome_arquivo,
        dpi=300,
        facecolor="white"
    )

    plt.show()
    plt.close(fig)

    print(f"Gráfico gerado para {regiao.title()}")

print("\nGRÁFICOS PROPORCIONAIS CONCLUÍDOS!")