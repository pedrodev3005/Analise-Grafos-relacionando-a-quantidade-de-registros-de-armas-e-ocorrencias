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


# Verifica e corrige possíveis problemas nos nomes das colunas
df_novas_ocorrencias.columns = df_novas_ocorrencias.columns.str.strip()  # Remove espaços em branco dos nomes das colunas

# Inicializa o grafo para todo o Brasil
grafo_brasil = GrafoMatrizAdjacenciaNaoDirecionado()

# Define os eventos válidos para a criação dos grafos
eventos_validos = [
    'Apreensão de Cocaína', 'Apreensão de Maconha', 'Estupro', 'Feminicídio',
    'Furto de veículo', 'Homicídio doloso', 'Lesão corporal seguida de morte',
    'Morte de Agente do Estado', 'Morte por intervenção de Agente do Estado',
    'Roubo a instituição financeira', 'Roubo de carga', 'Roubo de veículo',
    'Roubo seguido de morte (latrocínio)', 'Tentativa de homicídio', 'Tráfico de drogas'
]

# Adiciona os vértices ao grafo para todo o Brasil
for estado in df_novas_ocorrencias['uf'].dropna().unique():
    grafo_brasil.adiciona_vertice(estado)

# Adiciona os vértices e cria as arestas para os registros anteriores
ocorrencias = df_ocorrencias.groupby(['UF', 'TIPO_OCORRENCIA']).size().reset_index(name='PESO')
for index, row in ocorrencias.iterrows():
    estado = row['UF']
    tipo_ocorrencia = row['TIPO_OCORRENCIA']
    peso = row['PESO']

    # Adiciona o vértice do tipo de ocorrência, se ainda não existir
    if tipo_ocorrencia not in [v.rotulo for v in grafo_brasil.vertices]:
        grafo_brasil.adiciona_vertice(tipo_ocorrencia)

    # Cria a aresta ligando o tipo da ocorrência ao estado
    nome_aresta = f"ligacao_ocorrencia_{estado}_{index}"
    grafo_brasil.adiciona_aresta(nome_aresta, estado, tipo_ocorrencia, peso)

# Adiciona os vértices e cria as arestas para as categorias de registros
registros = df_registros.groupby(['UF', 'CATEGORIA']).size().reset_index(name='PESO')
for index, row in registros.iterrows():
    estado = row['UF']
    categoria = row['CATEGORIA']
    peso = row['PESO']

    # Adiciona o vértice da categoria, se ainda não existir
    if categoria not in [v.rotulo for v in grafo_brasil.vertices]:
        grafo_brasil.adiciona_vertice(categoria)

    # Cria a aresta ligando a categoria ao estado
    nome_aresta = f"ligacao_categoria_{estado}_{index}"
    grafo_brasil.adiciona_aresta(nome_aresta, estado, categoria, peso)

# Adiciona os vértices e cria as arestas para as novas ocorrências
novas_ocorrencias = df_novas_ocorrencias[df_novas_ocorrencias['evento'].isin(eventos_validos)]
ocorrencias_novas = novas_ocorrencias.groupby(['uf', 'evento']).size().reset_index(name='PESO')
for index, row in ocorrencias_novas.iterrows():
    estado = row['uf']
    evento = row['evento']
    peso = row['PESO']  # Peso baseado na contagem de ocorrências

    # Adiciona o vértice do evento, se ainda não existir
    if evento not in [v.rotulo for v in grafo_brasil.vertices]:
        grafo_brasil.adiciona_vertice(evento)

    # Cria a aresta ligando o evento ao estado
    nome_aresta = f"ligacao_evento_{estado}_{index}"
    grafo_brasil.adiciona_aresta(nome_aresta, estado, evento, peso)

# Exportação do grafo para arquivos CSV
# Salva os vértices
vertex_labels = {i: v.rotulo for i, v in enumerate(grafo_brasil.vertices)}
df_vertices = pd.DataFrame(list(vertex_labels.items()), columns=['ID', 'Label'])
df_vertices.to_csv('vertices_brasil.csv', index=False)

# Salva as arestas
arestas = []
for i in range(len(grafo_brasil.arestas)):
    for j in range(i + 1, len(grafo_brasil.arestas[i])):  # j começa de i+1 para evitar contar arestas duplas
        for nome_aresta in grafo_brasil.arestas[i][j]:
            aresta = grafo_brasil.get_aresta(nome_aresta)

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
df_arestas.to_csv('arestas_brasil.csv', index=False)

#-------------------------------------------------Funções para analise do Grafo------------------------------------


print("Funções para análise do Grafo\n")

def grau(self, V=''):
    '''
    Provê o grau do vértice passado como parâmetro
    :param V: O rótulo do vértice a ser analisado
    :return: Um valor inteiro que indica o grau do vértice
    :raises: VerticeInvalidoError se o vértice não existe no grafo
    '''

    if not self.existe_rotulo_vertice(V):
        raise VerticeInvalidoError("O vértice não existe no grafo.")

    grau = 0
    indice_vertice = self.indice_do_vertice(self.get_vertice(V))

    for j in range(indice_vertice, len(self.arestas)):
        if j == indice_vertice:
            grau += 2 * len(self.arestas[indice_vertice][j])
        else:
            grau += len(self.arestas[indice_vertice][j])

    for i in range(indice_vertice):
        grau += len(self.arestas[i][indice_vertice])

    return grau


