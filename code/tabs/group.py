import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go # Mantemos para referência, embora PX seja mais direto aqui

# 1. Simulação do DataFrame (manter igual ao anterior para consistência)
@st.cache_data
def render(df):

    # ASSUMIMOS QUE SEU DATAFRAME 'df' JÁ ESTÁ CARREGADO AQUI.
    # Exemplo de como seu 'df' deve ser, para referência:
    # df = ... (seus dados carregados/criados em outro lugar)

    st.title("Análise de Consumo de Energia de Computadores")
    st.subheader("Visualização da Distribuição de Equipamentos por Grupo de Consumo")

    # --- Preparação dos dados para o agrupamento ---

    # Filtrar apenas dias de semana e consumo > 0
    df_weekdays_filtered = df[(df['day_type'] == 'weekday') & (df['consumption_kwh'] > 0)].copy()

# 1. Calcular o Consumo Médio Diário por Equipamento (apenas dias de semana com consumo > 0)
    daily_avg_consumption_per_equipment = df_weekdays_filtered.groupby('equipment_id')['consumption_kwh'].mean().reset_index()
    daily_avg_consumption_per_equipment.rename(columns={'consumption_kwh': 'mean_daily_consumption'}, inplace=True)

# 2. Definir os Limites de Agrupamento (usando tercis)
# Calcular os quantis para dividir em 3 grupos aproximadamente iguais
    low_threshold = daily_avg_consumption_per_equipment['mean_daily_consumption'].quantile(0.33)
    high_threshold = daily_avg_consumption_per_equipment['mean_daily_consumption'].quantile(0.66)

# 3. Atribuir cada equipamento a um grupo
    def assign_consumption_group(consumption):
        if consumption <= low_threshold:
            return 'Baixo Consumo'
        elif consumption <= high_threshold:
            return 'Médio Consumo'
        else:
            return 'Alto Consumo'

    daily_avg_consumption_per_equipment['consumption_group'] = daily_avg_consumption_per_equipment['mean_daily_consumption'].apply(assign_consumption_group)

# Reordenar os grupos para a visualização
    group_order = ['Baixo Consumo', 'Médio Consumo', 'Alto Consumo']
    daily_avg_consumption_per_equipment['consumption_group'] = pd.Categorical(
        daily_avg_consumption_per_equipment['consumption_group'],
        categories=group_order,
        ordered=True
    )
    daily_avg_consumption_per_equipment.sort_values('consumption_group', inplace=True)


# --- Cálculo de Estatísticas do Grupo para o Hover ---
# Para o hover do agrupamento geral, vamos calcular as estatísticas por grupo
# Isso será uma tabela separada para as informações de hover do grupo.
    group_summary_for_hover = df_weekdays_filtered.merge(
        daily_avg_consumption_per_equipment[['equipment_id', 'consumption_group']],
        on='equipment_id',
        how='left'
    ).groupby('consumption_group').agg(
        num_equipamentos=('equipment_id', 'nunique'),
        consumo_medio_grupo=('consumption_kwh', 'mean'),
        desvio_padrao_grupo=('consumption_kwh', 'std')
    ).reset_index()

# Garantir a ordem dos grupos
    group_summary_for_hover['consumption_group'] = pd.Categorical(
        group_summary_for_hover['consumption_group'],
        categories=group_order,
        ordered=True
    )
    group_summary_for_hover.sort_values('consumption_group', inplace=True)


# --- Plotar o Gráfico de Dispersão Agrupado (mostrando cada equipamento) ---
# Usamos Plotly Express para um scatter plot com jitter para melhor visualização
    fig_scatter = px.scatter(
        daily_avg_consumption_per_equipment,
        x='consumption_group',
        y='mean_daily_consumption',
        color='consumption_group',
        color_discrete_map={
            'Baixo Consumo': 'green',
            'Médio Consumo': 'orange',
            'Alto Consumo': 'red'
      },
        title='Distribuição do Consumo Médio Diário por Equipamento e Grupo',
        labels={
            'consumption_group': 'Grupo de Consumo',
            'mean_daily_consumption': 'Consumo Médio Diário (kWh)'
       },
       hover_name='equipment_id', # Mostra o ID do equipamento no hover
       custom_data=['mean_daily_consumption'] # Passa o consumo médio individual para o hover
    )

# Adicionar jitter aos pontos para evitar sobreposição e melhor visualização
    fig_scatter.update_traces(
        marker=dict(size=10, opacity=0.8),
        jitter=0.3, # Adiciona um pequeno "embaralhamento" horizontal para separar os pontos
        hovertemplate=(
           "<b>Equipamento:</b> %{hovertext}<br>"
           "<b>Grupo de Consumo:</b> %{x}<br>"
           "<b>Consumo Médio Diário:</b> %{y:.2f} kWh<extra></extra>"
       )
   )

    fig_scatter.update_layout(
        xaxis_title='Grupo de Consumo',
        yaxis_title='Consumo Médio Diário (kWh)',
        showlegend=False,
        height=500
    )

    st.plotly_chart(fig_scatter, use_container_width=True)

    st.markdown("---")

# --- Opcional: Adicionar um gráfico de barras para as estatísticas gerais do grupo ---
# Para complementar a visualização anterior, podemos ter um gráfico de barras das estatísticas do grupo
# que era o que tínhamos antes, mas agora complementando o scatter plot.

    st.subheader("Consumo Médio e Estatísticas Gerais por Grupo")

    fig_bar_summary = px.bar(
        group_summary_for_hover,
        x='consumption_group',
        y='consumo_medio_grupo',
        color='consumption_group',
        color_discrete_map={
            'Baixo Consumo': 'green',
            'Médio Consumo': 'orange',
            'Alto Consumo': 'red'
       },
       labels={
           'consumption_group': 'Grupo de Consumo',
           'consumo_medio_grupo': 'Consumo Médio Diário (kWh)'
        },
        custom_data=['num_equipamentos', 'desvio_padrao_grupo']
   )

    fig_bar_summary.update_traces(
        hovertemplate=(
            "<b>Grupo:</b> %{x}<br>"
            "<b>Consumo Médio (Grupo):</b> %{y:.2f} kWh<br>"
            "<b>Quantidade de Equipamentos:</b> %{customdata[0]}<br>"
            "<b>Desvio Padrão do Grupo:</b> %{customdata[1]:.2f} kWh<extra></extra>"
        )
    )

    fig_bar_summary.update_layout(
        xaxis_title='Grupo de Consumo',
        yaxis_title='Consumo Médio Diário (kWh)',
        showlegend=False
    )

    st.plotly_chart(fig_bar_summary, use_container_width=True)


    st.markdown("---")

    st.info(
        f"Os grupos foram definidos com base no consumo médio diário dos equipamentos nos dias de semana (> 0 kWh):<br>"
        f"- **Baixo Consumo:** Equipamentos com consumo médio diário até {low_threshold:.2f} kWh.<br>"
        f"- **Médio Consumo:** Equipamentos com consumo médio diário entre {low_threshold:.2f} kWh e {high_threshold:.2f} kWh.<br>"
        f"- **Alto Consumo:** Equipamentos com consumo médio diário acima de {high_threshold:.2f} kWh."
    )