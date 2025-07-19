import streamlit as st

st.title("🚀 Explorando o Consumo Energético em Computadores do Banco")
st.markdown("_Relatório interativo para análise e insights sobre consumo de energia._")



st.image("https://picsum.photos/200?random=1", caption="Energia e Dados")

st.header("1️⃣ Introdução")
st.markdown("""
Nesta análise, exploramos o consumo energético de 600 computadores ao longo de 30 dias, destacando padrões e oportunidades de economia.
""")

st.header("2️⃣ Consumo ao Longo do Tempo")
col1, col2 = st.columns([1,2])
with col1:
    st.image("https://picsum.photos/200?random=2", caption="Consumo Diário")
with col2:
    st.markdown("""
    Observa-se que o consumo médio permanece em torno de 60 kWh por dia, com picos durante o horário comercial.
    """)

st.header("3️⃣ Insights e Oportunidades")
st.markdown("""
- **Uso intensivo:** 9h-18h representa 80% do consumo diário.
- **Possível economia:** desligamento automático fora do expediente pode reduzir consumo em 20%.
""")

with st.expander("Clique para detalhes técnicos"):
    st.code("""
# Leitura dos dados
import pandas as pd
df = pd.read_csv('consumo.csv')
# Análise de pico
df.groupby('hora')['consumo'].mean().plot()
    """, language='python')

st.header("4️⃣ Conclusões")
st.markdown("""
📌 Há oportunidades claras de economia ao revisar o uso de energia fora do horário de pico.  
📌 Recomenda-se implementar alertas de desligamento automático nos equipamentos.
""")

st.markdown("---")
st.markdown("📫 Contato: [LinkedIn](https://linkedin.com/in/seuperfil) | [GitHub](https://github.com/seuperfil)")

