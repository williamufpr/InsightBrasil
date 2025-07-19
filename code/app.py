# app.py
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events # Para interatividade de clique
from streamlit_lottie import st_lottie
import requests

# imports do projeto 

from transform import load_transformed_data 
from tabs import intro


if __name__ == "__main__":
    print("Modulo Principal Executado")
    
    # Caminho para o dataset .

    transformed_csv_path = 'data/energy30daysLong.csv'
    df_consumption = load_transformed_data(transformed_csv_path)

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
    st.set_page_config(page_title="Análise de Consumo de Energia no Banco",
                      page_icon="⚡",
                      layout="wide")

# -----------------------------
# Cabeçalho
# -----------------------------
    st.title("⚡ Análise de Consumo Energético de Computadores")

# Animação Lottie no cabeçalho
    lottie_energy = load_lottieurl("https://assets8.lottiefiles.com/packages/lf20_jcikwtux.json")

    st_lottie(lottie_energy, height=200, key="energy")

# -----------------------------
# Abas
# -----------------------------
    tabs = st.tabs(["📌 Introdução", "📈 Explorando os Dados", "💡 Descobertas", "✅ Plano de Ação"])

    with tabs[0]: 
        intro.render(df_consumption) 
        
    with tabs[1]:
        explore.render(df_consumption)
