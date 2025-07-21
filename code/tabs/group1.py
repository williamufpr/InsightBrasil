import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go # Mantemos para referência, embora PX seja mais direto aqui


from tabs.utils import mostrar_proxima_aba 
# 1. Simulação do DataFrame (manter igual ao anterior para consistência)
@st.cache_data
def render(df):



    st.title("📊 :Análise de Consumo de Energia de Computadores")
    st.subheader("Visualização da Distribuição de Equipamentos por Grupo de Consumo")

    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    Propomos inicialmente uma análise de segmentos de equipamentos que nos ofereça um melhor potencial para alcançar os objetivos
    Podemos analisar a distribuição de consumo e classificar os equipamentos em 3 grupos 
    <ul style="list-style-type: none; padding-left: 0;">
      <li>🔵 <span style="color:#003366; font-weight:bold;">Baixo Consumo</span></li>
      <li>🟠 <span style="color:#003366; font-weight:bold;">Consumo Médio</span></li>
      <li>🔴 <span style="color:#003366; font-weight:bold;">Alto Consumo</span></li>
  </p>

  <p>Veja o que obtivemos :</p>

  
</div>
""", unsafe_allow_html=True)



    
## Gemini 
    st.subheader("Segunda Distribuição de Equipamentos por Grupo de Consumo")

# 1. Calcular o consumo médio mensal para cada equipamento
    avg_consumption_per_equipment = df.groupby('equipment_id')['consumption_kwh'].mean().reset_index()
    avg_consumption_per_equipment.rename(columns={'consumption_kwh': 'monthly_avg_kwh'}, inplace=True)

    # 2. Calcular os quartis da distribuição de consumo médio
    q1 = avg_consumption_per_equipment['monthly_avg_kwh'].quantile(0.25)
    q2 = avg_consumption_per_equipment['monthly_avg_kwh'].quantile(0.50)
    q3 = avg_consumption_per_equipment['monthly_avg_kwh'].quantile(0.75)

    # 3. Categorizar os equipamentos e coletar dados para o hover
    categories_data = {
        'Baixo Consumo': {'count': 0, 'equipments_details': []},
        'Consumo Médio': {'count': 0, 'equipments_details': []},
        'Alto Consumo': {'count': 0, 'equipments_details': []}
    }

    for index, row in avg_consumption_per_equipment.iterrows():
        eq_id = row['equipment_id']
        avg_kwh = row['monthly_avg_kwh']

        if avg_kwh <= q1:
            category = 'Baixo Consumo'
        elif avg_kwh > q1 and avg_kwh <= q3:
            category = 'Consumo Médio'
        else: # avg_kwh > q3
            category = 'Alto Consumo'
        
        categories_data[category]['count'] += 1
        categories_data[category]['equipments_details'].append(f"{eq_id} ({avg_kwh:.2f} kWh)")

    # 4. Preparar o DataFrame para o gráfico de barras
    chart_data = pd.DataFrame({
        'Categoria de Consumo': list(categories_data.keys()),
        'Número de Equipamentos': [data['count'] for data in categories_data.values()],
        'Equipamentos Detalhados': ["<br>".join(data['equipments_details']) for data in categories_data.values()]
    })

    # Definir a ordem das categorias no gráfico
    category_order = ['Baixo Consumo', 'Consumo Médio', 'Alto Consumo']
    chart_data['Categoria de Consumo'] = pd.Categorical(chart_data['Categoria de Consumo'], categories=category_order, ordered=True)
    chart_data = chart_data.sort_values('Categoria de Consumo')

    # 5. Criar o gráfico de barras com Plotly
    fig = go.Figure(data=[
        go.Bar(
            x=chart_data['Categoria de Consumo'],
            y=chart_data['Número de Equipamentos'],
            marker_color=['#90CAF9', '#FFD54F', '#EF5350'], # Cores mais amigáveis (Azul, Amarelo, Vermelho)
            customdata=chart_data['Equipamentos Detalhados'], # Dados para o hover
            text=chart_data['Número de Equipamentos'],
            textposition='inside', # Posição do texto: dentro da barra
            textfont=dict(color='black', size=14), # Cor e tamanho da fonte do texto
            hovertemplate=(
                "<b>Categoria:</b> %{x}<br>" +
                "<b>Número de Equipamentos:</b> %{y}<br>" +
                "<extra>" + # Título para a seção de detalhes
                "<b>Detalhes dos Equipamentos:</b><br>" +
                "%{customdata}" +
                "</extra>"
            )
        )
    ])

    fig.update_layout(
        title='Contagem de Equipamentos por Categoria de Consumo Mensal',
        xaxis_title='Categoria de Consumo',
        yaxis_title='Número de Equipamentos',
        yaxis_tickformat='.0f', # Garante que o eixo Y mostre números inteiros
        bargap=0.3, # Espaçamento entre as barras
        height=500 # Altura ajustável
    )

    # 6. Plotar o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    # Adicionar explicação sobre os quartis para contexto
    
    st.markdown(f"""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
    <p style="font-size: 16px;">
        Conseguimos esclarecer os conjuntos sobre os quais teríamos mais oportunidades
        para gerar economia de energia :<br> 
            - Um conjunto de equipamentos de baixo Consumo <br>
            - Um conjunto de equipamentos de alto consumo 
    </p>
    <p>
        <ul style="list-style-type: none; padding-left: 0; color:#003366; font-weight:bold;">
            <li>🔵 Baixo Consumo Até {q1:.2f} kWh/mês </li>
            <li>🟠 <span style="color:#003366; font-weight:bold;">Consumo Médio de {q2:.2f} até {q3: .2f} kWh/mês</span></li>
            <li>🔴 <span style="color:#003366; font-weight:bold;">Alto Consumo Acima de {q3:.2f} kWh/mês</span></li>
        </ul>
    </p>
