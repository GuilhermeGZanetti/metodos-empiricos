import stan
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as st


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()

def plot_normal(times: list, mu_mean: float, sigma_mean: float, title: str, output_path: str):
    x = np.linspace(0, max(times) * 1.0, 1000)  # Ajustar o intervalo do eixo x
    pdf = (1 / (sigma_mean * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_mean) / sigma_mean) ** 2)
    
    fig, ax1 = plt.subplots(figsize=(12, 6))  # Criar a figura e o primeiro eixo

    # Criar histograma usando o primeiro eixo
    sns.countplot(x=times, ax=ax1, color="blue")
    ax1.set_xlabel("Períodos para Evasão")
    ax1.set_ylabel("Contagem", color="blue")
    ax1.tick_params(axis="y", labelcolor="blue")

    # Add labels on top of specific bars
    for p in ax1.patches:
        if int(p.get_x() + 0.5) in [1]:  # Only label bars for 1
            ax1.text(p.get_x() + p.get_width() / 2, p.get_height() + 2,  # Adjust vertical position
                     f"Desistências", ha="center", fontsize=12, color="black", fontweight="bold")
        if int(p.get_x() + 0.5) in [9]:  # Only label bars for 1
            ax1.text(p.get_x() + p.get_width() / 2, p.get_height() + 2,  # Adjust vertical position
                     f"Formandos", ha="center", fontsize=12, color="black", fontweight="bold")

    # Criar segundo eixo para a distribuição normal
    ax2 = ax1.twinx()
    ax2.plot(x, pdf, label="Distribuição Normal Estimada", color="red", linestyle="dashed")
    ax2.set_ylabel("Densidade", color="red")
    ax2.tick_params(axis="y", labelcolor="red")

    plt.title(title)
    plt.tight_layout()

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"Gráfico da normal salvo em {output_path}")


def read_and_clean_data(data_path: str) -> pd.DataFrame:
    # Read csv with ; separator
    df = pd.read_csv(data_path, sep=';')
    # Remove whitespaces from column names
    df.columns = df.columns.str.strip()
    # Strip all strings in the dataframe
    df = df.map(lambda x: x.strip() if isinstance(x, str) else x)
    # Remove linhas que não possuem '55 N' como código de curso
    df = df[df['COD_CURSO'] == '55 N']
    # Converte NUM_PERIODO_ALUNO para int
    df['NUM_PERIODO_ALUNO'] = df['NUM_PERIODO_ALUNO'].astype(int)
    return df

# Lendo os dados do arquivo argv
data_path = sys.argv[1]
df = read_and_clean_data(data_path)

num_periodos = df['NUM_PERIODO_ALUNO'].to_list()

# Dados para o modelo Stan
data = {
    'N': len(num_periodos),
    'x': num_periodos
}
print(f"\n\n>>Iniciando build do modelo...")
sm = stan.build(program_code=get_program_code("model.stan"), data=data)
# Ajustando o modelo com os dados
fit = sm.sample(num_chains=4)

# Imprimindo o resumo dos parâmetros
print("\n\n>Terminado build do modelo!")

posterior = fit.to_frame()

print("\n>Descrição dos parâmetros:")
print(posterior.describe())

plot_normal(num_periodos, posterior['mu'].mean(), posterior['sigma'].mean(), "Distribuição Normal da evasão Arquivologia", "figs/normal.png")

print("O maior fator para o gráfico não ter um comportamento de uma normal é o eixo x que está desordenado, em vez de estar em ordem crescente numérica.")
print("Ao plotar o gráfico com os dados verdadeiros, percebe-se um comportamento muito mais semelhante a uma normal (figs/normal.png). Ainda assim, \
o gráfico apresenta dois picos em vez de um único esperado por uma normal. Esse comportamento pode ser explicado pelas duas maiores formas de evasão:\n\
1. Desistência: O primeiro pico descreve os alunos que desistem ou são desligados do curso nos primeiros semestres.\n\
2. Formandos: O segundo pico descreve os alunos que se formam no curso, que é o objetivo final do curso e começa a acontecer mais entre os semestres 8 a 10.\n\")
