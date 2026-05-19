import streamlit as st
import json
from datetime import datetime
import pandas as pd
import hashlib

# Configuração da página
st.set_page_config(
    page_title="Franquia Prospector",
    page_icon="🏪",
    layout="wide"
)

# Inicializar session state
if 'oportunidades_franquias' not in st.session_state:
    st.session_state.oportunidades_franquias = []
if 'alertas_franquias' not in st.session_state:
    st.session_state.alertas_franquias = []

# ============================================================
# LINKS VERIFICADOS E FUNCIONAIS (atualizados em Maio 2026)
# ============================================================

PORTAIS_CONFIAVEIS = {
    "🏆 ABF - Associação Brasileira de Franchising": {
        "url": "https://www.abf.com.br",
        "secao_fornecedores": "https://www.abf.com.br/fornecedores/",
        "utilidade": "Portal oficial com lista de fornecedores homologados e eventos"
    },
    "📰 Portal do Franchising": {
        "url": "https://www.portaldofranchising.com.br",
        "secao_fornecedores": "https://www.portaldofranchising.com.br/fornecedores",
        "utilidade": "Notícias e oportunidades de fornecimento"
    },
    "📊 PEGN Franquias": {
        "url": "https://revistapegn.globo.com/Franquias/",
        "secao_noticias": "https://revistapegn.globo.com/Franquias/noticias/",
        "utilidade": "Notícias de expansão e novas redes"
    },
    "📈 Exame Franquias": {
        "url": "https://exame.com/franquias/",
        "utilidade": "Rankings e franquias em expansão"
    },
    "🏪 Franquias.com.br": {
        "url": "https://www.franquias.com.br",
        "utilidade": "Diretório de franquias no Brasil"
    },
    "📋 Guia de Franquias": {
        "url": "https://guiadefranquias.com.br",
        "utilidade": "Lista de franquias por setor"
    }
}

# ============================================================
# BUSCAS DIRETAS NO GOOGLE (MAIS CONFIÁVEIS)
# ============================================================

BUSCAS_GOOGLE = {
    "🎯 Editais de Credenciamento": [
        "edital de credenciamento de fornecedores",
        "chamamento público para credenciamento de fornecedores",
        "cadastro de fornecedores edital",
        "credenciamento de prestadores de serviços"
    ],
    "🤝 Homologação de Fornecedores": [
        "homologação de fornecedores",
        "homologação de fornecedores franquia",
        "como se tornar fornecedor homologado",
        "lista de fornecedores homologados"
    ],
    "🚀 Expansão de Franquias": [
        "expansão de franquias 2026",
        "novas franquias Brasil",
        "rede de franquias em crescimento",
        "franquias abrindo unidades"
    ],
    "🏪 Oportunidades de Fornecimento": [
        "seja um fornecedor franquia",
        "buscamos fornecedores para franquia",
        "parceiros comerciais franquia",
        "fornecedor para rede de franquias"
    ],
    "📢 Licitações e Compras Públicas": [
        "site:pncp.gov.br credenciamento",
        "site:compras.gov.br fornecedores",
        "edital de credenciamento prefeitura",
        "compras públicas fornecedores"
    ]
}

# ============================================================
# FUNÇÕES
# ============================================================

def gerar_link_google(termo):
    """Gera link de busca no Google para um termo"""
    termo_formatado = termo.replace(" ", "+")
    return f"https://www.google.com/search?q={termo_formatado}"

def gerar_link_google_avancado(termo, periodo="ultimo_mes"):
    """Gera link com filtro de data"""
    termo_formatado = termo.replace(" ", "+")
    
    filtros = {
        "ultima_hora": "&tbs=qdr:h",
        "ultimo_dia": "&tbs=qdr:d",
        "ultima_semana": "&tbs=qdr:w",
        "ultimo_mes": "&tbs=qdr:m",
        "ultimo_ano": "&tbs=qdr:y"
    }
    
    filtro = filtros.get(periodo, "")
    return f"https://www.google.com/search?q={termo_formatado}{filtro}"

def buscar_site_especifico(dominio, termo):
    """Busca um termo dentro de um site específico"""
    return f"https://www.google.com/search?q=site:{dominio}+{termo.replace(' ', '+')}"

