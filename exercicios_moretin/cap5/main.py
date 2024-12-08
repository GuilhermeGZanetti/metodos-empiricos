import matplotlib.pyplot as plt
import numpy as np

# Experimento dos dados
# Com um dado de 6 lados, e 10 experimentos, fazer tabela com ocorrências
dados = np.random.randint(1, 7, size=(10))
print("Experimento 10 dados")
print(dados)

# Draw plot of ocurrences
plt.hist(dados, bins=[1, 2, 3, 4, 5, 6, 7], edgecolor='black')
plt.show()

# Refaz experimento 100 vezes
dados = np.random.randint(1, 7, size=(100))
print("Experimento 100 dados")
print(dados)

# Draw plot of ocurrences
plt.hist(dados, bins=[1, 2, 3, 4, 5, 6, 7], edgecolor='black')
plt.show()

print("O experimento simula lançamentos de um dado de 6 lados, mostrando a distribuição das faces em 10 e 100 lançamentos. Para 100 lançamentos, o histograma tende a se aproximar das probabilidades calculadas.")

