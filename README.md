# SalesInsight PY — Análise e Visualização de Dados de Vendas com Python

## 1. Sobre o Projeto

O **SalesInsight PY** é um mini-projeto desenvolvido em Python para análise e organização de dados de vendas.

O projeto demonstra, de forma prática, conceitos fundamentais do Módulo 1, utilizando somente a biblioteca padrão do Python para geração e leitura de dados, inspeção, limpeza, transformação, análise, segmentação e exportação de resultados.

O projeto atende aos requisitos funcionais **RF01 a RF09**.

---

## 2. Objetivos do Projeto

O SalesInsight PY realiza um fluxo completo de tratamento e análise de dados de vendas:

1. Gerar ou carregar um dataset de vendas.
2. Inspecionar a estrutura e identificar problemas nos dados.
3. Limpar e validar os registros.
4. Criar colunas derivadas.
5. Calcular métricas de vendas.
6. Segmentar clientes por valor total comprado.
7. Utilizar funções reutilizáveis e Higher-Order Functions.
8. Exportar resultados em CSV e JSON.
9. Organizar todo o processamento por meio de `main()`.

---

# 3. Requisitos Funcionais

## RF01 — Geração e Carregamento do Dataset

A função:

```python
gerar_dataset_vendas(caminho_csv="vendas.csv", n_registros=200, seed=42)
```

gera um dataset de vendas em formato CSV.

O dataset contém informações como:

- ID da venda;
- data da venda;
- cliente;
- produto;
- categoria;
- região;
- quantidade;
- preço unitário.

São incluídos alguns dados propositalmente inconsistentes para permitir a demonstração do processo de limpeza, como campos vazios, espaços extras, datas inválidas e nomes de clientes com caracteres adicionais.

O arquivo principal é:

```text
vendas.csv
```

O carregamento é realizado pela função:

```python
carregar_dataset()
```

utilizando o módulo `csv`.

---

## RF02 — Inspeção do Dataset

A função:

```python
inspecionar_dados(registros)
```

realiza a inspeção inicial do dataset e apresenta:

- quantidade total de registros;
- nomes das colunas;
- quantidade de valores ausentes por coluna;
- primeiros registros.

Essa etapa permite identificar problemas antes da limpeza.

---

## RF03 — Limpeza e Validação dos Dados

A função:

```python
limpar_dados(registros)
```

realiza:

- remoção de espaços desnecessários com `strip()`;
- validação das datas com `datetime.strptime()`;
- remoção de registros com datas inválidas;
- remoção de quantidade ausente ou inválida;
- remoção de preço ausente ou inválido;
- conversão da quantidade para `int`;
- conversão do preço para `float`;
- limpeza dos nomes dos clientes com regex;
- validação do padrão dos clientes.

O padrão utilizado é:

```text
^Cliente_\d{3}$
```

Ao final, é apresentado um relatório de limpeza.

---

## RF04 — Criação de Colunas Derivadas

A função:

```python
criar_colunas_derivadas(registros)
```

cria:

### `receita_total`

Calculada por:

```text
quantidade × preço unitário
```

### `mes`

Mês numérico da venda.

### `mes_nome`

Nome do mês da venda.

### `trimestre`

Classificação em:

- Q1
- Q2
- Q3
- Q4

### `ano`

Ano da venda.

### `faixa_receita_item`

Classificação da receita individual:

- **Baixa:** menor que 500;
- **Média:** de 500 a 4.999,99;
- **Alta:** igual ou superior a 5.000.

---

## RF05 — Métricas e Agregações

A função:

```python
calcular_metricas(registros)
```

calcula métricas agregadas por:

- mês;
- produto;
- categoria;
- região.

Também são calculados:

- **Top 5 produtos por receita**;
- receita por categoria;
- receita por região;
- ticket médio por região.

O ticket médio regional é calculado considerando a receita total dividida pela quantidade de vendas da região.

---

## RF06 — Segmentação de Clientes

A função:

```python
segmentar_clientes(registros)
```

