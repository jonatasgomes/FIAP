import streamlit as st

st.set_page_config(
    page_title="Gerenciador de Dados",
    page_icon="🌿",
    layout="wide"
)

sensores = st.Page("sensores.py", title="Sensores", icon="📊")
usuarios = st.Page("usuarios.py", title="Usuários", icon="👥")
culturas = st.Page("culturas.py", title="Culturas", icon="🌱")

pg = st.navigation(
    {
        "Gerenciador de Dados": [sensores, culturas, usuarios],
    }
)

pg.run()
