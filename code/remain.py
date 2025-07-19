

### **Visualização 2: O Heatmap Interativo (Descoberta de Padrões)**


# app.py (continuação)

st.header("2. O Primeiro Nível de Refinamento: Padrões de Consumo Semanal")
st.write("""
Para começar a entender o consumo, vamos focar em uma pergunta fundamental: **como o consumo total de energia se comporta entre os dias de semana e os fins de semana?**
Aqui, agregamos o consumo de **todos os equipamentos** para cada semana do mês, separando os dias úteis dos sábados e domingos.
""")

# Adicionar uma coluna para identificar a semana do ano (ou do mês)
# Usaremos 'isocalendar().week' para a semana do ano
df_consumption['week_of_year'] = df_consumption['timestamp'].dt.isocalendar().week.astype(int)

# --- Agregação do consumo TOTAL para dias de semana e fins de semana por semana ---
# Agrupar por semana do ano e tipo de dia, e somar o consumo de todos os equipamentos
df_weekly_total_consumption = df_consumption.groupby(['week_of_year', 'day_type'])['consumption_kwh'].sum().reset_index()

# Garantir que a ordem dos tipos de dia seja consistente
df_weekly_total_consumption['day_type'] = pd.Categorical(
    df_weekly_total_consumption['day_type'], 
    categories=['Dia de Semana', 'Fim de Semana'], 
    ordered=True
)
df_weekly_total_consumption = df_weekly_total_consumption.sort_values(['week_of_year', 'day_type'])

fig_weekly_comparison = px.bar(df_weekly_total_consumption,
                               x='week_of_year',
                               y='consumption_kwh',
                               color='day_type',
                               barmode='group', # Barras agrupadas para comparar semana vs fim de semana
                               title='Consumo Total Agregado (kWh) por Semana: Dias de Semana vs. Fins de Semana',
                               labels={'week_of_year': 'Semana do Ano', 'consumption_kwh': 'Consumo Total (kWh)', 'day_type': 'Tipo de Dia'},
                               hover_data={'week_of_year': True, 'day_type': True, 'consumption_kwh': ':.0f'},
                               height=500
                              )

fig_weekly_comparison.update_layout(xaxis_title="Semana do Ano")
fig_weekly_comparison.update_yaxes(title_text="Consumo Total (kWh)")

st.plotly_chart(fig_weekly_comparison, use_container_width=True)

st.markdown("""
Com esta visualização, a diferença é evidente! Podemos notar que o consumo total em **dias de semana** é consistentemente **maior** que nos **fins de semana**.
Isso sugere que há uma correlação entre o horário de expediente/produção e o consumo de energia. A boa notícia é que, se o consumo de fim de semana não for zero ou muito baixo, ainda há **potencial para otimização** nos dias de não operação.

Agora que confirmamos essa diferença macro, podemos mergulhar mais fundo nos dias da semana para ver os padrões diários.
""")

# app.py (continuação) Parte 4 : Heatmaps 
df_avg_monthly_consumption = df_consumption.groupby('equipment_id')['consumption_kwh'].mean().round(2).to_dict()

# --- Identificar os Top 10 Equipamentos com maior consumo médio geral ---
top_10_equipments = df_consumption.groupby('equipment_id')['consumption_kwh'].mean().nlargest(10).index.tolist()

st.header("4. Detalhando o Consumo Diário: Equipamento por Dia da Semana (Semanas Chave)")
st.write("""
Com base na análise anterior, onde confirmamos que os dias de semana têm consumo total significativamente maior,
vamos aprofundar a investigação. Selecionamos a **Semana 24** (uma de menor consumo) e a **Semana 26** (uma de maior consumo)
para um olhar detalhado.

Este heatmap mostra o **consumo diário de cada equipamento** por dia da semana.
**Passe o mouse sobre uma célula para ver o consumo médio mensal desse equipamento!**
""")

# --- Filtrar para as semanas 24 e 26 E para os TOP 10 Equipamentos ---
df_selected_weeks_top10 = df_consumption[
    (df_consumption['week_of_year'].isin([24, 26])) &
    (df_consumption['equipment_id'].isin(top_10_equipments)) # NOVO FILTRO APLICADO AQUI
].copy() 

