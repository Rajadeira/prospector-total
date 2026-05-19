import streamlit as st
import pandas as pd
import json
import re
from datetime import datetime
import hashlib

# Configuração da página
st.set_page_config(
    page_title="LinkedIn Prospector PRO",
    page_icon="🚀",
    layout="wide"
)

# Inicializar session state
if 'alvos' not in st.session_state:
    st.session_state.alvos = []
if 'mudancas' not in st.session_state:
    st.session_state.mudancas = []
if 'alertas' not in st.session_state:
    st.session_state.alertas = []

# Funções auxiliares
def salvar_alvos():
    with open("alvos_linkedin.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.alvos, f, indent=2, ensure_ascii=False)

def carregar_alvos():
    try:
        with open("alvos_linkedin.json", "r", encoding="utf-8") as f:
            st.session_state.alvos = json.load(f)
    except:
        st.session_state.alvos = []

def salvar_alertas():
    with open("alertas_google.json", "w", encoding="utf-8") as f:
        json.dump(st.session_state.alertas, f, indent=2, ensure_ascii=False)

def carregar_alertas():
    try:
        with open("alertas_google.json", "r", encoding="utf-8") as f:
            st.session_state.alertas = json.load(f)
    except:
        st.session_state.alertas = []

def gerar_roteiro(nome, cargo, empresa, oportunidade):
    """Gera roteiro personalizado baseado no perfil"""
    
    roteiros = {
        "Gerente de Compras": f"""Olá {nome},

Vi que você é Gerente de Compras na {empresa} e que {oportunidade}.

Tenho experiência ajudando empresas do seu setor a otimizar a cadeia de suprimentos e reduzir custos com fornecedores.

Podemos conversar por 5 minutos para eu entender melhor seus desafios?

Atenciosamente,
[Seu Nome]""",

        "Diretor de Suprimentos": f"""Prezado {nome},

Acompanho a {empresa} e vi que {oportunidade}.

Como Diretor de Suprimentos, você deve estar avaliando novos parceiros estratégicos. Tenho cases de sucesso em homologação de fornecedores para redes em expansão.

Posso enviar mais informações?

Atenciosamente,
[Seu Nome]""",

        "Head de Trade Marketing": f"""Olá {nome},

Parabéns pelo trabalho na {empresa}! Percebi que {oportunidade}.

Tenho soluções que podem ajudar a maximizar seus resultados em trade marketing, especialmente em momentos de expansão.

Topa um café virtual de 10 minutos?

Abraço,
[Seu Nome]""",

        "Category Manager": f"""Oi {nome},

A {empresa} está em um momento interessante com {oportunidade}.

Como Category Manager, você deve estar buscando fornecedores que agreguem valor à sua categoria. Posso compartilhar algumas ideias?

Vamos conversar?

[Seu Nome]""",

        "Comprador Sênior": f"""Olá {nome},

Vi que a {empresa} está {oportunidade} e que você atua como Comprador Sênior.

Tenho produtos/serviços que podem ser relevantes para sua carteira. Posso enviar um material rápido?

Abs,
[Seu Nome]"""
    }
    
    return roteiros.get(cargo, f"""Olá {nome},

Vi seu perfil no LinkedIn e que você é {cargo} na {empresa}. Percebi também que {oportunidade}

Acredito que posso agregar valor com minhas soluções para o seu momento.

Podemos trocar uma ideia rápida?

Att,
[Seu Nome]""")

def monitorar_mudancas():
    """Monitora mudanças de cargo"""
    if st.session_state.alvos:
        st.info("📊 Para monitorar mudanças reais, salve os perfis e verifique manualmente a cada 30 dias.")
        
        df = pd.DataFrame(st.session_state.alvos)
        st.dataframe(df[["nome", "cargo", "empresa", "data_inclusao"]], use_container_width=True)
        
        st.markdown("### 📅 Próximos checkpoints:")
        for alvo in st.session_state.alvos:
            data = datetime.fromisoformat(alvo["data_inclusao"])
            dias = (datetime.now() - data).days
            if dias >= 30:
                st.warning(f"🔔 **{alvo['nome']}** - Já faz {dias} dias. Hora de verificar se mudou de cargo!")
            else:
                st.info(f"📌 {alvo['nome']} - Próxima verificação em {30-dias} dias")
    else:
        st.info("Adicione alvos para monitorar")

# Interface principal
st.title("🚀 LinkedIn Prospector PRO")
st.markdown("---")

# Sidebar
with st.sidebar:
    st.header("📊 Dashboard")
    st.metric("Total de Alvos", len(st.session_state.alvos))
    st.metric("Alertas Ativos", len(st.session_state.alertas))
    
    st.markdown("---")
    st.header("🎯 Ações Rápidas")
    if st.button("🔄 Carregar Alvos Salvos"):
        carregar_alvos()
        st.success(f"Carregados {len(st.session_state.alvos)} alvos")
    if st.button("🔔 Carregar Alertas"):
        carregar_alertas()
        st.success(f"Carregados {len(st.session_state.alertas)} alertas")

# Abas principais
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🔍 Buscar", "📝 Alvos", "✍️ Roteiros", "👀 Monitorar", "📡 Monitor Feed", "📈 Relatórios"
])

