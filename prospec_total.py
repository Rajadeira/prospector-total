import streamlit as st
import json
from datetime import datetime

# Configuração da página
st.set_page_config(
    page_title="Prospector Total",
    page_icon="🎯",
    layout="wide"
)

# ============================================================
# CABEÇALHO SIMPLES
# ============================================================

col1, col2 = st.columns([1, 5])
with col1:
    try:
        st.image("WhatsApp Image 2026-05-19 at 08.27.01.jpeg", width=60)
    except:
        st.markdown("🎯")
with col2:
    st.title("Prospector Total")
    st.caption("Franquias | LinkedIn | Oportunidades")

st.divider()

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:
    st.header("📊 Painel")
    
    try:
        with open("alvos_linkedin.json", "r") as f:
            alvos = json.load(f)
            st.metric("Alvos", len(alvos))
    except:
        st.metric("Alvos", 0)
    
    try:
        with open("oportunidades_completas.json", "r") as f:
            opps = json.load(f)
            st.metric("Oportunidades", len(opps))
    except:
        st.metric("Oportunidades", 0)
    
    st.divider()
    st.caption(f"Atualizado: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# ============================================================
# ABAS
# ============================================================

tab1, tab2, tab3 = st.tabs(["🏪 Franquias", "🔍 LinkedIn", "📰 Notícias"])

# ------------------------------------------------------------
# TAB 1: FRANQUIAS
# ------------------------------------------------------------
with tab1:
    st.subheader("🔍 Buscas no Google")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**Editais e Credenciamento**")
        st.markdown("- [edital de credenciamento de fornecedores](https://www.google.com/search?q=edital+de+credenciamento+de+fornecedores&tbs=qdr:m)")
        st.markdown("- [chamamento público fornecedores](https://www.google.com/search?q=chamamento+p%C3%BAblico+fornecedores&tbs=qdr:m)")
        st.markdown("- [homologação de fornecedores](https://www.google.com/search?q=homologa%C3%A7%C3%A3o+de+fornecedores&tbs=qdr:m)")
    
    with col2:
        st.markdown("**Expansão**")
        st.markdown("- [expansão de franquias](https://www.google.com/search?q=expans%C3%A3o+de+franquias+Brasil&tbs=qdr:m)")
        st.markdown("- [novas franquias](https://www.google.com/search?q=novas+franquias+Brasil&tbs=qdr:m)")
        st.markdown("- [franquias abrindo unidades](https://www.google.com/search?q=franquias+abrindo+unidades&tbs=qdr:m)")
    
    st.divider()
    st.subheader("🏢 Portais")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("- [ABF - Fornecedores](https://www.abf.com.br/fornecedores/)")
        st.markdown("- [Portal do Franchising](https://www.portaldofranchising.com.br/fornecedores)")
    with col2:
        st.markdown("- [PEGN Franquias](https://revistapegn.globo.com/Franquias/)")
        st.markdown("- [Guia de Franquias](https://guiadefranquias.com.br)")

# ------------------------------------------------------------
# TAB 2: LINKEDIN
# ------------------------------------------------------------
with tab2:
    st.info("🔐 Mantenha o LinkedIn logado em outra aba")
    
    localizacao = st.selectbox(
        "Localização",
        ["Brasil", "São Paulo", "Rio de Janeiro", "Belo Horizonte", "Porto Alegre", "Curitiba"]
    )
    
    st.subheader("🎯 Buscar por cargo")
    
    loc_param = "" if localizacao == "Brasil" else f"&location={localizacao.replace(' ', '%20')}"
    
    cargos = [
        "Gerente de Compras",
        "Diretor de Suprimentos",
        "Head de Trade Marketing",
        "Category Manager"
    ]
    
    for cargo in cargos:
        url = f"https://www.linkedin.com/search/results/people/?keywords={cargo.replace(' ', '%20')}{loc_param}"
        st.markdown(f"- [{cargo}]({url})")
    
    st.divider()
    st.subheader("🏢 Empresas em expansão")
    
    for sinal in ["expansão", "novas lojas", "franquias", "contratando"]:
        url = f"https://www.linkedin.com/search/results/companies/?keywords={sinal}"
        st.markdown(f"- [{sinal.upper()}]({url})")

# ------------------------------------------------------------
# TAB 3: NOTÍCIAS
# ------------------------------------------------------------
with tab3:
    st.subheader("📰 Notícias do setor")
    
    noticias = {
        "Franquias": "expansão+de+franquias+Brasil",
        "Varejo": "nova+loja+inauguração+varejo",
        "Trade": "trade+marketing+oportunidades"
    }
    
    for nome, termo in noticias.items():
        url = f"https://news.google.com/search?q={termo}&hl=pt-BR&gl=BR"
        st.markdown(f"- [{nome}]({url})")
    
    st.divider()
    st.subheader("📝 Últimas oportunidades salvas")
    
    try:
        with open("oportunidades_completas.json", "r") as f:
            oportunidades = json.load(f)
        
        if oportunidades:
            for opp in oportunidades[:3]:
                st.markdown(f"**{opp.get('categoria', 'Geral')}**")
                st.markdown(f"{opp.get('titulo', '')[:80]}...")
                if opp.get('link'):
                    st.markdown(f"[Ver mais]({opp['link']})")
                st.divider()
        else:
            st.info("Nenhuma oportunidade salva ainda. Use o botão no sidebar para buscar.")
    except:
        st.info("Nenhuma oportunidade salva ainda.")

# ============================================================
# RODAPÉ
# ============================================================

st.divider()
st.caption("Prospector Total - Busca oportunidades em franquias e LinkedIn")