# Agregação para o Heatmap: Consumo total por equipamento, dia da semana e semana do ano
# Note que estamos pegando o consumo SUM diário de cada equipamento
# Agregação para o Heatmap
df_heatmap_eq_day_top10 = df_selected_weeks_top10.groupby(['equipment_id', 'day_name', 'week_of_year', 'day_of_week_num'])['consumption_kwh'].sum().reset_index()

## Ordenar os dias da semana corretamente (Seg a Dom)
day_order_names = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
df_heatmap_eq_day_top10['day_name'] = pd.Categorical(df_heatmap_eq_day_top10['day_name'], categories=day_order_names, ordered=True)
df_heatmap_eq_day_top10 = df_heatmap_eq_day_top10.sort_values(['equipment_id', 'day_of_week_num'])

# Criar um pivoteamento para cada semana para gerar o heatmap
# X-axis: dia da semana (nome); Y-axis: equipamento_id
# Faremos dois heatmaps ou um com facet_col, dependendo do que ficar mais claro.
# Um com facet_col é geralmente melhor para comparação direta.

# Calcular o consumo médio MENSAL de cada equipamento para o hover
df_avg_monthly_consumption = df_consumption.groupby('equipment_id')['consumption_kwh'].mean().round(2).to_dict()


# --- Heatmap para a Semana 24 (Ajustado) ---
st.subheader("Consumo Diário (kWh) dos Top 10 Equipamentos - Semana 24 (Menor Consumo Geral)")
df_week_24_top10 = df_heatmap_eq_day_top10[df_heatmap_eq_day_top10['week_of_year'] == 24]
heatmap_data_24_top10 = df_week_24_top10.pivot_table(index='equipment_id', columns='day_name', values='consumption_kwh', fill_value=0)
heatmap_data_24_top10 = heatmap_data_24_top10[day_order_names] # Garante a ordem das colunas

custom_data_24_top10 = np.empty(heatmap_data_24_top10.shape, dtype=object)
for r_idx, eq_id in enumerate(heatmap_data_24_top10.index):
    for c_idx, day_name in enumerate(heatmap_data_24_top10.columns):
        custom_data_24_top10[r_idx, c_idx] = f"{df_avg_monthly_consumption.get(eq_id, 'N/A')} kWh"


fig_heatmap_24_top10 = go.Figure(data=go.Heatmap(
    z=heatmap_data_24_top10.values,
    x=heatmap_data_24_top10.columns,
    y=heatmap_data_24_top10.index,
    colorscale='Viridis_r', # NOVO: Invertida. Cores escuras para maior consumo
    colorbar=dict(title='Consumo Diário (kWh)'),
    customdata=custom_data_24_top10,
    hovertemplate=(
        "Equipamento: %{y}<br>"
        "Dia da Semana: %{x}<br>"
        "Consumo Diário: %{z:.0f} kWh<br>"
        "<extra><b>Consumo Médio Mensal:</b> %{customdata}</extra>"
    ),
    # NOVO: Linhas de GRID
    ygap=1, # Espaço entre as células no eixo Y
    xgap=1, # Espaço entre as células no eixo X
))

fig_heatmap_24_top10.update_layout(
    title='Consumo Diário dos TOP 10 Equipamentos - Semana 24 (Menor Consumo Geral)',
    xaxis_title='Dia da Semana',
    yaxis_title='Equipamento ID',
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(categoryarray=day_order_names, categoryorder='array'),
    height=700
)
st.plotly_chart(fig_heatmap_24_top10, use_container_width=True)


# --- Heatmap para a Semana 26 (Ajustado) ---
st.subheader("Consumo Diário (kWh) dos Top 10 Equipamentos - Semana 26 (Maior Consumo Geral)")
df_week_26_top10 = df_heatmap_eq_day_top10[df_heatmap_eq_day_top10['week_of_year'] == 26]
heatmap_data_26_top10 = df_week_26_top10.pivot_table(index='equipment_id', columns='day_name', values='consumption_kwh', fill_value=0)
heatmap_data_26_top10 = heatmap_data_26_top10[day_order_names] # Garante a ordem das colunas

