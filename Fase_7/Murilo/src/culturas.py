import streamlit as st
import requests
import json # For q parameter in get_insumos_for_cultura

# Configuration
API_BASE_URL_CULTURAS = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/culturas_insumos/"
API_BASE_URL_INSUMOS = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/insumos/"

# --- API Interaction Functions for Culturas ---
def get_all_culturas_data():
    try:
        response = requests.get(API_BASE_URL_CULTURAS)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados das culturas: {e}")
        return []
    except ValueError:
        st.error("Erro ao decodificar a resposta JSON da API de culturas.")
        return []

def add_cultura_data(data):
    headers = {'Content-Type': 'application/json'}
    payload = {k.lower(): v for k, v in data.items()} # Ensure keys are lowercase
    try:
        response = requests.post(API_BASE_URL_CULTURAS, json=payload, headers=headers)
        response.raise_for_status()
        st.success("Cultura adicionada com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao adicionar cultura: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao adicionar cultura: {e}")
    return False

def update_cultura_data(cultura_id, data):
    headers = {'Content-Type': 'application/json'}
    payload_for_put = {k.lower(): v for k, v in data.items()}
    payload_for_put['id'] = cultura_id # ORDS often requires ID in payload for PUT
    try:
        url = f"{API_BASE_URL_CULTURAS}{cultura_id}"
        response = requests.put(url, json=payload_for_put, headers=headers)
        response.raise_for_status()
        st.success(f"Cultura ID {cultura_id} atualizada com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao atualizar cultura {cultura_id}: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload_for_put}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao atualizar cultura {cultura_id}: {e}")
    return False

def delete_cultura_data(cultura_id):
    try:
        url = f"{API_BASE_URL_CULTURAS}{cultura_id}"
        response = requests.delete(url)
        response.raise_for_status()
        st.success(f"Cultura ID {cultura_id} deletada com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao deletar cultura {cultura_id}: {e.response.status_code} - {e.response.text}")
        # Check if error is due to FK constraint (e.g., ORA-02292)
        if "ORA-02292" in e.response.text:
            st.warning("Não é possível deletar esta cultura pois ela possui insumos associados. Remova os insumos primeiro.")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao deletar cultura {cultura_id}: {e}")
    return False

# --- API Interaction Functions for Insumos ---
def get_insumos_for_cultura(cultura_id_fk):
    try:
        query_filter = json.dumps({"cultura_id": int(cultura_id_fk)})
        params = {'q': query_filter}
        
        response = requests.get(API_BASE_URL_INSUMOS, params=params)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar insumos para cultura ID {cultura_id_fk}: {e}")
        return []
    except (ValueError, TypeError) as e: # Catches JSONDecodeError or int conversion error
        st.error(f"Erro ao processar dados para buscar insumos (Cultura ID {cultura_id_fk}): {e}")
        return []

def add_insumo_data(data):
    headers = {'Content-Type': 'application/json'}
    payload = {k.lower(): v for k, v in data.items()}
    try:
        # Ensure numeric fields are correctly typed
        payload['cultura_id'] = int(payload['cultura_id'])
        payload['qtde_ha'] = float(payload['qtde_ha'])

        response = requests.post(API_BASE_URL_INSUMOS, json=payload, headers=headers)
        response.raise_for_status()
        st.success("Insumo adicionado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao adicionar insumo: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao adicionar insumo: {e}")
    except (ValueError, TypeError) as e:
        st.error(f"Erro ao converter dados do insumo para o formato numérico correto: {e}")
    return False

def update_insumo_data(insumo_id, data):
    headers = {'Content-Type': 'application/json'}
    payload_for_put = {k.lower(): v for k, v in data.items()}
    payload_for_put['id'] = insumo_id
    try:
        # Ensure numeric fields are correctly typed
        payload_for_put['cultura_id'] = int(payload_for_put['cultura_id'])
        payload_for_put['qtde_ha'] = float(payload_for_put['qtde_ha'])
        
        url = f"{API_BASE_URL_INSUMOS}{insumo_id}"
        response = requests.put(url, json=payload_for_put, headers=headers)
        response.raise_for_status()
        st.success(f"Insumo ID {insumo_id} atualizado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao atualizar insumo {insumo_id}: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload_for_put}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao atualizar insumo {insumo_id}: {e}")
    except (ValueError, TypeError) as e:
        st.error(f"Erro ao converter dados do insumo para o formato numérico correto: {e}")
    return False

