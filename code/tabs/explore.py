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
    st.title("📈  : Um novo olhar sobre os dados")
     
    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    Inicaremos buscando um olhar diferente sobre a distribuição do consumo considerando um conhecimento que dispomos sobre o mercado do cliente: <br>
    <em>"Bancos operam de forma muito diferente nos finais de semana, uma vez que agências estão fechadas."</em>
  </p>

  <p>Vamos então olhar este padrão agregado antes de analisarmos equipamentos específico</p>

  <ul style="list-style-type: none; padding-left: 0;">
    <li>📅 <span style="color:#003366; font-weight:bold;">Vamos observar o consumo dos equipamentos nos dias semana pois sabemos que muitos sistemas não tem usuários aos sábados e domingos </span></li>
    <li>🌡️ <span style="color:#003366; font-weight:bold;">Vamos destacar os 5 equipamentos com maior amplitude entre consumo máximo e mínimo </span></li>

  </ul>
</div>
""", unsafe_allow_html=True)
     
    df_workweek = df_consumption[df_consumption['day_type'] == 'Dia de Semana']
    stats  = df_workweek.groupby("equipment_id")["consumption_kwh"].agg(['mean', 'min', 'max']).reset_index() 
    
    top5_equipment = stats.nlargest(5, 'mean')["equipment_id"].tolist() 
    bottom5_equipment = stats.nsmallest(5, 'mean')["equipment_id"].tolist()
    df_workweek["date_str"] = df_workweek["date"].dt.strftime("%Y-%m-%d")
    # Heatmap de consumo médio por equipamento e dia da semana 
    
    heatmap_df = df_workweek.pivot_table(
        index="equipment_id",
        columns="date_str",
        values="consumption_kwh"
    )

    hover_text = heatmap_df.copy()
    for eq in heatmap_df.index:
        row = stats[stats["equipment_id"] == eq]
        min_v = row["min"].values[0]
        max_v = row["max"].values[0]
        mean_v = row["mean"].values[0]
        for col in heatmap_df.columns:
            val = heatmap_df.loc[eq,col]
            hover_text.loc[eq, col] = (
                f"Equipment: {eq}<br>"
                f"Date: {col}<br>"
                f"Consumption: {heatmap_df.loc[eq, col]:.2f} kWh<br>"
                f"Min: {min_v:.2f} | Max: {max_v:.2f} | Mean: {mean_v:.2f}"
            ) if pd.notna(val) else "No Data"
    # Marca equipamentos top e bottom
    
    # --- Plot Heatmap ---
    fig = px.imshow(
        heatmap_df,
        labels=dict(x="Data", y="Equipamento", color="Consumo (kWh)"),
        color_continuous_scale="Viridis",
        aspect="auto"
    )

# --- Adiciona hover manualmente ---
    fig.update_traces(customdata=hover_text.values)
    fig.update_traces(hovertemplate="%{customdata}")

# --- Destacar top 5 (vermelho) e bottom 5 (azul) ---
    for eq in top5_equipment + bottom5_equipment:
        idx = list(heatmap_df.index).index(eq)
        fig.add_shape(
            type="rect",
            x0=-0.5,
            x1=len(heatmap_df.columns)-0.5,
            y0=idx-0.5,
            y1=idx+0.5,
            line=dict(color="red" if eq in top5_equipment else "blue", width=2),
            layer="above"
        )

# --- Mostrar no Streamlit ---
    st.plotly_chart(fig, use_container_width=True)