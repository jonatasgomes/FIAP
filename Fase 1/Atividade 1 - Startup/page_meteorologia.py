import streamlit as st
import subprocess

# executa o script R
def executar_script_r(_cidade, _pais):
    _resultado = subprocess.run(
        ['Rscript', 'r_chamar_api_clima.R', f'{_cidade}', f'{_pais}'],
        capture_output=True,
        text=True
    )
    return _resultado.stdout

st.markdown("Pesquise as condições climáticas em uma cidade.")

col1, col2 = st.columns(2)
with col1:
    cidade = st.text_input("Cidade")
with col2:
    pais = st.text_input("País")

if st.button("Buscar"):
    if not cidade:
        st.warning("Por favor, informe pelo menos a cidade.")
    else:
        resultado = executar_script_r(cidade, pais)
        st.write(resultado)
