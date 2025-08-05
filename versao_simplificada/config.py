# Configurações do TabNews Extractor
# ===================================

# Configurações da API
PAGINAS_PADRAO = 10
ITENS_POR_PAGINA = 30
ESTRATEGIA = "new"  # new, old, relevant

# Configurações de Performance
MAX_REQUISICOES_SIMULTANEAS = 5
TIMEOUT_SEGUNDOS = 10

# Palavras-chave para Engenharia de Dados
# (você pode personalizar esta lista)
PALAVRAS_CHAVE_CUSTOM = [
    # Ferramentas ETL/ELT
    'ETL',
    'ELT', 
    'Data Pipeline',
    'Apache Airflow',
    'Luigi',
    'Prefect',
    'Dagster',
    
    # Big Data
    'Apache Spark',
    'Hadoop',
    'Hive',
    'Presto',
    'Trino',
    'Apache Flink',
    'Apache Storm',
    
    # Bancos de Dados
    'PostgreSQL',
    'MySQL',
    'MongoDB',
    'Cassandra',
    'Redis',
    'Elasticsearch',
    'ClickHouse',
    'TimescaleDB',
    
    # Data Warehouses
    'Snowflake',
    'BigQuery',
    'Redshift',
    'Synapse',
    'Databricks',
    
    # Cloud Data
    'AWS Glue',
    'AWS EMR',
    'Azure Data Factory',
    'Google Dataflow',
    'Lambda Architecture',
    'Kappa Architecture',
    
    # Streaming
    'Apache Kafka',
    'Apache Pulsar',
    'Amazon Kinesis',
    'Azure Event Hubs',
    'Stream Processing',
    'Real-time Data',
    
    # Formatos de Dados
    'Parquet',
    'Avro',
    'ORC',
    'Delta Lake',
    'Apache Iceberg',
    'Apache Hudi',
    
    # Data Quality
    'Data Quality',
    'Data Validation',
    'Data Profiling',
    'Data Lineage',
    'Data Governance',
    'Data Catalog',
    
    # Linguagens e Ferramentas
    'Python Data',
    'Pandas',
    'Dask',
    'Polars',
    'SQL',
    'dbt',
    'Apache Arrow',
    
    # DevOps para Dados
    'Docker',
    'Kubernetes',
    'Terraform',
    'Infrastructure as Code',
    'CI/CD Data',
    'DataOps',
    
    # Conceitos Gerais
    'Data Engineering',
    'Engenharia de Dados',
    'Data Lake',
    'Data Lakehouse',
    'Data Mesh',
    'Data Fabric'
]

# Configurações do arquivo Excel
NOME_ARQUIVO_PADRAO = None  # None para nome automático com timestamp
INCLUIR_ESTATISTICAS = True
INCLUIR_PALAVRAS_CHAVE = True
