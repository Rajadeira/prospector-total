import feedparser
import re
import json
from datetime import datetime
import subprocess
import sys

# Configurações
CATEGORIAS = {
    "Franquias": ["franquia", "franquias", "rede de franquias", "expansão de franquia", "franqueado"],
    "Lojas": ["nova loja", "novas lojas", "abertura de loja", "inauguração", "unidade"],
    "Trade Marketing": ["trade marketing", "merchandising", "pdv", "ponto de venda", "gôndola", "expositor"],
    "Compras/Suprimentos": ["compras", "suprimentos", "supply chain", "fornecedores", "homologação", "credenciamento", "logística"],
    "Mudança de Cargo": ["gerente de compras", "diretor de suprimentos", "head de compras", "novo gerente", "contratação", "supply chain manager"]
}

def buscar_google_news():
    """Busca oportunidades no Google News"""
    print("🔍 [Google News] Buscando oportunidades...")
    url = "https://news.google.com/rss?q=empresas+negócios+brasil+mercado&hl=pt-BR&gl=BR&ceid=BR:pt"
    
    try:
        feed = feedparser.parse(url)
        oportunidades = []
        
        for entry in feed.entries:
            titulo = entry.get('title', '')
            for categoria, palavras in CATEGORIAS.items():
                for palavra in palavras:
                    if palavra.lower() in titulo.lower():
                        oportunidades.append({
                            "fonte": "Google News",
                            "titulo": titulo,
                            "link": entry.get('link', ''),
                            "data": entry.get('published', ''),
                            "categoria": categoria,
                            "palavra_chave": palavra
                        })
                        break
                else:
                    continue
                break
        
        return oportunidades
    except Exception as e:
        print(f"   ❌ Erro no Google News: {e}")
        return []

def gerar_relatorio(oportunidades):
    """Gera relatório formatado"""
    if not oportunidades:
        print("\n⚠️ Nenhuma oportunidade encontrada.")
        return
    
    print(f"\n📊 RELATÓRIO DE OPORTUNIDADES - {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    print("=" * 70)
    
    # Agrupar por categoria
    por_categoria = {}
    for opp in oportunidades:
        cat = opp['categoria']
        if cat not in por_categoria:
            por_categoria[cat] = []
        por_categoria[cat].append(opp)
    
    for categoria, items in por_categoria.items():
        print(f"\n📌 {categoria} ({len(items)} oportunidades):")
        for item in items[:5]:  # Mostra até 5 por categoria
            print(f"   • {item['titulo'][:80]}...")
            print(f"     🔗 {item['link'][:60]}...")
            print(f"     🏷️  Palavra: {item['palavra_chave']}")
    
    # Salvar em JSON
    with open("oportunidades_completas.json", "w", encoding="utf-8") as f:
        json.dump(oportunidades, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 {len(oportunidades)} oportunidades salvas em 'oportunidades_completas.json'")

def main():
    print("=" * 70)
    print("🚀 MEGA PROSPECTOR - Franquias | Lojas | Trade | Suprimentos")
    print("=" * 70)
    
    # Buscar no Google News
    oportunidades = buscar_google_news()
    
    # Gerar relatório
    gerar_relatorio(oportunidades)
    
    # Dicas para LinkedIn
    print("\n" + "=" * 70)
    print("📌 DICA PARA LINKEDIN:")
    print("Execute: python linkedin_prospector.py")
    print("para obter links de busca de cargos no LinkedIn")
    print("=" * 70)

if __name__ == "__main__":
    main()