import streamlit as st
import database as db

# adicionar cultura em janela modal
@st.dialog("Detalhes da Cultura")
def detalhes_cultura(_id=None):
    _cultura = ""
    if _id is not None:
        cultura = db.cultura(_id)
        if cultura is not None:
            _cultura = cultura[0][1]

    _cultura = st.text_input("Cultura", value=_cultura)
    erro_msg = None
    _col1, _col2 = st.columns([2, 9])
    with _col1:
        if st.button("Salvar", type="primary"):
            if _cultura:
                db.salvar_cultura(_id, _cultura)
                st.rerun()
            else:
                erro_msg = "Por favor, informe a cultura."
    with _col2:
        if _id is not None and st.button("Excluir"):
            db.excluir_cultura(_id)
            st.rerun()

    if erro_msg:
        st.error(erro_msg)

# grid mostrando as culturas
st.markdown("Com quais culturas você deseja trabalhar? <small>(selecione um registro para editar)</small>", unsafe_allow_html=True)
df = db.culturas()
grid = st.dataframe(df, use_container_width=True, selection_mode="single-row", on_select='rerun', hide_index=True)
col1, col2 = st.columns([4, 14])
with col1:
    # botão adicionar cultura
    st.button("Adicionar Cultura", type="primary", on_click=detalhes_cultura)
if len(grid.selection['rows']) > 0:
    # botão editar cultura
    with col2:
        selected_idx = grid.selection['rows'][0]
        selected_id = int(df.index[selected_idx])
        if st.button("Editar Cultura"):
            detalhes_cultura(selected_id)
