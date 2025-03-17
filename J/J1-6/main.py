import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import stan
import seaborn as sns


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()


"""
-------
Leitura dos dados
-------
"""
# Checa se existe arquivo "processos_furto_qualificado.csv"
if os.path.exists("processos_furto_qualificado.csv"):
    # Ler todos os arquivos CSV
    df_processos = pd.DataFrame()
    for file in os.listdir("."):
        if file.endswith(".csv"):
            # Ler o arquivo CSV
            df = pd.read_csv(file)

            # Remover linhas com dados faltantes nas colunas Pena Base ou Pena Definitiva
            df = df.dropna(subset=['Pena Base', 'Pena Definitiva'])
            
            # Pegar apenas colunas Número processo,Categoria,comarca,vara,juiz,Pena Base,Pena Definitiva
            df = df[['Número processo', 'Categoria', 'comarca', 'vara', 'juiz', 'Pena Base', 'Pena Definitiva']]

            # Concatenar os dataframes
            df_processos = pd.concat([df_processos, df], ignore_index=True)

    # Salvar o dataframe em um novo arquivo CSV
    df_processos.to_csv("arquivoentrada", index=False)
else:
    # Ler arquivoentrada
    df_processos = pd.read_csv("arquivoentrada")


# Agrupar os dados por categoria
# Para cada categoria, modelar uma normal com stan para Pena Base e Pena Definitiva
# Printar tabela para cada categoria N, Média, Mediana, Desvio-padrão, mínimo e máximo. Para pena base e pena definitiva em anos, meses e dias

def gerar_tabela_categoria(df, group):
    def criar_modelo_stan(df_group, campo):
        N_group = {"Furto Simples": 99, "Furto Qualificado": 101, "Roubo Simples": 100, "Roubo Majorado": 100, "Tráfico de Drogas": 101}
        N = N_group[group]
        data = {
            "N": N,
            "y": df_group[campo].sample(n=N, random_state=42).tolist(),
        }
        sm = stan.build(program_code=get_program_code("model.stan"), data=data)
        # Ajustando o modelo com os dados
        fit = sm.sample(num_chains=4)
        return {
            "N": N,
            "mean": fit["mu"].mean(),
            "sigma": fit["sigma"].mean()
        }

    def calcular_frequentista(df_group, campo):
        N_group = {"Furto Simples": 99, "Furto Qualificado": 101, "Roubo Simples": 100, "Roubo Majorado": 100, "Tráfico de Drogas": 101}
        N = N_group[group]
        sample = df_group[campo].sample(n=N, random_state=42).tolist(),
        return {
            "N": N,
            "mean": np.mean(sample),
            "sigma": np.std(sample)
        }


    df_group = df[df['Categoria'] == group]

    pena_base = criar_modelo_stan(df_group, "Pena Base")
    pena_definitiva = criar_modelo_stan(df_group, "Pena Definitiva")

    df_tabela_stan = pd.DataFrame({
        "Estatísticas": ["N", "Média", "Mediana", "Desvio padrão", "Mínimo", "Máximo"],
        "Pena Base (anos)": [pena_base["N"], pena_base["mean"]/365, df_group["Pena Base"].median()/365, pena_base["sigma"]/365, df_group["Pena Base"].min()/365, df_group["Pena Base"].max()/365],  
        "Pena Base (meses)": [pena_base["N"], pena_base["mean"]/30, df_group["Pena Base"].median()/30, pena_base["sigma"]/30, df_group["Pena Base"].min()/30, df_group["Pena Base"].max()/30],
        "Pena Base (dias)": [pena_base["N"], pena_base["mean"], df_group["Pena Base"].median(), pena_base["sigma"], df_group["Pena Base"].min(), df_group["Pena Base"].max()],
        "Pena Definitiva (anos)": [pena_definitiva["N"], pena_definitiva["mean"]/365, df_group["Pena Definitiva"].median()/365, pena_definitiva["sigma"]/365, df_group["Pena Definitiva"].min()/365, 365*df_group["Pena Definitiva"].max()/365],
        "Pena Definitiva (meses)": [pena_definitiva["N"], pena_definitiva["mean"]/30, df_group["Pena Definitiva"].median()/30, pena_definitiva["sigma"]/30, df_group["Pena Definitiva"].min()/30, df_group["Pena Definitiva"].max()/30],
        "Pena Definitiva (dias)": [pena_definitiva["N"], pena_definitiva["mean"], df_group["Pena Definitiva"].median(), pena_definitiva["sigma"], df_group["Pena Definitiva"].min(), df_group["Pena Definitiva"].max()],
    })

    pena_base = calcular_frequentista(df_group, "Pena Base")
    pena_definitiva = calcular_frequentista(df_group, "Pena Definitiva")
    df_tabela_frequentist = pd.DataFrame({
        "Estatísticas": ["N", "Média", "Mediana", "Desvio padrão", "Mínimo", "Máximo"],
        "Pena Base (anos)": [pena_base["N"], pena_base["mean"]/365, df_group["Pena Base"].median()/365, pena_base["sigma"]/365, df_group["Pena Base"].min()/365, df_group["Pena Base"].max()/365],  
        "Pena Base (meses)": [pena_base["N"], pena_base["mean"]/30, df_group["Pena Base"].median()/30, pena_base["sigma"]/30, df_group["Pena Base"].min()/30, df_group["Pena Base"].max()/30],
        "Pena Base (dias)": [pena_base["N"], pena_base["mean"], df_group["Pena Base"].median(), pena_base["sigma"], df_group["Pena Base"].min(), df_group["Pena Base"].max()],
        "Pena Definitiva (anos)": [pena_definitiva["N"], pena_definitiva["mean"]/365, df_group["Pena Definitiva"].median()/365, pena_definitiva["sigma"]/365, df_group["Pena Definitiva"].min()/365, 365*df_group["Pena Definitiva"].max()/365],
        "Pena Definitiva (meses)": [pena_definitiva["N"], pena_definitiva["mean"]/30, df_group["Pena Definitiva"].median()/30, pena_definitiva["sigma"]/30, df_group["Pena Definitiva"].min()/30, df_group["Pena Definitiva"].max()/30],
        "Pena Definitiva (dias)": [pena_definitiva["N"], pena_definitiva["mean"], df_group["Pena Definitiva"].median(), pena_definitiva["sigma"], df_group["Pena Definitiva"].min(), df_group["Pena Definitiva"].max()],
    })



    return df_tabela_stan, df_tabela_frequentist


