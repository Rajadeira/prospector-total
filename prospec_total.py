import streamlit as st
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Prospector Total",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PERSONALIZADO
# ============================================================

st.markdown("""
<style>
    /* Cards para as abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: white;
        border-radius: 8px;
        padding: 8px 20px;
        font-weight: 500;
    }
    .stTabs [aria-selected="true"] {
        background-color: #1E88E5;
        color: white;
    }
    
    /* Cards personalizados */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        margin-bottom: 16px;
        border: 1px solid #eaeaea;
    }
    
    /* Títulos */
    .section-title {
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 16px;
        color: #1E88E5;
        border-left: 4px solid #1E88E5;
        padding-left: 12px;
    }
    
    /* Links personalizados */
    .link-card {
        background: #F8F9FA;
        padding: 10px 15px;
        border-radius: 8px;
        margin: 5px 0;
        transition: 0.2s;
    }
    .link-card:hover {
        background: #E3F2FD;
        transform: translateX(5px);
    }
    .link-card a {
        text-decoration: none;
        color: #1E88E5;
        font-weight: 500;
    }
    
    /* Sidebar personalizada */
    [data-testid="stSidebar"] {
        background-color: #FFFFFF;
        border-right: 1px solid #EAEAEA;
    }
    
    /* Footer */
    .footer {
        text-align: center;
        padding: 20px;
        color: #6C757D;
        font-size: 0.8rem;
        border-top: 1px solid #EAEAEA;
        margin-top: 40px;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# CABEÇALHO COM LOGO
# ============================================================

try:
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image("WhatsApp Image 2026-05-19 at 08.27.01.jpeg", width=100)
    st.markdown("<h1 style='text-align: center; color: #2C3E50;'>Prospector Total</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6C757D;'>Seu centro de prospecção para Franquias e LinkedIn</p>", unsafe_allow_html=True)
except:
    st.markdown("<h1 style='text-align: center;'>🎯 Prospector Total</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>Seu centro de prospecção para Franquias e LinkedIn</p>", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# SIDEBAR - Painel de Controle
# ============================================================

with st.sidebar:
    st.markdown("## 📊 Painel")
    
    try:
        with open("alvos_linkedin.json", "r") as f:
            alvos = json.load(f)
            st.metric("🎯 Alvos", len(alvos), delta="+ este mês", delta_color="normal")
    except:
        st.metric("🎯 Alvos", 0)
    
    try:
        with open("oportunidades_completas.json", "r") as f:
            opps = json.load(f)
            st.metric("📰 Oportunidades", len(opps))
    except:
        st.metric("📰 Oportunidades", 0)
    
    st.markdown("---")
    st.markdown("### 📅 Última atualização")
    st.caption(f"{datetime.now().strftime('%d/%m/%Y às %H:%M')}")
    
    st.markdown("---")
    st.markdown("### ⚡ Comando Rápido")
    st.code("python mega_prospector.py", language="bash")
    st.caption("Atualizar oportunidades")

# ============================================================
# TABS
# ============================================================

tab1, tab2, tab3 = st.tabs(["🏪 FRANQUIAS", "🔍 LINKEDIN", "📰 NOTÍCIAS"])

# ============================================================
# TAB 1: FRANQUIAS
# ============================================================
with tab1:
    st.markdown('<div class="section-title">🔍 Buscas no Google</div>', unsafe_allow_html=True)
    
    # Cards de busca
    buscas = {
        "Editais de Credenciamento": [
            "edital de credenciamento de fornecedores",
            "chamamento público fornecedores"
        ],
        "Homologação de Fornecedores": [
            "homologação de fornecedores",
            "homologação de fornecedores franquia"
        ],
        "Expansão": [
            "expansão de franquias Brasil",
            "novas franquias em expansão"
        ]
    }
    
    cols = st.columns(3)
    for idx, (categoria, termos) in enumerate(buscas.items()):
        with cols[idx]:
            st.markdown(f"**{categoria}**")
            for termo in termos:
                url = f"https://www.google.com/search?q={termo.replace(' ', '+')}&tbs=qdr:m"
                st.markdown(f'<div class="link-card">🔗 [{termo}]({url})</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-title">🏢 Portais Oficiais</div>', unsafe_allow_html=True)
    
    portais = {
        "ABF": "https://www.abf.com.br/fornecedores/",
        "Portal do Franchising": "https://www.portaldofranchising.com.br/fornecedores",
        "PEGN Franquias": "https://revistapegn.globo.com/Franquias/",
        "Guia de Franquias": "https://guiadefranquias.com.br"
    }
    
    cols = st.columns(2)
    for i, (nome, url) in enumerate(portais.items()):
        with cols[i % 2]:
            st.markdown(f'<div class="link-card">🏢 [{nome}]({url})</div>', unsafe_allow_html=True)

# ============================================================
# TAB 2: LINKEDIN
# ============================================================
with tab2:
    st.info("🔐 Mantenha o LinkedIn logado em outra aba para os links funcionarem")
    
    st.markdown('<div class="section-title">🎯 Decisores por Cargo</div>', unsafe_allow_html=True)
    
    localizacao = st.selectbox(
        "📍 Filtrar por localização",
        ["Brasil", "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre", "Curitiba"]
    )
    
    cargos = [
        "Gerente de Compras",
        "Diretor de Suprimentos",
        "Head de Trade Marketing",
        "Category Manager",
        "Comprador Sênior"
    ]
    
    cols = st.columns(2)
    for i, cargo in enumerate(cargos):
        with cols[i % 2]:
            termo_url = cargo.replace(" ", "%20")
            loc_url = "" if localizacao == "Brasil" else f"&location={localizacao.replace(' ', '%20')}"
            url = f"https://www.linkedin.com/search/results/people/?keywords={termo_url}{loc_url}"
            st.markdown(f'<div class="link-card">👤 [{cargo}]({url})</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-title">🏢 Empresas em Expansão</div>', unsafe_allow_html=True)
    
    sinais = ["expansão", "novas lojas", "franquias", "contratando"]
    for sinal in sinais:
        url = f"https://www.linkedin.com/search/results/companies/?keywords={sinal}"
        st.markdown(f'<div class="link-card">📈 [{sinal.upper()}]({url})</div>', unsafe_allow_html=True)

# ============================================================
# TAB 3: NOTÍCIAS
# ============================================================
with tab3:
    st.markdown('<div class="section-title">📰 Últimas Notícias do Setor</div>', unsafe_allow_html=True)
    
    noticias = {
        "Franquias": "expansão de franquias Brasil",
        "Varejo": "nova loja inauguração varejo",
        "Trade Marketing": "trade marketing oportunidades",
        "Suprimentos": "contratação gerente de compras"
    }
    
    cols = st.columns(2)
    for i, (categoria, termo) in enumerate(noticias.items()):
        with cols[i % 2]:
            url = f"https://news.google.com/search?q={termo.replace(' ', '+')}&hl=pt-BR&gl=BR"
            st.markdown(f'<div class="link-card">📌 [{categoria}]({url})</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown('<div class="section-title">📝 Oportunidades Salvas</div>', unsafe_allow_html=True)
    
    try:
        with open("oportunidades_completas.json", "r") as f:
            oportunidades = json.load(f)
        
        if oportunidades and len(oportunidades) > 0:
            for opp in oportunidades[:5]:
                with st.container():
                    st.markdown(f"**{opp.get('categoria', 'Geral')}**")
                    st.markdown(f"{opp.get('titulo', '')[:100]}")
                    if opp.get('link'):
                        st.markdown(f"[🔗 Ver notícia]({opp['link']})")
                    st.markdown("---")
        else:
            st.info("Nenhuma oportunidade salva. Execute o comando no sidebar para buscar.")
    except:
        st.info("Nenhuma oportunidade salva ainda.")

# ============================================================
# RODAPÉ
# ============================================================

st.markdown('<div class="footer">🚀 Prospector Total | Versão 2.0 | Desenvolvido para sua empresa</div>', unsafe_allow_html=True)