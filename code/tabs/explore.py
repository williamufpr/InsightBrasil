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
     
    df_weekdays = df_consumption[df_consumption['day_type'] == 'Dia de Semana'].copy()
    df_weekdays = df_weekdays[df_weekdays['consumption_kwh'] > 0] 
# Garantir que a coluna 'date' seja do tipo datetime para ordenação correta no Plotly
    df_weekdays['date'] = pd.to_datetime(df_weekdays['date'])

# 3. Calcular estatísticas de consumo por equipamento (APENAS DIAS DE SEMANA)
# Estas estatísticas serão usadas no hover e para identificar top/bottom 5
    equipment_stats = df_weekdays.groupby('equipment_id')['consumption_kwh'].agg(
       min_consumption='min',
       max_consumption='max',
       mean_consumption='mean'
   ).reset_index()

# 4. Identificar os 5 equipamentos com maior e menor consumo médio
    top_5_equipment = equipment_stats.nlargest(5, 'mean_consumption')['equipment_id'].tolist()
    bottom_5_equipment = equipment_stats.nsmallest(5, 'mean_consumption')['equipment_id'].tolist()

# 5. Preparar os dados para o heatmap
# Agregação por data e equipment_id para obter o consumo diário de cada equipamento
    heatmap_data = df_weekdays.groupby(['date', 'equipment_id'])['consumption_kwh'].sum().reset_index()

# Criar a matriz Z para o heatmap (equipments no Y, dates no X)
    pivot_table = heatmap_data.pivot_table(index='equipment_id', columns='date', values='consumption_kwh')

# Ordenar as colunas (datas) para o eixo X
    all_weekdays_dates_sorted = sorted(heatmap_data['date'].unique())
    pivot_table = pivot_table[all_weekdays_dates_sorted]

# Ordenar o eixo Y (equipments) para destacar top/bottom 5
# Criar uma lista ordenada de equipment_ids para o eixo Y
    ordered_equipment_ids = []
    for eq_id in top_5_equipment:
        ordered_equipment_ids.append(f"{eq_id} (Top 5)")
        remaining_equipment = [eq for eq in pivot_table.index if eq not in top_5_equipment and eq not in bottom_5_equipment]
        ordered_equipment_ids.extend(remaining_equipment) # Adiciona os restantes (pode precisar de uma ordenação aqui também se quiser)
        for eq_id in bottom_5_equipment:
            ordered_equipment_ids.append(f"{eq_id} (Bottom 5)")

# Mapear os equipment_ids originais para os novos labels para o Plotly
    original_to_labeled_map = {}
    for eq_id in top_5_equipment:
        original_to_labeled_map[eq_id] = f"{eq_id} (Top 5)"
    for eq_id in bottom_5_equipment:
        original_to_labeled_map[eq_id] = f"{eq_id} (Bottom 5)"
    for eq_id in remaining_equipment:
        original_to_labeled_map[eq_id] = eq_id

# Reindexar o pivot_table com os labels do eixo Y para a ordem desejada
    pivot_table['labeled_equipment_id'] = pivot_table.index.map(original_to_labeled_map)
    pivot_table = pivot_table.set_index('labeled_equipment_id').reindex(ordered_equipment_ids)


# 6. Preparar customdata para o hover (min, max, mean por equipamento)
# Criar um dicionário para mapear equipment_id original para suas estatísticas
    equipment_stats_dict = equipment_stats.set_index('equipment_id').to_dict(orient='index')

# Criar uma matriz customdata que tenha a mesma forma do Z, preenchendo as estatísticas para cada célula
# O customdata deve ser uma lista de listas, onde cada sub-lista corresponde a uma linha do heatmap (um equipamento)
    customdata_matrix = []
    for labeled_eq_id in ordered_equipment_ids:
    # Obter o ID original do equipamento
        original_eq_id = labeled_eq_id.replace(" (Top 5)", "").replace(" (Bottom 5)", "")
        stats = equipment_stats_dict.get(original_eq_id, {'min_consumption': np.nan, 'max_consumption': np.nan, 'mean_consumption': np.nan})
    # Repetir as estatísticas para todos os dias na linha para que o hover possa acessá-las
        customdata_matrix.append([[stats['min_consumption'], stats['max_consumption'], stats['mean_consumption']] for _ in all_weekdays_dates_sorted])

# 7. Criar o Heatmap
    fig = go.Figure(data=go.Heatmap(
        x=pd.to_datetime(pivot_table.columns).strftime('%Y-%m-%d').tolist(), # Eixo X: Datas dos dias de semana
        y=pivot_table.index.tolist(),                       # Eixo Y: Equipamentos (com marcações)
        z=pivot_table.values,                               # Valores Z: Consumo diário
        colorscale='Jet',                               # Escala de cores (cores mais fortes para maiores valores)
        colorbar=dict(title='Consumo (kWh)'),
        hovertemplate=(
        "<b>Data:</b> %{x}<br>"
        "<b>Equipamento:</b> %{y}<br>"
        "<b>Consumo Diário:</b> %{z:.2f} kWh<br>"
        "<extra>" # Isso permite ter um título para o hover, mas escondendo o nome da trace padrão
        "<b>Estatísticas do Equipamento (Dias de Semana):</b><br>"
        "  Mínimo: %{customdata[0]:.2f} kWh<br>"
        "  Máximo: %{customdata[1]:.2f} kWh<br>"
        "  Médio: %{customdata[2]:.2f} kWh"
        "</extra>"
       ),
    customdata=customdata_matrix # Adiciona os dados personalizados para o hover
    ))

# 8. Layout e customizações
    fig.update_layout(
        title='Consumo de Energia por Equipamento ao Longo dos Dias de Semana',
        xaxis_title='Dia da Semana',
        yaxis_title='ID do Equipamento',
        xaxis_nticks=len(all_weekdays_dates_sorted) + 1, # Garante que todos os dias sejam exibidos
        yaxis_automargin=True, # Ajusta margem para labels longos
        height=800, # Altura ajustável
        width=1000, # Largura ajustável
    )

# Exibir o heatmap no Streamlit
    st.plotly_chart(fig, use_container_width=True)

# Opcional: Mostrar os top 5 e bottom 5 equipamentos em uma tabela
    st.markdown("---")
    st.subheader("Equipamentos com Maior e Menor Consumo Médio (Dias de Semana)")

    st.write("**Top 5 Equipamentos com Maior Consumo Médio:**")
    st.dataframe(equipment_stats[equipment_stats['equipment_id'].isin(top_5_equipment)].sort_values(by='mean_consumption', ascending=False).set_index('equipment_id'))

    st.write("**Top 5 Equipamentos com Menor Consumo Médio:**")
    st.dataframe(equipment_stats[equipment_stats['equipment_id'].isin(bottom_5_equipment)].sort_values(by='mean_consumption', ascending=True).set_index('equipment_id'))
