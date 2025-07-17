import streamlit as st
import pandas as pd
import plotly.express as px
from pathlib import Path

# === Configuração de página ===
st.set_page_config(page_title="Storytelling com Consumo de Energia", layout="wide")

# === Caminhos fixos ===
BASE_DIR = Path.cwd()
DATA_DIR = BASE_DIR / "../data"
DATA_FILE = DATA_DIR / "energy30daysLongFormat.csv"

print("Base Dir", BASE_DIR)
print("Data Dir", DATA_DIR)
print(f"Buscando arquivo em: {DATA_FILE.resolve()}")
print(f"Arquivo existe? {DATA_FILE.exists()}")

if not DATA_FILE.exists():
    import sys
    sys.exit(f"❌ Arquivo {DATA_FILE.resolve()} não encontrado. Corrija o caminho ou a localização do arquivo.")
# === Carregar dados ===
@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    return df

df = load_data()

# === Título e introdução ===
st.title("⚡ Storytelling com Dados: Consumo de Energia Residencial/Industrial")

st.markdown("""
Este aplicativo demonstra a **transformação de visualizações caóticas em insights claros** 
usando **técnicas de Storytelling com Dados**.
""")

# === Visualização Inicial: Gráfico de Linha (Caótico) ===
st.subheader("🔍 Visualização Inicial: Gráfico de Linha (Caótico)")

fig_line = px.line(
    df,
    x="date",
    y="consumo_kWh",
    color="equipamento",
    title="Consumo Diário de Energia por Equipamento (kWh)"
)
st.plotly_chart(fig_line, use_container_width=True)

st.markdown("""
❌ **Problema:** Visualização densa e difícil de identificar padrões ou oportunidades de economia.
""")

# === Heatmap ===
st.subheader("🌡️ Heatmap: Consumo de Energia ao Longo do Tempo")

# Agregar dados por data e equipamento
pivot = df.pivot_table(
    index="equipamento",
    columns="date",
    values="consumo_kWh",
    aggfunc="sum",
    fill_value=0
)

# Para heatmap em Plotly, converter para formato long novamente
pivot_long = pivot.reset_index().melt(id_vars="equipamento", var_name="date", value_name="consumo_kWh")

fig_heatmap = px.density_heatmap(
    pivot_long,
    x="date",
    y="equipamento",
    z="consumo_kWh",
    color_continuous_scale="Viridis",
    title="Heatmap de Consumo de Energia (kWh) por Equipamento ao Longo do Tempo"
)
st.plotly_chart(fig_heatmap, use_container_width=True)

st.markdown("""
✅ **Agora conseguimos identificar rapidamente equipamentos e datas com maior consumo.**
""")

# === Drill-down: Top 3 Equipamentos ===
st.subheader("🔎 Top 3 Equipamentos por Consumo em um Dia")

selected_date = st.date_input(
    "Selecione a data para detalhar o consumo:",
    value=df["date"].max().date(),
    min_value=df["date"].min().date(),
    max_value=df["date"].max().date()
)

filtered = df[df["date"].dt.date == selected_date]

if not filtered.empty:
    top3 = (
        filtered.groupby("equipamento")["consumo_kWh"]
        .sum()
        .sort_values(ascending=False)
        .head(3)
        .reset_index()
    )
    fig_top3 = px.bar(
        top3,
        x="equipamento",
        y="consumo_kWh",
        color="equipamento",
        text="consumo_kWh",
        title=f"Top 3 Equipamentos em Consumo no dia {selected_date}"
    )
    st.plotly_chart(fig_top3, use_container_width=True)
else:
    st.info("Nenhum dado disponível para a data selecionada.")

# === Footer ===
st.markdown("---")
st.caption("Desenvolvido para projeto de Storytelling com Dados | williamufpr")

