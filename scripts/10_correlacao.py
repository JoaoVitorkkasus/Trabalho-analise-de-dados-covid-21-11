import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
resultados = pasta / "resultados"

regioes = ["brasil", "sergipe"]

for regiao in regioes:

    arquivo = resultados / f"{regiao}_vacinacao_mortes_mensal.csv"

    dados = pd.read_csv(arquivo, index_col=0)

    dados = dados.dropna(
        subset=["mortes_no_mes", "novas_segundas_doses"]
    )

    print(f"\n{'=' * 15} {regiao.upper()} {'=' * 15}")

    print("Quantidade de meses analisados:", len(dados))

    for atraso in [0, 1, 2]:

        doses = dados["novas_segundas_doses"].shift(atraso)
        mortes = dados["mortes_no_mes"]

        comparacao = pd.concat(
            [doses, mortes],
            axis=1
        ).dropna()

        correlacao = comparacao.iloc[:, 0].corr(
            comparacao.iloc[:, 1]
        )

        if atraso == 0:
            descricao = "Mesmo mês"
        else:
            descricao = f"Vacinação {atraso} mês(es) antes"

        print(f"\n{descricao}:")
        print("Meses utilizados:", len(comparacao))
        print(f"Correlação de Pearson: {correlacao:.4f}")

        if correlacao <= -0.5:
            interpretacao = "Associação negativa forte"
        elif correlacao <= -0.3:
            interpretacao = "Associação negativa moderada"
        elif correlacao < 0:
            interpretacao = "Associação negativa fraca"
        elif correlacao < 0.3:
            interpretacao = "Associação positiva fraca"
        elif correlacao < 0.5:
            interpretacao = "Associação positiva moderada"
        else:
            interpretacao = "Associação positiva forte"

        print("Interpretação:", interpretacao)

    print("\nObservação: correlação não implica causalidade.")

print("\nANÁLISE DE CORRELAÇÃO CONCLUÍDA!")