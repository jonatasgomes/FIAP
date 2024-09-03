import streamlit as st
import database as db
import time

def limpar_sessao():
    st.session_state.pop('novo_insumo')

# Adicionar Insumo em janela modal
@st.dialog("Detalhes do Insumo")
def novo_insumo():
    culturas = db.culturas()
    cols = st.columns(3)
    with cols[0]:
        id_cultura = st.selectbox("Cultura", culturas, index=0, placeholder="Selecione...", format_func=lambda x: x[1])[0]
    with cols[1]:
        ruas = st.number_input("Total de Ruas", min_value=1, step=1)
    with cols[2]:
        comprimento = st.number_input("Comprimento (m)", min_value=1, step=1)
    cols = st.columns(3)
    with cols[0]:
        produto = st.selectbox("Insumo", ["Nitrogênio", "Fósforo", "Potássio", "Calcárioo", "Herbicidas", "Fungicidas", "Inseticidas"], index=0, placeholder="Selecione...")
    with cols[1]:
        unidade = st.selectbox("Unidade", ["L", "Kg"], index=0, placeholder="Selecione...")
    with cols[2]:
        dosagem = st.number_input(f'Qtde p/ metro ({unidade})', min_value=0.5, step=0.5)
    total = dosagem * comprimento * ruas
    st.metric(f"Total de {produto}", f"{total:.2f}{unidade}")
    if st.button("Salvar", type="primary"):
        st.session_state.novo_insumo = {"id_cultura": id_cultura, "ruas": ruas, "comprimento": comprimento, "produto": produto, "unidade": unidade, "dosagem": dosagem, "total": total}
        st.rerun()

# botão adicionar insumo
st.button("Adicionar Insumo", type="primary", on_click=novo_insumo)
if "novo_insumo" in st.session_state:
    db.salvar_insumo(
        st.session_state.novo_insumo["id_cultura"],
        st.session_state.novo_insumo["produto"],
        st.session_state.novo_insumo["dosagem"],
        st.session_state.novo_insumo["unidade"],
        st.session_state.novo_insumo["ruas"],
        st.session_state.novo_insumo["comprimento"],
        st.session_state.novo_insumo["total"]
    )
    st.success("Insumo adicionado com sucesso!")
    limpar_sessao()

# grid mostrandos os insumos
df = db.insumos()
grid = st.dataframe(df, use_container_width=True, selection_mode="single-row", on_select='rerun')
if len(grid.selection['rows']) > 0:
    selected_idx = grid.selection['rows'][0]
    selected_id = int(df.index[selected_idx])
    if st.button("Excluir Insumo Selecionado"):
        db.excluir_insumo(selected_id)
        st.success(f"Insumo excluído com sucesso! {selected_id}")
        time.sleep(1)
        st.rerun()
