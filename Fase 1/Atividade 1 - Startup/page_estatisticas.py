import subprocess
from io import StringIO
import streamlit as st
import pandas as pd

def executar_script_r():
    # executa o script R
    resultado = subprocess.run(
        ['Rscript', 'R_calcular_estatisticas.R'],
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
estatisticas = estatisticas.style.format({"Média": "{:,.2f}", "Desvio Padrão": "{:,.2f}"})

# exibir os resultados no Streamlit
st.markdown("Descubra os números de sua fazenda.")
st.dataframe(
    estatisticas,
    hide_index=True,
    use_container_width=True
)
