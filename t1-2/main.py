print("Não consegui implementar a lógica do modelo com Stan após muita pesquisa, então realizei com Python convencional:")

# Dados iniciais
p_sunny_today = 0.2
p_not_sunny_today = 0.8
p_hello_given_sunny = 0.6
p_sunny_tomorrow_given_sunny = 0.8
p_sunny_tomorrow_given_not_sunny = 0.05

# 1. Predizer o cumprimento de hoje
p_hello_today = p_sunny_today * 0.6 + p_not_sunny_today * 0.2
p_howdy_today = p_sunny_today * 0.4
p_ohno_today = p_not_sunny_today * 0.8

# 2. Inferir o clima de hoje dado que a saudação de hoje é "Hello, world!"  
# Utilizando o Teorema de Bayes:
p_sunny_given_hello = (p_hello_given_sunny * p_sunny_today) / p_hello_today

# 3. Prever a saudação de amanhã após observar "Hello, world!" hoje
# Calcular as probabilidades do clima de amanhã
p_sunny_tomorrow_given_sunny = 0.8
p_sunny_tomorrow_given_not_sunny = 0.05

p_sunny_tomorrow = (p_sunny_given_hello * p_sunny_tomorrow_given_sunny +
                    (1 - p_sunny_given_hello) * p_sunny_tomorrow_given_not_sunny)
p_not_sunny_tomorrow = 1 - p_sunny_tomorrow

# Calcular as probabilidades da saudação de amanhã
p_hello_tomorrow = p_sunny_tomorrow * 0.6 + p_not_sunny_tomorrow * 0.2
p_howdy_tomorrow = p_sunny_tomorrow * 0.4
p_ohno_tomorrow = p_not_sunny_tomorrow * 0.8

# Exibir os resultados
print("1. Probabilidades da saudação de hoje:")
print(f"  'Hello, world!': {p_hello_today:.4f}")
print(f"  'Howdy, universe!': {p_howdy_today:.4f}")
print(f"  'Oh no, not again': {p_ohno_today:.4f}\n")

print("2. Probabilidade de hoje estar ensolarado dado 'Hello, world!':")
print(f"  {p_sunny_given_hello:.4f}\n")

print("3. Probabilidades da saudação de amanhã após observar 'Hello, world!':")
print(f"  'Hello, world!': {p_hello_tomorrow:.4f}")
print(f"  'Howdy, universe!': {p_howdy_tomorrow:.4f}")
print(f"  'Oh no, not again': {p_ohno_tomorrow:.4f}")

