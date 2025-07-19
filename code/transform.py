

import numpy as np
import pandas as pd
import streamlit as st



# --- 1. Carregar e Preparar os Dados ---
# Usamos st.cache_data para que os dados sejam carregados e processados apenas uma vez
# e depois armazenados em cache, otimizando a performance do app.
@st.cache_data
def load_transformed_data(file_path):
    """
    Carrega o CSV de consumo já transformado.
    """
    df = pd.read_csv(file_path)
    # Garante que a coluna 'timestamp' seja do tipo datetime
    df['timestamp'] = pd.to_datetime(df['timestamp'], utc=True)
    # Extrai o dia do mês e a hora do dia novamente, se não estiverem corretos ou para garantir
    df['day_of_month'] = df['timestamp'].dt.day
    df['hour_of_day'] = df['timestamp'].dt.hour
    df['date_only'] = df['timestamp'].dt.date # Para visualização de data simples
    # Adicionar coluna para identificar a semana do ano
    # Usaremos 'isocalendar().week' para a semana do ano
    df['week_of_year'] = df['timestamp'].dt.isocalendar().week.astype(int)

    # Adicionar coluna para tipo de dia (Dia de Semana / Fim de Semana)
    # weekday() retorna 0 para segunda-feira e 6 para domingo
    df['day_of_week_num'] = df['timestamp'].dt.weekday # 0=Monday, 6=Sunday
    df['day_name'] = df['timestamp'].dt.day_name() # e.g., 'Monday', 'Saturday'
    df['day_type'] = df['day_of_week_num'].apply(lambda x: 'Fim de Semana' if x >= 5 else 'Dia de Semana')
    
    
    
    return df