def delete_insumo_data(insumo_id):
    try:
        url = f"{API_BASE_URL_INSUMOS}{insumo_id}"
        response = requests.delete(url)
        response.raise_for_status()
        st.success(f"Insumo ID {insumo_id} deletado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao deletar insumo {insumo_id}: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao deletar insumo {insumo_id}: {e}")
    return False

# --- Streamlit UI ---
st.header("Culturas")

# Initialize session state variables
if "show_add_cultura_form" not in st.session_state:
    st.session_state.show_add_cultura_form = False
if "editing_cultura_obj" not in st.session_state:
    st.session_state.editing_cultura_obj = None
if "manage_insumos_for_cultura_obj" not in st.session_state:
    st.session_state.manage_insumos_for_cultura_obj = None
if "show_add_insumo_form" not in st.session_state:
    st.session_state.show_add_insumo_form = False
if "editing_insumo_obj" not in st.session_state:
    st.session_state.editing_insumo_obj = None

# --- Add Cultura Form ---
if st.button("Nova Cultura", type="primary", key="btn_nova_cultura"):
    st.session_state.show_add_cultura_form = True
    st.session_state.editing_cultura_obj = None
    st.session_state.manage_insumos_for_cultura_obj = None
    st.session_state.show_add_insumo_form = False # Reset insumo states
    st.session_state.editing_insumo_obj = None
    st.rerun()

if st.session_state.show_add_cultura_form:
    st.subheader("Adicionar Nova Cultura")
    with st.form("add_cultura_form", clear_on_submit=True):
        nome = st.text_input("Nome da Cultura", key="add_cult_nome")
        clima_ideal = st.text_area("Clima Ideal", key="add_cult_clima")
        solo_ideal = st.text_area("Solo Ideal", key="add_cult_solo")
        duracao_plantio = st.text_input("Duração do Plantio (ex: 90 dias)", key="add_cult_duracao")

        col_s, col_c = st.columns(2)
        submitted_add_cult = col_s.form_submit_button("Salvar Cultura", type="primary", use_container_width=True)
        cancelled_add_cult = col_c.form_submit_button("Cancelar", type="secondary", use_container_width=True)

        if submitted_add_cult:
            if nome and clima_ideal and solo_ideal and duracao_plantio:
                if add_cultura_data({"nome": nome, "clima_ideal": clima_ideal, "solo_ideal": solo_ideal, "duracao_plantio": duracao_plantio}):
                    st.session_state.show_add_cultura_form = False
                    st.rerun()
            else:
                st.warning("Todos os campos da cultura são obrigatórios.")
        if cancelled_add_cult:
            st.session_state.show_add_cultura_form = False
            st.rerun()

# --- Edit Cultura Form ---
if st.session_state.editing_cultura_obj:
    cultura = st.session_state.editing_cultura_obj
    cult_id = cultura.get("id")
    st.subheader(f"Editar Cultura: {cultura.get('nome', '')} (ID: {cult_id})")
    with st.form(f"edit_cultura_form_{cult_id}", clear_on_submit=False):
        nome = st.text_input("Nome", value=cultura.get("nome", ""), key=f"ed_c_n_{cult_id}")
        clima = st.text_area("Clima Ideal", value=cultura.get("clima_ideal", ""), key=f"ed_c_cl_{cult_id}")
        solo = st.text_area("Solo Ideal", value=cultura.get("solo_ideal", ""), key=f"ed_c_sl_{cult_id}")
        duracao = st.text_input("Duração Plantio", value=cultura.get("duracao_plantio", ""), key=f"ed_c_dr_{cult_id}")
        
        col_s, col_c = st.columns(2)
        submitted_edit_cult = col_s.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
        cancelled_edit_cult = col_c.form_submit_button("Cancelar Edição", type="secondary", use_container_width=True)

        if submitted_edit_cult:
            if nome and clima and solo and duracao:
                if update_cultura_data(cult_id, {"nome": nome, "clima_ideal": clima, "solo_ideal": solo, "duracao_plantio": duracao}):
                    st.session_state.editing_cultura_obj = None
                    st.rerun()
            else:
                st.warning("Todos os campos da cultura são obrigatórios.")
        if cancelled_edit_cult:
            st.session_state.editing_cultura_obj = None
            st.rerun()

