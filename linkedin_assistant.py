import streamlit as st
import pandas as pd
import re
from datetime import datetime
import json

# Configuração da página
st.set_page_config(
    page_title="LinkedIn Prospector",
    page_icon="🔍",
    layout="wide"
)

# Título
st.title("🔍 LinkedIn Prospector Assistant")
st.markdown("---")

# Sidebar com instruções
with st.sidebar:
    st.header("📌 Como usar")
    st.markdown("""
    1. **Defina seu perfil de cliente ideal**
    2. **Use os filtros para refinar a busca**
    3. **Copie os links gerados e cole no navegador**
    4. **Analise os perfis manualmente**
    
    ⚠️ **Importante**: O LinkedIn não permite scraping automático.
    Esta ferramenta gera links de busca para você usar manualmente.
    """)
    
    st.markdown("---")
    st.header("🎯 Dicas de prospecção")
    st.markdown("""
    - **Job changes**: 27% dos contatos mudam de cargo a cada 90 dias
    - **Melhor janela**: 2-8 semanas após a mudança
    - **Funding rounds**: Empresas que levantam investimento têm budget
    - **Hiring surges**: Empresas contratando = empresas investindo
    """)

# Layout principal em colunas
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎯 Defina seu alvo")
    
    # Cargos de interesse
    cargos = st.text_area(
        "Cargos que você quer encontrar",
        value="Gerente de Compras\nDiretor de Suprimentos\nCoordenador de Supply Chain\nHead de Trade Marketing\nCategory Manager\nComprador Sênior",
        height=150,
        help="Um cargo por linha"
    )
    
    # Setores
    setores = st.text_input(
        "Setores de interesse (opcional)",
        placeholder="Ex: Varejo, Alimentação, Construção, Tecnologia",
        help="Separe por vírgula"
    )
    
    # Localização
    localizacao = st.selectbox(
        "Localização",
        ["Brasil", "São Paulo", "Rio de Janeiro", "Minas Gerais", "Paraná", "Santa Catarina", "Rio Grande do Sul", "Todas"]
    )

with col2:
    st.subheader("🔧 Filtros avançados")
    
    # Tipo de busca
    tipo_busca = st.multiselect(
        "O que você quer buscar?",
        ["Pessoas", "Empresas", "Vagas"],
        default=["Pessoas"]
    )
    
    # Senioridade
    senioridade = st.multiselect(
        "Senioridade",
        ["Diretor", "Gerente", "Coordenador", "Especialista", "Head", "VP"],
        default=["Diretor", "Gerente"]
    )
    
    # Sinal de oportunidade
    sinais = st.multiselect(
        "Sinais de oportunidade (timing)",
        ["Mudança de cargo recente", "Empresa em expansão", "Empresa contratando", "Funding recente"],
        help="Empresas com estes sinais têm maior chance de precisar dos seus serviços"
    )

st.markdown("---")

# Botão de geração
if st.button("🚀 Gerar links de prospecção", type="primary", use_container_width=True):
    
    st.markdown("### 📋 Links para prospecção manual")
    st.info("Copie os links abaixo e cole no seu navegador para analisar os perfis")
    
    # Processar cargos
    lista_cargos = [c.strip() for c in cargos.split('\n') if c.strip()]
    
    # Preparar localização para URL
    loc_param = "" if localizacao == "Todas" else f"&location={localizacao.replace(' ', '%20')}"
    
    # Gerar links
    tabs = st.tabs(["🔍 Pessoas", "🏢 Empresas", "💼 Vagas", "📊 Estratégias"])
    
    # Aba de Pessoas
    with tabs[0]:
        st.subheader("Links para busca de pessoas")
        
        for cargo in lista_cargos:
            for nivel in senioridade:
                termo = f"{nivel} {cargo}"
                termo_url = termo.replace(" ", "%20")
                
                # Link para busca no LinkedIn
                linkedin_url = f"https://www.linkedin.com/search/results/people/?keywords={termo_url}{loc_param}"
                
                # Link para Google (alternativa)
                google_url = f"https://www.google.com/search?q=site%3Alinkedin.com%2Fin+%22{termo.replace(' ', '%20')}%22+Brasil"
                
                col_a, col_b = st.columns([3, 1])
                with col_a:
                    st.markdown(f"**{termo}**")
                    st.markdown(f"[🔗 Buscar no LinkedIn]({linkedin_url})")
                with col_b:
                    st.markdown(f"[Google alternativa]({google_url})")
                st.markdown("---")
    
    # Aba de Empresas
    with tabs[1]:
        st.subheader("Links para busca de empresas")
        
        # Palavras-chave para empresas em expansão
        termos_empresa = [
            "expansão", "novas lojas", "franquias", "crescimento",
            "investimento", "contratando", "oportunidades"
        ]
        
        for termo in termos_empresa:
            empresa_url = f"https://www.linkedin.com/search/results/companies/?keywords={termo}{loc_param}"
            st.markdown(f"**Empresas com sinal de: {termo.upper()}**")
            st.markdown(f"[🔗 Buscar no LinkedIn]({empresa_url})")
            st.markdown("---")
    
    # Aba de Vagas
    with tabs[2]:
        st.subheader("Links para busca de vagas")
        
        for cargo in lista_cargos:
            vaga_url = f"https://www.linkedin.com/jobs/search/?keywords={cargo.replace(' ', '%20')}{loc_param}"
            st.markdown(f"**Vagas para {cargo}**")
            st.markdown(f"[🔗 Ver vagas no LinkedIn]({vaga_url})")
            st.markdown("---")
    
    # Aba de Estratégias
    with tabs[3]:
        st.subheader("🎯 Estratégias de prospecção por sinal")
        
        st.markdown("""
        ### Mudança de cargo recente
        
        Quando uma pessoa muda de cargo, ela está mais aberta a novas soluções nos primeiros 90 dias.
        
        **Como usar:**
        1. Identifique profissionais que assumiram novos cargos em compras/suprimentos
        2. Espere 2-3 semanas para a pessoa se ambientar
        3. Envie uma mensagem parabenizando pela nova posição
        4. Ofereça valor relevante para os desafios do novo cargo
        
        ### Empresa em expansão
        
        Empresas abrindo novas unidades ou contratando têm necessidades urgentes.
        
        **Como usar:**
        1. Identifique empresas com anúncios de expansão
        2. Pesquise quem é o responsável por compras/suprimentos
        3. Ofereça soluções que escalem com o crescimento
        
        ### Funding recente
        
        Empresas que receberam investimento têm budget e precisam crescer rápido.
        
        **Como usar:**
        1. Acompanhe anúncios de investimento no setor
        2. Contate 2-4 semanas após o anúncio
        3. Posicione sua solução como facilitadora do crescimento
        """)
    
    # Salvar resultados
    resultados = {
        "data_geracao": datetime.now().isoformat(),
        "cargos_buscados": lista_cargos,
        "localizacao": localizacao,
        "senioridade": senioridade,
        "sinais": sinais
    }
    
    with open("prospeccao_log.json", "w", encoding="utf-8") as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False)
    
    st.success(f"✅ Log salvo em prospeccao_log.json")

# Rodapé
st.markdown("---")
st.caption("⚠️ **Aviso**: Esta ferramenta gera links para busca manual no LinkedIn. O scraping automático viola os Termos de Serviço do LinkedIn.")