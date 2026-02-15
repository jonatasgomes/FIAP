# importar pacotes
import streamlit as st

# criar páginas
inicio = st.Page(
    "pagina_dashboard.py", title="Dashboard", icon="📊", default=True
)
dados = st.Page(
    "pagina_dados.py", title="Entrada de Dados", icon="✨"
)

# carregar páginas
nav = st.navigation(
    {
        "FIAP - Farmtech Solutions": [inicio, dados],
    }
)

#iniciar aplicação
nav.run()
