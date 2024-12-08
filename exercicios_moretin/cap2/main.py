import matplotlib.pyplot as plt
import numpy as np


print("O que seriam variáveis Qualitativas?")
print("Resposta: Variáveis qualitativas são variáveis que representam uma qualidade ou categoria do ponto de dados, como 'alto', 'medio' ou 'baixo'.")


def create_bar_plot(categories, frequencies, xlabel, ylabel, title, ylim=None, color='gray', edgecolor='black', output_figname="fig2.2.png"):
    """
    Creates a bar plot with the given parameters.
    
    Parameters:
        categories (list): List of category names or numbers for the x-axis.
        frequencies (list): List of frequencies for each category.
        xlabel (str): Label for the x-axis.
        ylabel (str): Label for the y-axis.
        title (str): Title of the bar plot.
        ylim (tuple, optional): Limits for the y-axis (min, max). Default is None.
        color (str, optional): Color of the bars. Default is 'gray'.
        edgecolor (str, optional): Color of the bar edges. Default is 'black'.
    """
    plt.figure(figsize=(6, 4))
    plt.bar(categories, frequencies, color=color, edgecolor=edgecolor)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    if ylim:
        plt.ylim(ylim)
    plt.tight_layout()
    plt.savefig(output_figname, dpi=300)
    plt.show()


# Figura 2.2
# Criar o gráfico de barras
categories = ["Fundamental", "Médio", "Superior"]
frequencies = [12, 20, 8]
create_bar_plot(
    categories,
    frequencies,
    xlabel="",
    ylabel="Frequência",
    title="Gráfico em barras para a variável γ: grau de instrução.",
    ylim=(0, 20),
    output_figname="fig2.2.png"
)



## Figura 2.4
categories = [0, 1, 2, 3, 4, 5]
frequencies = [2, 4, 6, 3, 1, 1]
create_bar_plot(
    categories,
    frequencies,
    xlabel="Número de filhos",
    ylabel="Frequência",
    title="Gráfico em barras para a variável Z: número de filhos.",
    ylim=(0, 6),
    output_figname="fig2.4.png"
)

## Figura 2.20
# create normal distribution from 4 to 24
salarios = np.random.normal(loc=10, scale=5, size=50)
# create histogram
bin_edges = np.arange(0, 26, 2)  # Bins from 0 to 26 with width of 2
counts, bins, patches = plt.hist(salarios, bins=bin_edges, edgecolor='black')
# set title
plt.title("Histograma para a variável S: salario, delta = 2.")
# set labels
plt.xlabel("Salários")
plt.ylabel("Frequência")
# Set x-ticks at the bin edges
plt.xticks(bins, labels=[f"{b:.0f}" for b in bins], rotation=45)
# show histogram
plt.savefig("fig2.20.png", dpi=300)
plt.show()



