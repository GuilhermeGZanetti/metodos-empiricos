import contextlib
import os
import time
import numpy as np
import stan
import matplotlib.pyplot as plt


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
    
def plot_hist(times: list, positive_limit: float, title: str, output_path: str):
    times = np.array(times)  # Convertendo para um array numpy
    
    # Separando os valores
    below_limit = times[times <= positive_limit]
    above_limit = times[times > positive_limit]
    
    # Criando o histograma
    plt.hist(below_limit, bins=15, alpha=0.5, color='blue', label="≤ limite")
    plt.hist(above_limit, bins=15, alpha=0.5, color='red', label="> limite")
    
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



print(">> Rodando Procedure 5.1 do Cohen Cap. 5.1...")

print("> Para uma distribuição normal com média 50 e desvio padrão 5, calculando o IQR de 20 amostras 500 vezes...")
data = {
    'N': 20,
    'mu': 50,
    'sigma': 5
}
sm = stan.build(program_code=get_program_code("model_5.1.stan"), data=data)
fit = sm.fixed_param(num_chains=1, num_samples=500)

posterior = fit.to_frame()
IQRs = posterior['IQR'].to_numpy()
print(f"\n\n>>>> Resultado:\n> Média dos IQRs: {np.mean(IQRs)}")
print(f"> Desvio padrão dos IQRs: {np.std(IQRs)}")

print("> Plotando histograma dos IQRs amostrados por Monte Carlo...")
plot_hist(IQRs, positive_limit=8.5, title="Distribuição dos IQRs", output_path="figs/5_1.png")
print("> Calculando proporção de IQRs acima de 8.5...")
above_limit = np.sum(IQRs > 8.5) / len(IQRs)
print(f"> Proporção de IQRs acima de 8.5: {above_limit}")
print(f"Como a proporção de IQR* acima de 8.5 é de {above_limit:.2f}, ele não é significativamente diferente do esperado de uma amostra aleatória, porém está bem perto desse limite.")



print("\n\n#############")
print(">> Rodando Procedure 5.2 do Cohen Cap. 5.1...")

print("> Para duas distribuições normais A e B com médias mu_a=50 e mu_b=53 e desvios padrão sigma_a=5 e sigma_b=6, calculando a diferença entre o IQR de Sa de Na=20 e de Sb de Nb=25 amostras 500 vezes...")
data = {
    'N_a': 20,
    'mu_a': 50,
    'sigma_a': 5,
    'N_b': 25,
    'mu_b': 53,
    'sigma_b': 6
}
sm = stan.build(program_code=get_program_code("model_5.2.stan"), data=data)
fit = sm.fixed_param(num_chains=1, num_samples=500)

posterior = fit.to_frame()
delta_IQR = posterior['delta_IQR'].to_numpy()
print(f"\n\n>>>> Resultado:\n> Média da diferença dos IQRs: {np.mean(delta_IQR)}")
print(f"> Desvio padrão da diferença dos IQRs: {np.std(delta_IQR)}")

print("> Plotando histograma da diferença dos IQRs amostrados por Monte Carlo...")
plot_hist(delta_IQR, positive_limit=2.5, title="Distribuição da diferença dos IQRs", output_path="figs/5_2.png")
print("> Calculando proporção de diferenças de IQRs acima de 2.5...")
above_limit = np.sum(delta_IQR > 2.5) / len(delta_IQR)
print(f"> Proporção de diferenças de IQRs acima de 2.5: {above_limit}")
if above_limit > 0.05:
    print(f"Como a proporção de diferenças de IQR* acima de 2.5 é de {above_limit:.2f} > 0.05, mais uma vez, esse valor indica que ele não é significativamente diferente do esperado de uma amostra aleatória, ainda que esteja muito próximo do limite.")
else:
    print(f"Como a proporção de diferenças de IQR* acima de 2.5 é de {above_limit:.2f} < 0.05, ele é significativamente diferente do esperado de uma amostra aleatória, então a hipótese nula de que ambas as populações tem a mesma distribuição de IQRs pode ser rejeitada.")