import streamlit as st
from streamlit_lottie import st_lottie
import requests

# -----------------------------
# Função para carregar animação Lottie
# -----------------------------
def load_lottieurl(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()

# -----------------------------
# Configuração da Página
# -----------------------------
st.set_page_config(page_title="Análise de Energia no Banco",
                   page_icon="⚡",
                   layout="wide")

# -----------------------------
# Cabeçalho
# -----------------------------
st.title("⚡ Análise de Consumo Energético de Computadores")
st.markdown("_Dashboard interativo simulando um artigo online em Streamlit._")

# Animação Lottie no cabeçalho
lottie_energy = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json")

st_lottie(lottie_energy, height=200, key="energy")

# -----------------------------
# Abas
# -----------------------------
tabs = st.tabs(["📌 Introdução", "📈 Análise de Dados", "💡 Insights", "✅ Conclusões"])

# -----------------------------
# Aba 1: Introdução
# -----------------------------
with tabs[0]:
    st.header("O Desafio")
    st.image("https://picsum.photos/1000/300?random=3", caption="Energia e Tecnologia")
    st.markdown("""
    Com o crescimento do parque tecnológico, o consumo de energia em computadores de agências e data centers de um banco se tornou relevante. Este relatório busca explorar os dados de consumo energético ao longo de 30 dias em 600 computadores, simulando um artigo interativo.
    """)
    st.info("Você pode navegar entre as abas acima para acompanhar cada etapa do estudo de forma didática.")

# -----------------------------
# Aba 2: Análise de Dados
# -----------------------------
with tabs[1]:
    st.header("Análise de Consumo ao Longo do Tempo")
    col1, col2 = st.columns([1, 2])
    with col1:
        st.image("https://picsum.photos/400/300?random=4", caption="Consumo Diário Simulado")
    with col2:
        st.markdown("""
        Os dados indicam que **80% do consumo energético ocorre entre 9h e 18h**, com picos significativos às 10h e às 15h. Fora do horário comercial, observa-se um consumo residual que representa cerca de 20% da energia total consumida.
        """)
    st.success("Dica: Para análises reais, você pode integrar gráficos do Plotly ou Altair aqui para maior interatividade.")

# -----------------------------
# Aba 3: Insights
# -----------------------------
with tabs[2]:
    st.header("Principais Insights e Recomendações")
    st.markdown("""
    - 🕘 **Horário comercial concentra 80% do consumo.**
    - 🌙 **Consumo fora do expediente pode ser reduzido.**
    - 💻 **Automatização de desligamento pode gerar economia de até 20%.**
    - 🔄 **Monitoramento contínuo possibilita ajustes em tempo real.**
    """)

    with st.expander("Ver detalhes técnicos das análises"):
        st.code("""
import pandas as pd
df = pd.read_csv('consumo.csv')
df['hora'] = pd.to_datetime(df['timestamp']).dt.hour
df.groupby('hora')['consumo'].mean().plot()
        """, language='python')

# -----------------------------
# Aba 4: Conclusões
# -----------------------------
with tabs[3]:
    st.header("Conclusões e Próximos Passos")
    st.markdown("""
    ✅ A análise demonstrou que há **oportunidades claras de redução de custos** com medidas simples de desligamento automático e conscientização.
    
    ✅ Recomenda-se **testes A/B em agências piloto** para estimar economia real.
    
    ✅ Monitorar continuamente os indicadores para identificar novos padrões de uso.
    """)

    st.info("Entre em contato para implementar dashboards interativos de consumo energético no seu banco ou organização.")
    st.markdown("📫 Contato: [LinkedIn](https://linkedin.com/in/seuperfil) | [GitHub](https://github.com/seuperfil)")

# -----------------------------
# Rodapé
# -----------------------------
st.markdown("---")
st.caption("Desenvolvido com ❤️ usando Streamlit para apresentações de dados de forma moderna e acessível.")
