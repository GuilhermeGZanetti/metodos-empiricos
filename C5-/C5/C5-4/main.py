import contextlib
import os
import time
import numpy as np
import stan
import matplotlib.pyplot as plt


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
    
def plot_hist(times: list, positive_limit: float | None, title: str, output_path: str):
    times = np.array(times)  # Convertendo para um array numpy
    
    if positive_limit is not None:
        # Separando os valores
        below_limit = times[times <= positive_limit]
        above_limit = times[times > positive_limit]
    
        # Criando o histograma
        plt.hist(below_limit, bins=15, alpha=0.5, color='blue', label="≤ limite")
        plt.hist(above_limit, bins=15, alpha=0.5, color='red', label="> limite")
    else:
        # Criando o histograma
        plt.hist(times, bins=15, alpha=0.5, color='blue')
    
    # Configurações do gráfico
    plt.title(title)
    plt.xlabel("IQR*")
    plt.ylabel("Frequência")
    plt.legend()
    plt.grid()
    
    # Salvando o arquivo
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico do histograma salvo em {output_path}")



print(">> Rodando Procedure 5.6 do Cohen Cap. 5.2...")

data = {
    'x' :[5,
1.75,
.8,
5,
1.75,
5,
1.75,
1,
5,
1.75,
    ],
    'y': [27.8,
20.82,
44.12,
29.41,
31.19,
28.68,
29.53,
34.62,
20,
41.54],
    'N': 10
}

sm = stan.build(program_code=get_program_code("model_5.6.stan"), data=data)
fit = sm.sample(num_chains=1, num_samples=1000)

posterior = fit.to_frame()
print(posterior)

corr_mu = posterior['corr_mu'].to_numpy()
corr_sigma = posterior['sigma'].to_numpy()

print("mu primeiros 5% : ", np.percentile(corr_mu, 5))
print("mu 95% : ", np.percentile(corr_mu, 95))

print(f"Intervalo de 90% para mu segundo o stan: [{np.percentile(corr_mu, 5)}, {np.percentile(corr_mu, 95)}")
print("Intervalo de 90% para mu segundo o livro: [-0.834, -0.123]")
