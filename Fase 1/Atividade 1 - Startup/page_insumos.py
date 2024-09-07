import streamlit as st
import database as db

lista_produtos = ["Nitrogênio", "Fósforo", "Potássio", "Calcário", "Herbicidas", "Fungicidas", "Inseticidas"]
lista_unidades = ["L", "Kg"]

# adicionar insumo em janela modal
@st.dialog("Detalhes do Insumo")
def detalhes_insumo(_id=None):
    _id_cultura = 0
    _id_area = 0
    _ruas = 1
    _comprimento = 1
    _produto = 0
    _unidade = 1
    _dosagem = 0.5
    culturas = db.culturas_lov()
    areas = db.areas_lov()
    if _id is not None:
        insumo = db.insumo(_id)
        if insumo is not None:
            try:
                _id_cultura = [x[0] for x in culturas].index(insumo[0][0])
            except ValueError:
                _id_cultura = 0
            try:
                _id_area = [x[0] for x in areas].index(insumo[0][1])
            except ValueError:
                _id_cultura = 0
            try:
                _produto = lista_produtos.index(insumo[0][2])
            except ValueError:
                _produto = 0
            try:
                _dosagem = insumo[0][3]
            except ValueError:
                _dosagem = 0.5
            try:
                _unidade = lista_unidades.index(insumo[0][4])
            except ValueError:
                _unidade = 1
            try:
                _ruas = insumo[0][5]
            except ValueError:
                _ruas = 1
            try:
                _comprimento = insumo[0][6]
            except ValueError:
                _comprimento = 1

    culturas = culturas or [(0, "Selecione...")]
    id_cultura = st.selectbox("Cultura", culturas, index=_id_cultura, placeholder="Selecione...", format_func=lambda x: x[1])[0]
    cols = st.columns(3)
    with cols[0]:
        areas = areas or [(0, "Selecione...")]
        id_area = st.selectbox("Área de Plantio", areas, index=_id_area, placeholder="Selecione...", format_func=lambda x: x[1])[0]
    with cols[1]:
        ruas = st.number_input("Total de Ruas", min_value=_ruas, step=1)
    with cols[2]:
        comprimento = st.number_input("Comprimento (m)", min_value=_comprimento, step=1)
    cols = st.columns(3)
    with cols[0]:
        produto = st.selectbox("Insumo", lista_produtos, index=_produto, placeholder="Selecione...")
    with cols[1]:
        unidade = st.selectbox("Unidade", lista_unidades, index=_unidade, placeholder="Selecione...")
    with cols[2]:
        dosagem = st.number_input(f'Qtde p/ metro ({unidade})', min_value=_dosagem, step=0.5)
    total = dosagem * comprimento * ruas
    st.metric(f"Total de {produto}", f"{total:.2f}{unidade}")
    erro_msg = None
    _col1, _col2 = st.columns([2, 9])
    with _col1:
        if st.button("Salvar", type="primary"):
            if id_cultura > 0 and id_area > 0:
                db.salvar_insumo(_id, id_cultura, id_area, produto, dosagem, unidade, ruas, comprimento, total)
                st.rerun()
            else:
                erro_msg = "Por favor, informe os dados do insumo."
    with _col2:
        if _id is not None and st.button("Excluir"):
            db.excluir_insumo(_id)
            st.rerun()

    if erro_msg:
        st.error(erro_msg)

# grid mostrando os insumos
st.markdown("Insumos cadastrados. <small>(selecione um registro para editar)</small>", unsafe_allow_html=True)
df = db.insumos()
grid = st.dataframe(df, use_container_width=True, selection_mode="single-row", on_select='rerun', hide_index=True)
col1, col2 = st.columns([4, 14])
with col1:
    # botão adicionar insumo
    st.button("Adicionar Insumo", type="primary", on_click=detalhes_insumo)
if len(grid.selection['rows']) > 0:
    with col2:
        selected_idx = grid.selection['rows'][0]
        selected_id = int(df.index[selected_idx])
        if st.button("Editar Insumo"):
            detalhes_insumo(selected_id)