# Tab 1: Buscar (Busca tradicional LinkedIn)
with tab1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("🎯 Defina seu alvo")
        
        cargos = st.text_area(
            "Cargos",
            value="Gerente de Compras\nDiretor de Suprimentos\nHead de Trade Marketing\nCategory Manager\nComprador Sênior",
            height=150
        )
        
        palavras_chave = st.text_input(
            "Palavras-chave adicionais",
            placeholder="Ex: expansão, franquias, novas lojas"
        )
    
    with col2:
        st.subheader("📍 Localização")
        localizacao = st.selectbox(
            "Região",
            ["Brasil", "São Paulo", "Rio de Janeiro", "Minas Gerais", "Paraná", "Santa Catarina", "Rio Grande do Sul"]
        )
        
        setores = st.multiselect(
            "Setores",
            ["Varejo", "Alimentação", "Construção", "Tecnologia", "Saúde", "Educação", "Logística"]
        )
    
    if st.button("🔍 Gerar Links de Busca", type="primary"):
        lista_cargos = [c.strip() for c in cargos.split('\n') if c.strip()]
        
        st.markdown("### 📋 Links para prospecção")
        st.info("⚠️ Faça login no LinkedIn antes de clicar nos links")
        
        for cargo in lista_cargos:
            termo_url = cargo.replace(" ", "%20")
            linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={termo_url}&location={localizacao.replace(' ', '%20')}"
            
            with st.expander(f"🔗 {cargo}"):
                st.markdown(f"[🔍 Buscar {cargo} no LinkedIn]({linkedin_url})")
                
                with st.form(key=f"form_{cargo}"):
                    nome = st.text_input("Nome do contato", key=f"nome_{cargo}")
                    empresa = st.text_input("Empresa", key=f"emp_{cargo}")
                    oportunidade = st.text_area("Oportunidade identificada", key=f"opp_{cargo}")
                    
                    if st.form_submit_button("⭐ Salvar como alvo"):
                        if nome and empresa:
                            novo_alvo = {
                                "id": hashlib.md5(f"{nome}{datetime.now()}".encode()).hexdigest()[:8],
                                "nome": nome,
                                "cargo": cargo,
                                "empresa": empresa,
                                "oportunidade": oportunidade,
                                "data_inclusao": datetime.now().isoformat(),
                                "status": "ativo"
                            }
                            st.session_state.alvos.append(novo_alvo)
                            salvar_alvos()
                            st.success(f"✅ {nome} salvo na lista de alvos!")
                        else:
                            st.warning("Preencha nome e empresa")

