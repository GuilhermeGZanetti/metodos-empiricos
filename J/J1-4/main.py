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

def plot_normal(times: list, mu_mean: float, sigma_mean: float, title: str, output_path: str):
    x = np.linspace(0, max(times) * 1.2, 1000)  # Ajustar o intervalo do eixo x
    pdf = (1 / (sigma_mean * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_mean) / sigma_mean) ** 2)

    plt.hist(times, bins=15, density=True, alpha=0.5, label="Dados observados")
    plt.plot(x, pdf, label="Distribuição Normal Estimada", color="red")
    plt.title(title)
    plt.xlabel("Tamanho Sentença")
    plt.ylabel("Densidade")
    plt.text(0.5, 0.5, f"mu = {mu_mean:.2f}\nsigma = {sigma_mean:.2f}", transform=plt.gca().transAxes)
    plt.legend()
    plt.grid()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico da normal salvo em {output_path}")

def build_model(data: dict, group: str) -> dict:
    print(f"\n\n>>Iniciando build do modelo do grupo {group}...")
    sm = stan.build(program_code=get_program_code("model.stan"), data=data)
    # Ajustando o modelo com os dados
    fit = sm.sample(num_chains=4)

    # Imprimindo o resumo dos parâmetros
    print("\n\n>Terminado build do modelo!")

    posterior = fit.to_frame()

    print("\n>Descrição dos parâmetros:")
    print(posterior.describe())

    plot_normal(data["x"], posterior['mu'].mean(), posterior['sigma'].mean(), f"Distribuição Normal da sentença provisória para tipo {group}", f"figs/normal_{group}.png")

    return {
        'tipo': group,
        'mu': posterior['mu'].mean(),
        'sigma': posterior['sigma'].mean()
    }

# Lendo arquivos de entrada
df_sentencas = pd.read_csv('arquivoentrada', sep=';')
if 'tipo' not in df_sentencas.columns:
    try:
        df_processos = pd.read_csv('processos.csv')
        df_processos["num_processo"] = df_processos["Link"].apply(lambda x: x.split("/")[-1].replace(".pdf", ""))

        # Pegando processos num_processo de df_sentencas e adicionando o Tipo do df_processos
        df_sentencas['tipo'] = ""
        for index, row in df_sentencas.iterrows():
            num_processo = str(row['num_processo']).replace("#", "")
            tipo = df_processos[df_processos['num_processo'] == num_processo]['Tipo'].values
            if len(tipo) > 0:
                tipo = tipo[0]
                df_sentencas.loc[index, 'tipo'] = tipo
            else:
                df_sentencas.loc[index, 'tipo'] = "Desconhecido"

        print(df_sentencas)
        df_sentencas.to_csv("arquivoentrada", index=False)
    except Exception:
        print("Erro: Arquivo processos.csv não encontrado. arquivoentrada não possui coluna tipo! Infelizmente não será possível fazer a analise sem essa coluna. Utilize o arquivoentrada enviado no moodle.")

# Filtrando sentenças por tipo
sentencas_tipos = {}
for tipo in df_sentencas["tipo"].unique():
    sentencas_tipos[tipo] = df_sentencas[df_sentencas["tipo"] == tipo]

# Para cada tipo de sentença, ajustar um modelo de distribuição normal com stan
params: list[dict] = []
for tipo in sentencas_tipos:
    print(f"Processando o tipo {tipo}")
    data = {
        'N': len(sentencas_tipos[tipo]),
        'x': sentencas_tipos[tipo]['sentenca_prov'].values
    }
    params.append(build_model(data, tipo))

# Salvar os parâmetros em um arquivo csv
print("\n\n\n>>>Salvando os parâmetros em um arquivo de saida csv arquivosaida...")
df_params = pd.DataFrame(params)
df_params.to_csv("arquivosaida", index=False)

print(">> Fazendo plot de todos os tipos juntos com cores diferentes")

# Fazer plot com todas as normais juntas e cores diferentes por grupo
plt.figure(figsize=(10, 6))

colors = sns.color_palette("tab10", len(sentencas_tipos))  # Paleta de cores para diferenciar os grupos
x_max = max([max(sentencas_tipos[tipo]['sentenca_prov']) for tipo in sentencas_tipos]) * 1.2
x = np.linspace(0, x_max, 1000)  # Ajustar o intervalo do eixo x

for i, tipo in enumerate(sentencas_tipos):
    data = sentencas_tipos[tipo]['sentenca_prov'].values
    plt.plot(x, (1 / params[i]['sigma']) * np.exp(-0.5 * ((x - params[i]['mu']) / params[i]['sigma']) ** 2), label=f"Normal {tipo}", color=colors[i])

plt.xlabel("Tamanho Sentença Provisória")
plt.ylabel("Densidade")
plt.legend()
plt.grid()
os.makedirs(os.path.dirname("figs/normal_todos.png"), exist_ok=True)
plt.savefig("figs/normal_todos.png")
plt.close()
print("> Gráfico da normal comparando todos os tipos salvo em figs/normal_todos.png")

print("> O gráfico gerado não serve de muita coisa pois, vemos que todos os tipos com a exceção de 'trafico' possuem muito poucas amostras e os desvios padrões ficaram muito elevados:")
print(df_sentencas["tipo"].value_counts())



    