calcula o valor total comprado por cada cliente e realiza a classificação:

| Segmento | Valor total comprado |
|---|---:|
| Bronze | Menor que 5.000 |
| Silver | De 5.000 até 15.000 |
| Gold | Maior que 15.000 |

A classificação utiliza uma função `lambda`.

A função também:

- ordena os clientes por valor total comprado;
- identifica o **Top 10 clientes**;
- apresenta a distribuição dos clientes por segmento.

---

## RF07 — Funções Reutilizáveis e Higher-Order Function

O projeto utiliza funções para separar as diferentes etapas do processamento.

Entre as principais funções estão:

```python
gerar_dataset_vendas()
carregar_dataset()
inspecionar_dados()
limpar_dados()
criar_colunas_derivadas()
calcular_metricas()
segmentar_clientes()
processar_coluna()
calcular_estatisticas_gerais()
exportar_metricas_csv()
exportar_segmentacao_csv()
exportar_estatisticas_json()
main()
```

### Higher-Order Function

A função:

```python
processar_coluna(registros, coluna, funcao_transformacao, nome_saida=None)
```

recebe outra função como argumento e aplica essa transformação aos valores de uma coluna.

Um exemplo utilizado no projeto é:

```python
lambda valor: round(valor / 1000, 2)
```

Essa transformação cria a informação:

```text
receita_em_milhares
```

Também é aplicada uma transformação para classificar o volume das vendas em:

```text
Alto Volume
Baixo Volume
```

---

## RF08 — Exportação dos Resultados

Os principais resultados são exportados para arquivos.

### Métricas mensais

```text
metricas_por_mes.csv
```

Gerado por:

```python
exportar_metricas_csv()
```

### Segmentação de clientes

```text
segmentacao_clientes.csv
```

Gerado por:

```python
exportar_segmentacao_csv()
```

### Estatísticas gerais

```text
estatisticas_gerais.json
```

Gerado por:

```python
exportar_estatisticas_json()
```

As estatísticas gerais incluem:

- total de registros;
- receita total;
- quantidade total vendida;
- quantidade de clientes;
- ticket médio;
- receita média por venda;
- quantidade de vendas acima da receita média.

O arquivo JSON também é lido novamente utilizando:

```python
json.load()
```

---

## RF09 — Função Principal e Fluxo Completo

Todo o processamento é organizado na função:

```python
main()
```

O fluxo é:

```text
Verificar dataset
      ↓
Gerar dataset, se necessário
      ↓
Carregar dados
      ↓
Inspecionar dados
      ↓
Limpar dados
      ↓
Criar colunas derivadas
      ↓
Aplicar transformações
      ↓
Calcular métricas
      ↓
Segmentar clientes
      ↓
Calcular estatísticas gerais
      ↓
Exportar CSV e JSON
      ↓
Apresentar resumo final
```

O projeto utiliza:

```python
if __name__ == "__main__":
    main()
```

---

# 4. Estrutura do Projeto

```text
SalesInsight-PY/
│
├── salesinsight.py
├── vendas.csv
├── README.md
│
├── outputs/
│   ├── metricas_por_mes.csv
│   ├── segmentacao_clientes.csv
│   └── estatisticas_gerais.json
│
└── planejamento/
    └── tarefas-kanban.md
```

---

# 5. Bibliotecas Utilizadas

O projeto utiliza somente a biblioteca padrão do Python:

```python
import csv
import json
import os
import random
import re
from datetime import datetime, timedelta
```

### `csv`
Leitura, geração e exportação dos dados em CSV.

### `json`
Exportação e leitura das estatísticas gerais.

### `os`
Verificação de existência de arquivos e organização do fluxo.

### `random`
Geração do dataset.

### `re`
Limpeza e validação dos nomes dos clientes.

### `datetime`
Geração e validação das datas.

---

# 6. Como Executar o Projeto

## Requisitos

É necessário ter:

- Python 3.x.

Não são necessárias bibliotecas externas.

## Execução

Execute:

