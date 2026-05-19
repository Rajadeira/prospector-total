import feedparser
import re
import json
from datetime import datetime

# Suas palavras-chave organizadas por categoria
CATEGORIAS = {
    "Franquias": ["franquia", "franquias", "rede de franquias", "expansão de franquia"],
    "Lojas": ["nova loja", "novas lojas", "abertura de loja", "inauguração", "unidade"],
    "Trade Marketing": ["trade marketing", "merchandising", "pdv", "ponto de venda", "gôndola"],
    "Compras/Suprimentos": ["compras", "suprimentos", "supply chain", "fornecedores", "homologação", "credenciamento"],
    "Mudança de Cargo": ["gerente de compras", "diretor de suprimentos", "head de compras", "novo gerente", "contratação"]
}

def buscar_oportunidades():
    print("🔍 Buscando oportunidades de negócios...")
    print("=" * 60)
    
    # Busca ampla (sem filtro muito restritivo)
    url = "https://news.google.com/rss?q=empresas+negócios+brasil+mercado&hl=pt-BR&gl=BR&ceid=BR:pt"
    
    try:
        feed = feedparser.parse(url)
        print(f"📰 Total de notícias analisadas: {len(feed.entries)}")
        
        todas_oportunidades = []
        
        for entry in feed.entries:
            titulo = entry.get('title', '')
            link = entry.get('link', '')
            data = entry.get('published', '')
            
            # Verifica cada categoria
            for categoria, palavras in CATEGORIAS.items():
                for palavra in palavras:
                    if palavra.lower() in titulo.lower():
                        todas_oportunidades.append({
                            "titulo": titulo,
                            "link": link,
                            "data": data,
                            "categoria": categoria,
                            "palavra_encontrada": palavra
                        })
                        break  # Sai para não duplicar a mesma notícia na mesma categoria
                else:
                    continue
                break
        
        # Remove duplicatas (mesmo título)
        oportunidades_unicas = []
        titulos_vistos = set()
        for opp in todas_oportunidades:
            if opp['titulo'] not in titulos_vistos:
                titulos_vistos.add(opp['titulo'])
                oportunidades_unicas.append(opp)
        
        # Salva resultados
        with open("oportunidades.json", "w", encoding="utf-8") as f:
            json.dump(oportunidades_unicas, f, indent=2, ensure_ascii=False)
        
        # Mostra resultados organizados
        if oportunidades_unicas:
            print(f"\n✅ Encontradas {len(oportunidades_unicas)} oportunidades:\n")
            
            # Mostrar por categoria
            for categoria in CATEGORIAS.keys():
                da_categoria = [opp for opp in oportunidades_unicas if opp['categoria'] == categoria]
                if da_categoria:
                    print(f"\n📌 {categoria} ({len(da_categoria)}):")
                    for opp in da_categoria[:5]:  # Mostra até 5 por categoria
                        print(f"   • {opp['titulo'][:80]}...")
            
            # Mostrar primeiras 10 em detalhe
            print(f"\n📋 DETALHES (primeiras 10):\n")
            for i, opp in enumerate(oportunidades_unicas[:10], 1):
                print(f"{i}. [{opp['categoria']}] {opp['titulo']}")
                print(f"   🔗 {opp['link']}\n")
        else:
            print("\n⚠️ Nenhuma oportunidade encontrada.")
            
        print(f"📁 Resultados salvos em: oportunidades.json")
        
    except Exception as e:
        print(f"❌ Erro: {e}")

def mostrar_estatisticas():
    """Mostra estatísticas das oportunidades encontradas"""
    try:
        with open("oportunidades.json", "r", encoding="utf-8") as f:
            dados = json.load(f)
        
        if dados:
            print("\n📊 ESTATÍSTICAS:")
            print(f"   Total de oportunidades: {len(dados)}")
            
            # Conta por categoria
            categorias_count = {}
            for opp in dados:
                cat = opp['categoria']
                categorias_count[cat] = categorias_count.get(cat, 0) + 1
            
            for cat, count in categorias_count.items():
                print(f"   • {cat}: {count}")
    except:
        pass

if __name__ == "__main__":
    buscar_oportunidades()
    mostrar_estatisticas()