</div>
""", unsafe_allow_html=True)
    
    
    
    
def grafico_evolucao_consumo_por_faixa(df):
    
    st.markdown("""
<div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
  <p style="font-size: 16px;">
    O grupo de gerentes solicitou ainda uma visão temporal. <br> 
    Queriam uma melhor compreensão de como este agrupamento de equipamentos se comportava dia a dia. <br>
    Além disso, tinham o temor de que algum final de semana revelasse uma surpresa. <br>
    Propusemos então  a visualização a seguir para atender ao solicitado. 
    
  </p>

  
</div>
""", unsafe_allow_html=True)
    # Passo 1: Média de consumo por equipamento para classificação por faixa
    consumo_medio = df.groupby("equipment_id")["consumption_kwh"].mean()
    q1 = consumo_medio.quantile(0.25)
    q3 = consumo_medio.quantile(0.75)

    def faixa(consumo):
        if consumo <= q1:
            return "Baixo Consumo"
        elif consumo <= q3:
            return "Consumo Médio"
        else:
            return "Alto Consumo"

    # Classificar equipamentos
    classificacao = consumo_medio.apply(faixa).reset_index()
    classificacao.columns = ["equipment_id", "faixa"]

    # Unir faixa ao DataFrame original
    df = df.merge(classificacao, on="equipment_id")

    # Passo 2: Somar consumo diário por faixa
    df_agg = df.groupby(["date", "faixa"])["consumption_kwh"].sum().reset_index()

    # Ordenar faixas para visualização consistente
    ordem_faixa = ["Baixo Consumo", "Consumo Médio", "Alto Consumo"]
    df_agg["faixa"] = pd.Categorical(df_agg["faixa"], categories=ordem_faixa, ordered=True)
    df_agg = df_agg.sort_values(["date", "faixa"])

    # Passo 3: Gráfico de área empilhada
    fig = px.area(
        df_agg,
        x="date",
        y="consumption_kwh",
        color="faixa",
        color_discrete_map={
            "Baixo Consumo": "lightblue",
            "Consumo Médio": "orange",
            "Alto Consumo": "red"
        },
        title="📈 Evolução Diária do Consumo por Faixa de Equipamentos",
        markers=True
    )

    fig.update_layout(
        xaxis_title="Data",
        yaxis_title="Consumo (kWh)",
        legend_title="Faixa de Consumo",
        hovermode="x unified"
    )

    # Exibir no Streamlit
    st.subheader("📊 Evolução de Consumo por Faixa")
    st.plotly_chart(fig, use_container_width=True)



    
def plot_top_dispersion_boxplots(df_consumption):
    """
    Identifica os 5 equipamentos com maior dispersão de consumo ao longo do mês
    e plota um gráfico Box Plot para cada um deles.

    Parâmetros:
    df_consumption """

    st.subheader("Análise de Dispersão de Consumo: Equipamentos Mais Voláteis")
    
    st.markdown("""
       <div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
          <p style="font-size: 16px;">
              Esta última análise objetivou verificar se haveria outros equipamentos que <br>
              tivessem apresentado comportamento de consumo mais variado <br>
              ao longo do mês. Uma alta dispersão pode indicar comportamentos irregulares, <br>
              problemas ou oportunidades de otimização no uso desses equipamentos.
          </p>
       </div>
    """, unsafe_allow_html=True)
    
    # 1. Calcular o desvio padrão (dispersão) do consumo para cada equipamento
    # Consideramos todos os dias do mês para a dispersão.
    dispersion_per_equipment = df_consumption.groupby('equipment_id')['consumption_kwh'].std().reset_index()
    dispersion_per_equipment.rename(columns={'consumption_kwh': 'consumption_std'}, inplace=True)

    # Ordenar por desvio padrão e selecionar os top 5
    top_5_dispersion_equipments = dispersion_per_equipment.nlargest(5, 'consumption_std')
    
    # Verificar se há equipamentos suficientes
    if top_5_dispersion_equipments.empty:
        st.warning("Não há dados suficientes ou equipamentos para calcular a dispersão.")
        return

    top_5_ids = top_5_dispersion_equipments['equipment_id'].tolist()
    
    st.markdown(f"""
        <div style="border-left: 5px solid #003366; background-color: #f0f4f8; padding: 1rem; border-radius: 6px; margin-bottom: 1rem;">
            <p style="font-size: 16px;">
              Os 5 equipamentos com a maior dispersão (variabilidade) no consumo são: <br>
              **{', '.join(top_5_ids)}** <br>
              Abaixo, apresentamos os Box Plots para cada um deles, que ilustram a distribuição
              e variabilidade diária do consumo.</br>
              Destacamos o SMV340211 que também faz parte do grupo de equipamentos de alto consumo.
            </p>
        </div>
    """, unsafe_allow_html=True)


    # 2. Filtrar o DataFrame original para incluir apenas os top 5 equipamentos com maior dispersão
    df_top_5_dispersion = df_consumption[df_consumption['equipment_id'].isin(top_5_ids)].copy()

    # 3. Criar o Box Plot para os 5 equipamentos
    # Usamos Plotly Express para facilitar a criação de múltiplos boxplots
    fig = px.box(df_top_5_dispersion, 
                 x='equipment_id', 
                 y='consumption_kwh', 
                 title='Box Plot do Consumo Diário para os 5 Equipamentos de Maior Dispersão',
                 labels={'consumption_kwh': 'Consumo (kWh)', 'equipment_id': 'ID do Equipamento'},
                 color='equipment_id', # Colore cada boxplot de forma diferente
                 points="outliers", # Mostra os pontos fora da caixa
                 hover_data={'consumption_kwh': ':.2f'}
                )

    fig.update_layout(
        xaxis_title="ID do Equipamento",
        yaxis_title="Consumo (kWh)",
        # Garante que os equipamentos sejam mostrados na ordem decrescente de dispersão
        xaxis_categoryorder='array', 
        xaxis_categoryarray=top_5_dispersion_equipments['equipment_id'].tolist(),
        height=500
    )

    # Plotar o gráfico no Streamlit
    st.plotly_chart(fig, use_container_width=True)

    st.markdown("""
    <div style="background-color:#fff8e1; padding: 15px; border-radius: 8px; margin-top: 20px; border: 1px solid #ffecb3;">
        <h4 style="color:#fb8c00; margin-top: 0px;">Interpretação do Box Plot:</h4>
        <ul>
            <li>A linha central da caixa representa a **mediana** (Q2) do consumo diário.</li>
            <li>As bordas da caixa (Q1 e Q3) indicam o **intervalo interquartil (IQR)**, onde estão 50% dos dados.</li>
            <li>Os "bigodes" (linhas) se estendem até os valores mínimo e máximo, excluindo outliers.</li>
            <li>Os **pontos individuais** fora dos bigodes são considerados **outliers** (consumos atípicos).</li>
        </ul>
        <p>Um box plot "alto" ou com "bigodes" longos e muitos outliers indica **alta dispersão**.</p>
    </div>
    """, unsafe_allow_html=True)    
    
    mostrar_proxima_aba(nome_aba="Plano de ação",emoji="🚀")