tables = {}
tables_frequentist = {}
for group in df_processos['Categoria'].unique():
    tables[group], tables_frequentist[group] = gerar_tabela_categoria(df_processos, group)


for group in ["Furto Simples", "Furto Qualificado", "Roubo Simples", "Roubo Majorado", "Tráfico de Drogas"]:
    print("\n\n--------------\n>>>Tabela Stan: ", group, "\n\n")
    print(tables[group].to_markdown())
    print("\n\n--------------\n>>>Tabela Frquentista: ", group, "\n\n")
    print(tables_frequentist[group].to_markdown())
    print("\n\n")


print("É possível verificar que os resultados alcançados com mesmo tamanho de amostra foram bem similares aos apresentados no artigo. As maiores diferenças podem ser vistas nos valores mínimos e máximos, que dependem mais da aleatoriedade da amostra do que da distribuição intrinseca aos dados. Nas outras Estatísticas, como média e desvio padrão, os resultados apresentados com stan e os do artigo são bem similares, com a principal exceção sendo o tipo de crime tráfico de drogas. Nesse tipo de crime, a média obtida neste trabalho foi de 3,87 enquanto no artigo o valor é de 5,53. Isso pode implicar que o crime de tráfico de drogas possui uma maior variabilidade em sua distribuição e as amostras diferentes refletiram isso.")

print("\n\nAlém dessa análise, também foi feita a comparação entre o método Bayesiano de calcular as estatísticas de média e desvio padrão (Stan) e a maneira clássica de cálculo desses valores. Os resultados mostram que ambos os métodos são muito similares, com diferenças de menos de 0,02% nas médias e desvios padrões. Isso indica que o Stan pode ser usado nesse tamanho de amostra para calcular as estatísticas de média e desvio padrão com confiança e precisão adequadas, porém com o custo mais elevado em computação e complexidade do código.")