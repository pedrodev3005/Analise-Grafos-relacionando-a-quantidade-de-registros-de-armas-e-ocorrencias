# Analise-Grafos-relacionando-a-quantidade-de-registros-de-armas-e-ocorrencias
Projeto de análise de dados criminais utilizando grafos para identificar relações entre registros de armas e ocorrências criminais em estados brasileiros.
## Objetivo
- Avaliar a correlação entre o número de registros de armas e as ocorrências criminais em cada estado.
- Identificar estados com maior risco de criminalidade baseado no volume de ocorrências e registros de armas.
- Propor sugestões de políticas públicas para mitigação da criminalidade.

## Tecnologias Utilizadas
- **Python** com a biblioteca **bibgrafo** para a modelagem de grafos.
- **Pandas** para manipulação de dados.
- **Gephi** para visualização gráfica dos grafos.

## Colaboradores
Este projeto foi desenvolvido em colaboração por:

- [Maria Clara Colaço](https://github.com/claracolaco)
- [Pedro Augusto Gonçalves Lucena](https://github.com/pedrodev3005)
- [Sophia Sales](https://github.com/Sophia7b)

## Como Executar o Projeto
1. Baixe os arquivos presentes na pasta "Base_dados".
2. Cerifique-se de ter as bibliotecas necessárias já instaladas no seu computador.
3. Abra os códigos fontes na sua IDE.
4. Corrija os caminhos de arquivos presentes nos códigos fonte para os seus respectivos caminhos.
5. Execute os códigos.

## Observação:
- O código "criador_grafo_Brasil+analise.py" criará arquivos .csv de arestas e vértices de um grafo reunindo todos os estados brasileiros e seus respectivos registros/ocorrências, e o código "criador_grafos_por_estado.py" irá criar arquivos .csv de arestas e vértices para cada estado da paraíba. Esses arquivos podem ser adicionados ao gephi para análise visual dos grafos.
- Além disso, algumas análises já são feitas no própio arquivo "criador_grafo_Brasil+analise.py", análise a saída do mesmo.

## Explicacão dos documentos desse repositório:
- Arestas_Criadas: Possui os arquivos .csv das arestas de cada estado. Os arquivos dessa pasta foram criados pelos algoritmos "criador_grafo_Brasil+analise.py" e "criador_grafo_Brasil+analise.py".
- Base_dados: Possui os arquivos .csv que serviram como base para nossa análise.
- Codigo_fonte: Possui os códigos fontes utilizados para análise.
- Vertices_Criados: Possui os arquivos .csv dos vertices de cada estado. Os arquivos dessa pasta foram criados pelos algoritmos "criador_grafo_Brasil+analise.py" e "criador_grafo_Brasil+analise.py".

## Contribuição
Contribuições são bem-vindas! Se você quiser contribuir com o projeto, por favor, faça um fork e envie um pull request.
