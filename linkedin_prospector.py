import json
from datetime import datetime

# Palavras-chave para cargos que você quer monitorar
CARGOS = [
    "gerente de compras",
    "diretor de compras",
    "coordenador de compras",
    "gerente de suprimentos",
    "diretor de suprimentos",
    "supply chain manager",
    "trade marketing",
    "category manager",
    "comprador senior",
    "head de compras",
    "gerente de supply chain"
]

def buscar_linkedin_oportunidades():
    """
    Gera URLs de busca do LinkedIn que você pode abrir no navegador
    """
    print("🔍 LinkedIn - Busca de cargos estratégicos")
    print("=" * 70)
    print("⚠️ IMPORTANTE: O LinkedIn não permite scraping automático.")
    print("   Copie e cole as URLs abaixo no seu NAVEGADOR:\n")
    
    links = []
    
    for cargo in CARGOS:
        # URL de busca do LinkedIn (pública)
        query = cargo.replace(" ", "%20")
        url = f"https://www.linkedin.com/jobs/search/?keywords={query}&location=Brasil"
        links.append({"cargo": cargo, "url": url})
        print(f"📌 {cargo.upper()}:")
        print(f"   {url}\n")
    
    # Salva os links em um arquivo para fácil acesso
    with open("linkedin_buscas.json", "w", encoding="utf-8") as f:
        json.dump({
            "data_geracao": datetime.now().isoformat(),
            "cargos": CARGOS,
            "links": links
        }, f, indent=2, ensure_ascii=False)
    
    print("=" * 70)
    print("💾 Links salvos em 'linkedin_buscas.json'")
    print("📝 Você também pode usar o Google com:")
    print('   site:linkedin.com/in "gerente de compras" Brasil')

def gerar_busca_google():
    """Gera buscas no Google como alternativa"""
    print("\n" + "=" * 70)
    print("🔍 BUSCA NO GOOGLE (alternativa ao LinkedIn):")
    print("=" * 70)
    
    for cargo in CARGOS[:5]:  # Mostra os 5 primeiros
        query = f'site:linkedin.com/in "{cargo}" Brasil'
        google_url = f"https://www.google.com/search?q={query.replace(' ', '%20')}"
        print(f"\n📌 {cargo}:")
        print(f"   {google_url}")

if __name__ == "__main__":
    buscar_linkedin_oportunidades()
    gerar_busca_google()