```bash
python salesinsight.py
```

Caso `vendas.csv` não exista, o programa poderá gerar automaticamente um novo dataset.

Durante a execução serão realizadas as etapas de:

1. geração ou carregamento;
2. inspeção;
3. limpeza;
4. criação de colunas derivadas;
5. transformações;
6. cálculo das métricas;
7. segmentação;
8. exportação dos resultados.

---

# 7. Resultados Gerados

| Arquivo | Descrição |
|---|---|
| `vendas.csv` | Dataset utilizado na análise |
| `metricas_por_mes.csv` | Métricas agregadas por mês |
| `segmentacao_clientes.csv` | Segmentação dos clientes |
| `estatisticas_gerais.json` | Estatísticas gerais |

---

# 8. Conceitos de Python Demonstrados

O projeto demonstra:

- variáveis;
- tipos de dados;
- listas e dicionários;
- estruturas condicionais;
- estruturas de repetição;
- funções;
- parâmetros e argumentos;
- funções `lambda`;
- Higher-Order Functions;
- manipulação de strings;
- expressões regulares;
- validação de datas;
- leitura e escrita de arquivos;
- CSV;
- JSON;
- organização de código;
- função `main()`.

---

# 9. Git e GitHub

O projeto deve ser versionado com Git e disponibilizado em um repositório público no GitHub.

## Branches

```text
main
develop
feat/pipeline-dados
docs/readme
```

### `main`
Versão principal e estável.

### `develop`
Integração das funcionalidades antes da versão final.

### `feat/pipeline-dados`
Desenvolvimento das funcionalidades do pipeline de dados.

### `docs/readme`
Alterações e melhorias da documentação.

---

# 10. Histórico de Commits

Exemplos de commits:

```text
feat: cria estrutura inicial do projeto e salesinsight.py
feat: adiciona geracao e leitura do dataset de vendas
feat: implementa limpeza de dados com datetime e regex
feat: adiciona colunas derivadas e transformacoes condicionais
feat: implementa metricas agregadas por mes produto categoria e regiao
feat: organiza o fluxo em funcoes reutilizaveis
feat: implementa exportacao de resultados em csv e json
fix: corrige conversao de datas invalidas na limpeza
docs: atualiza readme com instrucoes e conceitos
```

---

# 11. Planejamento / Kanban

O projeto pode utilizar um quadro Kanban para acompanhar as atividades:

```text
Backlog
    ↓
A Fazer
    ↓
Em Desenvolvimento
    ↓
Em Teste
    ↓
Concluído
```

As tarefas podem ser organizadas conforme os requisitos RF01 a RF09.

---

# 12. Demonstração em Vídeo

A apresentação deve demonstrar:

1. objetivo do SalesInsight PY;
2. estrutura dos arquivos;
3. execução do programa;
4. geração e leitura do dataset;
5. processo de limpeza;
6. criação das métricas;
7. segmentação dos clientes;
8. exportação dos resultados;
9. organização do Git/GitHub;
10. uma decisão técnica adotada durante o desenvolvimento.

O vídeo deve respeitar o limite máximo de **5 minutos**.

**Link do vídeo:** inserir aqui.

---

# 13. Repositório GitHub

**Link do repositório:** inserir aqui.

O repositório deverá ser público e conter os arquivos necessários para execução e avaliação do projeto.

---

# 14. Considerações Finais

O SalesInsight PY apresenta um fluxo completo de processamento de dados utilizando Python e a biblioteca padrão da linguagem.

O projeto contempla geração e carregamento, inspeção, limpeza, transformação, análise, segmentação e exportação dos dados.

Também demonstra o uso de funções reutilizáveis e Higher-Order Functions, contribuindo para uma estrutura de código organizada e modular.

Este README tem como objetivo facilitar a compreensão, execução e avaliação do projeto.

# 15. Video de demonstração
Assistir o video de demosntração: https://drive.google.com/file/d/1TbaAlg2OPsd_R-HHrxcRnPw9UmeJJR8q/view?usp=sharing