# Tab 2: Alvos
with tab2:
    st.subheader("📋 Lista de Alvos")
    
    if st.session_state.alvos:
        df_alvos = pd.DataFrame(st.session_state.alvos)
        st.dataframe(
            df_alvos[["nome", "cargo", "empresa", "data_inclusao"]],
            use_container_width=True
        )
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("🗑️ Limpar todos os alvos"):
                st.session_state.alvos = []
                salvar_alvos()
                st.rerun()
        with col2:
            if st.button("💾 Exportar CSV"):
                df_alvos.to_csv("alvos_exportados.csv", index=False, encoding="utf-8-sig")
                st.success("Exportado para alvos_exportados.csv")
    else:
        st.info("Nenhum alvo salvo ainda. Use a aba 'Buscar' para adicionar contatos.")

# Tab 3: Roteiros
with tab3:
    st.subheader("✍️ Gerador de Roteiros Personalizados")
    
    if st.session_state.alvos:
        alvo_selecionado = st.selectbox(
            "Selecione um alvo",
            options=st.session_state.alvos,
            format_func=lambda x: f"{x['nome']} - {x['cargo']} na {x['empresa']}"
        )
        
        if alvo_selecionado:
            roteiro = gerar_roteiro(
                alvo_selecionado["nome"],
                alvo_selecionado["cargo"],
                alvo_selecionado["empresa"],
                alvo_selecionado.get("oportunidade", "está em expansão")
            )
            
            st.text_area("📝 Roteiro sugerido", roteiro, height=300)
            
            if st.button("📋 Copiar roteiro"):
                st.success("✅ Roteiro copiado! Cole no LinkedIn mensagem.")
    else:
        st.warning("Nenhum alvo salvo. Adicione alvos na aba 'Buscar' primeiro.")

# Tab 4: Monitorar
with tab4:
    st.subheader("👀 Monitoramento de Mudanças de Cargo")
    monitorar_mudancas()
    
    st.markdown("---")
    st.markdown("### 💡 Dicas de prospecção por timing")
    st.markdown("""
    | Sinal | Melhor momento para contato |
    |-------|----------------------------|
    | Mudança de cargo | 2-8 semanas após |
    | Empresa em expansão | Imediato |
    | Funding recebido | 2-4 semanas após |
    | Nova loja anunciada | Antes da abertura |
    """)