# --- Main Display Area (Culturas List or Insumos Management) ---
if not st.session_state.show_add_cultura_form and not st.session_state.editing_cultura_obj:

    # --- Insumos Management Section ---
    if st.session_state.manage_insumos_for_cultura_obj:
        cult_for_ins = st.session_state.manage_insumos_for_cultura_obj
        cult_id_for_ins = cult_for_ins.get("id")
        st.subheader(f"Gerenciando Insumos para Cultura: {cult_for_ins.get('nome')} (ID: {cult_id_for_ins})")

        if st.button("⬅️ Voltar para Lista de Culturas", key="back_to_cult_list"):
            st.session_state.manage_insumos_for_cultura_obj = None
            st.session_state.show_add_insumo_form = False
            st.session_state.editing_insumo_obj = None
            st.rerun()
        st.markdown("---")

        # Add Insumo Button
        if st.button("Adicionar Novo Insumo", type="secondary", key=f"add_ins_btn_{cult_id_for_ins}"):
            st.session_state.show_add_insumo_form = True
            st.session_state.editing_insumo_obj = None 
            st.rerun()

        # Add Insumo Form
        if st.session_state.show_add_insumo_form:
            st.markdown("##### Cadastrar Novo Insumo")
            with st.form(f"add_insumo_f_{cult_id_for_ins}", clear_on_submit=True):
                ins_nome = st.text_input("Nome do Insumo", key=f"add_i_n_{cult_id_for_ins}")
                ins_qtde = st.number_input("Qtde/ha", min_value=0.0, format="%.2f", key=f"add_i_q_{cult_id_for_ins}")
                ins_info = st.text_area("Outras Informações", key=f"add_i_o_{cult_id_for_ins}")

                col_si, col_ci = st.columns(2)
                sub_add_ins = col_si.form_submit_button("Salvar Insumo", type="primary", use_container_width=True)
                can_add_ins = col_ci.form_submit_button("Cancelar", type="secondary", use_container_width=True)

                if sub_add_ins:
                    if ins_nome and ins_qtde is not None:
                        if add_insumo_data({"cultura_id": cult_id_for_ins, "nome": ins_nome, "qtde_ha": ins_qtde, "outras_info": ins_info}):
                            st.session_state.show_add_insumo_form = False
                            st.rerun()
                    else:
                        st.warning("Nome e Quantidade por Hectare do insumo são obrigatórios.")
                if can_add_ins:
                    st.session_state.show_add_insumo_form = False
                    st.rerun()
        
        # Edit Insumo Form
        if st.session_state.editing_insumo_obj:
            ins_to_edit = st.session_state.editing_insumo_obj
            ins_id = ins_to_edit.get("id")
            st.markdown(f"##### Editando Insumo: {ins_to_edit.get('nome', '')} (ID: {ins_id})")
            with st.form(f"edit_insumo_f_{ins_id}", clear_on_submit=False):
                ed_ins_n = st.text_input("Nome", value=ins_to_edit.get("nome", ""), key=f"ed_i_n_{ins_id}")
                ed_ins_q = st.number_input("Qtde/ha", value=float(ins_to_edit.get("qtde_ha",0.0)), min_value=0.0, format="%.2f", key=f"ed_i_q_{ins_id}")
                ed_ins_o = st.text_area("Outras Informações", value=ins_to_edit.get("outras_info", ""), key=f"ed_i_o_{ins_id}")

                col_sei, col_cei = st.columns(2)
                sub_edit_ins = col_sei.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
                can_edit_ins = col_cei.form_submit_button("Cancelar Edição", type="secondary", use_container_width=True)

                if sub_edit_ins:
                    if ed_ins_n and ed_ins_q is not None:
                        if update_insumo_data(ins_id, {"cultura_id": cult_id_for_ins, "nome": ed_ins_n, "qtde_ha": ed_ins_q, "outras_info": ed_ins_o}):
                            st.session_state.editing_insumo_obj = None
                            st.rerun()
                    else:
                        st.warning("Nome e Quantidade por Hectare do insumo são obrigatórios.")
                if can_edit_ins:
                    st.session_state.editing_insumo_obj = None
                    st.rerun()

        # Display Insumos List (if not adding/editing an insumo)
        if not st.session_state.show_add_insumo_form and not st.session_state.editing_insumo_obj:
            st.markdown("##### Insumos Cadastrados para esta Cultura")
            insumos = get_insumos_for_cultura(cult_id_for_ins)
            if not insumos:
                st.info("Nenhum insumo cadastrado.")
            else:
                h_cols = st.columns((2, 1, 2, 1.5)) # Nome, Qtde/ha, Outras Infos, Ações
                headers_ins = ["Nome", "Qtde/ha", "Outras Informações", "Ações"]
                for h_col, h_txt in zip(h_cols, headers_ins):
                    h_col.markdown(f"**{h_txt}**")

                for ins in insumos:
                    i_id = ins.get("id")
                    d_cols = st.columns((2, 1, 2, 1.5))
                    d_cols[0].write(ins.get("nome", "N/A"))
                    d_cols[1].write(str(ins.get("qtde_ha", "N/A")))
                    d_cols[2].write(ins.get("outras_info", "N/A"))
                    
                    act_i_col = d_cols[3]
                    b_ei, b_di = act_i_col.columns(2)
                    if b_ei.button("✏️", key=f"ed_i_{i_id}", help="Editar Insumo"):
                        st.session_state.editing_insumo_obj = ins
                        st.session_state.show_add_insumo_form = False
                        st.rerun()
                    if b_di.button("🗑️", key=f"del_i_{i_id}", help="Deletar Insumo"):
                        if delete_insumo_data(i_id):
                            st.rerun()

    # --- Culturas List Display ---
    else:
        st.subheader("Lista de Culturas Cadastradas")
        culturas = get_all_culturas_data()
        if not culturas:
            st.info("Nenhuma cultura cadastrada.")
        else:
            # Headers: ID, Nome, Clima, Solo, Duração, Ações
            h_cult_cols = st.columns((0.5, 1.5, 1.5, 1.5, 1, 2.5))
            h_cult_txt = ["ID", "Nome", "Clima", "Solo", "Plantio", "Ações"]
            for hc_col, hc_txt in zip(h_cult_cols, h_cult_txt):
                hc_col.markdown(f"**{hc_txt}**")

            for cult in culturas:
                c_id = cult.get("id")
                d_cult_cols = st.columns((0.5, 1.5, 1.5, 1.5, 1, 2.5))
                d_cult_cols[0].write(str(c_id))
                d_cult_cols[1].write(cult.get("nome", "N/A"))
                d_cult_cols[2].write(cult.get("clima_ideal", "N/A"))
                d_cult_cols[3].write(cult.get("solo_ideal", "N/A"))
                d_cult_cols[4].write(cult.get("duracao_plantio", "N/A"))

                act_c_col = d_cult_cols[5]
                b_ec, b_dc, b_ic = act_c_col.columns([1,1,2])

                if b_ec.button("✏️", key=f"ed_c_{c_id}", help="Editar Cultura"):
                    st.session_state.editing_cultura_obj = cult
                    st.session_state.manage_insumos_for_cultura_obj = None # Close insumos view
                    st.rerun()
                if b_dc.button("🗑️", key=f"del_c_{c_id}", help="Deletar Cultura"):
                    if delete_cultura_data(c_id):
                        st.rerun()
                if b_ic.button("🌱 Insumos", key=f"mng_ins_{c_id}", help="Gerenciar Insumos"):
                    st.session_state.manage_insumos_for_cultura_obj = cult
                    st.session_state.show_add_insumo_form = False # Reset insumo forms
                    st.session_state.editing_insumo_obj = None
                    st.rerun()
