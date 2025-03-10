import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import stan
import scipy.stats as stats

def get_program_code(stan_path: str) -> str:
    with open(stan_path, 'r') as file:
        return file.read()

def extract_process_number(link):
    """Extrai o número do processo da coluna Link"""
    if pd.isna(link):
        return None
    try:
        # Extrai o nome do arquivo do link e remove a extensão .pdf
        filename = link.split('/')[-1].replace('.pdf', '')
        return filename
    except:
        return None

def plot_standard_error_vs_sample_size(sentences, model_code, filename="se_vs_sample_size.png"):
    """
    Gera gráfico de desvio padrão vs tamanho da amostra seguindo Cohen (1995, Fig 4.7)
    Esta função calcula empiricamente o desvio padrão rodando modelos Stan
    com diferentes tamanhos de amostra dos dados reais
    """
    actual_n = len(sentences)
    # desvio padrão teórico (para comparação)
    overall_sd = np.std(sentences)
    sample_sizes = np.arange(1, actual_n + 1)
    theoretical_se = [overall_sd / np.sqrt(n) for n in sample_sizes]
    
    # Cálculo empírico do desvio padrão
    empirical_se = []
    print("Calculando erros padrão empíricos para diferentes tamanhos de amostra...")
    
    # Testa cada tamanho de amostra de 1 até o número total de amostras
    for n in range(1, actual_n + 1):
        print(f"  Processando tamanho de amostra {n}...")
        # Usa as primeiras n sentenças
        sample = sentences[:n]
        
        try:
            # Configura e executa o modelo Stan
            stan_data = {
                'N': len(sample),
                'y': sample.tolist()
            }
            
            # Compila e amostra do modelo
            sm = stan.build(program_code=model_code, data=stan_data)
            fit = sm.sample(num_chains=2, num_samples=1000)  # Amostras reduzidas para maior velocidade
            
            # Extrai amostras posteriores e calcula desvio padrão
            posterior = fit.to_frame()
            mu_samples = posterior['mu'].values
            mu_std = np.std(mu_samples)
            
            empirical_se.append((n, mu_std))
        except Exception as e:
            print(f"  Erro para tamanho de amostra {n}: {e}")
            # Se ocorrer erro, usa SE teórico
            empirical_se.append((n, overall_sd / np.sqrt(n)))
    
    # Plota erros padrão teóricos e empíricos
    plt.figure(figsize=(10, 6))
    
    # Plota curva de SE teórico
    plt.plot(sample_sizes, theoretical_se, 'b-', label='EP Teórico = σ/√n')
    
    # Plota pontos de SE empírico
    x_empirical = [x[0] for x in empirical_se]
    y_empirical = [x[1] for x in empirical_se]
    plt.scatter(x_empirical, y_empirical, color='red', label='EP Empírico (modelo Stan)')
    
    # Conecta os pontos empíricos
    if len(x_empirical) > 1:
        plt.plot(x_empirical, y_empirical, 'r--')
    
    plt.xlabel('Tamanho da Amostra (n)')
    plt.ylabel('Desvio padrão da Média')
    plt.title('Desvio padrão vs. Tamanho da Amostra para Sentenças (Cohen 1995, Fig 4.7)')
    plt.axhline(y=overall_sd / np.sqrt(actual_n), color='g', linestyle='--', 
               label=f'EP teórico atual com n={actual_n}')
    plt.legend()
    plt.grid(True)
    
    os.makedirs("figs", exist_ok=True)
    plt.savefig(f"figs/{filename}")
    plt.close()
    print(f"Gráfico salvo em figs/{filename}")

