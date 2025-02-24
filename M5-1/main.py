import contextlib
import os
import time
import numpy as np
import stan


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
    
    
@contextlib.contextmanager
def suppress_stdout_stderr():
    with open(os.devnull, 'w') as devnull:
        old_stdout = os.dup(1)
        old_stderr = os.dup(2)
        try:
            os.dup2(devnull.fileno(), 1)
            os.dup2(devnull.fileno(), 2)
            yield
        finally:
            os.dup2(old_stdout, 1)
            os.dup2(old_stderr, 2)
            # Don't close old_stdout or old_stderr!


def get_sample(lower_bound: float, upper_bound: float, n: int) -> np.ndarray:
    data = {
        'lower_bound': lower_bound,
        'upper_bound': upper_bound
    }
    # Suppress output from pystan build and sampling
    with suppress_stdout_stderr():
        sm = stan.build(program_code=get_program_code("model.stan"), data=data)
        fit = sm.sample(num_chains=1, num_samples=n)
    
    posterior = fit.to_frame()
    return posterior['x'].to_numpy()

print("Gerando algumas amostras com STAN. Isso pode demorar alguns minutos porque o STAN é mais lento que o numpy.")

# Fazer todas as amostras aqui
u_5_15_stan = get_sample(0, 1, 100000)
u_5_16_stan = get_sample(2, 5, 100000)

# Comparação de tempo de execução entre numpy e stan
tempo_stan = time.time()
get_sample(2, 7, 100000)
tempo_stan = time.time() - tempo_stan

tempo_numpy = time.time()
np.random.uniform(2, 7, 100000)
tempo_numpy = time.time() - tempo_numpy

n = 10000
x = get_sample(2, 7, n)
print(f"Exemplo com stan, realizando {n} amostras uniformes de ]2, 7[: ")
#print(f"Amostra de {n} valores entre 0 e 1: {x}")
print(f"Valor médio da amostra: {np.mean(x)}")
print(f"Desvio padrão da amostra: {np.std(x)}")
print(f"Tamanho da amostra: {len(x)}")
# max e min
print(f"Valor máximo da amostra: {np.max(x)}")
print(f"Valor mínimo da amostra: {np.min(x)}")

print(f"\n\nComparação entre tempo para geração de 10000 amostras com numpy e stan.\n>Tempo de execução com stan: {tempo_stan:.6f} segundos")
print(f">Tempo de execução com numpy: {tempo_numpy:.6f} segundos")

print("\n>Assim, o stan pode ser usado para gerar as amostras em distribuições uniformes em comparação com o numpy nos exemplos 5.15 e 5.16.\n")


# Exemplo 5.15: Aproximação da integral ∫[0,1] x^4 dx
u = np.random.uniform(0, 1, 100000)
approx_5_15 = np.mean(u**4)
approx_5_15_stan = np.mean(u_5_15_stan**4)
print(f"\n> Exemplo 5.15 com  - ∫[0,1] x^4 dx: {approx_5_15:.6f} - np / {approx_5_15_stan} - stan / (Valor exato: 0.2)")


# Exemplo 5.16: Aproximação da integral ∫[2,5] sin(x) dx
u = np.random.uniform(2, 5, 100000)
approx_5_16 = np.mean(np.sin(u)) * (5 - 2)
approx_5_16_stan = np.mean(np.sin(u_5_16_stan)) * (5 - 2)
print(f"Exemplo 5.16 - ∫[2,5] sin(x) dx: {approx_5_16:.6f} - np / {approx_5_16_stan} - stan / (Valor exato: -0.700)")

# Exemplo 5.17: Aproximação da integral dupla ∫[3,10] ∫[1,7] sin(x - y) dx dy
U = np.random.uniform(1, 7, 10000000)
V = np.random.uniform(3, 10, 10000000)
approx_5_17 = np.mean(np.sin(U - V)) * (7 - 1) * (10 - 3)
print(f"Exemplo 5.17 - ∫[3,10] ∫[1,7] sin(x - y) dx dy: {approx_5_17:.6f} - np / (Valor exato: 0.119)")
print("Obs.: Aproximação com 10^7 amostras, para ter maior precisão")

# Exemplo 5.18: Aproximação da integral ∫[1,∞] exp(-x²) dx usando uma distribuição exponencial
X = np.random.exponential(scale=1, size=100000)
approx_5_18 = np.mean(np.exp(-(X + 1)**2) / (np.exp(-X)))
print(f"Exemplo 5.18 - ∫[1,∞] exp(-x²) dx: {approx_5_18:.6f} (Valor exato: 0.1394)")


print("\n\n>Após os exemplos acima, é possível observar que os resultados com stan são muito similares aos resultados com numpy. \
Assim, devido ao tempo muito maior para geração com stan, os exercícios seguintes serão feitos com numpy.\n")





print("\n\nExercício 1:")
# Exercício 1: Aproximar integrais simples
# ∫[0,1] x dx
u = np.random.uniform(0, 1, 100000)
approx_1 = np.mean(u) * (1 - 0)
print(f"Exercício 1.1 - ∫[0,1] x dx: {approx_1:.6f} (Valor exato: 0.5)")