def salvar_alertas():
    with open("alertas_franquias.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.alertas_franquias, f, indent=2, ensure_ascii=False)

# ============================================================
# INTERFACE
# ============================================================

st.title("🏪 Franquia Prospector")
st.markdown("### Encontre oportunidades de fornecimento em redes de franquias")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    periodo_padrao = st.selectbox(
        "Período padrão para buscas",
        ["ultimo_mes", "ultima_semana", "ultimo_dia", "ultimo_ano"],
        index=0
    )
    
    st.markdown("---")
    st.header("📊 Estatísticas")
    st.metric("Alertas ativos", len(st.session_state.alertas_franquias))
    st.metric("Oportunidades salvas", len(st.session_state.oportunidades_franquias))
    
    st.markdown("---")
    st.caption("💡 Dica: Clique nos 🔗 para abrir as buscas")

# Abas principais
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🔍 Buscas Diretas", "🏢 Portais de Franquias", "📄 Editais e Licitações", 
    "🔔 Alertas", "📝 Oportunidades Salvas"
])

# ============================================================
# TAB 1: BUSCAS DIRETAS
# ============================================================
with tab1:
    st.subheader("🎯 Buscas prontas - Clique e pesquise")
    st.markdown("Os links abaixo abrem buscas no Google com as palavras-chave mais relevantes")
    
    for categoria, termos in BUSCAS_GOOGLE.items():
        with st.expander(f"{categoria} (clique para expandir)", expanded=False):
            for termo in termos:
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col1:
                    st.markdown(f"`{termo}`")
                with col2:
                    url = gerar_link_google_avancado(termo, periodo_padrao)
                    st.markdown(f"[🔍 Buscar]({url})")
                with col3:
                    url_mes = gerar_link_google_avancado(termo, "ultimo_mes")
                    st.markdown(f"[📅 Último mês]({url_mes})")
                
                # Botão para salvar oportunidade
                if st.button(f"⭐ Salvar", key=f"save_{hashlib.md5(termo.encode()).hexdigest()}"):
                    nova_opp = {
                        "id": hashlib.md5(f"{termo}{datetime.now()}".encode()).hexdigest()[:8],
                        "termo": termo,
                        "categoria": categoria,
                        "url": gerar_link_google(termo),
                        "data": datetime.now().isoformat()
                    }
                    st.session_state.oportunidades_franquias.append(nova_opp)
                    salvar_alertas()
                    st.toast(f"✅ Oportunidade salva!", icon="✅")
    
    st.markdown("---")
    st.markdown("### 🔎 Busca personalizada")
    
    col1, col2 = st.columns([3, 1])
    with col1:
        termo_personalizado = st.text_input(
            "Digite seu próprio termo de busca",
            placeholder="Ex: 'fornecedor de embalagens para franquias'"
        )
    with col2:
        periodo_personalizado = st.selectbox(
            "Período",
            ["ultimo_mes", "ultima_semana", "ultimo_dia", "ultimo_ano"],
            index=0,
            key="periodo_custom"
        )
    
    if termo_personalizado:
        url_custom = gerar_link_google_avancado(termo_personalizado, periodo_personalizado)
        st.markdown(f"🔗 [Buscar: {termo_personalizado}]({url_custom})")

# ============================================================
# TAB 2: PORTAIS DE FRANQUIAS
# ============================================================
with tab2:
    st.subheader("🏢 Portais oficiais e diretórios")
    st.markdown("Acesse diretamente os portais especializados em franquias")
    
    for nome, info in PORTAIS_CONFIAVEIS.items():
        with st.container():
            col1, col2, col3 = st.columns([2, 1, 1])
            
            with col1:
                st.markdown(f"**{nome}**")
                st.caption(info.get("utilidade", ""))
            
            with col2:
                st.markdown(f"[🌐 Acessar site]({info['url']})")
            
            with col3:
                if "secao_fornecedores" in info:
                    st.markdown(f"[🤝 Fornecedores]({info['secao_fornecedores']})")
                elif "secao_noticias" in info:
                    st.markdown(f"[📰 Notícias]({info['secao_noticias']})")
            
            st.markdown("---")