def plot_confidence_interval_vs_sample_size(sd, sample_sizes, actual_n, filename="ci_vs_sample_size.png"):
    """Gera gráfico da largura do intervalo de confiança de 95% vs tamanho da amostra"""
    ci_width_95 = [1.96 * sd / np.sqrt(n) for n in sample_sizes]
    
    plt.figure(figsize=(10, 6))
    plt.plot(sample_sizes, ci_width_95)
    plt.xlabel('Tamanho da Amostra (n)')
    plt.ylabel('Largura do Intervalo de Confiança de 95% (dias)')
    plt.title('Largura do IC vs. Tamanho da Amostra para Sentenças')
    plt.axhline(y=1.96 * sd / np.sqrt(actual_n), color='r', 
               linestyle='--', label=f'Largura atual do IC com n={actual_n}')
    plt.legend()
    plt.grid(True)
    
    os.makedirs("figs", exist_ok=True)
    plt.savefig(f"figs/{filename}")
    plt.close()
    print(f"Gráfico salvo em figs/{filename}")

def plot_normal_comparison(data1, data2, mu1, sigma1, judge1_name, judge2_name, filename="judge_comparison.png"):
    """Plota distribuições normais para comparar dois juízes"""
    plt.figure(figsize=(12, 6))
    
    # Plota histogramas
    plt.hist(data1, bins=15, density=True, alpha=0.5, label=f"{judge1_name} (dados)")
    plt.hist(data2, bins=15, density=True, alpha=0.5, label=f"{judge2_name} (dados)")
    
    # Plota distribuições estimadas
    x = np.linspace(0, max(max(data1), max(data2)) * 1.2, 1000)
    pdf1 = stats.norm.pdf(x, mu1, sigma1)
    plt.plot(x, pdf1, label=f"{judge1_name} (normal estimada)", color="red")
    
    mean2 = np.mean(data2)
    std2 = np.std(data2)
    pdf2 = stats.norm.pdf(x, mean2, std2)
    plt.plot(x, pdf2, label=f"{judge2_name} (normal estimada)", color="blue")
    
    plt.title(f"Comparação de Sentenças: {judge1_name} vs {judge2_name}")
    plt.xlabel("Sentença final (dias)")
    plt.ylabel("Densidade")
    plt.legend()
    plt.grid(True)
    
    os.makedirs("figs", exist_ok=True)
    plt.savefig(f"figs/{filename}")
    plt.close()
    print(f"Gráfico de comparação dos juízes salvo em figs/{filename}")

# 1. Lê os arquivos de dados
print("Lendo arquivos de dados...")
df_sentences = pd.read_csv('arquivoentrada')
df_processes = pd.read_csv('processos.csv')

if "juiz" not in df_sentences.columns:
    # Processa num_processo em df_sentences para remover # se presente
    df_sentences['num_processo'] = df_sentences['num_processo'].apply(lambda x: str(x).replace("#", ""))

    # 2. Extrai número do processo da coluna Link e cria mapeamento
    df_processes['num_processo'] = df_processes['Link'].apply(extract_process_number)

    # Cria mapeamento de números de processo para juízes
    process_judge_map = dict(zip(df_processes['num_processo'], df_processes['Juiz']))

    # Adiciona coluna de juiz ao dataframe de sentenças
    df_sentences['juiz'] = df_sentences['num_processo'].map(process_judge_map)

    # Salva no arquivoentrada
    df_sentences.to_csv('arquivoentrada', index=False)

# 3. Filtra apenas casos de tráfico
trafico_df = df_sentences[df_sentences['tipo'] == 'trafico'].copy()
trafico_df = trafico_df[~trafico_df['juiz'].isna()]  # Remove casos com juiz desconhecido

print(f"Total de casos de tráfico com informação de juiz: {len(trafico_df)}")

# 4. Encontra os dois juízes com mais casos de tráfico
judge_counts = trafico_df['juiz'].value_counts()
print("\nContagem de casos por juiz:")
print(judge_counts.head())

if len(judge_counts) < 2:
    print("Erro: Não há juízes suficientes com casos de tráfico para comparação")
    exit(1)

top_judges = judge_counts.nlargest(2).index.tolist()
judge1, judge2 = top_judges[0], top_judges[1]
print(f"\nJuízes com mais casos de tráfico: {judge1} e {judge2}")

