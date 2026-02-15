import streamlit as st
import plotly.express as px
from db import OracleDatabase

# Instância do banco de dados (a configuração já está no db.py)
db = OracleDatabase()

# Função para construir gráficos
def construir_graficos(df):
    st.title("Monitoramento Agrícola")

    # Gráfico de Dispersão entre Sensor e Valor de Leitura
    fig_dispersao = px.scatter(df, x='Data', y='Valor', color='Sensor', 
                               title="Dispersão de Leituras por Sensor ao Longo do Tempo")
    st.plotly_chart(fig_dispersao)

    # Gráfico de Barras por Sensor
    fig_barras = px.bar(df, x='Sensor', y='Valor', color='Cultura', 
                        title="Valores de Leitura por Sensor")
    st.plotly_chart(fig_barras)

    # Gráfico de Linha para Leituras ao longo do tempo
    fig_linhas = px.line(df, x='Data', y='Valor', color='Cultura', 
                         title="Valores de Leitura ao Longo do Tempo")
    st.plotly_chart(fig_linhas)

# Carregar dados
df = db.carregar_leituras()

# Construir gráficos
construir_graficos(df)
