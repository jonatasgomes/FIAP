import streamlit as st
import database as db

def limpar_sessao():
    st.session_state['id_cultura'] = None
    st.session_state['nome_cultura'] = None

def editar_area(_id_cultura, _nome, _largura, _comprimento, _base, _altura, _raio, _base_menor, _figura):
    st.session_state['id_cultura'] = _id_cultura
    st.session_state['nome_cultura'] = _nome
    st.session_state['largura'] = _largura
    st.session_state['comprimento'] = _comprimento
    st.session_state['base'] = _base
    st.session_state['altura'] = _altura
    st.session_state['raio'] = _raio
    st.session_state['base_menor'] = _base_menor
    st.session_state['figura'] = _figura

def salvar_area(_id_cultura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area, _figura):
    db.salvar_area(_id_cultura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area, _figura)
    limpar_sessao()

# mostrar as culturas
st.markdown('Calcule as áreas de plantio para cada cultura. <small>(clique na cultura para editar)</small>', unsafe_allow_html=True)
culturas = db.culturas_info()
if culturas:
    col1, col2, col3 = st.columns(3)
    for i, cult in enumerate(culturas):
        col = [col1, col2, col3][i % 3]
        with col:
            st.button(f'{cult[9]}', on_click=editar_area, args=(cult[0], cult[1], cult[2], cult[3], cult[4], cult[5], cult[6], cult[7], cult[8]), key=cult[0])

# criar o formulário
id_cultura = st.session_state.get('id_cultura', None)
nome_cultura = st.text_input('Cultura', max_chars=128, value=st.session_state.get('nome_cultura', ''), disabled=True)
figura = st.selectbox('Geometria da Área Plantada', ['Retângulo', 'Triângulo', 'Círculo', 'Trapézio'], key='figura', index=None, placeholder='Selecione...')
largura = None
comprimento = None
base = None
altura = None
raio = None
base_menor = None
area = None
with st.form('form_cultura', clear_on_submit=True):
    if figura == 'Retângulo':
        largura = st.number_input('Largura (m)', min_value=0, max_value=9999, step=1, key='largura')
        comprimento = st.number_input('Comprimento (m)', min_value=0, max_value=9999, step=1, key='comprimento')
        if largura and comprimento:
            area = largura * comprimento
    elif figura == 'Triângulo':
        base = st.number_input('Base (m)', min_value=0, max_value=9999, step=1, key='base')
        altura = st.number_input('Altura (m)', min_value=0, max_value=9999, step=1, key='altura')
        if base and altura:
            area = (base * altura) / 2
    elif figura == 'Círculo':
        raio = st.number_input('Raio (m)', min_value=0, max_value=9999, step=1, key='raio')
        if raio:
            area = 3.14 * raio ** 2
    elif figura == 'Trapézio':
        base = st.number_input('Base Maior (m)', min_value=0, max_value=9999, step=1, key='base')
        base_menor = st.number_input('Base Menor (m)', min_value=0, max_value=9999, step=1, key='base_menor')
        altura = st.number_input('Altura (m)', min_value=0, max_value=9999, step=1, key='altura')
        if base and base_menor and altura:
            area = ((base + base_menor) * altura) / 2
    # converter área para hectares
    area = round(area / 10000, 2)
    col1, col2, col3 = st.columns([3, 3, 14])
    with col1:
        submit_button = st.form_submit_button('Calcular', type='primary')
    with col2:
        st.form_submit_button('Limpar', type='secondary', on_click=limpar_sessao)

if submit_button:
    if id_cultura:
        salvar_area(id_cultura, largura, comprimento, base, altura, raio, base_menor, area, figura)
        st.rerun()
    else:
        st.error('Por favor, selecione uma cultura')
