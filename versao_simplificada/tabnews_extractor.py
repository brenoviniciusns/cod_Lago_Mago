#!/usr/bin/env python3
"""
TabNews Data Engineering Scraper
=====================================

Este script coleta publicações do TabNews relacionadas a Engenharia de Dados
e salva os resultados em um arquivo Excel.

Funcionalidades:
- Busca publicações da API do TabNews
- Filtra por palavras-chave relacionadas a engenharia de dados
- Busca o conteúdo completo dos posts relevantes
- Salva tudo em um arquivo Excel (.xlsx)

Autor: Versão Simplificada do Projeto Lago Mago
"""

import requests
import pandas as pd
import asyncio
import aiohttp
import json
import logging
import ssl
from datetime import datetime
from typing import List, Dict, Any, Optional, Tuple
from pathlib import Path

# Desabilitar verificação SSL para ambientes corporativos
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configuração de logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class TabNewsDataExtractor:
    """Classe principal para extrair dados do TabNews relacionados à Engenharia de Dados"""
    
    def __init__(self):
        self.base_url = "https://www.tabnews.com.br/api/v1/contents"
        self.session = None
        
        # Palavras-chave relacionadas à Engenharia de Dados
        self.palavras_chave = [
            'ETL',
            'Data Engineering',
            'Engenharia de Dados',
            'Data Pipeline',
            'Apache Spark',
            'Airflow',
            'Kafka',
            'Data Lake',
            'Data Warehouse',
            'Big Data',
            'Databricks',
            'Snowflake',
            'dbt',
            'Python Data',
            'SQL',
            'NoSQL',
            'MongoDB',
            'PostgreSQL',
            'Redis',
            'Elasticsearch',
            'Docker',
            'Kubernetes',
            'AWS Data',
            'Azure Data',
            'GCP Data',
            'Hadoop',
            'Hive',
            'Presto',
            'Trino',
            'Delta Lake',
            'Parquet',
            'Apache Arrow',
            'Stream Processing',
            'Real-time Data',
            'Batch Processing',
            'Data Quality',
            'Data Governance',
            'Data Modeling',
            'Data Transformation',
            'API REST',
            'GraphQL',
            'Microservices',
            'Event Driven',
            'CQRS',
            'Event Sourcing'
        ]
    
    def buscar_publicacoes(self, paginas: int = 5, por_pagina: int = 30) -> List[Dict]:
        """
        Busca publicações do TabNews
        
        Args:
            paginas: Número de páginas para buscar
            por_pagina: Número de itens por página
            
        Returns:
            Lista de publicações
        """
        logger.info(f"Iniciando busca de publicações - {paginas} páginas, {por_pagina} por página")
        
        todas_publicacoes = []
        
        for pagina in range(1, paginas + 1):
            try:
                params = {
                    'page': pagina,
                    'per_page': por_pagina,
                    'strategy': 'new'  # Estratégia para buscar novos conteúdos
                }
                
                logger.info(f"Buscando página {pagina}...")
                response = requests.get(self.base_url, params=params, timeout=10, verify=False)
                response.raise_for_status()
                
                publicacoes = response.json()
                todas_publicacoes.extend(publicacoes)
                
                logger.info(f"Página {pagina}: {len(publicacoes)} publicações obtidas")
                
            except requests.exceptions.RequestException as e:
                logger.error(f"Erro ao buscar página {pagina}: {e}")
                continue
                
            except json.JSONDecodeError as e:
                logger.error(f"Erro ao decodificar JSON da página {pagina}: {e}")
                continue
        
        logger.info(f"Total de publicações coletadas: {len(todas_publicacoes)}")
        return todas_publicacoes
    
    def filtrar_por_palavras_chave(self, publicacoes: List[Dict]) -> List[Dict]:
        """
        Filtra publicações por palavras-chave relacionadas à engenharia de dados
        
        Args:
            publicacoes: Lista de publicações
            
        Returns:
            Lista de publicações filtradas
        """
        logger.info("Iniciando filtragem por palavras-chave...")
        
        publicacoes_relevantes = []
        
        for pub in publicacoes:
            titulo = pub.get('title', '').lower()
            
            # Verifica se alguma palavra-chave está no título
            palavras_encontradas = []
            for palavra in self.palavras_chave:
                if palavra.lower() in titulo:
                    palavras_encontradas.append(palavra)
            
            if palavras_encontradas:
                pub['palavras_chave_encontradas'] = ', '.join(palavras_encontradas)
                publicacoes_relevantes.append(pub)
        
        logger.info(f"Publicações relevantes encontradas: {len(publicacoes_relevantes)}")
        return publicacoes_relevantes
    
    async def buscar_conteudo_completo_async(self, session: aiohttp.ClientSession, 
                                           autor: str, slug: str) -> Tuple[Optional[Dict], str]:
        """
        Busca o conteúdo completo de uma publicação de forma assíncrona
        
        Args:
            session: Sessão aiohttp
            autor: Nome do autor
            slug: Slug da publicação
            
        Returns:
            Tupla com (dados, url)
        """
        url = f"{self.base_url}/{autor}/{slug}"
        
        try:
            # Criar contexto SSL que ignora verificação de certificado
            ssl_context = ssl.create_default_context()
            ssl_context.check_hostname = False
            ssl_context.verify_mode = ssl.CERT_NONE
            
            async with session.get(url, timeout=aiohttp.ClientTimeout(total=10), ssl=ssl_context) as response:
                if response.status == 200:
                    dados = await response.json()
                    return dados, url
                else:
                    logger.warning(f"Status {response.status} para {url}")
                    return None, url
                    
        except asyncio.TimeoutError:
            logger.error(f"Timeout para {url}")
            return None, url
        except Exception as e:
            logger.error(f"Erro ao buscar {url}: {e}")
            return None, url
    
    async def buscar_todos_conteudos_completos(self, publicacoes_relevantes: List[Dict]) -> List[Dict]:
        """
        Busca o conteúdo completo de todas as publicações relevantes
        
        Args:
            publicacoes_relevantes: Lista de publicações filtradas
            
        Returns:
            Lista de publicações com conteúdo completo
        """
        logger.info("Iniciando busca de conteúdos completos...")
        
        publicacoes_completas = []
        
        # Limitar requisições simultâneas para não sobrecarregar a API
        semaforo = asyncio.Semaphore(5)
        
        async def buscar_com_limite(pub):
            async with semaforo:
                autor = pub.get('owner_username')
                slug = pub.get('slug')
                
                if not autor or not slug:
                    return pub
                
                ssl_context = ssl.create_default_context()
                ssl_context.check_hostname = False
                ssl_context.verify_mode = ssl.CERT_NONE
                connector = aiohttp.TCPConnector(ssl=ssl_context)
                
                async with aiohttp.ClientSession(connector=connector) as session:
                    dados_completos, url = await self.buscar_conteudo_completo_async(session, autor, slug)
                    
                    if dados_completos:
                        # Mescla os dados básicos com o conteúdo completo
                        pub_completa = {**pub, **dados_completos}
                        pub_completa['api_url'] = url
                        return pub_completa
                    else:
                        pub['api_url'] = url
                        pub['erro_conteudo'] = True
                        return pub
        
        # Executa todas as requisições de forma assíncrona
        tasks = [buscar_com_limite(pub) for pub in publicacoes_relevantes]
        publicacoes_completas = await asyncio.gather(*tasks, return_exceptions=True)
        
        # Filtra exceções
        publicacoes_validas = []
        for pub in publicacoes_completas:
            if isinstance(pub, Exception):
                logger.error(f"Exceção no processamento: {pub}")
            else:
                publicacoes_validas.append(pub)
        
        logger.info(f"Conteúdos completos obtidos: {len(publicacoes_validas)}")
        return publicacoes_validas
    
    def preparar_dados_para_excel(self, publicacoes: List[Dict]) -> pd.DataFrame:
        """
        Prepara os dados para serem salvos no Excel
        
        Args:
            publicacoes: Lista de publicações completas
            
        Returns:
            DataFrame pandas
        """
        logger.info("Preparando dados para Excel...")
        
        dados_excel = []
        
        for pub in publicacoes:
            dados_excel.append({
                'ID': pub.get('id', ''),
                'Título': pub.get('title', ''),
                'Autor': pub.get('owner_username', ''),
                'Data Criação': pub.get('created_at', ''),
                'Data Atualização': pub.get('updated_at', ''),
                'URL Fonte': pub.get('source_url', ''),
                'TabCoins': pub.get('tabcoins', 0),
                'Palavras-chave Encontradas': pub.get('palavras_chave_encontradas', ''),
                'URL da API': pub.get('api_url', ''),
                'Slug': pub.get('slug', ''),
                'Status': pub.get('status', ''),
                'Tipo': pub.get('type', ''),
                'Tem Erro': pub.get('erro_conteudo', False),
                'Conteúdo (Início)': (pub.get('body', '') or '')[:500] + '...' if pub.get('body') else 'Sem conteúdo',
                'Contagem de Filhos': pub.get('children_deep_count', 0)
            })
        
        df = pd.DataFrame(dados_excel)
        
        # Converte datas para formato mais legível
        for col in ['Data Criação', 'Data Atualização']:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%d/%m/%Y %H:%M')
        
        # Ordena por TabCoins (mais relevantes primeiro)
        df = df.sort_values('TabCoins', ascending=False).reset_index(drop=True)
        
        logger.info(f"DataFrame preparado com {len(df)} registros")
        return df
    
    def salvar_excel(self, df: pd.DataFrame, caminho_arquivo: str = None) -> str:
        """
        Salva o DataFrame em arquivo Excel
        
        Args:
            df: DataFrame a ser salvo
            caminho_arquivo: Caminho do arquivo (opcional)
            
        Returns:
            Caminho do arquivo salvo
        """
        if caminho_arquivo is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            caminho_arquivo = f"publicacoes_engenharia_dados_{timestamp}.xlsx"
        
        caminho_completo = Path(caminho_arquivo).resolve()
        
        logger.info(f"Salvando arquivo Excel: {caminho_completo}")
        
        try:
            with pd.ExcelWriter(caminho_completo, engine='openpyxl') as writer:
                # Planilha principal com os dados
                df.to_excel(writer, sheet_name='Publicações', index=False)
                
                # Planilha com estatísticas
                stats_data = {
                    'Métrica': [
                        'Total de Publicações',
                        'Publicações com Conteúdo',
                        'Publicações com Erro',
                        'Média de TabCoins',
                        'Total de TabCoins',
                        'Autores Únicos',
                        'Data da Extração'
                    ],
                    'Valor': [
                        len(df),
                        len(df[df['Tem Erro'] == False]),
                        len(df[df['Tem Erro'] == True]),
                        df['TabCoins'].mean(),
                        df['TabCoins'].sum(),
                        df['Autor'].nunique(),
                        datetime.now().strftime('%d/%m/%Y %H:%M:%S')
                    ]
                }
                
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='Estatísticas', index=False)
                
                # Planilha com as palavras-chave usadas
                palavras_df = pd.DataFrame({
                    'Palavras-chave Utilizadas': self.palavras_chave
                })
                palavras_df.to_excel(writer, sheet_name='Palavras-chave', index=False)
            
            logger.info(f"Arquivo Excel salvo com sucesso: {caminho_completo}")
            return str(caminho_completo)
            
        except Exception as e:
            logger.error(f"Erro ao salvar arquivo Excel: {e}")
            raise
    
    async def executar_pipeline_completo(self, paginas: int = 5, por_pagina: int = 30, 
                                       arquivo_saida: str = None) -> str:
        """
        Executa o pipeline completo de extração de dados
        
        Args:
            paginas: Número de páginas para buscar
            por_pagina: Itens por página
            arquivo_saida: Nome do arquivo de saída
            
        Returns:
            Caminho do arquivo Excel gerado
        """
        logger.info("=== INICIANDO PIPELINE DE EXTRAÇÃO TABNEWS ===")
        
        try:
            # 1. Buscar publicações
            publicacoes = self.buscar_publicacoes(paginas, por_pagina)
            
            if not publicacoes:
                raise ValueError("Nenhuma publicação foi encontrada")
            
            # 2. Filtrar por palavras-chave
            publicacoes_relevantes = self.filtrar_por_palavras_chave(publicacoes)
            
            if not publicacoes_relevantes:
                logger.warning("Nenhuma publicação relevante encontrada com as palavras-chave")
                return None
            
            # 3. Buscar conteúdo completo
            publicacoes_completas = await self.buscar_todos_conteudos_completos(publicacoes_relevantes)
            
            # 4. Preparar dados para Excel
            df = self.preparar_dados_para_excel(publicacoes_completas)
            
            # 5. Salvar em Excel
            caminho_arquivo = self.salvar_excel(df, arquivo_saida)
            
            logger.info("=== PIPELINE CONCLUÍDO COM SUCESSO ===")
            logger.info(f"Arquivo gerado: {caminho_arquivo}")
            logger.info(f"Total de registros: {len(df)}")
            
            return caminho_arquivo
            
        except Exception as e:
            logger.error(f"Erro no pipeline: {e}")
            raise


async def main():
    """Função principal para executar o scraper"""
    
    print("🚀 TabNews Data Engineering Scraper")
    print("=" * 50)
    
    # Configurações (você pode alterar aqui)
    PAGINAS = 10        # Número de páginas para buscar
    POR_PAGINA = 30     # Itens por página
    ARQUIVO_SAIDA = None  # None para nome automático
    
    try:
        extractor = TabNewsDataExtractor()
        
        caminho_arquivo = await extractor.executar_pipeline_completo(
            paginas=PAGINAS,
            por_pagina=POR_PAGINA,
            arquivo_saida=ARQUIVO_SAIDA
        )
        
        if caminho_arquivo:
            print(f"\n✅ Sucesso! Arquivo Excel criado: {caminho_arquivo}")
        else:
            print("\n⚠️  Nenhuma publicação relevante encontrada.")
            
    except Exception as e:
        print(f"\n❌ Erro na execução: {e}")
        return 1
    
    return 0


if __name__ == "__main__":
    # Execute o script
    exit_code = asyncio.run(main())
    exit(exit_code)