# Tab 5: Monitor Feed (NOVA FUNCIONALIDADE!)
with tab5:
    st.subheader("📡 Monitor de Posts do LinkedIn via Google")
    st.markdown("Encontre empresas que publicaram sobre expansão, novas lojas ou chamada para fornecedores")
    st.info("🔍 O Google indexa posts públicos do LinkedIn. Use os links abaixo para encontrar oportunidades!")
    
    # Categorias de busca
    categorias = {
        "🏪 Nova Loja/Unidade": [
            '"nova loja" site:linkedin.com',
            '"nova unidade" site:linkedin.com', 
            '"inauguração" site:linkedin.com',
            '"estamos crescendo" "nova loja" site:linkedin.com'
        ],
        "🚀 Expansão Franquias": [
            '"expansão" "franquia" site:linkedin.com',
            '"novos franqueados" site:linkedin.com',
            '"rede de franquias" "crescimento" site:linkedin.com',
            '"franquia" "oportunidade" site:linkedin.com'
        ],
        "🤝 Fornecedores/Parceiros": [
            '"homologação de fornecedores" site:linkedin.com',
            '"credenciamento" site:linkedin.com',
            '"buscamos fornecedores" site:linkedin.com',
            '"parceiros comerciais" site:linkedin.com',
            '"queremos conhecer fornecedores" site:linkedin.com'
        ],
        "📊 Trade Marketing": [
            '"trade marketing" "parceiro" site:linkedin.com',
            '"ponto de venda" "estratégia" site:linkedin.com',
            '"PDV" "fornecedor" site:linkedin.com',
            '"trade" "parceria" site:linkedin.com'
        ]
    }
    
    # Filtro de data
    col1, col2 = st.columns([1, 2])
    with col1:
        data_filtro = st.selectbox(
            "Período",
            ["qualquer data", "último mês", "últimos 3 meses", "último ano"],
            index=0
        )
    
    # Mapeamento de data
    data_map = {
        "qualquer data": "",
        "último mês": "after:2025-04-01",
        "últimos 3 meses": "after:2025-02-01",
        "último ano": "after:2024-05-01"
    }
    filtro_data = data_map.get(data_filtro, "")
    
    # Exibir links por categoria
    for categoria, termos in categorias.items():
        with st.expander(f"{categoria} (clique para expandir)", expanded=False):
            for termo in termos:
                # Construir URL do Google
                termo_completo = termo
                if filtro_data:
                    termo_completo = f"{termo} {filtro_data}"
                
                google_url = f"https://www.google.com/search?q={termo_completo.replace(' ', '%20')}"
                
                col1, col2 = st.columns([3, 1])
                with col1:
                    st.markdown(f"`{termo}`")
                with col2:
                    st.markdown(f"[🔍 Buscar no Google]({google_url})")
    
    st.markdown("---")
    st.markdown("### 🔔 Criar Alertas do Google (enviam email automaticamente)")
    st.markdown("""
    **Passo a passo:**
    1. Acesse [google.com/alerts](https://www.google.com/alerts)
    2. Cole uma das buscas acima
    3. Configure frequência: "uma vez por dia"
    4. Configure destino: seu email
    
    **Exemplos de alertas úteis:**
    - `site:linkedin.com "homologação de fornecedores" - Curitiba`
    - `site:linkedin.com "nova loja" "franquia" - SP`
    - `site:linkedin.com "expansão" "rede" - shopping`
    """)
    
    # Criar novo alerta personalizado
    st.markdown("---")
    st.markdown("### ✨ Criar Alerta Personalizado")
    
    with st.form("novo_alerta"):
        termo_personalizado = st.text_input(
            "Termo de busca",
            placeholder='Ex: site:linkedin.com "trade marketing" "fornecedor"'
        )
        
        col1, col2 = st.columns(2)
        with col1:
            email_alerta = st.text_input("Seu email", value="", placeholder="seu@email.com")
        with col2:
            frequencia = st.selectbox("Frequência", ["como acontece", "uma vez ao dia", "uma vez por semana"])
        
        if st.form_submit_button("💾 Salvar Alerta"):
            if termo_personalizado:
                novo_alerta = {
                    "id": hashlib.md5(termo_personalizado.encode()).hexdigest()[:8],
                    "termo": termo_personalizado,
                    "email": email_alerta if email_alerta else "não informado",
                    "frequencia": frequencia,
                    "data_criacao": datetime.now().isoformat(),
                    "link": f"https://www.google.com/alerts?q={termo_personalizado.replace(' ', '%20')}"
                }
                st.session_state.alertas.append(novo_alerta)
                salvar_alertas()
                st.success(f"✅ Alerta salvo! Configure no Google Alerts: {novo_alerta['link']}")
            else:
                st.warning("Digite um termo de busca")

# Tab 6: Relatórios
with tab6:
    st.subheader("📈 Relatórios e Estatísticas")
    
    if st.session_state.alvos:
        df_stats = pd.DataFrame(st.session_state.alvos)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total de alvos", len(df_stats))
        with col2:
            st.metric("Empresas únicas", df_stats['empresa'].nunique())
        with col3:
            st.metric("Cargos diferentes", df_stats['cargo'].nunique())
        
        st.markdown("---")
        st.markdown("### 📊 Distribuição por cargo")
        st.bar_chart(df_stats['cargo'].value_counts())
        
        st.markdown("### 🏢 Principais empresas")
        st.dataframe(df_stats['empresa'].value_counts().reset_index(), use_container_width=True)
    else:
        st.info("Adicione alvos para ver estatísticas")
    
    if st.session_state.alertas:
        st.markdown("---")
        st.markdown("### 🔔 Alertas Ativos")
        df_alertas = pd.DataFrame(st.session_state.alertas)
        st.dataframe(df_alertas[["termo", "frequencia", "data_criacao"]], use_container_width=True)

# Rodapé
st.markdown("---")
st.caption("⚡ LinkedIn Prospector PRO | 🔍 Monitor Feed via Google | 📡 Alertas automáticos")