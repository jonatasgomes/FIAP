
# Projeto de Modelagem de Dados para Produção Agrícola

Este repositório contém os arquivos e documentos relacionados ao projeto de modelagem de dados para a análise da produção agrícola no Brasil, utilizando dados de órgãos oficiais como CONAB, IBGE, MAPA, Embrapa, INPE, e CNABRASIL. O objetivo é criar um modelo de banco de dados estruturado e eficiente para armazenar e analisar dados sobre a produção agrícola, como área plantada, produtividade, e produção de diferentes culturas por estado e safra.

## Objetivo do Projeto

Aplicar os conceitos de modelagem de dados para desenvolver um banco de dados normalizado que permita armazenar e analisar informações agrícolas no Brasil. A modelagem segue as etapas de criação de um modelo conceitual e lógico, com normalização e definição de chaves primárias e estrangeiras.

## Estrutura do Repositório

- `docs/`
  - `Site_PREVISAO_DE_SAFRA-POR_PRODUTO-OUT-2024.xlsx`: Dados de previsão de safra por produto para outubro de 2024.
  - `Site_PREVISAO_DE_SAFRA-POR_PRODUTO-SET-2023.xlsx`: Dados de previsão de safra por produto para setembro de 2023.
  - `Tarefa_ Cap 10 - Explorando SQL e tipos de dados na Oracle.pdf`: Instruções detalhadas da tarefa e requisitos para o projeto.

- `src/`
  - `Produção_Agrícola/`: Diretório contendo arquivos específicos para o projeto de produção agrícola.
  - `Consultas_SQL.docx` e `Consultas_SQL.pdf`: Documentação das consultas SQL realizadas para análise dos dados.
  - `Criação_das_Tabelas.sql`: Código SQL para criação das tabelas do banco de dados.
  - `Dicionario_de_Dados.docx` e `Dicionario_de_Dados.pdf`: Dicionário de dados detalhando as tabelas e colunas do banco de dados.
  - `Modelo_Lógico.jpg`: Imagem do diagrama do modelo lógico relacional.
  - `Modelo_Relacional.jpg`: Imagem do diagrama do modelo relacional.
  - `Produção_Agrícola.dmd`: Arquivo de modelagem em formato `.dmd` para software de design de banco de dados.

## Entregáveis

1. **Diagrama Entidade-Relacionamento (MER)**:
   - O diagrama MER apresenta as principais entidades, atributos e relacionamentos identificados nos dados de produção agrícola, conforme análise inicial.

2. **Diagrama do Modelo Relacional**:
   - O diagrama do modelo relacional representa o banco de dados em um formato lógico, incluindo as tabelas normalizadas e as relações entre elas.

3. **Código SQL para Criação das Tabelas**:
   - Arquivo `Criação_das_Tabelas.sql` contendo o código SQL para criação das tabelas, incluindo definição de chaves primárias, estrangeiras e restrições de integridade.

4. **Consultas SQL**:
   - Exemplos de consultas SQL para análise dos dados, como:
     - Produção total de uma cultura específica por estado em uma safra.
     - Evolução da área plantada de uma cultura ao longo dos anos.
     - Ranking dos estados com maior produtividade em uma cultura específica.

5. **Dicionário de Dados**:
   - Documento que descreve as tabelas e colunas do banco de dados, incluindo detalhes sobre cada campo, tipo de dado, restrições, e chaves.

## Instruções para Execução

1. **Criação das Tabelas**:
   - Execute o script `Criação_das_Tabelas.sql` em um banco de dados Oracle para criar as tabelas necessárias.

2. **Consultas SQL**:
   - Utilize os exemplos em `Consultas_SQL.docx` ou `Consultas_SQL.pdf` para realizar consultas e analisar os dados inseridos.

## Contribuidores

Jônatas Gomes Alves - RM559693 
