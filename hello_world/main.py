import stan

def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()
# Ajustando o modelo com os dados
posterior = stan.build(get_program_code("hello_world.stan"))
fit = posterior.sample(num_chains=1, init=[{"y": 3}], num_samples=1, num_warmup=1)

print("hello world!")




