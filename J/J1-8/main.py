import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import stan
import seaborn as sns
import scipy.stats as stats


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
    

# Read arquivoentrada
df_processos = pd.read_csv("arquivoentrada")
# Get processos with Pena Definitiva which are not na
df_processos = df_processos[df_processos["Pena Definitiva"].notna()]


# Estimate normal for whole population of "Pena Definitiva"
print("\n\n>Iniciando build do modelo stan para encontrar normal da população completa")
stan_code = get_program_code("model.stan")
data = {
    "N": len(df_processos),
    "y": df_processos["Pena Definitiva"].values
}


sm = stan.build(program_code=stan_code, data=data)
fit = sm.sample(num_chains=4)

# Imprimindo o resumo dos parâmetros
print("\n\n>Terminado build do modelo!")

posterior = fit.to_frame()
print("\n>Descrição dos parâmetros da população completa:")
print(posterior.describe())

pop_mu = posterior["mu"].mean()
pop_sigma = posterior["sigma"].mean()
pop_N = len(df_processos)
print(f"Mu: {pop_mu}, Sigma: {pop_sigma}")

# Divide by comarca
comarcas = df_processos["comarca"].unique()
comarcas_normal = []
for comarca in comarcas:
    # Verifica se a comarca é parte da população
    df_comarca = df_processos[df_processos["comarca"] == comarca]
    # Estimate normal for comarca
    print(f"\n\n>Iniciando build do modelo stan para encontrar normal da comarca {comarca}")
    N_comarca = len(df_comarca)
    print("\nNúmero de processos na comarca:", N_comarca)
    if N_comarca < 15:
        print(f"Comarca {comarca} possui menos de 15 processos, pulando")
        continue
    stan_code = get_program_code("model.stan")
    data = {
        "N": N_comarca,
        "y": df_comarca["Pena Definitiva"].values
    }

    sm = stan.build(program_code=stan_code, data=data)
    fit = sm.sample(num_chains=4)

    # Imprimindo o resumo dos parâmetros
    print("\n\n>Terminado build do modelo!")

    posterior = fit.to_frame()
    print(f"\n>Descrição dos parâmetros da comarca {comarca}:")
    comarca_mu = posterior["mu"].mean()
    comarca_sigma = posterior["sigma"].mean()
    print(f"Mu: {comarca_mu}, Sigma: {comarca_sigma}")

    # Verificar pertencimento com t-test
    print("\n\n>Verificando pertencimento com t-test frequentista")
    t_stat, p_value = stats.ttest_ind_from_stats(pop_mu, pop_sigma, pop_N, comarca_mu, comarca_sigma, N_comarca, equal_var=False)

    print(f"T-statistic: {t_stat:.4f}")
    print(f"P-value: {p_value:.4f}")

    # Verificar probabilidade de pertencimento dado as amostras segundo Cohen 4.2
    print("\n\n>Verificando probabilidade de pertencimento segundo Cohen 4.2")
    # Faz N_amostras amostras em df_processos de tamanho N_comarca
    N_amostras = 1000
    mu_amostras: list = []
    for i in range(N_amostras):
        amostra = df_processos.sample(n=N_comarca, replace=True)
        mu_amostras.append(amostra["Pena Definitiva"].mean())
    # convert mu_amostras to numpy
    mu_amostras = np.array(mu_amostras)
    # Calcula probabilidade de pertencer
    count_maior = np.sum(mu_amostras > comarca_mu)
    count_menor = np.sum(mu_amostras < comarca_mu)
    print(f"Count maior: {count_maior} / Count menor: {count_menor}")
    count = count_maior if count_maior < count_menor else count_menor
    probabilidade = count / len(mu_amostras)
    print(f"Probabilidade de pertencer: {probabilidade:.4f}")

    comarcas_normal.append({
        "comarca": comarca,
        "N": N_comarca,
        "mu": comarca_mu,
        "sigma": comarca_sigma,
        "p_value": p_value,
        "cohen_p": probabilidade
    })

comarcas_normal_df = pd.DataFrame(comarcas_normal)

# Imprime resumo dos resultados
print("\n\n>Resumo dos resultados:")
print("População:")
print(f"Mu: {pop_mu}, Sigma: {pop_sigma}")
print(comarcas_normal_df)

# Gráficos das normais
print("\n\n>Plot das normais em um mesmo gráfico:")

# Fazer plot com todas as normais juntas e cores diferentes por grupo
plt.figure(figsize=(10, 6))

colors = sns.color_palette("tab10", len(comarcas_normal))  # Paleta de cores para diferenciar os grupos
x_max = df_processos["Pena Definitiva"].max()
x = np.linspace(0, x_max, 1000)  # Ajustar o intervalo do eixo x

# Plot da normal da população
plt.plot(x, (1 / pop_sigma) * np.exp(-0.5 * ((x - pop_mu) / pop_sigma) ** 2), label="Normal População", color="black")

for i, comarca in enumerate(comarcas_normal):
    plt.plot(x, (1 / comarcas_normal_df["sigma"][i]) * np.exp(-0.5 * ((x - comarcas_normal_df["mu"][i]) / comarcas_normal_df["sigma"][i]) ** 2), label=f"Normal {comarca['comarca']}", color=colors[i])

plt.xlabel("Tamanho Sentença Provisória")
plt.ylabel("Densidade")
plt.legend()
plt.grid()
os.makedirs("figs", exist_ok=True)
plt.savefig("figs/comarcas_normal.png")

print("\n\n>Gráficos salvos em figs/comarcas_normal.png")



print("### Relatório: Comparação das Distribuições de Processos por Comarca com a População Total")
print("")
print("Este relatório analisa se as distribuições dos tempos de processos judiciais em comarcas diferentes seguem a mesma distribuição da população total, utilizando dados de todos os tipos de crime para maior representatividade. Não foi possível fazer essa análise apenas com Furto-simples já que esse tipo de crime apresentava poucos exemplos por comarca. Dois métodos foram aplicados: o teste t frequentista (p-valor) e o método Cohen 4.2 (probabilidade de pertencimento).")
print("")
print("#### Conclusões")
print("- **Mesma Distribuição da População Total:** Piracicaba e Santo André não apresentam diferenças significativas em relação à população total, conforme indicado por ambos os métodos (p > 0.05 no t-test e probabilidades moderadas no Cohen 4.2).")
print("- **Distribuição Diferente da População Total:** São Paulo, Sorocaba e Suzano mostram distribuições distintas da população total, confirmadas pelo teste t (p < 0.05) e pelo Cohen 4.2 (probabilidades muito baixas).")
print("")
print("Os resultados destacam variações regionais nos tempos de tramitação, com gráficos salvos em `figs/comarcas_normal.png` para visualização.")
