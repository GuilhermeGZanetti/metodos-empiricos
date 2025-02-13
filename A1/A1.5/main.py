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
    x = np.linspace(0, max(times) * 1.2, 1000)  # Ajustar o intervalo do eixo x
    pdf = (1 / (sigma_mean * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_mean) / sigma_mean) ** 2)

    plt.hist(times, bins=15, density=True, alpha=0.5, label="Dados observados")
    plt.plot(x, pdf, label="Distribuição Normal Estimada", color="red")
    plt.title(title)
    plt.xlabel("Períodos para Evasão")
    plt.ylabel("Densidade")
    plt.legend()
    plt.grid()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico da normal salvo em {output_path}")

def plot_histogram(df1, df2, column_name, title, output_path):
    # Assign groups
    df1 = df1.copy()  # Ensure df1 is a new copy
    df2 = df2.copy()  # Ensure df2 is a new copy
    df1.loc[:, "Grupo"] = "Mais de 8 semestres"
    df2.loc[:, "Grupo"] = "Menos de 8 semestres"
    df_combined = pd.concat([df1, df2])
    # Compute value counts normalized by group
    counts = df_combined.groupby(["Grupo", column_name]).size().reset_index(name="count")
    # Convert absolute counts to proportions within each group
    counts["proportion"] = counts.groupby("Grupo")["count"].transform(lambda x: x / x.sum())
    plt.figure(figsize=(12, 6))  # Set figure size
    # Plot normalized proportions instead of raw counts
    sns.barplot(data=counts, x=column_name, y="proportion", hue="Grupo")

    plt.legend(title="Grupo")
    plt.title(title)
    plt.xlabel(column_name)
    plt.ylabel("Proporção")
    
    plt.xticks(rotation=45, ha="right")
    plt.tight_layout()

    plt.savefig(output_path, bbox_inches="tight")
    plt.close()
    print(f"\nGráfico salvo em {output_path}")



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

    plot_normal(num_periodos, posterior['mu'].mean(), posterior['sigma'].mean(), f"Distribuição Normal da evasão para Grupo {group}", f"figs/normal_{group}.png")

    return {
        'group': group,
        'mu': posterior['mu'].mean(),
        'sigma': posterior['sigma'].mean()
    }

# Lendo os dados do arquivo argv
data_path = sys.argv[1]
df = read_and_clean_data(data_path)

print(">>>>>> Os ingressantes do curso serão divididos em grupos devido ao tipo de cota de ingresso. Sendo eles:")
print(df['TIPO_COTA'].unique())

models = []
for group in df['TIPO_COTA'].unique():
    df_group = df[df['TIPO_COTA'] == group]

    num_periodos = df_group['NUM_PERIODO_ALUNO'].to_list()

    # Dados para o modelo Stan
    data = {
        'N': len(num_periodos),
        'x': num_periodos
    }
    model = build_model(data, group)
    models.append(model)

# Fazer plot com todas as normais juntas e cores diferentes por grupo
plt.figure(figsize=(10, 6))

colors = sns.color_palette("tab10", len(models))  # Paleta de cores para diferenciar os grupos
x_max = max([max(df[df['TIPO_COTA'] == model['group']]['NUM_PERIODO_ALUNO']) for model in models]) * 1.2
x = np.linspace(0, x_max, 1000)  # Ajustar o intervalo do eixo x

for i, model in enumerate(models):
    mu, sigma = model['mu'], model['sigma']
    pdf = (1 / (sigma * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu) / sigma) ** 2)
    plt.plot(x, pdf, label=f"Grupo {model['group']}", color=colors[i])

plt.title("Distribuições Normais Estimadas para Cada Grupo")
plt.xlabel("Períodos para Evasão")
plt.ylabel("Densidade")
plt.legend()
plt.grid()

output_path = "figs/normal_todos_grupos.png"
os.makedirs(os.path.dirname(output_path), exist_ok=True)
plt.savefig(output_path)
plt.close()
print(f">> Gráfico comparativo de todos os grupos salvo em {output_path}")

print("\n\n> Analisando o gráfico comparativo com as normais de todos os tipos de ingressantes, \
podemos observar que existe uma diferença estatísticamente significativa entre as distribuições dos grupos.\n\
Em especial, pode-se perceber que o grupo de Baixa Renda e PPI tem uma maior média de períodos para evasão, \
enquanto os grupos 'Renda Normal e não PPI' e 'Ampla Concorrencia' tem uma média menor de períodos para evasão. \
Isso pode ser explicado por uma aparente maior número de desistência desses últimos grupos nos primeiros períodos do curso.")




