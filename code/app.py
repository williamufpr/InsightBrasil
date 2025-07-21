# app.py

import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from streamlit_plotly_events import plotly_events # Para interatividade de clique
from streamlit_lottie import st_lottie
import requests
from streamlit_plotly_events import plotly_events


# imports do projeto 

from transform import load_transformed_data 
from tabs import intro, group1, action

dashboard_css = """
<style>
    /* Estilo para o container principal do dashboard */
    .dashboard-wrapper {
        border: 2px solid #607D8B; /* Cor da borda principal */
        border-radius: 15px; /* Bordas arredondadas */
        box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.2); /* Sombra */
        padding: 20px;
        margin-bottom: 20px;
        background-color: #ECEFF1; /* Fundo levemente cinza */
    }

    /* Estilo para cada região interna */
    .box-region {
        border: 1px solid #90A4AE; /* Cor da borda da região */
        border-radius: 10px; /* Bordas arredondadas */
        box-shadow: 3px 3px 10px rgba(0, 0, 0, 0.1); /* Sombra mais suave */
        padding: 15px;
        margin-bottom: 15px; /* Espaço entre as regiões */
        background-color: #FFFFFF; /* Fundo branco para as regiões internas */
    }

    h3 {
        color: #37474F;
        font-size: 1.5em;
        margin-top: 0;
    }

    p {
        font-size: 1.0em;
        line-height: 1.5;
    }
</style>
"""

if __name__ == "__main__":
    print("Modulo Principal Executado")
    
    # Caminho para o dataset .

    transformed_csv_path = 'data/energy30daysLong.csv'
    df_consumption = load_transformed_data(transformed_csv_path)
    print(df_consumption.info()) 
    
    equipment_stats = df_consumption.groupby('equipment_id')['consumption_kwh'].agg(
        min_consumption='min',
        max_consumption='max',
        mean_consumption='mean',
        total_consumption='sum'
    ).reset_index()
    
    num_equipments = df_consumption['equipment_id'].nunique()
    top_n_equipment = min(5, num_equipments) # Pega no máximo 5, ou menos se houver menos equipamentos
    bottom_n_equipment = min(3, num_equipments) # Pega no máximo 3 para consolidação
    
    
    # Recalcula top_n_ids e bottom_n_ids com base nos dados filtrados
    # top_n_ids e bottom_n_ids precisam ser definidos aqui para serem acessíveis às funções
    
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
    tabs = st.tabs(["📌 Introdução", "📈 Explorando os Dados", "🚀 Plano de Ação"])

    with tabs[0]: 
        intro.render(df_consumption) 
        
    with tabs[1]:
        group1.render(df_consumption)
        group1.grafico_evolucao_consumo_por_faixa(df_consumption)
        group1.plot_top_dispersion_boxplots(df_consumption)
    with tabs[2]:
        action.render(df_consumption) 
