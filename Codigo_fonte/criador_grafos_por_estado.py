import pandas as pd
from bibgrafo.grafo_matriz_adj_nao_dir import GrafoMatrizAdjacenciaNaoDirecionado

# Caminho dos arquivos CSV
file_path_ocorrencias = "C:/Users/pedro/Documents/Terceiroperiodocomputacao/GRAFOS_PROJETO/OCORRENCIAS_2024.csv"#Coloque o caminho do seu arquivo "OCORRENCIAS_2024", presente no repositório
file_path_registros = "C:/Users/pedro/Documents/Terceiroperiodocomputacao/GRAFOS_PROJETO/REGISTROS_com_categoria_2024.csv"#Coloque o caminho do seu arquivo "REGISTROS_com_categoria_2024", presente no repositório
file_path_novas_ocorrencias = "C:/Users/pedro\Documents/Terceiroperiodocomputacao/GRAFOS_PROJETO/BancoVDE 2024.csv" #Coloque o caminho do seu arquivo "BANCOVDE 2024", presente no repositório

# Leitura dos arquivos CSV
df_ocorrencias = pd.read_csv(file_path_ocorrencias)
df_registros = pd.read_csv(file_path_registros)
df_novas_ocorrencias = pd.read_csv(file_path_novas_ocorrencias)

# Inicializa o dicionário para armazenar um grafo para cada estado
grafos_estados = {}

# Define os eventos válidos para a criação dos grafos
eventos_validos = [
    'Apreensão de Cocaína', 'Apreensão de Maconha', 'Estupro', 'Feminicídio',
    'Furto de veículo', 'Homicídio doloso', 'Lesão corporal seguida de morte',
    'Morte de Agente do Estado', 'Morte por intervenção de Agente do Estado',
    'Roubo a instituição financeira', 'Roubo de carga', 'Roubo de veículo',
    'Roubo seguido de morte (latrocínio)', 'Tentativa de homicídio', 'Tráfico de drogas'
]

# Adiciona os vértices ao grafo para cada estado
for estado in df_novas_ocorrencias['uf'].dropna().unique():
    grafo = GrafoMatrizAdjacenciaNaoDirecionado()
    grafos_estados[estado] = grafo
    grafo.adiciona_vertice(estado)

# Adiciona os vértices e cria as arestas para os registros anteriores
ocorrencias = df_ocorrencias.groupby(['UF', 'TIPO_OCORRENCIA']).size().reset_index(name='PESO')
for index, row in ocorrencias.iterrows():
    estado = row['UF']
    tipo_ocorrencia = row['TIPO_OCORRENCIA']
    peso = row['PESO']

    grafo = grafos_estados.get(estado)
    if not grafo:
        continue

    # Adiciona o vértice do tipo de ocorrência, se ainda não existir
    if tipo_ocorrencia not in [v.rotulo for v in grafo.vertices]:
        grafo.adiciona_vertice(tipo_ocorrencia)

    # Cria a aresta ligando o tipo da ocorrência ao estado
    nome_aresta = f"ligacao_ocorrencia_{estado}_{index}"
    grafo.adiciona_aresta(nome_aresta, estado, tipo_ocorrencia, peso)

# Adiciona os vértices e cria as arestas para as categorias de registros
registros = df_registros.groupby(['UF', 'CATEGORIA']).size().reset_index(name='PESO')
for index, row in registros.iterrows():
    estado = row['UF']
    categoria = row['CATEGORIA']
    peso = row['PESO']

    grafo = grafos_estados.get(estado)
    if not grafo:
        continue

    # Adiciona o vértice da categoria, se ainda não existir
    if categoria not in [v.rotulo for v in grafo.vertices]:
        grafo.adiciona_vertice(categoria)

    # Cria a aresta ligando a categoria ao estado
    nome_aresta = f"ligacao_categoria_{estado}_{index}"
    grafo.adiciona_aresta(nome_aresta, estado, categoria, peso)

# Adiciona os vértices e cria as arestas para as novas ocorrências
novas_ocorrencias = df_novas_ocorrencias[df_novas_ocorrencias['evento'].isin(eventos_validos)]
ocorrencias_novas = novas_ocorrencias.groupby(['uf', 'evento']).size().reset_index(name='PESO')
for index, row in ocorrencias_novas.iterrows():
    estado = row['uf']
    evento = row['evento']
    peso = row['PESO']  # Peso baseado na contagem de ocorrências

    grafo = grafos_estados.get(estado)
    if not grafo:
        continue

    # Adiciona o vértice do evento, se ainda não existir
    if evento not in [v.rotulo for v in grafo.vertices]:
        grafo.adiciona_vertice(evento)

    # Cria a aresta ligando o evento ao estado
    nome_aresta = f"ligacao_evento_{estado}_{index}"
    grafo.adiciona_aresta(nome_aresta, estado, evento, peso)

# Exportação dos grafos para arquivos CSV
for estado, grafo in grafos_estados.items():
    # Salva os vértices
    vertex_labels = {i: v.rotulo for i, v in enumerate(grafo.vertices)}
    df_vertices = pd.DataFrame(list(vertex_labels.items()), columns=['ID', 'Label'])
    df_vertices.to_csv(f'vertices_{estado}.csv', index=False)

    # Salva as arestas
    arestas = []
    for i in range(len(grafo.arestas)):
        for j in range(i + 1, len(grafo.arestas[i])):  # j começa de i+1 para evitar contar arestas duplas
            for nome_aresta in grafo.arestas[i][j]:
                aresta = grafo.get_aresta(nome_aresta)

                # Definir o tipo de aresta baseado no nome

                if 'categoria' in nome_aresta:
                    tipo_aresta = 'Categoria'
                elif 'ocorrencia' or 'evento' in nome_aresta:
                    tipo_aresta = 'Ocorrencia'
                else:
                    tipo_aresta = 'Desconhecido'

                arestas.append({
                    'Source': i,
                    'Target': j,
                    'Label': nome_aresta,
                    'Weight': aresta.peso,
                    'Edge_Type': tipo_aresta
                })
    df_arestas = pd.DataFrame(arestas)
    df_arestas.to_csv(f'arestas_{estado}.csv', index=False)
