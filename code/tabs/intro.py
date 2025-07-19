import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events # Para interatividade de clique
from streamlit_lottie import st_lottie

from tabs.utils import mostrar_proxima_aba

@st.cache_data 

def render(df_consumption):
    
    st.title("📊 : Otimizando o Consumo de Energia de Equipamentos")
    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    Um grupo de gerentes de data center do meu cliente no segmento de bancos trouxe-me um problema: <br>
    <em>"Hoje nosso grande problema é Energia: Caso ganhássemos computadores de presente, não poderíamos ligar."</em>
  </p>

  <p>Eles fizeram um levantamento do consumo diário dos servidores que fornecemos tempos atrás, porém os resultados não ajudaram.<br>
  Eles plotaram o gráfico abaixo, mas não conseguiram responder às questões que os interessavam:</p>

  <ul style="list-style-type: none; padding-left: 0;">
    <li>🔍 <span style="color:#003366; font-weight:bold;">Há equipamentos que consomem muito mais que os demais?</span></li>
    <li>⏰ <span style="color:#003366; font-weight:bold;">Existem dias ou horários com picos de consumo inesperados?</span></li>
    <li>💤 <span style="color:#003366; font-weight:bold;">Temos equipamentos com consumo muito baixo que poderiam ser desligados?</span></li>
  </ul>
</div>
""", unsafe_allow_html=True)

### **Visualização 1: O "Prato de Espaguete" **


    st.header("1. O Ponto de Partida: Acompanhamento de Consumo por 30 dias ")
    st.write("Começamos com a representação direta de todas as medições de consumo dos 20 equipamentos ao longo do mês.")

# Gráfico de linha "caótico"
    fig_chaotic = px.line(df_consumption, 
                         x='timestamp', 
                         y='consumption_kwh', 
                         color='equipment_id', # Cada equipamento uma linha/cor
                         title='Consumo de Energia de Todos os Equipamentos ao Longo do Mês (Dificil de Analisar)',
                         labels={'timestamp': 'Data e Hora', 'consumption_kwh': 'Consumo (kWh)', 'equipment_id': 'Equipamento ID'})

    fig_chaotic.update_layout(
       xaxis_title="Data e Hora",
       yaxis_title="Consumo (kWh)",
       showlegend=True, # Mostrar a legenda para evidenciar o excesso
       height=600,
       hovermode="x unified" # Ajuda um pouco, mas ainda é confuso
   )
   
    st.plotly_chart(fig_chaotic, use_container_width=True)

    
    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    Com esta visualização não conseguimos identificar padrões ou oportunidades de economia. <br>
  </p>

  <p>Em dois dias precisamos apresentar ao Vice Presidente de Tecnologia um plano de economia de energia da área.
    Teremos 20 minutos para mostrar o que descobrirmos e elencar 2 ou 3 ações que possam contribuir para o esforço de economia de energia.
    Não podemos apresentar um gráfico complicado e confuso como esse.
  </p>

  <ul style="list-style-type: none; padding-left: 0;">
    <li><span style="color:#003366; font-weight:bold;">Em dois dias precisamos apresentar ao VP de Tecnoloigia um plano de economia de energia da área</span></li>
    <li><span style="color:#003366; font-weight:bold;">Teremos 20 minutos para mostrar o que descobrirmos e elencar 2 ou 3 ações que possam contribuir para o esforço de economia de energia</span></li>
    <li><span style="color:#003366; font-weight:bold;">Não podemos apresentar um gráfico complicado e confuso como esse</span></li>
  </ul>
</div>
""", unsafe_allow_html=True)
    
    mostrar_proxima_aba(nome_aba="📈 Explorando os Dados")