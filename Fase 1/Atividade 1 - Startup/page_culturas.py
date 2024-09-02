import streamlit as st
import database as db

def limpar_sessao():
    st.session_state['id_cultura'] = None
    st.session_state['nome_cultura'] = None

def editar_cultura(_id, _nome):
    st.session_state['id_cultura'] = _id
    st.session_state['nome_cultura'] = _nome

def deletar_cultura(_id):
    c.execute('DELETE FROM culturas WHERE id = ?', (_id,))
    conn.commit()
    limpar_sessao()

def salvar_cultura(_id, _nome):
    if _id:
        c.execute('UPDATE culturas SET cultura = ? WHERE id = ?', (_nome.capitalize(), _id))
    else:
        c.execute('INSERT INTO culturas (cultura) VALUES (?)', (_nome.capitalize(),))
    limpar_sessao()
    conn.commit()

# conectar ao banco de dados
conn = db.get_connection()
c = conn.cursor()

# mostrar as culturas
st.markdown('Culturas usadas nesta fazenda <small>(clique para editar)</small>:', unsafe_allow_html=True)
c.execute('SELECT * FROM culturas')
culturas = c.fetchall()
col1, col2, col3 = st.columns(3)
for i, cult in enumerate(culturas):
    col = [col1, col2, col3][i % 3]
    with col:
        st.button(f'🌱 &nbsp;&nbsp;{cult[1]} ', on_click=editar_cultura, args=(cult[0], cult[1]), key=cult[0])

# criar o formulário
with st.form('form_cultura', clear_on_submit=True):
    id_cultura = st.session_state.get('id_cultura', None)
    nome_cultura = st.text_input('Cultura', max_chars=128, value=st.session_state.get('nome_cultura', ''))
    col1, col2, col3 = st.columns([2, 2, 12])
    with col1:
        submit_button = st.form_submit_button('Salvar', type='primary')
    with col2:
        st.form_submit_button('Limpar', type='secondary', on_click=limpar_sessao)
    with col3:
        delete_button = None
        if id_cultura:
            delete_button = st.form_submit_button('Excluir', type='secondary', on_click=deletar_cultura, args=(id_cultura,))

if submit_button:
    if nome_cultura:
        salvar_cultura(id_cultura, nome_cultura)
        st.rerun()
    else:
        st.error('Por favor, informe o nome da cultura')
