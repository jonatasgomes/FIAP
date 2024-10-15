import streamlit as st
import database as db

figuras_lov = ['Retângulo', 'Triângulo', 'Círculo', 'Trapézio']

# adicionar área em janela modal
@st.dialog("Detalhes da Área")
def detalhes_area(_id=None):
    _nome = None
    _figura = 0
    _largura = None
    _comprimento = None
    _base = None
    _altura = None
    _raio = None
    _base_menor = None
    _area = 0.0
    if _id is not None:
        area = db.area(_id)
        if area is not None:
            _nome = area[0][0]
            try:
                _figura = figuras_lov.index(area[0][1])
            except ValueError:
                _figura = 0
            _largura = area[0][2]
            _comprimento = area[0][3]
            _base = area[0][4]
            _altura = area[0][5]
            _raio = area[0][6]
            _base_menor = area[0][7]

    _nome = st.text_input("Nome da Área", value=_nome)
    _figura = st.selectbox('Geometria da Área de Plantio', figuras_lov, index=_figura, placeholder='Selecione...')
    if _figura == 'Retângulo':
        _col1, _col2 = st.columns(2)
        with _col1:
            _largura = st.number_input("Largura (m)", min_value=_largura, step=1)
        with _col2:
            _comprimento = st.number_input("Comprimento (m)", min_value=_comprimento, step=1)
        if _largura and _comprimento:
            _area = _largura * _comprimento
        _base = None
        _altura = None
        _raio = None
        _base_menor = None
    elif _figura == 'Triângulo':
        _col1, _col2 = st.columns(2)
        with _col1:
            _base = st.number_input("Base (m)", min_value=_base, step=1)
        with _col2:
            _altura = st.number_input("Altura (m)", min_value=_altura, step=1)
        if _base and _altura:
            _area = (_base * _altura) / 2
        _largura = None
        _comprimento = None
        _raio = None
        _base_menor = None
    elif _figura == 'Círculo':
        _raio = st.number_input("Raio (m)", min_value=_raio, step=1)
        if _raio:
            _area = 3.14 * _raio * _raio
        _largura = None
        _comprimento = None
        _base = None
        _altura = None
        _base_menor = None
    elif _figura == 'Trapézio':
        _col1, _col2, _col3 = st.columns(3)
        with _col1:
            _base = st.number_input("Base (m)", min_value=_base, step=1)
        with _col2:
            _base_menor = st.number_input("Base Menor (m)", min_value=_base_menor, step=1)
        with _col3:
            _altura = st.number_input("Altura (m)", min_value=_altura, step=1)
        if _base and _base_menor and _altura:
            _area = (_base + _base_menor) * _altura / 2
        _largura = None
        _comprimento = None
        _raio = None

    # converter area em hectares
    _area = _area / 10000 if _area else None
    st.metric('Área de Plantio', f'{_area:.2f}ha' if _area else '0.0ha')
    erro_msg = None
    _col1, _col2 = st.columns([2, 9])
    with _col1:
        if st.button("Salvar", type="primary"):
            if _nome and _figura:
                db.salvar_area(_id, _nome, _figura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area)
                st.rerun()
            else:
                erro_msg = "Por favor, informe os dados da área de plantio."
    with _col2:
        if _id is not None and st.button("Excluir"):
            db.excluir_area(_id)
            st.rerun()

    if erro_msg:
        st.error(erro_msg)

# grid mostrando as culturas
st.markdown("Calcule a área de plantio para cada cultura. <small>(selecione um registro para editar)</small>", unsafe_allow_html=True)
df = db.areas().fillna('')
grid = st.dataframe(df, use_container_width=True, selection_mode="single-row", on_select='rerun', hide_index=True)
col1, col2 = st.columns([0.29, 0.71])
with col1:
    # botão adicionar cultura
    st.button("Adicionar Área de Plantio", type="primary", on_click=detalhes_area)
if len(grid.selection['rows']) > 0:
    # botão editar cultura
    with col2:
        selected_idx = grid.selection['rows'][0]
        selected_id = int(df.index[selected_idx])
        if st.button("Editar Cultura"):
            detalhes_area(selected_id)
