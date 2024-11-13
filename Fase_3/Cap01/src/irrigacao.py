import streamlit as st

# criar páginas
dashboard = st.Page(
    "pagina_dashboard.py", title="Dashboard", icon="📈", default=True
)
dados = st.Page(
    "pagina_dados.py", title="Entrada de Dados", icon="🌱"
)

# carregar páginas
pg = st.navigation(
    {
        "Início": [dashboard],
        "Dados": [dados],
    }
)

#iniciar aplicação
pg.run()
