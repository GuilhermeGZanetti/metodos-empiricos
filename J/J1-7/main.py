import re
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import stan
import seaborn as sns

# Ler arquivoentrada com a lista de processos de Furto Simples analisados
# Para cada id_processo, baixar texto da sentença na internet http://200.137.66.21/tjsp/law-tjsp/decisoes/dados/{id}.txt
# Criar DataFrame com id do arquivo e seu conteúdo em texto

if not os.path.exists("conteudo.csv"):
    df_processos = pd.read_csv("arquivoentrada")
    for index, row in df_processos.iterrows():
        id_processo = str(row['id_processo']).strip()
        url = f"http://200.137.66.21/tjsp/law-tjsp/decisoes/dados/{id_processo}.txt"
        text = requests.get(url).text
        df_processos.loc[index, 'texto'] = text
    # Save
    df_processos.to_csv("conteudo.csv", index=False)
else:
    df_processos = pd.read_csv("conteudo.csv")


# Criar regras de regex para extrair as informações de cada variável
# Aplicar cada regra ao dataframe e separar os dados dependendo da resposta

print("""
### Estratégia para a Reprodução da Tabela 3 do Artigo do Advogado

A análise dos processos de Furto Simples foi conduzida com base na extração e processamento de textos das decisões judiciais, seguindo os seguintes passos:

#### 1. Coleta de Dados
- Inicialmente, o script verifica se o arquivo `conteudo.csv` existe para evitar downloads repetidos.
- Se o arquivo não existir, os IDs dos processos são lidos a partir de `arquivoentrada`.
- Para cada ID de processo, o texto da sentença correspondente é baixado da URL `http://200.137.66.21/tjsp/law-tjsp/decisoes/dados/{id}.txt`.
- O conteúdo é armazenado em um `DataFrame` e salvo localmente para uso posterior.

#### 2. Extração de Informações via Expressões Regulares
- Foram definidas listas de palavras-chave para cada variável analisada, como "mau antecedente", "reincidência", "confissão espontânea", "crime tentado" e "repouso noturno".
- A função `str.contains('|'.join(lista_palavras))` foi usada para verificar se os textos continham pelo menos uma das palavras-chave associadas a cada variável.
- O número total de processos contendo cada característica foi contado e comparado com o número de processos onde a característica não estava presente.

#### 3. Estrutura das Fases de Análise
A análise foi dividida em três fases, correspondendo às categorias principais da Tabela 3:

**1ª fase - Antecedentes**
- Contagem de processos que mencionam "mau antecedente" ou "maus antecedentes".
- Cálculo da proporção de casos com e sem antecedentes.

**2ª fase - Reincidência e Confissão Espontânea**
- Verificação da presença de termos relacionados à reincidência.
- Contagem de menções à "confissão espontânea".
- Comparação entre a quantidade de processos em que essas características aparecem e aqueles em que não aparecem.

**3ª fase - Circunstâncias do Crime**
- Identificação de processos que mencionam tentativa de crime.
- Contagem de ocorrências relacionadas ao crime cometido durante o repouso noturno.

#### 4. Apresentação dos Resultados
- Para cada variável, o script imprime a quantidade absoluta e a proporção relativa de casos com e sem a característica correspondente.
- Essas informações permitem a reprodução da Tabela 3 do artigo do advogado, refletindo a distribuição das características analisadas nos processos coletados.

### Considerações Finais
A estratégia usada baseia-se na automação da coleta e análise dos textos das decisões judiciais, aplicando técnicas de busca por palavras-chave para quantificar a presença de características específicas. Isso possibilita a construção da Tabela 3 de forma reprodutível e verificável, permitindo inferências sobre a aplicação da lei nos casos de Furto Simples.



""")

#### 1 fase
print("\n\n>>>> 1 fase <<<<")
# Variável Antecedentes
print("\n>>> Antecedentes")
lista_palavras = ['mau antecedente', 'maus antecedentes']
# Contar quantos textos contém uma dessas palavras
num_mau_antecedente = df_processos['texto'].str.contains('|'.join(lista_palavras)).sum()
print(f"Quantidade de processos com mau antecedente: {num_mau_antecedente} - {num_mau_antecedente/len(df_processos):.2f}")
print(f"Quantidade de processos sem mau antecedente: {len(df_processos) - num_mau_antecedente} - {(len(df_processos) - num_mau_antecedente)/len(df_processos):.2f}")

#### 2 fase
print("\n\n>>>> 2 fase <<<<")
# Variável Reincidencia
print("\n>>> Reincidencia")
lista_palavras = ['reincidencia', 'reincidencias', 'reincidente', 'reincidÃªncia']
# Contar quantos textos contém uma dessas palavras
num_reincidencia = df_processos['texto'].str.contains('|'.join(lista_palavras)).sum()
print(f"Quantidade de processos com reincidencia: {num_reincidencia} - {num_reincidencia/len(df_processos):.2f}")
print(f"Quantidade de processos sem reincidencia: {len(df_processos) - num_reincidencia} - {(len(df_processos) - num_reincidencia)/len(df_processos):.2f}")

# Confissão espontânea
print("\n>>> Confissão espontânea")
lista_palavras = ['confissão espontânea', 'confissÃ£o espontÃ¢nea', 'confissÃ£o']
# Contar quantos textos contém uma dessas palavras
num_confissao_espontanea = df_processos['texto'].str.contains('|'.join(lista_palavras)).sum()
print(f"Quantidade de processos com confissão espontânea: {num_confissao_espontanea} - {num_confissao_espontanea/len(df_processos):.2f}")
print(f"Quantidade de processos sem confissão espontânea: {len(df_processos) - num_confissao_espontanea} - {(len(df_processos) - num_confissao_espontanea)/len(df_processos):.2f}")


#### 3 fase
print("\n\n>>>> 3 fase <<<<")
# Variável Crime Tentado
print("\n>>> Crime Tentado")
lista_palavras = ['crime tentado', 'crimes tentados', 'furto tentado', 'foi meramente tentado', 'furto\ntentado', 'furto simples tentado']
# Contar quantos textos contém uma dessas palavras
num_crime_tentado = df_processos['texto'].str.contains('|'.join(lista_palavras)).sum()
print(f"Quantidade de processos com crime tentado: {num_crime_tentado} - {num_crime_tentado/len(df_processos):.2f}")
print(f"Quantidade de processos sem crime tentado: {len(df_processos) - num_crime_tentado} - {(len(df_processos) - num_crime_tentado)/len(df_processos):.2f}")


# Variável Repouso Noturno
print("\n>>> Repouso Noturno")
lista_palavras = ['repouso']
# Contar quantos textos contém uma dessas palavras
num_repouso_noturno = df_processos['texto'].str.contains('|'.join(lista_palavras)).sum()
print(f"Quantidade de processos com repouso noturno: {num_repouso_noturno} - {num_repouso_noturno/len(df_processos):.2f}")
print(f"Quantidade de processos sem repouso noturno: {len(df_processos) - num_repouso_noturno} - {(len(df_processos) - num_repouso_noturno)/len(df_processos):.2f}")


