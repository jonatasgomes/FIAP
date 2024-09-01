import streamlit as st

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login():
    with st.form("login_form"):
        cliente = st.selectbox("Selecione um Cliente", ["Fazenda Boa Colheita"])
        username = st.text_input("Usuário", value="demo")
        password = st.text_input("Senha", type="password", value="demo")

        if st.form_submit_button("Entrar"):
            if username == "demo" and password == "demo":
                st.session_state.logged_in = True
                st.rerun()
            else:
                st.error("Invalid username or password")

def logout():
    if st.button("Sair"):
        st.session_state.logged_in = False
        st.rerun()

login_page = st.Page(login, title="Entrar", icon=":material/login:")
logout_page = st.Page(logout, title="Sair", icon=":material/logout:")

inicio = st.Page(
    "page_inicio.py", title="Início", icon=":material/dashboard:", default=True
)
culturas = st.Page("page_culturas.py", title="Culturas", icon=":material/bug_report:")
areas = st.Page(
    "page_areas.py", title="Áreas de Plantio", icon=":material/notification_important:"
)
insumos = st.Page(
    "page_insumos.py", title="Manejo de Insumos", icon=":material/notification_important:"
)

estatisticas = st.Page("page_estatisticas.py", title="Estatísticas", icon=":material/search:")
meteorologia = st.Page("page_meteorologia.py", title="Meteorologia", icon=":material/history:")

st.markdown(
    '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.3/css/all.min.css">',
    unsafe_allow_html=True
)
header_container = st.container()
with header_container:
    leaf = "<i class='fas fa-leaf' style='color: green;'>"
    st.markdown("<h1 style='text-align: center; color: darkgreen;'>FarmTech Solutions</h1>"
                f"<h6 style='text-align: center; color: darkgreen; margin-top: -20px;'>{leaf} Agricultura digital => inovação + tecnologia = produtividade + sustentabilidade {leaf}</h6>",
                unsafe_allow_html=True
    )

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

pg.run()
