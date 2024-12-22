import os
import json
import numpy as np
import matplotlib.pyplot as plt
import stan

# Função para carregar o modelo Stan
def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()

# Função para carregar dados JSON
def load_json_data(json_path: str):
    with open(json_path, 'r') as file:
        return json.load(file)

# Função para extrair os tempos de pena de um conjunto de dados
def extract_sentence_times(data, key="Pena Definitiva"):
    return np.array([item[key] for item in data])

# Função para ajustar o modelo e retornar os resultados
def fit_stan_model(data, model_path):
    stan_data = {
        "N": len(data),
        "y": data,
    }
    program_code = get_program_code(model_path)
    sm = stan.build(program_code=program_code, data=stan_data)
    fit = sm.sample(num_chains=4)
    return fit.to_frame()

# Função para plotar os resultados
def plot_results(times, mu_mean, sigma_mean, title, output_path):
    x = np.linspace(0, max(times) * 1.2, 1000)  # Ajustar o intervalo do eixo x
    pdf = (1 / (sigma_mean * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_mean) / sigma_mean) ** 2)

    plt.hist(times, bins=15, density=True, alpha=0.5, label="Dados observados")
    plt.plot(x, pdf, label="Distribuição Normal Estimada", color="red")
    plt.title(title)
    plt.xlabel("Tempo de Sentença")
    plt.ylabel("Densidade")
    plt.legend()
    plt.grid()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.show()

# Função para filtrar dados por tipo de crime
def filter_data_by_type(data, crime_type):
    return [item for item in data if item["Tipo"] == crime_type]

# Função principal
def main():
    # Caminhos dos arquivos
    json_path = "processos.json"
    model_path = "model.stan"

    # Carregar os dados
    data = load_json_data(json_path)

    # Processar todos os dados juntos
    times_all = extract_sentence_times(data)
    fit_results_all = fit_stan_model(times_all, model_path)
    mu_all = fit_results_all["mu"].mean()
    sigma_all = fit_results_all["sigma"].mean()
    print(f"Todos os crimes - Média estimada (mu): {mu_all:.2f}, Desvio padrão estimado (sigma): {sigma_all:.2f}")
    plot_results(times_all, mu_all, sigma_all, "Todos os Crimes", "figs/all_crimes_distribution.png")

    # Processar dados por tipo de crime
    crime_types = ["roubo_simples", "roubo_qualificado", "trafico"]
    for crime in crime_types:
        filtered_data = filter_data_by_type(data, crime)
        times = extract_sentence_times(filtered_data)
        if len(times) > 0:
            fit_results = fit_stan_model(times, model_path)
            mu = fit_results["mu"].mean()
            sigma = fit_results["sigma"].mean()
            print(f"{crime.capitalize()} - Média estimada (mu): {mu:.2f}, Desvio padrão estimado (sigma): {sigma:.2f}")
            plot_results(
                times,
                mu,
                sigma,
                f"Distribuição para {crime.capitalize()}",
                f"figs/{crime}_distribution.png",
            )
        else:
            print(f"Não há dados suficientes para o crime: {crime}")

if __name__ == "__main__":
    main()