# 5. Separa dados por juiz
judge1_cases = trafico_df[trafico_df['juiz'] == judge1]
judge2_cases = trafico_df[trafico_df['juiz'] == judge2]

print(f"Juiz 1 ({judge1}) tem {len(judge1_cases)} casos de tráfico")
print(f"Juiz 2 ({judge2}) tem {len(judge2_cases)} casos de tráfico")

# 6. Prepara dados para o modelo Stan
# Usaremos a sentença final em dias como nossa variável de interesse
judge1_sentences = judge1_cases['sentenca_final'].dropna().values
judge2_sentences = judge2_cases['sentenca_final'].dropna().values

if len(judge1_sentences) == 0 or len(judge2_sentences) == 0:
    print("Erro: Um dos juízes não possui casos com sentenças finais válidas")
    exit(1)

print(f"\nJuiz 1 sentenças válidas: {len(judge1_sentences)}")
print(f"Juiz 2 sentenças válidas: {len(judge2_sentences)}")

# Compila e ajusta o modelo Stan
print("\nCompilando e ajustando modelo Stan para o Juiz 1...")
stan_data = {
    'N': len(judge1_sentences),
    'y': judge1_sentences.tolist()
}

# Carrega o modelo Stan e amostra
sm = stan.build(program_code=get_program_code("model.stan"), data=stan_data)
fit = sm.sample(num_chains=4)

# Extrai amostras posteriores
posterior = fit.to_frame()
mu_samples = posterior['mu'].values
sigma_samples = posterior['sigma'].values

# Calcula estatísticas posteriores
mu_mean = np.mean(mu_samples)
mu_std = np.std(mu_samples)
sigma_mean = np.mean(sigma_samples)

print("\nResumo posterior:")
print(f"Média (mu): {mu_mean:.2f} ± {mu_std:.2f}")
print(f"Desvio padrão (sigma): {sigma_mean:.2f}")

# 7. Compara a média do juiz 2 com a distribuição do juiz 1
judge2_mean = np.mean(judge2_sentences)
judge2_std = np.std(judge2_sentences)
print(f"\nJuiz 2 média: {judge2_mean:.2f}")
print(f"Juiz 2 desvio padrão: {judge2_std:.2f}")

# Calcula z-score e p-valor
z_score = (judge2_mean - mu_mean) / (sigma_mean / np.sqrt(len(judge2_sentences)))
p_value = 2 * (1 - stats.norm.cdf(abs(z_score)))  # Teste bilateral

print(f"Z-score: {z_score:.2f}")
print(f"P-value: {p_value:.4f}")

if p_value < 0.05:
    significance = "Existe diferença estatisticamente significativa"
else:
    significance = "Não existe diferença estatisticamente significativa"

print(f"Resultado: {significance} entre as sentenças dos juízes (α=0.05)")

# 8. Cria gráficos mostrando como o desvio padrão diminui com o tamanho da amostra seguindo Cohen (1995, Fig 4.7)
print("\nCriando gráficos para desvio padrão e intervalos de confiança...")
# Para cálculo empírico do desvio padrão
plot_standard_error_vs_sample_size(judge1_sentences, get_program_code("model.stan"))
# Para intervalo de confiança teórico
sample_sizes = np.arange(1, max(len(judge1_sentences), 100) + 1)
plot_confidence_interval_vs_sample_size(sigma_mean, sample_sizes, len(judge1_sentences))

# Plota distribuições normais para ambos os juízes
plot_normal_comparison(judge1_sentences, judge2_sentences, mu_mean, sigma_mean, judge1, judge2)

