# TabNews Data Engineering Extractor

## 📋 Descrição

Esta é uma versão **simplificada** do projeto Lago Mago, focada exclusivamente em extrair publicações do TabNews relacionadas à **Engenharia de Dados** e salvar os resultados em um arquivo Excel.

## 🎯 Objetivo

Coletar e organizar publicações relevantes sobre Engenharia de Dados do TabNews em um formato Excel (.xlsx) para análise posterior.

## 🚀 Funcionalidades

- ✅ **Busca automática** de publicações na API do TabNews
- ✅ **Filtro inteligente** por palavras-chave de Engenharia de Dados
- ✅ **Coleta assíncrona** do conteúdo completo dos posts relevantes
- ✅ **Exportação para Excel** com múltiplas planilhas
- ✅ **Logging detalhado** para acompanhar o processo
- ✅ **Tratamento de erros** robusto
- ✅ **Configuração personalizável**
- ✅ **Exemplos de uso** incluídos

## 📦 Instalação

### 1. Instalar dependências

```bash
pip install -r requirements.txt
```

### 2. Executar o script

```bash
# Execução simples
python tabnews_extractor.py

# Ou executar exemplos de uso
python exemplo_uso.py
```

## � Arquivos do Projeto

| Arquivo | Descrição |
|---------|-----------|
| `tabnews_extractor.py` | Script principal com a classe TabNewsDataExtractor |
| `requirements.txt` | Dependências do projeto |
| `config.py` | Configurações personalizáveis |
| `exemplo_uso.py` | Exemplos de como usar o extractor |
| `README.md` | Este arquivo de documentação |

## �🔧 Configuração

Você pode personalizar o comportamento editando as configurações em `config.py` ou diretamente no código:

```python
# Configurações básicas na função main()
PAGINAS = 10        # Número de páginas para buscar
POR_PAGINA = 30     # Itens por página
ARQUIVO_SAIDA = None  # None para nome automático
```

## 💡 Exemplos de Uso

### 1. Uso Simples (Script Principal)
```bash
python tabnews_extractor.py
```

### 2. Uso Programático
```python
import asyncio
from tabnews_extractor import TabNewsDataExtractor

async def meu_extractor():
    extractor = TabNewsDataExtractor()
    arquivo = await extractor.executar_pipeline_completo(
        paginas=5,
        por_pagina=20,
        arquivo_saida="meus_dados.xlsx"
    )
    print(f"Arquivo criado: {arquivo}")

asyncio.run(meu_extractor())
```

### 3. Pipeline Personalizado
```python
# Veja exemplos completos em exemplo_uso.py
python exemplo_uso.py
```

## 📊 Palavras-chave Utilizadas

O script filtra publicações baseado nestas categorias de palavras-chave:

### 🔧 Ferramentas ETL/Pipeline
- ETL, ELT, Data Pipeline
- Apache Airflow, Luigi, Prefect, Dagster

### 🚀 Big Data & Processamento
- Apache Spark, Hadoop, Hive, Presto, Trino
- Apache Flink, Apache Storm

### 🗄️ Bancos de Dados
- PostgreSQL, MySQL, MongoDB
- Redis, Elasticsearch, ClickHouse

### ☁️ Cloud Data Platforms
- Snowflake, BigQuery, Redshift
- Databricks, AWS Glue, Azure Data Factory

### 📡 Streaming & Real-time
- Apache Kafka, Apache Pulsar
- Stream Processing, Real-time Data

### 📄 Formatos de Dados
- Parquet, Avro, ORC
- Delta Lake, Apache Iceberg

### 🎛️ Data Quality & Governance
- Data Quality, Data Validation
- Data Lineage, Data Governance

*Lista completa disponível em `config.py`*

## 📈 Arquivo Excel Gerado

O arquivo Excel contém **3 planilhas**:

### 1. **Publicações** (dados principais)
| Coluna | Descrição |
|--------|-----------|
| ID | Identificador único |
| Título | Título da publicação |
| Autor | Nome do autor |
| Data Criação/Atualização | Timestamps |
| TabCoins | Pontuação/relevância |
| Palavras-chave Encontradas | Palavras que ativaram o filtro |
| Conteúdo (Início) | Primeiros 500 caracteres |
| URL, Slug, Status | Metadados técnicos |

### 2. **Estatísticas**
- Total de publicações
- Publicações com/sem conteúdo
- Métricas de TabCoins
- Autores únicos
- Data da extração

### 3. **Palavras-chave**
- Lista completa das palavras-chave utilizadas

## 🔄 Comparação com a Versão Original

| Versão Original (Spark) | Versão Simplificada |
|-------------------------|---------------------|
| Multiple notebooks | 1 arquivo Python |
| Apache Spark/Databricks | Pandas + requests |
| Delta Lake | Arquivo Excel |
| Complexo pipeline | Pipeline linear simples |
| Múltiplas dependências | Dependências mínimas |
| Configuração complexa | Configuração simples |

## 📝 Log de Execução

O script fornece logs detalhados durante a execução:

```
🚀 TabNews Data Engineering Scraper
==================================================
2025-08-05 20:37:28 - INFO - === INICIANDO PIPELINE DE EXTRAÇÃO TABNEWS ===
2025-08-05 20:37:28 - INFO - Iniciando busca de publicações - 10 páginas, 30 por página
2025-08-05 20:37:30 - INFO - Página 1: 30 publicações obtidas
...
2025-08-05 20:37:44 - INFO - Publicações relevantes encontradas: 9
2025-08-05 20:37:47 - INFO - Conteúdos completos obtidos: 9
2025-08-05 20:37:48 - INFO - Arquivo Excel salvo com sucesso
✅ Sucesso! Arquivo Excel criado: publicacoes_engenharia_dados_20250805_203748.xlsx
```

## 🛠️ Dependências

```
requests==2.31.0      # Para chamadas à API
pandas==2.1.4         # Para manipulação de dados  
openpyxl==3.1.2       # Para geração de arquivos Excel
aiohttp==3.9.1        # Para requisições assíncronas
asyncio-throttle==1.0.2  # Para controle de requisições
urllib3==2.0.7        # Para tratamento de SSL
```

## ⚡ Performance & Características

- ✅ **Requisições assíncronas** para melhor performance
- ✅ **Limite de 5 requisições simultâneas** para não sobrecarregar a API
- ✅ **Tratamento de SSL** para ambientes corporativos
- ✅ **Processamento eficiente** com pandas
- ✅ **Logs detalhados** para acompanhamento
- ✅ **Tratamento robusto de erros**

## 🔧 Personalização

### Alterar Palavras-chave
Edite a lista `PALAVRAS_CHAVE_CUSTOM` em `config.py`.

### Alterar Configurações da API
Modifique as constantes no início de `config.py`:
```python
PAGINAS_PADRAO = 10
ITENS_POR_PAGINA = 30
MAX_REQUISICOES_SIMULTANEAS = 5
```

### Personalizar Saída Excel
Modifique os métodos `preparar_dados_para_excel()` e `salvar_excel()` na classe principal.

## 🚀 Resultados

O script já foi testado com sucesso:
- ✅ 300 publicações analisadas (10 páginas × 30 itens)
- ✅ 9 publicações relevantes encontradas
- ✅ Arquivo Excel gerado com 3 planilhas
- ✅ Tempo de execução: ~20 segundos
- ✅ Taxa de sucesso: 100% das requisições

## 📄 Licença

Este projeto é uma versão simplificada do Lago Mago original.
