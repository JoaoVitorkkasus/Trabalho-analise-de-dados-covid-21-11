
import pandas as pd
from pathlib import Path

# Caminhos do projeto
pasta = Path(__file__).resolve().parent.parent
arquivo_dados = pasta / "dados" / "cases-brazil-states.csv"
resultados = pasta / "resultados"

# Carregar dados
df = pd.read_csv(arquivo_dados)
df["date"] = pd.to_datetime(df["date"])

# Regiões analisadas
regioes = {
    "Brasil": "TOTAL",
    "Sergipe": "SE"
}

linhas = []

for nome, sigla in regioes.items():

    dados = df[
        (df["state"] == sigla) &
        (df["city"] == "TOTAL")
    ].copy()

    dados = dados.sort_values("date")

    # Informações gerais
    primeiro_dia = dados["date"].min()
    ultimo_dia = dados["date"].max()

    ultimo_registro = dados.iloc[-1]

    total_casos = ultimo_registro["totalCases"]
    total_mortes = ultimo_registro["deaths"]

    # Maior número de mortes em um mês
    mensal = dados.set_index("date").resample("ME")["newDeaths"].sum()
    pico_mortes = mensal.idxmax()
    quantidade_pico = mensal.max()

    # Vacinação
    vacinacao = dados.dropna(subset=["vaccinated_second"])

    ultima_vacinacao = vacinacao.iloc[-1]

    total_segunda_dose = ultima_vacinacao["vaccinated_second"]
    cobertura = ultima_vacinacao["vaccinated_second_per_100_inhabitants"]

    # Correlações proporcionais
    arquivo_taxas = resultados / f"{nome.lower()}_taxas_proporcionais.csv"
    taxas = pd.read_csv(arquivo_taxas, index_col=0)

    mortes = taxas["mortes_por_100mil_no_mes"]
    vacinas = taxas["aumento_cobertura_vacinal"]

    correlacao_0 = mortes.corr(vacinas)
    correlacao_1 = mortes.iloc[1:].reset_index(drop=True).corr(
    vacinas.iloc[:-1].reset_index(drop=True)
)

    correlacao_2 = mortes.iloc[2:].reset_index(drop=True).corr(
    vacinas.iloc[:-2].reset_index(drop=True)
)

    # Montar resumo
    linhas.extend([
        f"\n{'=' * 45}",
        f"REGIÃO: {nome.upper()}",
        f"{'=' * 45}",
        f"Período: {primeiro_dia.date()} até {ultimo_dia.date()}",
        f"Total de casos: {total_casos:,.0f}",
        f"Total de mortes: {total_mortes:,.0f}",
        f"Maior número de mortes em um mês: {quantidade_pico:,.0f}",
        f"Mês do pico de mortes: {pico_mortes.strftime('%Y-%m')}",
        f"Total com segunda dose: {total_segunda_dose:,.0f}",
        f"Cobertura da segunda dose: {cobertura:.2f}%",
        "",
        "CORRELAÇÃO ENTRE AUMENTO DA COBERTURA E MORTES:",
        f"Mesmo mês: {correlacao_0:.4f}",
        f"Vacinação um mês antes: {correlacao_1:.4f}",
        f"Vacinação dois meses antes: {correlacao_2:.4f}",
    ])

# Aviso sobre os dados
linhas.extend([
    "\n" + "=" * 45,
    "OBSERVAÇÕES IMPORTANTES",
    "=" * 45,
    "A base de dados termina em 18/03/2023.",
    "Portanto, o ano de 2023 possui dados parciais.",
    "A correlação não demonstra relação de causa e efeito.",
    "Os indicadores de vacinação são acumulados e não devem ser somados.",
])

# Salvar arquivo
arquivo_saida = resultados / "resumo_final.txt"

with open(arquivo_saida, "w", encoding="utf-8") as arquivo:
    arquivo.write("\n".join(linhas))

# Exibir no terminal
print("\n".join(linhas))
print(f"\nResumo salvo em: {arquivo_saida}")
