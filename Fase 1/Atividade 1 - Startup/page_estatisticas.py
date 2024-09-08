import subprocess
from io import StringIO
import streamlit as st
import pandas as pd
import plotly.express as px

def executar_script_r():
    # executa o script R
    resultado = subprocess.run(
        ['Rscript', 'r_calcular_estatisticas.R'],
        capture_output=True,
        text=True
    )
    return resultado.stdout

# chamar a função para executar o script R
output = executar_script_r()

# carregar a saída JSON em um DataFrame
estatisticas = pd.read_json(StringIO(output))
if estatisticas.shape[1] == 2:
    estatisticas.columns = ["Variável", "Média"]
elif estatisticas.shape[1] == 3:
    estatisticas.columns = ["Variável", "Média", "Desvio Padrão"]

# exibir os resultados no Streamlit
st.markdown("Descubra os números de sua fazenda.")
st.dataframe(
    estatisticas.style.format({"Média": "{:,.2f}", "Desvio Padrão": "{:,.2f}"}),
    hide_index=True,
    use_container_width=True
)

# tratar dados para o gráfico
if "Desvio Padrão" in estatisticas.columns:
    fig = px.bar(
        estatisticas, x='Variável', y=['Média', 'Desvio Padrão'], barmode='group',
        labels={'value': 'Valores', 'variable': 'Estatísticas'},
    )
else:
    fig = px.bar(
        estatisticas, x='Variável', y='Média',
        labels={'Média': 'Valores'},
    )
fig.update_layout(
    xaxis_title=None,
    yaxis_title=None,
    legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.1)
)

# exibir o gráfico
st.plotly_chart(fig, use_container_width=True)
