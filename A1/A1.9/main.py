

import stan
import numpy as np
import os
import sys
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import scipy.stats as st

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
    df['PERIODO_INGRESSO'] = df['PERIODO_INGRESSO'].str[0].astype(int)
    df['ANO_INGRESSO'] = df['ANO_INGRESSO'].astype(int)
    df['ANO_EVASAO'] = df['ANO_EVASAO'].astype(int)
    return df

# Lendo os dados do arquivo argv
data_path = sys.argv[1]
df = read_and_clean_data(data_path)

os.makedirs('figs', exist_ok=True)

# Pegar apenas colunas numéricas
df = df.select_dtypes(include=[np.number])

# Criando matrix de correlação entre NUM_PERIODO_ALUNO e todas as outras colunas
correlation_matrix = df.corr()
# Plotando a matrix de correlação
sns.heatmap(correlation_matrix, annot=True)
plt.title('Correlation Matrix')
plt.tight_layout()
plt.savefig('figs/correlation_matrix.png')
print("Correlation Matrix saved at figs/correlation_matrix.png")

# Print column NUM_PERIODO_ALUNO
print("NUM_PERIODO_ALUNO Correlação com os outros features numéricos:")
print(correlation_matrix['NUM_PERIODO_ALUNO'])

print("\n\n>> Ao analisar a matriz de correlação, percebemos que a coluna NUM_PERIODO_ALUNO possui uma forte correlação negativa com a coluna ANO_INGRESSO. Isso faz sentido, já que os dados só mostram alunos que já evadiram, portanto aqueles com maior ANO_INGRESSO são os que com tempo menor do que a diferença entre o ingresso e a data da coleta de dados. Ou seja, alunos que ingressaram nos anos mais recentes mas ainda não evadiram não estão nos dados.")
print("Além dessa informação, não há mais nenhuma correlação entre NUM_PERIODO_ALUNO e os outros features numéricos de ANO_EVASAO e PERIODO_INGRESSO.")

