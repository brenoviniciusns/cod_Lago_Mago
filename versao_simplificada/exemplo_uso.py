#!/usr/bin/env python3
"""
Exemplo de uso simples do TabNews Extractor
==========================================

Este é um exemplo de como usar o extractor de forma simples
com configurações personalizadas.
"""

import asyncio
from tabnews_extractor import TabNewsDataExtractor

async def exemplo_basico():
    """Exemplo básico de uso"""
    print("📊 Exemplo Básico - Busca Rápida")
    
    extractor = TabNewsDataExtractor()
    
    # Configuração para busca rápida (menos páginas)
    arquivo = await extractor.executar_pipeline_completo(
        paginas=3,          # Apenas 3 páginas
        por_pagina=20,      # 20 itens por página
        arquivo_saida="busca_rapida.xlsx"
    )
    
    print(f"✅ Arquivo gerado: {arquivo}")

async def exemplo_completo():
    """Exemplo de busca completa"""
    print("📊 Exemplo Completo - Busca Extensiva")
    
    extractor = TabNewsDataExtractor()
    
    # Configuração para busca completa
    arquivo = await extractor.executar_pipeline_completo(
        paginas=20,         # 20 páginas
        por_pagina=30,      # 30 itens por página
        arquivo_saida="busca_completa.xlsx"
    )
    
    print(f"✅ Arquivo gerado: {arquivo}")

async def exemplo_personalizado():
    """Exemplo com pipeline personalizado"""
    print("📊 Exemplo Personalizado - Pipeline Detalhado")
    
    extractor = TabNewsDataExtractor()
    
    # 1. Buscar publicações
    print("🔍 Buscando publicações...")
    publicacoes = extractor.buscar_publicacoes(paginas=5, por_pagina=25)
    print(f"📄 Total encontrado: {len(publicacoes)}")
    
    # 2. Filtrar
    print("🔍 Filtrando por palavras-chave...")
    relevantes = extractor.filtrar_por_palavras_chave(publicacoes)
    print(f"🎯 Relevantes: {len(relevantes)}")
    
    # 3. Buscar conteúdo completo
    print("🔍 Buscando conteúdo completo...")
    completas = await extractor.buscar_todos_conteudos_completos(relevantes)
    print(f"📚 Conteúdos completos: {len(completas)}")
    
    # 4. Preparar e salvar
    print("📊 Preparando dados para Excel...")
    df = extractor.preparar_dados_para_excel(completas)
    arquivo = extractor.salvar_excel(df, "pipeline_personalizado.xlsx")
    
    print(f"✅ Arquivo gerado: {arquivo}")
    
    # Mostrar algumas estatísticas
    print("\n📈 Estatísticas:")
    print(f"   • Total de registros: {len(df)}")
    print(f"   • Média de TabCoins: {df['TabCoins'].mean():.1f}")
    print(f"   • Autores únicos: {df['Autor'].nunique()}")

async def main():
    """Menu principal"""
    print("🚀 Exemplos de Uso do TabNews Extractor")
    print("=" * 50)
    
    opcoes = {
        "1": ("Busca Rápida (3 páginas)", exemplo_basico),
        "2": ("Busca Completa (20 páginas)", exemplo_completo),
        "3": ("Pipeline Personalizado", exemplo_personalizado)
    }
    
    print("\nEscolha uma opção:")
    for key, (desc, _) in opcoes.items():
        print(f"  {key}. {desc}")
    
    # Para demo, vamos executar a opção 1 automaticamente
    print("\n🔄 Executando automaticamente: Busca Rápida...")
    await exemplo_basico()

if __name__ == "__main__":
    asyncio.run(main())
