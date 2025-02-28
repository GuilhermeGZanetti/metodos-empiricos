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



print(">> Rodando Procedure 5.3 do Cohen Cap. 5.2...")

print("> Para uma amostra S com 10 elementos, fazer amostragem bootstrap para obter a distribuição 'bootstrapped' da média censurada da população.")
data = {
    'N': 10,
    'S': [287, 610, 545, 400, 123, 5000, 5000, 601, 483, 250],
    'c': 5000
}
sm = stan.build(program_code=get_program_code("model_5.3.stan"), data=data)
fit = sm.fixed_param(num_chains=1, num_samples=1000)

posterior = fit.to_frame()
mean_xc = []
for i in range(1000):
    sum_xc_i = 0
    num_x_i = 0
    for j in range(10):
        x_i = posterior.loc[i, 'Si.{}'.format(j+1)]
        if x_i < 5000:
            sum_xc_i += x_i
            num_x_i += 1
    mean_xc.append(sum_xc_i / num_x_i)

print("\n\n> Resultados:")
amostra_censurada = []
for i in range(data['N']):
    if data['S'][i] < data['c']:
        amostra_censurada.append(data['S'][i])
print("> Média censurada da amostra original: ", np.mean(amostra_censurada))
print("> Média da amostra bootstrap: ", np.mean(mean_xc))
print("> Desvio padrão da amostra bootstrap: ", np.std(mean_xc))

print("> Plotando histograma da média censurada da população estimada com bootstrap...")   
plot_hist(mean_xc, positive_limit=None, title="Distribuição da média censurada", output_path="figs/5_3.png")

print("Ao realizar o bootstrap para obter a distribuição 'bootstrapped' da média censurada da população, conseguimos além de um estimador da média da população, também o desvio padrão dessa estimativa. Com isso, podemos ter uma ideia da variabilidade da média censurada da população, e não apenas um único valor estimado. Essa é uma grande vantagem deste método empírico ao se comparar com o método clássico de apenas calcular a média da amostra original.")




print("\n\n#############")
print(">> Rodando Procedure 5.5 Bootstrap Sampling with Randomization for a Two-Sample Test")
print("> Tendo duas amostras Sa e Sb com valores censurados, o objetivo é usar bootstrap para obter a distriubição da diferença das médias censuradas sob a hipótese nula de que Sa e Sb são amostras da mesma população. Assim, será possível comparar a diferença real das amostras para verificar se ela é significativa.")
data = {
    'N_a': 10,
    'S_a': [300, 290, 600, 5000, 200, 600, 30, 800, 55, 190],
    'N_b': 10,
    'S_b': [400, 280, 5000, 5000, 300, 820, 120, 5000, 120, 400],
    'c': 5000
}
sm = stan.build(program_code=get_program_code("model_5.5.stan"), data=data)
fit = sm.fixed_param(num_chains=1, num_samples=1000)

posterior = fit.to_frame()
mean_diff = posterior['mean_diff'].to_numpy()
print("\n\n> Resultados:")
print("> Diferença das amostras originais das médias censuradas: -8,02")
print("> Média da diferença das médias censuradas: ", np.mean(mean_diff))
print("> Desvio padrão da diferença das médias censuradas: ", np.std(mean_diff))

print("> Plotando histograma da diferença das médias censuradas estimada com bootstrap...")
plot_hist(mean_diff, positive_limit=-8.02, title="Distribuição da diferença das médias censuradas", output_path="figs/5_5.png")

proporcao = np.sum(mean_diff < -8.02) / 1000
print("> Proporção de valores menores que -8,02: ", proporcao)
print("Como a proporção de valores menores que -8,02 é muito maior que 0,05, não podemos rejeitar a hipótese nula de que Sa e Sb são amostras da mesma população.")
