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


# Lendo os dados do arquivo argv
data_path = sys.argv[1]
df = read_and_clean_data(data_path)
# print(df.head())
num_periodos = df['NUM_PERIODO_ALUNO'].to_list()

# Dados para o modelo Stan
data = {
    'N': len(num_periodos),
    'x': num_periodos
}

sm = stan.build(program_code=get_program_code("model.stan"), data=data)
# Ajustando o modelo com os dados
fit = sm.sample(num_chains=4)

# Imprimindo o resumo dos parâmetros
print("\n\n>Terminado build do modelo!")

posterior = fit.to_frame()

print("\n>Descrição dos parâmetros:")
print(posterior.describe())

plot_normal(num_periodos, posterior['mu'].mean(), posterior['sigma'].mean(), "Distribuição Normal dos Períodos para Evasão", "figs/normal.png")


## a) Qual seria a probabilidade de um aluno qualquer terminar o curso em até 7 semestres?
print("\n\n>a) Probabilidade de um aluno qualquer terminar o curso em até 7 semestres:")
# Extrair as amostras de mu e sigma
mu_mean = posterior['mu'].mean()
sigma_mean = posterior['sigma'].mean()

# Define o limiar de 7 semestres
threshold = 7 

# Para cada amostra posterior, compute P(X < threshold) usando a CDF normal
posterior_probability = st.norm.cdf(threshold, loc=mu_mean, scale=sigma_mean)
print(f"{posterior_probability:.2%}")
print("\nValor calculado com base na média dos parâmetros mu e sigma estimados pelo modelo stan e a função cdf do scipy.")

## b) Qual a probabilidade de terminarem entre 8 e 10 semestres?
print("\n\n>b) Probabilidade de um aluno qualquer terminar o curso entre 8 e 10 semestres:")
# Define os limites de 8 e 10 semestres
lower_bound = 8
upper_bound = 10

# Para cada amostra posterior, compute P(lower_bound < X < upper_bound) usando a CDF normal
lower_bound_prob = st.norm.cdf(lower_bound, loc=mu_mean, scale=sigma_mean)
upper_bound_prob = st.norm.cdf(upper_bound, loc=mu_mean, scale=sigma_mean)
posterior_probability = upper_bound_prob - lower_bound_prob
print(f"{posterior_probability:.2%}")
print("\nValor calculado da mesma maneira para a probabilidade de 8 semestres subtraindo da probabilidade de 10 semestres.")


## c) Qual seria a maior das características daqueles que terminaram em mais de 8 semestres? 
print("\n\n>c) Maior característica dos alunos que terminaram em mais de 8 semestres:")
# Filtrar os alunos que terminaram em mais de 8 semestres
df_mais_de_8 = df[df['NUM_PERIODO_ALUNO'] > 8]
df_menos_de_8 = df[df['NUM_PERIODO_ALUNO'] <= 8]
# Plot histograma TIPO_COTA
plot_histogram(df_mais_de_8, df_menos_de_8, 'TIPO_COTA', "Distribuição de alunos por tipo de cota", "figs/tipo_cota.png")
# Plot ANO_EVASAO
plot_histogram(df_mais_de_8, df_menos_de_8, 'ANO_EVASAO', "Distribuição de alunos por ano de evasão", "figs/ano_evasao.png")
# Plot FORMA_EVASAO
plot_histogram(df_mais_de_8, df_menos_de_8, 'FORMA_EVASAO', "Distribuição de alunos por forma de evasão", "figs/forma_evasao.png")
# Plot SEXO
plot_histogram(df_mais_de_8, df_menos_de_8, 'SEXO', "Distribuição de alunos por sexo", "figs/sexo.png")
# Plot ETNIA
plot_histogram(df_mais_de_8, df_menos_de_8, 'ETNIA', "Distribuição de alunos por etnia", "figs/etnia.png")

print("\n\n>Terminado análise dos dados por meio dos gráficos de contagem, pode-se perceber a seguinte tendência:\n")
print("Alunos que entraram sem cota têm maior tendência de evadir o curso em menos de 8 semestres do que outros tipos de cota.\n")
print("Além disso, a metade dos alunos que evadiram antes de 8 semestres foi por desistência, enquanto a maioria dos alunos que evadiram após 8 semestres foi por terem se formado.\n")
print("Alunos do sexo feminino tiveram uma tendência maior de levar mais de 8 semestres para evadir do que os alunos homens.\n")
print("Por fim, as outras características não apresentaram diferenças significativas entre os grupos de alunos que evadiram em menos ou mais de 8 semestres.\n")


