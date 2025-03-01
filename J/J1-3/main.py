import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import stan


def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()

def plot_normal(times: list, mu_mean: float, sigma_mean: float, title: str, output_path: str):
    x = np.linspace(0, max(times) * 1.2, 1000)  # Ajustar o intervalo do eixo x
    pdf = (1 / (sigma_mean * np.sqrt(2 * np.pi))) * np.exp(-0.5 * ((x - mu_mean) / sigma_mean) ** 2)

    plt.hist(times, bins=15, density=True, alpha=0.5, label="Dados observados")
    plt.plot(x, pdf, label="Distribuição Normal Estimada", color="red")
    plt.title(title)
    plt.xlabel("Tamanho Sentença")
    plt.ylabel("Densidade")
    plt.legend()
    plt.grid()
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    plt.savefig(output_path)
    plt.close()
    print(f"Gráfico da normal salvo em {output_path}")

def fix_line(line):
    """Corrige uma linha do arquivo de entrada. Se dentro de uma data tiver vírgula entre ano e mês, mantém ela e troca o restante por ponto e vírgula."""
    # Esse padrão captura:
    # Grupo 1: "ano" ou "anos"
    # Grupo 2: a vírgula
    # Grupo 3: dígitos, opcionalmente seguido de parênteses e a palavra "mes" ou "meses"
    pattern = re.compile(r'\b(ano|anos)(,)\s*(\d+(?:\s*\([^)]*\))?\s*mes(?:es)?)', re.IGNORECASE)
    # Substitui o padrão, trocando a vírgula por um marcador temporário.
    # Exemplo: "anos, 04 (quatro) meses" -> "anos{{COMMA}} 04 (quatro) meses"
    line = pattern.sub(r'\1{{COMMA}} \3', line)
    
    # Agora, como os separadores de campo são vírgulas, substituímos todas por ponto‑vírgula.
    line = line.replace(',', ';')
    
    # Por fim, restauramos as vírgulas internas, voltando o marcador temporário para vírgula.
    line = line.replace('{{COMMA}}', ',')

    if line.count(';') > 3:
        # Remove todo o texto após a quarta ponto e vírgula.
        line = line.split(';')
        trimmed_line = [item.strip() for item in line[:4]]
        line = ';'.join(trimmed_line)
    
    return line

def sentenca_to_days(sentenca):
    """
    Converte uma sentença textual em número de dias.
    
    São considerados:
      - 365 dias para cada "ano"
      - 30 dias para cada "mês"
      - 1 dia para cada "dia"
    
    A sentença pode conter números e unidades de duas formas:
      1. Sem parênteses: ex.: "05 anos", "10 meses" ou "20 dias"
      2. Com a unidade entre parênteses: ex.: "02 (anos)" ou "11 (dias - multa)"
    
    Se a sentença não conter nenhum número,    retorna 0.
    """
    sentenca = str(sentenca).strip().lower()
    # Se não conter nenhum número, retorna 0.
    if not any(char.isdigit() for char in sentenca):
        return 0
    
    # Padrão que captura:
    #   Grupo 1: dígitos
    #   Grupo 2: (opcional) texto entre parênteses (pode conter a unidade)
    #   Grupo 3: (opcional) unidade se fornecida fora dos parênteses (ex: "anos", "meses", "dias-multa")
    pattern = re.compile(r'(\d+)\s*(?:\(([^)]+)\))?\s*(anos?|mes(?:es)?|dias?(?:-multa)?)?', re.IGNORECASE)
    matches = pattern.findall(sentenca)
    
    total_days = 0
    for num, par_unit, unit in matches:
        # Ignora correspondências sem número
        if not num:
            continue
        try:
            value = int(num)
        except ValueError:
            value = 0
        
        # Determina a unidade:
        # Se o grupo 3 (unidade fora dos parênteses) não foi capturado, tenta extrair do grupo 2
        unit_str = unit.strip() if unit else ""
        if not unit_str and par_unit:
            unit_str = par_unit.strip()
        
        # Verifica qual a unidade a partir do conteúdo da string
        if "ano" in unit_str:
            total_days += value * 365
        elif "mes" in unit_str:
            total_days += value * 30
        elif "dia" in unit_str:
            total_days += value
    return total_days

# Exemplo de uso: processa o arquivo de entrada e grava o resultado num arquivo de saída.
with open('arquivoentrada', 'r', encoding='utf-8') as infile, \
     open('intermediario.csv', 'w', encoding='utf-8') as outfile:
    outfile.write("num_processo;reu;sentenca_prov;sentenca_final\n")
    for line in infile:
        fixed_line = fix_line(line.strip())
        outfile.write(fixed_line + "\n")

# Ler intermediario.csv com pandas
df = pd.read_csv('intermediario.csv', sep=';')

# Converter as colunas 'sentenca_prov' e 'sentenca_final' para número de dias
df['sentenca_prov'] = df['sentenca_prov'].apply(sentenca_to_days)
df['sentenca_final'] = df['sentenca_final'].apply(sentenca_to_days)

df.to_csv('arquivosaida', sep=';', index=False)
print("Arquivo de saída arquivosaida gerado com sucesso no formato CSV substituindo as colunas 2 e 3 pelos valores em dia.")

print("\n> Criando modelo stan para análise dos dados")

sentencas_prov = df['sentenca_prov'].astype(int).to_list()

# Dados para o modelo Stan
data = {
    'N': len(sentencas_prov),
    'x': sentencas_prov
}

sm = stan.build(program_code=get_program_code("model.stan"), data=data)
# Ajustando o modelo com os dados
fit = sm.sample(num_chains=4)

# Imprimindo o resumo dos parâmetros
print("\n\n>Terminado build do modelo!")

posterior = fit.to_frame()
print("\n>Descrição dos parâmetros:")
print(posterior.describe())

plot_normal(sentencas_prov, posterior['mu'].mean(), posterior['sigma'].mean(), "Distribuição Normal da sentença provisória", "figs/normal.png")

print("Observando o gŕafico plotado em figs/normal.png fica claro que os dados não seguem uma distribuição normal, portanto nenhuma conclusão sobre esses dados pode ser tirada sem uma análise mais aprofundada.")

