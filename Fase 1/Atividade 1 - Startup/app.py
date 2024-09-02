import streamlit as st
import database as db

def login():
    with st.form("login_form"):
        st.selectbox("Selecione um Cliente", ["Fazenda Boa Colheita"])
        username = st.text_input("Usuário", value="demo")
        password = st.text_input("Senha", type="password", value="demo")

        if st.form_submit_button("Entrar", type="primary"):
            if username == "demo" and password == "demo":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    if st.button("Sair", type="primary"):
        st.session_state.logged_in = False
        st.rerun()

# criar as páginas
login_page = st.Page(login, title="Entrar", icon=":material/login:")
logout_page = st.Page(logout, title="Sair", icon=":material/logout:")
inicio = st.Page(
    "page_inicio.py", title="Início", icon="🏡", default=True
)
culturas = st.Page("page_culturas.py", title="Culturas", icon="🌱")
areas = st.Page(
    "page_areas.py", title="Áreas de Plantio", icon="📐"
)
insumos = st.Page(
    "page_insumos.py", title="Manejo de Insumos", icon="⚖️"
)
estatisticas = st.Page("page_estatisticas.py", title="Estatísticas", icon="📈")
meteorologia = st.Page("page_meteorologia.py", title="Meteorologia", icon="🌦️")

# script para adicionar fontawesome
st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
    unsafe_allow_html=True
)

# adicionar header na aplicação
with st.container():
    leaf = "<i class='fas fa-leaf' style='color: green;'>"
    st.markdown("<h1 style='text-align: center; color: darkgreen;'>FarmTech Solutions</h1>"
                f"<h6 style='text-align: center; color: darkgreen; margin-top: -20px;'>{leaf} Agricultura digital => inovação + tecnologia = produtividade + sustentabilidade {leaf}</h6>",
                unsafe_allow_html=True
                )

# checar se o usuário está logado
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# mostrar menu lateral esquerdo
if st.session_state.logged_in:
    pg = st.navigation(
        {
            "Principal": [inicio, culturas, areas, insumos],
            "Ferramentas": [estatisticas, meteorologia],
            "Sistema": [logout_page],
        }
    )
else:
    pg = st.navigation([login_page])

db.check_database()
pg.run()
