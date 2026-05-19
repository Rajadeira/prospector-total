import streamlit as st
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Prospector Total",
    page_icon="🎯",
    layout="wide"
)
# Cabeçalho com logo
try:
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image("WhatsApp Image 2026-05-19 at 08.27.01.jpeg", width=80)
    with col2:
        st.title("Prospector Total")
        st.markdown("### Seu centro de prospecção para Franquias e LinkedIn")
except:
    st.title("🎯 Prospector Total")
    st.markdown("### Seu centro de prospecção para Franquias e LinkedIn")

st.markdown("---")

# ============================================================
# CABEÇALHO
# ============================================================

# ============================================================
# CABEÇALHO COM LOGO
# ============================================================

# Carregar e exibir o logo
try:
    from PIL import Image
    logo = Image.open("logo.png")  # ou logo.jpg
    col1, col2 = st.columns([1, 4])
    with col1:
        st.image(logo, width=80)
    with col2:
        st.title("Prospector Total")
        st.markdown("### Seu centro de prospecção para Franquias e LinkedIn")
except:
    # Se não encontrar o logo, mostra só o título
    st.title("🎯 Prospector Total")
    st.markdown("### Seu centro de prospecção para Franquias e LinkedIn")

st.markdown("---")

# ============================================================
# SIDEBAR - Dashboard
# ============================================================

with st.sidebar:
    st.header("📊 Painel de Controle")
    
    # Estatísticas
    col1, col2 = st.columns(2)
    
    with col1:
        try:
            with open("alvos_linkedin.json", "r") as f:
                alvos = json.load(f)
                st.metric("🎯 Alvos", len(alvos))
        except:
            st.metric("🎯 Alvos", 0)
    
    with col2:
        try:
            with open("oportunidades_completas.json", "r") as f:
                opps = json.load(f)
                st.metric("📰 Oportunidades", len(opps))
        except:
            st.metric("📰 Oportunidades", 0)
    
    st.markdown("---")
    st.caption(f"🕐 {datetime.now().strftime('%d/%m/%Y %H:%M')}")
    
    st.markdown("### 📌 Comandos")
    st.code("python mega_prospector.py", language="bash")
    st.caption("Buscar novas oportunidades")

# ============================================================
# FUNÇÃO PARA GERAR LINK GOOGLE
# ============================================================

def google_link(termo, periodo="m"):
    """Gera link de busca no Google com filtro de período"""
    termo_formatado = termo.replace(" ", "+")
    filtros = {"h": "última hora", "d": "último dia", "w": "última semana", "m": "último mês"}
    filtro = f"&tbs=qdr:{periodo}" if periodo else ""
    return f"https://www.google.com/search?q={termo_formatado}{filtro}"

# ============================================================
# ABA 1: FRANQUIAS
# ============================================================

tab1, tab2, tab3 = st.tabs(["🏪 FRANQUIAS", "🔍 LINKEDIN", "📰 NOTÍCIAS"])

with tab1:
    st.markdown("## 🏪 Franquias e Fornecedores")
    
    # Seção 1: Buscas principais
    st.markdown("### 🔍 Buscas no Google")
    st.markdown("Clique nos links abaixo para encontrar oportunidades:")
    
    buscas_franquias = {
        "📄 Editais de Credenciamento": [
            "edital de credenciamento de fornecedores",
            "chamamento público fornecedores",
            "cadastro de fornecedores edital"
        ],
        "🤝 Homologação": [
            "homologação de fornecedores",
            "homologação de fornecedores franquia",
            "lista de fornecedores homologados"
        ],
        "🚀 Expansão": [
            "expansão de franquias",
            "novas franquias Brasil",
            "franquias abrindo unidades"
        ],
        "🏪 Oportunidades": [
            "seja um fornecedor franquia",
            "buscamos fornecedores franquia",
            "parceiros comerciais franquia"
        ]
    }
    
    for categoria, termos in buscas_franquias.items():
        with st.expander(categoria):
            for termo in termos:
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"`{termo}`")
                with col2:
                    st.markdown(f"[🔍 Buscar]({google_link(termo, 'm')})")
    
    st.markdown("---")
    
    # Seção 2: Portais oficiais
    st.markdown("### 🏢 Portais Oficiais")
    
    portais = {
        "ABF - Associação Brasileira de Franchising": "https://www.abf.com.br/fornecedores/",
        "Portal do Franchising": "https://www.portaldofranchising.com.br/fornecedores",
        "PEGN Franquias": "https://revistapegn.globo.com/Franquias/",
        "Guia de Franquias": "https://guiadefranquias.com.br"
    }
    
    cols = st.columns(2)
    for i, (nome, url) in enumerate(portais.items()):
        with cols[i % 2]:
            st.markdown(f"🔗 [{nome}]({url})")
    
    st.markdown("---")
    
    # Seção 3: Alertas Google
    st.markdown("### 🔔 Alertas Automáticos")
    st.markdown("Configure alertas para receber oportunidades por email:")
    
    alertas = [
        '"homologação de fornecedores"',
        '"credenciamento de fornecedores" -emprego',
        '"seja um fornecedor" franquia',
        'edital de credenciamento "fornecedores"'
    ]
    
    for alerta in alertas:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"`{alerta}`")
        with col2:
            alerta_url = f"https://www.google.com/alerts?q={alerta.replace(' ', '%20')}"
            st.markdown(f"[⚙️ Criar Alerta]({alerta_url})")