# ∫[1,3] x^2 dx
u = np.random.uniform(1, 3, 100000)
approx_2 = np.mean(u**2) * (3 - 1)
print(f"Exercício 1.2 - ∫[1,3] x^2 dx: {approx_2:.6f} (Valor exato: 8.6667)")

# ∫[0,π] sin(x) dx
u = np.random.uniform(0, np.pi, 100000)
approx_3 = np.mean(np.sin(u)) * np.pi
print(f"Exercício 1.3 - ∫[0,π] sin(x) dx: {approx_3:.6f} (Valor exato: 2)")

# ∫[1,π] exp(x) dx
u = np.random.uniform(1, np.pi, 100000)
approx_4 = np.mean(np.exp(u)) * (np.pi - 1)
print(f"Exercício 1.4 - ∫[1,π] exp(x) dx: {approx_4:.6f} (Valor exato: {np.exp(np.pi) - np.exp(1):.6f})")

# ∫[0,∞] exp(-x) dx
X = np.random.exponential(scale=1, size=1000000)
approx_5 = np.mean(np.exp(-X) / (np.exp(-X))) 
print(f"Exercício 1.5 - ∫[0,∞] exp(-x) dx: {approx_5:.6f} (Valor exato: 1.000)")

# ∫[0,∞] exp(-x^3) dx
X = np.random.exponential(scale=1, size=1000000)
approx_6 = np.mean(np.exp(-X**3) / (np.exp(-X))) 
print(f"Exercício 1.6 - ∫[0,∞] exp(-x^3) dx: {approx_6:.6f} (Valor exato: 0.893)")

# ∫[0,3] sin(exp(x)) dx
u = np.random.uniform(0, 3, 100000)
approx_7 = np.mean(np.sin(np.exp(u))) * (3 - 0)
print(f"Exercício 1.7 - ∫[0,3] sin(exp(x)) dx: {approx_7:.6f} (Valor exato: 0.606)")

# ∫[0,1] (1/sqrt(2π)) exp(-x²/2) dx
u = np.random.uniform(0, 1, 100000)
approx_8 = np.mean((1/np.sqrt(2*np.pi)) * np.exp(-u**2/2)) * (1 - 0)
print(f"Exercício 1.8 - ∫[0,1] (1/sqrt(2π)) exp(-x²/2) dx: {approx_8:.6f} (Valor exato: 0.341)")

# ∫[0,2] (1/sqrt(2π)) exp(-x²/2) dx
u = np.random.uniform(0, 2, 100000)
approx_9 = np.mean((1/np.sqrt(2*np.pi)) * np.exp(-u**2/2)) * (2 - 0)
print(f"Exercício 1.9 - ∫[0,2] (1/sqrt(2π)) exp(-x²/2) dx: {approx_9:.6f} (Valor exato: 0.477)")

# ∫[0,3] (1/sqrt(2π)) exp(-x²/2) dx
u = np.random.uniform(0, 3, 100000)
approx_10 = np.mean((1/np.sqrt(2*np.pi)) * np.exp(-u**2/2)) * (3 - 0)
print(f"Exercício 1.10 - ∫[0,3] (1/sqrt(2π)) exp(-x²/2) dx: {approx_10:.6f} (Valor exato: 0.499)")




print("\n\nExercício 2:")
# Exercício 2: Aproximar integrais duplas
# ∫[0,1] ∫[0,1] cos(x - y) dx dy
U = np.random.uniform(0, 1, 100000)
V = np.random.uniform(0, 1, 100000)
approx_2_1 = np.mean(np.cos(U - V)) * (1 - 0) * (1 - 0)
print(f"Exercício 2.1 - ∫[0,1] ∫[0,1] cos(x - y) dx dy: {approx_2_1:.6f} (Valor exato: 0.919)")

# ∫[0,1] ∫[0,1] e^-(y+x)^2 / (x + y)^2 dx dy
U = np.random.uniform(0, 1, 100000)
V = np.random.uniform(0, 1, 100000)
approx_2_2 = np.mean(np.exp(-(U + V)**2) / (U + V)**2) * (1 - 0) * (1 - 0)
print(f"Exercício 2.2 - ∫[0,1] ∫[0,1] e^-(y+x)^2 / (x + y)^2 dx dy: {approx_2_2:.6f} (Valor exato: Indefinido)")

# ∫[0,3] ∫[0,1] cos(x - y) dx dy
U = np.random.uniform(0, 1, 100000)
V = np.random.uniform(0, 3, 100000)
approx_2_3 = np.mean(np.cos(U - V)) * (1 - 0) * (3 - 0)
print(f"Exercício 2.3 - ∫[0,3] ∫[0,1] cos(x - y) dx dy: {approx_2_3:.6f} (Valor exato: 1.0335)")

# ∫[0,5] ∫[0,2] e^-(y+x)^2 / (x + y)^2 dx dy
U = np.random.uniform(0, 2, 100000)
V = np.random.uniform(0, 5, 100000)
approx_2_4 = np.mean(np.exp(-(U + V)**2) / (U + V)**2) * (2 - 0) * (5 - 0)
print(f"Exercício 2.4 - ∫[0,5] ∫[0,2] e^-(y+x)^2 / (x + y)^2 dx dy: {approx_2_4:.6f} (Valor exato: Indefinido)")