custom_data_26_top10 = np.empty(heatmap_data_26_top10.shape, dtype=object)
for r_idx, eq_id in enumerate(heatmap_data_26_top10.index):
    for c_idx, day_name in enumerate(heatmap_data_26_top10.columns):
        custom_data_26_top10[r_idx, c_idx] = f"{df_avg_monthly_consumption.get(eq_id, 'N/A')} kWh"


fig_heatmap_26_top10 = go.Figure(data=go.Heatmap(
    z=heatmap_data_26_top10.values,
    x=heatmap_data_26_top10.columns,
    y=heatmap_data_26_top10.index,
    colorscale='Viridis_r', # NOVO: Invertida. Cores escuras para maior consumo
    colorbar=dict(title='Consumo Diário (kWh)'),
    customdata=custom_data_26_top10,
    hovertemplate=(
        "Equipamento: %{y}<br>"
        "Dia da Semana: %{x}<br>"
        "Consumo Diário: %{z:.0f} kWh<br>"
        "<extra><b>Consumo Médio Mensal:</b> %{customdata}</extra>"
    ),
    # NOVO: Linhas de GRID
    ygap=1, # Espaço entre as células no eixo Y
    xgap=1, # Espaço entre as células no eixo X
))

fig_heatmap_26_top10.update_layout(
    title='Consumo Diário dos TOP 10 Equipamentos - Semana 26 (Maior Consumo Geral)',
    xaxis_title='Dia da Semana',
    yaxis_title='Equipamento ID',
    yaxis=dict(categoryorder='category ascending'),
    xaxis=dict(categoryarray=day_order_names, categoryorder='array'),
    height=700
)
st.plotly_chart(fig_heatmap_26_top10, use_container_width=True)

st.markdown("""
Estes heatmaps focados nos **TOP 10 equipamentos** e com a **escala de cores invertida** (onde cores mais escuras representam maior consumo) tornam os padrões de consumo muito mais visíveis. As **linhas de grade** ajudam a delimitar cada célula, facilitando a identificação rápida.

Ao comparar a Semana 24 e a Semana 26, podemos ver:
* Quais equipamentos aumentaram ou diminuíram significativamente o consumo em dias específicos.
* Padrões de consumo persistentes em fins de semana para os top consumidores.
* Novas oportunidades de otimização em equipamentos que talvez não fossem tão visíveis antes.
""")

# app.py (continuação - Parte 5: Conclusão)

st.header("5. Conclusão: De Dados a Decisões Acionáveis")
st.write("""
Através de uma sequência de visualizações focadas e interativas, conseguimos transformar um conjunto de dados complexo em inteligência de negócio.
Partimos de um "prato de espaguete" ilegível para dashboards claros que revelam padrões e oportunidades.
""")

st.markdown("""
**Principais Insights Obtidos com esta Abordagem:**
* **Diferenças entre Dias de Semana e Fins de Semana:** Confirmamos que o consumo total é significativamente maior em dias úteis, mas que ainda há consumo considerável nos fins de semana, indicando potencial de otimização.
* **Identificação de 'Vilões' Persistentes:** Ao focar nos Top 10 equipamentos, pudemos ver quais são os maiores consumidores e como seu padrão varia entre semanas de alto e baixo consumo.
* **Padrões de Consumo por Equipamento e Dia:** Os heatmaps detalhados permitem identificar dias específicos onde certos equipamentos têm picos de consumo inesperados ou sustentam alto uso fora do horário de operação.

**Oportunidades de Otimização e Próximos Passos Recomendados:**
1.  **Auditoria Operacional Focada:** Investigar os equipamentos que apresentam consumo elevado em fins de semana ou padrões atípicos (identificados nos heatmaps) para entender a causa raiz. Isso pode envolver verificações de operação, manutenção ou agendamentos.
2.  **Otimização de Horários:** Programar o desligamento ou operação em baixa potência de equipamentos fora do horário de pico ou em dias de inatividade (especialmente fins de semana).
3.  **Manutenção Preventiva:** Analisar equipamentos que mostram consumo inconsistente ou picos inexplicáveis, pois podem indicar falhas ou ineficiências.
4.  **Monitoramento Contínuo:** Utilizar este dashboard como ferramenta para acompanhar os resultados das ações de otimização e garantir a sustentabilidade dos esforços de economia de energia.

""")

st.success("Com a análise correta, dados de consumo se tornam um mapa para a **eficiência, sustentabilidade e economia**!")