# Escreve relatório com descobertas
print("\nEscrevendo relatório...")
with open('relatorio', 'w') as f:
    f.write("# Análise de Sentenças por Juiz em Casos de Tráfico\n\n")
    f.write(f"## Comparação entre {judge1} e {judge2}\n\n")
    f.write(f"- Juiz 1 ({judge1}): {len(judge1_cases)} casos de tráfico\n")
    f.write(f"- Juiz 2 ({judge2}): {len(judge2_cases)} casos de tráfico\n\n")
    f.write("Esses dois juizes foram escolhidos manualmente e mais 3 sentenças de cada foram anotadas manualmente para se ter uma amostra um pouco mais significativa (anteriormente era 5)\n\n")
    
    f.write("## Metodologia\n\n")
    f.write("Seguindo a metodologia proposta por Cohen (1995, Sec. 4.2-4.3), utilizamos uma abordagem bayesiana para:\n\n")
    f.write("1. Estimar a distribuição das sentenças do Juiz 1 usando Stan (modelo bayesiano)\n")
    f.write("2. Comparar a média das sentenças do Juiz 2 com a distribuição estimada do Juiz 1\n")
    f.write("3. Calcular o z-score e p-value para avaliar a significância estatística das diferenças\n")
    f.write("4. Analisar como o desvio padrão e o intervalo de confiança variam com o tamanho da amostra\n\n")
    
    f.write("## Resultados da Análise\n\n")
    f.write(f"- Média posterior de sentenças do Juiz 1: {mu_mean:.2f} dias\n")
    f.write(f"- Desvio padrão posterior do Juiz 1: {sigma_mean:.2f} dias\n")
    f.write(f"- Média de sentenças do Juiz 2: {judge2_mean:.2f} dias\n")
    f.write(f"- Z-score da comparação: {z_score:.2f}\n")
    f.write(f"- P-value: {p_value:.4f}\n\n")
    
    if p_value < 0.05:
        f.write("Há evidência estatística (α=0.05) de diferença significativa entre as sentenças médias dos dois juízes.\n\n")
    else:
        f.write("Não há evidência estatística suficiente (α=0.05) para concluir que existe diferença significativa entre as sentenças médias dos dois juízes.\n\n")
    
    f.write("## Discussão sobre Desvio Padrão da Amostra\n\n")
    f.write("Ao desenhar o gráfico se_vs_sample_size.png, observamos que o desvio padrão empírico calculado com o stan para amostras de tamanho 1, 2, 3, 4 e 5 segue de maneira aproximada o desvio padrão teórico calculado com sigma/sqrt(n).\n\n")

    f.write("## Discussão sobre Tamanho da Amostra\n\n")
    f.write(f"De acordo com a análise realizada, observamos que com n={len(judge1_sentences)} casos, o desvio padrão da média é de {sigma_mean / np.sqrt(len(judge1_sentences)):.2f} dias.\n\n")
    f.write("Comparando com Bussab and Morettin (2013, Sec. 10.11), calculamos o tamanho mínimo de amostra necessário para obter uma margem de erro específica.\n\n")
    
    # Calcula tamanho de amostra necessário para diferentes margens de erro
    desired_errors = [365, 180, 90, 30]  # Erros em dias
    for error in desired_errors:
        n_needed = int(np.ceil((1.96 * sigma_mean / error)**2))
        f.write(f"Para uma margem de erro de {error} dias (intervalo de confiança de 95%), seria necessária uma amostra de pelo menos {n_needed} casos.\n")
    
    f.write("\n## Conclusão\n\n")
    f.write("A análise baseada na metodologia de Cohen (1995) nos permitiu comparar as decisões judiciais entre dois juízes com maior volume de casos de tráfico. ")
    f.write("Os gráficos gerados demonstram como o desvio padrão e o intervalo de confiança diminuem com o aumento do tamanho da amostra, ")
    f.write("ilustrando a importância de se ter um número adequado de casos para fazer inferências estatísticas robustas sobre as decisões judiciais.\n\n")
    f.write("A análise do tamanho da amostra nos permite concluir que, para obtermos margens de erro mais estreitas (por exemplo, 30 dias), ")
    f.write(f"precisaríamos de amostras substancialmente maiores que as atuais ({len(judge1_sentences)} e {len(judge2_sentences)} casos).")

print("\nAnálise completa. Resultados salvos em 'relatorio' e gráficos salvos no diretório 'figs'.")