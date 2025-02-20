import numpy as np
from scipy.stats import expon

# Exemplo 5.15: Aproximação da integral ∫[0,1] x^4 dx
u = np.random.uniform(0, 1, 100000)
approx_5_15 = np.mean(u**4)
print(f"Exemplo 5.15 - ∫[0,1] x^4 dx: {approx_5_15:.6f} (Valor exato: 0.2)")

# Exemplo 5.16: Aproximação da integral ∫[2,5] sin(x) dx
u = np.random.uniform(2, 5, 100000)
approx_5_16 = np.mean(np.sin(u)) * (5 - 2)
print(f"Exemplo 5.16 - ∫[2,5] sin(x) dx: {approx_5_16:.6f} (Valor exato: -0.700)")

# Exemplo 5.17: Aproximação da integral dupla ∫[3,10] ∫[1,7] sin(x - y) dx dy
U = np.random.uniform(1, 7, 10000000)
V = np.random.uniform(3, 10, 10000000)
approx_5_17 = np.mean(np.sin(U - V)) * (7 - 1) * (10 - 3)
print(f"Exemplo 5.17 - ∫[3,10] ∫[1,7] sin(x - y) dx dy: {approx_5_17:.6f} (Valor exato: 0.119)")
print("Obs.: Aproximação com 10^7 amostras, para ter maior precisão")

# Exemplo 5.18: Aproximação da integral ∫[1,∞] exp(-x²) dx usando uma distribuição exponencial
X = np.random.exponential(scale=1, size=100000)
approx_5_18 = np.mean(np.exp(-(X + 1)**2) / (np.exp(-X)))
print(f"Exemplo 5.18 - ∫[1,∞] exp(-x²) dx: {approx_5_18:.6f} (Valor exato: 0.1394)")





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