# ============================================================
# ABA 2: LINKEDIN
# ============================================================

with tab2:
    st.markdown("## 🔍 LinkedIn Prospector")
    st.info("⚠️ Mantenha o LinkedIn logado em outra aba para os links funcionarem")
    
    # Seção 1: Busca por cargos
    st.markdown("### 🎯 Buscar Decisores")
    
    localizacao = st.selectbox(
        "Localização",
        ["Brasil", "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre", "Curitiba"],
        index=0
    )
    
    cargos = [
        "Gerente de Compras",
        "Diretor de Suprimentos",
        "Head de Trade Marketing",
        "Category Manager",
        "Comprador Sênior",
        "Gerente de Supply Chain"
    ]
    
    st.markdown("**Clique para buscar:**")
    
    cols = st.columns(2)
    for i, cargo in enumerate(cargos):
        termo_url = cargo.replace(" ", "%20")
        loc_url = "" if localizacao == "Brasil" else f"&location={localizacao.replace(' ', '%20')}"
        linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={termo_url}{loc_url}"
        
        with cols[i % 2]:
            st.markdown(f"🔗 [{cargo}]({linkedin_url})")
    
    st.markdown("---")
    
    # Seção 2: Busca por empresas
    st.markdown("### 🏢 Buscar Empresas em Expansão")
    
    sinais = ["expansão", "novas lojas", "franquias", "contratando", "crescimento"]
    
    st.markdown("**Sinais de oportunidade:**")
    for sinal in sinais:
        url = f"https://www.linkedin.com/search/results/companies/?keywords={sinal}"
        st.markdown(f"- [{sinal.upper()}]({url})")
    
    st.markdown("---")
    
    # Seção 3: Dicas
    with st.expander("💡 Dicas de prospecção no LinkedIn"):
        st.markdown("""
        1. **Melhor momento para contato**: 2-8 semanas após mudança de cargo
        2. **Abordagem**: Personalize a mensagem mencionando a empresa
        3. **Empresas em expansão**: Contate antes da abertura da nova loja
        4. **Timing**: Segunda e terça-feira são os melhores dias
        """)

# ============================================================
# ABA 3: NOTÍCIAS
# ============================================================

with tab3:
    st.markdown("## 📰 Monitor de Notícias")
    
    # Buscas no Google News
    st.markdown("### 🔍 Últimas notícias do setor")
    
    termos_noticias = {
        "Franquias": "expansão de franquias Brasil",
        "Varejo": "nova loja inauguração varejo",
        "Trade": "trade marketing oportunidades",
        "Suprimentos": "contratação gerente de compras"
    }
    
    cols = st.columns(2)
    for i, (categoria, termo) in enumerate(termos_noticias.items()):
        url = f"https://news.google.com/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR&ceid=BR:pt"
        with cols[i % 2]:
            st.markdown(f"**{categoria}**")
            st.markdown(f"[🔍 Ver notícias]({url})")
            st.markdown("---")
    
    st.markdown("---")
    
    # Oportunidades salvas
    st.markdown("### 📝 Oportunidades Salvas")
    
    try:
        with open("oportunidades_completas.json", "r") as f:
            oportunidades = json.load(f)
        
        if oportunidades and len(oportunidades) > 0:
            for opp in oportunidades[-5:]:
                with st.container():
                    st.markdown(f"**{opp.get('categoria', 'Geral')}**")
                    st.markdown(f"{opp.get('titulo', '')[:100]}")
                    if opp.get('link'):
                        st.markdown(f"[Ver notícia]({opp['link']})")
                    st.markdown("---")
        else:
            st.info("Nenhuma oportunidade salva ainda.")
            st.code("python mega_prospector.py", language="bash")
            st.caption("Execute este comando para buscar oportunidades")
    except:
        st.info("Nenhuma oportunidade salva ainda.")
        st.code("python mega_prospector.py", language="bash")
        st.caption("Execute este comando para buscar oportunidades")

# ============================================================
# RODAPÉ
# ============================================================

st.markdown("---")
st.caption("🎯 Prospector Total | Links verificados | Atualizado em Maio 2026")