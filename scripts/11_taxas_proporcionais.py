import pandas as pd
from pathlib import Path

pasta = Path(__file__).resolve().parent.parent
arquivo = pasta / "dados" / "cases-brazil-states.csv"
resultados = pasta / "resultados"

resultados.mkdir(exist_ok=True)

df = pd.read_csv(arquivo)
df["date"] = pd.to_datetime(df["date"])

regioes = {
    "Brasil": ("TOTAL", "TOTAL"),
    "Sergipe": ("SE", "TOTAL")
}

for nome, (estado, cidade) in regioes.items():

    dados = df[
        (df["state"] == estado) &
        (df["city"] == cidade)
    ].copy()

    dados = dados.sort_values("date")
    dados["mes"] = dados["date"].dt.to_period("M")

    mensal = dados.groupby("mes").agg(
        mortes_acumuladas_por_100mil=(
            "deaths_per_100k_inhabitants", "last"
        ),
        cobertura_segunda_dose=(
            "vaccinated_second_per_100_inhabitants", "last"
        )
    )

    # Criar sequência contínua de meses
    meses_completos = pd.period_range(
        start=dados["date"].min().to_period("M"),
        end=dados["date"].max().to_period("M"),
        freq="M"
    )

    mensal = mensal.reindex(meses_completos)

    # Variação mensal da mortalidade por 100 mil habitantes
    mensal["mortes_por_100mil_no_mes"] = (
        mensal["mortes_acumuladas_por_100mil"].diff()
    )

    # Variação mensal da cobertura vacinal
    mensal["aumento_cobertura_vacinal"] = (
        mensal["cobertura_segunda_dose"].diff()
    )

    # Exportar tabela
    mensal.to_csv(
        resultados / f"{nome.lower()}_taxas_proporcionais.csv"
    )

    print(f"\n{'=' * 15} {nome.upper()} {'=' * 15}")

    print("\nÚltimos 12 meses:")
    print(mensal.tail(12).round(4).to_string())

    print("\nCorrelação entre aumento da cobertura e mortes:")

    for atraso in [0, 1, 2]:

        doses = mensal["aumento_cobertura_vacinal"].shift(atraso)
        mortes = mensal["mortes_por_100mil_no_mes"]

        comparacao = pd.concat(
            [doses, mortes], axis=1
        ).dropna()

        correlacao = comparacao.iloc[:, 0].corr(
            comparacao.iloc[:, 1]
        )

        print(f"\nAtraso de {atraso} mês(es):")
        print("Meses utilizados:", len(comparacao))
        print(f"Correlação de Pearson: {correlacao:.4f}")

print("\nANÁLISE PROPORCIONAL CONCLUÍDA!")