# Função para calcular a centralidade de grau de todos os vértices no grafo
def calcular_centralidade_de_grau(grafo):
    centralidade = {}
    for vertice in grafo.vertices:
        rotulo = vertice.rotulo
        grau_vertice = grau (grafo_brasil,rotulo)
        centralidade[rotulo] = grau_vertice
    return centralidade

# Função para encontrar e exibir os vértices mais centrais
def vertices_mais_centrais(centralidade, n=5):
    # Ordena os vértices por grau em ordem decrescente
    vertices_ordenados = sorted(centralidade.items(), key=lambda item: item[1], reverse=True)
    # Retorna os n vértices com maior grau
    return vertices_ordenados[:n]

centralidade = calcular_centralidade_de_grau(grafo_brasil)

# Encontra os 5 vértices mais centrais
mais_centrais = vertices_mais_centrais(centralidade, n=5)

# Exibe os vértices mais centrais
print("1º Vértices mais centrais")
for vertice, grau in mais_centrais:
    print(f"Vértice: {vertice}, Grau: {grau}")


def dfs(grafo, vertice, visitados):
    """
    Função recursiva de busca em profundidade (DFS) para percorrer o grafo.
    """
    visitados.add(vertice)
    indice_vertice = grafo.indice_do_vertice(grafo.get_vertice(vertice))

    # Percorre todos os vértices adjacentes ao vértice atual
    for i in range(len(grafo.arestas)):
        if i != indice_vertice:
            if grafo.arestas[indice_vertice][i]:  # Se houver uma aresta
                adjacente = grafo.vertices[i].rotulo
                if adjacente not in visitados:
                    dfs(grafo, adjacente, visitados)

def is_completamente_conectado(grafo):
    """
    Verifica se o grafo é completamente conectado.
    Retorna True se o grafo for conectado e False se houver subgrupos isolados.
    """
    if not grafo.vertices:
        return True  # Grafo vazio é considerado conectado

    # Inicia DFS a partir do primeiro vértice
    visitados = set()
    dfs(grafo, grafo.vertices[0].rotulo, visitados)

    # Verifica se todos os vértices foram visitados
    return len(visitados) == len(grafo.vertices)

# Verifica se o grafo é completamente conectado
conectado = is_completamente_conectado(grafo_brasil)

print("\n2º O grafo é completamente conectado ou há componentes conexos?")

if conectado:
    print("O grafo é completamente conectado.")
else:
    print("Existem subgrupos isolados no grafo.")


# Análise dos pesos das ocorrências anteriores e novas
def analisar_pesos_ocorrencias(df_ocorrencias, df_novas_ocorrencias, eventos_validos):
    # Agrupando os pesos das ocorrências anteriores por estado
    ocorrencias_anteriores = df_ocorrencias.groupby('UF').size().reset_index(name='Peso_Ocorrencias_Ateriores')

    # Filtrando as novas ocorrências válidas e agrupando os pesos por estado
    #novas_ocorrencias = df_novas_ocorrencias[df_novas_ocorrencias['evento'].isin(eventos_validos)]
    ocorrencias_novas = novas_ocorrencias.groupby('uf').size().reset_index(name='Peso_Novas_Ocorrencias')
    ocorrencias_novas.columns = ['UF', 'Peso_Novas_Ocorrencias']

    # Combinando os pesos das ocorrências anteriores e novas
    risco_ocorrencias = pd.merge(ocorrencias_anteriores, ocorrencias_novas, on='UF', how='outer').fillna(0)

    # Calculando o risco total (soma dos pesos)
    risco_ocorrencias['Risco_Ocorrencias_Total'] = risco_ocorrencias['Peso_Ocorrencias_Ateriores'] + risco_ocorrencias[
        'Peso_Novas_Ocorrencias']

    # Ordenando os estados pelo risco total em ordem decrescente
    risco_ocorrencias = risco_ocorrencias.sort_values(by='Risco_Ocorrencias_Total', ascending=False)

    return risco_ocorrencias


# Executar a análise de pesos de ocorrências e novas ocorrências
risco_ocorrencias = analisar_pesos_ocorrencias(df_ocorrencias, df_novas_ocorrencias, eventos_validos)

print("\n3º Número total de ocorrências em cada estado")

# Exibir os estados de maior risco com base nos pesos de ocorrências
print("-Ordem decrescente dos estados com maior risco de criminalidade (baseado nos pesos das ocorrências):\n")

print(risco_ocorrencias[['UF', 'Risco_Ocorrencias_Total']])

# Soma total de ocorrências
total_ocorrencias = risco_ocorrencias['Risco_Ocorrencias_Total'].sum()

print(f"\n-Total de ocorrências no Brasil: {total_ocorrencias}")


# Função para criar uma tabela com o total de registros por estado
def tabela_registros_por_estado(df):
    # Agrupa por estado e soma o total de registros
    registros_por_estado = df.groupby('UF').size().reset_index(name='Total_Registros')
    # Ordena os estados pelo maior número de registros
    registros_ordenados = registros_por_estado.sort_values(by='Total_Registros', ascending=False)
    return registros_ordenados

# Cria a tabela de registros por estado
tabela_registros = tabela_registros_por_estado(df_registros)

print("\n4º Número total de registros em cada estado")

print("-Ordem decrescente dos estados com maior número de registros:\n")

print(tabela_registros)

total_registros = tabela_registros['Total_Registros'].sum()

print(f"\n-Total de registros no Brasil: {total_registros}")