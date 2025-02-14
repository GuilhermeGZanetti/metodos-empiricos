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

os.makedirs("figs", exist_ok=True)

# Boxplot com seaborn para plotar períodos por Sexo
sns.boxplot(data=df, x='SEXO', y='NUM_PERIODO_ALUNO')
plt.title("Boxplot dos períodos por Sexo")
plt.savefig("figs/boxplot_sexo.png")
plt.close()
print("-> Boxplot dos períodos por Sexo salvo em figs/boxplot_sexo.png\n")

print(">> Ao analisar o boxplot gerado, pode-se observar que a mediana, 1° e 3° quartis são muito similares para ambos os sexos, demonstrando um comportamento muito semelhante independente dessa característica.")
print("Entretando, o limite superior para homens é aproximadamente 3 períodos maior do que para as mulheres, indicando que há alguns poucos homens que demoram mais para evadir do que todas as mulheres.")


# Boxplot com seaborn para plotar períodos por TIPO_COTA
sns.boxplot(data=df, x='TIPO_COTA', y='NUM_PERIODO_ALUNO')
plt.xticks(rotation=45)
plt.title("Boxplot dos períodos por Tipo de Cota")
plt.savefig("figs/boxplot_cota.png")
plt.close()
print("\n\n-> Boxplot dos períodos por Tipo de Cota salvo em figs/boxplot_cota.png\n")

print(">> Ao analisar o boxplot gerado para os diferentes tipos de cota (formas de entrada do aluno), já é possível observar uma diferença mais significativa entre os grupos. Alunos de baixa renda e PPI possuem a maior mediana e terceiro quartis, indicando um maior tempo para evasão. Enquanto Ampla Concorrência e Renda Normal sem PPI possuem as menores medianas e primeiros quartis, indicando evasão mais rápida. Ampla concorrência também possui a maior variação interna em relação a outliers, tendo limites inferiores muito baixos e limites superiores muito altos.")

