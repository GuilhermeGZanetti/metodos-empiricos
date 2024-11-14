import stan
import numpy as np
import os
import matplotlib.pyplot as plt

def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
    

# Dados de exemplo
x = np.linspace(0, 10, 100)
y = 2 * x + 1 + np.random.normal(0, 1, 100)

# Dados para o modelo Stan
data = {
    'N': len(x),
    'x': x,
    'y': y
}

sm = stan.build(program_code=get_program_code("linear_regression.stan"), data=data)
# Ajustando o modelo com os dados
fit = sm.sample(num_chains=4)

# Imprimindo o resumo dos parâmetros
# print(fit)

df_params = fit.to_frame()

print(df_params.head())
print()
print(df_params.describe())

alpha = df_params['alpha'].mean()
beta = df_params['beta'].mean()

print(f"alpha: {alpha}")
print(f"beta: {beta}")

# plot pontos mais a reta ajustada

plt.scatter(x, y)
plt.plot(x, alpha + beta * x, 'r')
plt.show()