# ============================================================
# TAB 3: EDITAIS E LICITAÇÕES
# ============================================================
with tab3:
    st.subheader("📄 Editais de Credenciamento e Licitações")
    
    st.info("Portais oficiais onde empresas publicam editais buscando fornecedores")
    
    # Portais oficiais de compras
    portais_oficiais = {
        "PNCP - Portal Nacional de Contratações Públicas": "https://pncp.gov.br",
        "Compras.gov.br": "https://www.gov.br/compras",
        "Portal de Compras Públicas": "https://www.portaldecompraspublicas.com.br",
        "BEC - São Paulo": "https://bec.sp.gov.br",
        "ComprasNet (Federativo)": "https://www.comprasnet.gov.br"
    }
    
    st.markdown("### 🏛️ Portais de Compras Públicas")
    for nome, url in portais_oficiais.items():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"**{nome}**")
        with col2:
            st.markdown(f"[🔗 Acessar]({url})")
    
    st.markdown("---")
    st.markdown("### 🔍 Busca específica por editais")
    
    termos_edital = [
        "edital de credenciamento",
        "chamamento público fornecedores", 
        "cadastramento de fornecedores",
        "credenciamento de prestadores"
    ]
    
    for termo in termos_edital:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"`{termo}`")
        with col2:
            url = gerar_link_google_avancado(f'"{termo}"', periodo_padrao)
            st.markdown(f"[🔍 Buscar]({url})")

# ============================================================
# TAB 4: ALERTAS
# ============================================================
with tab4:
    st.subheader("🔔 Google Alerts - Receba oportunidades por email")
    
    st.markdown("""
    ### Como configurar:
    
    1. Acesse [Google Alerts](https://www.google.com/alerts)
    2. Copie e cole um dos termos abaixo
    3. Escolha frequência: **"uma vez ao dia"**
    4. Configure seu email
    """)
    
    # Termos sugeridos para alertas
    st.markdown("### 📋 Termos sugeridos para alertas")
    
    termos_alerta = [
        '"homologação de fornecedores"',
        '"credenciamento de fornecedores" -emprego',
        '"buscamos fornecedores" franquia',
        '"seja um fornecedor" franquia',
        'edital de credenciamento "fornecedores"'
    ]
    
    for termo in termos_alerta:
        col1, col2 = st.columns([3, 1])
        with col1:
            st.markdown(f"`{termo}`")
        with col2:
            alerta_url = f"https://www.google.com/alerts?q={termo.replace(' ', '%20')}"
            st.markdown(f"[⚙️ Criar Alerta]({alerta_url})")
    
    st.markdown("---")
    st.markdown("### ✨ Criar alerta personalizado")
    
    with st.form("novo_alerta"):
        termo_novo = st.text_input(
            "Termo para monitorar",
            placeholder='ex: "fornecedor de alimentos" franquia'
        )
        frequencia = st.selectbox("Frequência", ["uma vez ao dia", "como acontece", "uma vez por semana"])
        
        if st.form_submit_button("💾 Salvar alerta"):
            if termo_novo:
                alerta = {
                    "id": hashlib.md5(termo_novo.encode()).hexdigest()[:8],
                    "termo": termo_novo,
                    "frequencia": frequencia,
                    "data_criacao": datetime.now().isoformat(),
                    "link_alerta": f"https://www.google.com/alerts?q={termo_novo.replace(' ', '%20')}"
                }
                st.session_state.alertas_franquias.append(alerta)
                salvar_alertas()
                st.success(f"✅ Alerta salvo! Configure em: {alerta['link_alerta']}")

# ============================================================
# TAB 5: OPORTUNIDADES SALVAS
# ============================================================
with tab5:
    st.subheader("📝 Oportunidades salvas")
    
    if st.session_state.oportunidades_franquias:
        df = pd.DataFrame(st.session_state.oportunidades_franquias)
        st.dataframe(df, use_container_width=True)
        
        if st.button("🗑️ Limpar todas as oportunidades"):
            st.session_state.oportunidades_franquias = []
            salvar_alertas()
            st.rerun()
    else:
        st.info("Nenhuma oportunidade salva ainda. Clique em '⭐ Salvar' nas buscas para guardar oportunidades.")

# ============================================================
# RODAPÉ
# ============================================================
st.markdown("---")
st.caption("⚡ Franquia Prospector | Links verificados e funcionais | Atualizado em Maio 2026")