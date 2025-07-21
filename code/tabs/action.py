import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go # Mantemos para referência, embora PX seja mais direto aqui
from datetime import timedelta # Import necessário para plot_initial_chaos, caso use

def render(df_consumption):
    st.title("📋 : Plano de ação Sugerido")
    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    A partir do apresentado e considerando as limitações discutidas com os gerentes <br>
    realizamos as seguintes sugestões como um plano de acão de curto prazo : 
    
  </p>

  <ul style="list-style-type: none; padding-left: 0;">
    <li>🥇 <span style="color:#003366; font-weight:bold;">Investigar os 3 equipamentos de maior consumo buscando melhorias de configuração </span></li>
    <li>🥈 <span style="color:#003366; font-weight:bold;">Considerar fortemente consolidar serviços dos 3 equipamentos de menor consumo em apenas 1, desligando os outros 2</span></li>
    <li>🥉 <span style="color:#003366; font-weight:bold;">Verificar os equipamentos com alta variabilidade no consumo, particularmente o SMV340211</span></li>
  </ul>
</div>
""", unsafe_allow_html=True)
    
    
    st.set_page_config(page_title="Dashboard Consumo Energia", layout="wide")

# CSS para bordas arredondadas e sombra
    st.markdown("""
    <style>
    .dashboard-container {
        border: 2px solid #ccc;
        border-radius: 20px;
        padding: 20px;
        box-shadow: 4px 4px 12px rgba(0,0,0,0.1);
        margin-bottom: 20px;
    }
    .dashboard-box {
        border: 1px solid #ddd;
        border-radius: 15px;
        padding: 15px;
        box-shadow: 2px 2px 8px rgba(0,0,0,0.05);
        background-color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Calcular consumo total por equipamento
    consumo_total = df_consumption.groupby("equipment_id")["consumption_kwh"].sum().reset_index()

# Top 3 maiores consumidores
    top3 = consumo_total.sort_values(by="consumption_kwh", ascending=False).head(3)

# Top 3 menores consumidores
    bottom3 = consumo_total.sort_values(by="consumption_kwh", ascending=True).head(3)

# --- Início do dashboard ---
    with st.container():
        st.markdown("<div class='dashboard-container'>", unsafe_allow_html=True)

    # 3 colunas lado a lado
        col1, col2 = st.columns(2)

    # --- Região 1: Top 3 maiores consumidores ---
        with col1:
            st.markdown("<div class='dashboard-box'>", unsafe_allow_html=True)
            st.subheader("🔝 Top 3 Maiores Consumidores")
            fig_top3 = px.bar(top3, 
                          x="equipment_id", 
                          y="consumption_kwh", 
                          text_auto=".2s",
                          labels={"equipment_id": "Equipamento", "consumption_kwh": "Consumo Total (kWh)"},
                          color="equipment_id",
                          title="Top 3 Equipamentos de Maior Consumo")
            st.plotly_chart(fig_top3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- Região 2: Top 3 menores consumidores ---
        with col2:
            st.markdown("<div class='dashboard-box'>", unsafe_allow_html=True)
            st.subheader("🔻 Top 3 Menores Consumidores")
            fig_bottom3 = px.bar(bottom3, 
                             x="equipment_id", 
                             y="consumption_kwh", 
                             text_auto=".2s",
                             labels={"equipment_id": "Equipamento", "consumption_kwh": "Consumo Total (kWh)"},
                             color="equipment_id",
                             title="Top 3 Equipamentos de Menor Consumo")
            st.plotly_chart(fig_bottom3, use_container_width=True)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- Região 3: Texto com bullets ---

        st.markdown("<div class='dashboard-box'>", unsafe_allow_html=True)
        st.subheader("🛠️ Ações Adicionais")
        st.markdown("""
            - Verificar o equipamento SMV340211 devido a variabilidade  
            - Verificar os serviços dos equipamentos de menor consumo para possível consolidação 

        """)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)