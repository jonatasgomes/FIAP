import streamlit as st
import requests

# Configuration
API_BASE_URL_USUARIOS = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/usuarios/"

# --- Helper Functions ---
def map_ativo_to_display(ativo_api_value):
    """Maps API 'S'/'N' to human-readable 'Sim'/'Não'."""
    if ativo_api_value and ativo_api_value.upper() == 'S':
        return "Sim"
    return "Não"

def map_ativo_to_api(ativo_display_value):
    """Maps human-readable 'Sim'/'Não' to API 'S'/'N'."""
    if ativo_display_value == "Sim":
        return 'S'
    return 'N'

# --- API Interaction Functions ---
def get_all_users_data():
    try:
        response = requests.get(API_BASE_URL_USUARIOS)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados dos usuários: {e}")
        return []
    except ValueError: # Includes JSONDecodeError
        st.error("Erro ao decodificar a resposta JSON da API de usuários.")
        return []

def add_user_data(data):
    headers = {'Content-Type': 'application/json'}
    # Assuming 'data' dict already has lowercase keys as per its construction
    try:
        response = requests.post(API_BASE_URL_USUARIOS, json=data, headers=headers)
        response.raise_for_status()
        st.success("Usuário adicionado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao adicionar usuário: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {data}") # For debugging
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao adicionar usuário: {e}")
    return False

def update_user_data(user_id, data):
    headers = {'Content-Type': 'application/json'}
    try:
        # Ensure keys are lowercase for the API (as in sensores.py)
        # and include the id in the payload as often required by ORDS for PUT.
        payload_for_put = {k.lower(): v for k, v in data.items()}
        payload_for_put['id'] = user_id

        url = f"{API_BASE_URL_USUARIOS}{user_id}"
        response = requests.put(url, json=payload_for_put, headers=headers)

        response.raise_for_status()
        st.success(f"Usuário ID {user_id} atualizado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao atualizar usuário {user_id}: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload_for_put}") # For debugging
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao atualizar usuário {user_id}: {e}")
    return False

def delete_user_data(user_id):
    try:
        url = f"{API_BASE_URL_USUARIOS}{user_id}"
        response = requests.delete(url)
        response.raise_for_status()
        st.success(f"Usuário ID {user_id} deletado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao deletar usuário {user_id}: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao deletar usuário {user_id}: {e}")
    return False

# --- Streamlit UI ---
st.header("Usuários")

# Session state for managing modals/dialogs
if "show_add_user_modal" not in st.session_state:
    st.session_state.show_add_user_modal = False
if "editing_user" not in st.session_state:
    st.session_state.editing_user = None # Stores the user data for editing

# --- Add User "Dialog" ---
if st.button("Novo Usuário", type="primary"):
    st.session_state.show_add_user_modal = True
    st.session_state.editing_user = None # Ensure edit mode is off
    st.rerun()

if st.session_state.show_add_user_modal:
    st.subheader("Adicionar Novo Usuário")
    with st.form("add_user_form", clear_on_submit=True):
        add_usuario = st.text_input("Usuário (login)", key="add_usuario_login")
        add_senha = st.text_input("Senha", type="password", key="add_senha")
        add_nome_completo = st.text_input("Nome Completo", key="add_nome_completo")
        add_email = st.text_input("Email", key="add_email")
        add_ativo_display = st.selectbox("Ativo", ["Sim", "Não"], key="add_ativo", index=0) # Default to "Sim"

        col_save, col_cancel = st.columns(2)
        with col_save:
            submitted_add = st.form_submit_button("Salvar", type="primary", use_container_width=True)
            if submitted_add:
                if not all([add_usuario, add_senha, add_nome_completo, add_email]):
                    st.warning("Todos os campos (Usuário, Senha, Nome Completo, Email) são obrigatórios.")
                else:
                    new_user_data = {
                        "usuario": add_usuario,
                        "senha": add_senha,
                        "nome_completo": add_nome_completo,
                        "email": add_email,
                        "ativo": map_ativo_to_api(add_ativo_display)
                    }
                    if add_user_data(new_user_data):
                        st.session_state.show_add_user_modal = False
                        st.rerun()
        with col_cancel:
            if st.form_submit_button("Cancelar", type="secondary", use_container_width=True):
                st.session_state.show_add_user_modal = False
                st.rerun()

# --- Edit User "Dialog" ---
if st.session_state.editing_user:
    user = st.session_state.editing_user
    user_id_edit = user.get('id', 'N/A') # API response uses lowercase 'id'

    st.subheader(f"Editar Usuário ID: {user_id_edit}")
    with st.form(f"edit_user_form_{user_id_edit}", clear_on_submit=False):
        edit_usuario = st.text_input(
            "Usuário (login)",
            value=user.get("usuario", ""),
            key=f"edit_usuario_login_{user_id_edit}"
        )
        # For security and simplicity, password must be re-entered or changed.
        # It's not pre-filled. Schema states 'senha' is NOT NULL.
        edit_senha = st.text_input(
            "Senha (obrigatório para salvar, insira atual ou nova)",
            type="password",
            key=f"edit_senha_{user_id_edit}"
        )
        edit_nome_completo = st.text_input(
            "Nome Completo",
            value=user.get("nome_completo", ""),
            key=f"edit_nome_completo_{user_id_edit}"
        )
        edit_email = st.text_input(
            "Email",
            value=user.get("email", ""),
            key=f"edit_email_{user_id_edit}"
        )
        
        current_ativo_api = user.get("ativo", 'N') # Default to 'N' if not present in API response
        current_ativo_display = map_ativo_to_display(current_ativo_api)
        ativo_options = ["Sim", "Não"]
        edit_ativo_display = st.selectbox(
            "Ativo", ativo_options,
            index=ativo_options.index(current_ativo_display), # Set index based on current value
            key=f"edit_ativo_{user_id_edit}"
        )

        col_save_edit, col_cancel_edit = st.columns(2)
        with col_save_edit:
            submitted_edit = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
        with col_cancel_edit:
            cancel_pressed_edit = st.form_submit_button("Cancelar Edição", type="secondary", use_container_width=True)

        if submitted_edit:
            if not all([edit_usuario, edit_senha, edit_nome_completo, edit_email]):
                 st.warning("Todos os campos (Usuário, Senha, Nome Completo, Email) são obrigatórios.")
            else:
                updated_user_data = {
                    "usuario": edit_usuario,
                    "senha": edit_senha,
                    "nome_completo": edit_nome_completo,
                    "email": edit_email,
                    "ativo": map_ativo_to_api(edit_ativo_display)
                }
                if update_user_data(user_id_edit, updated_user_data):
                    st.session_state.editing_user = None
                    st.rerun()
        elif cancel_pressed_edit:
            st.session_state.editing_user = None
            st.rerun()


# Only fetch and display data if not in add or edit mode to prevent UI jumps
if not st.session_state.show_add_user_modal and not st.session_state.editing_user:
    users_data = get_all_users_data()

    if not users_data:
        st.info("Nenhum usuário cadastrado.")
    else:
        # Headers
        # Adjusted column widths: ID, Usuário, Nome Completo, Email, Ativo, Ações
        cols_header = st.columns((0.5, 1.5, 2.5, 2.5, 0.8, 1.2)) 
        headers = ["ID", "Usuário", "Nome Completo", "Email", "Ativo", "Ações"]
        for col, header_text in zip(cols_header, headers):
            col.markdown(f"**{header_text}**")


        for user_item in users_data:
            user_id = user_item.get("id", "N/A")
            usuario_login = user_item.get("usuario", "N/A")
            nome_completo = user_item.get("nome_completo", "N/A")
            email = user_item.get("email", "N/A")
            ativo_api = user_item.get("ativo", "N") 
            ativo_display = map_ativo_to_display(ativo_api)

            # Data row columns
            cols_data = st.columns((0.5, 1.5, 2.5, 2.5, 0.8, 1.2))
            cols_data[0].write(str(user_id)[:6] + "..." if len(str(user_id)) > 6 else str(user_id))
            cols_data[1].write(usuario_login)
            cols_data[2].write(nome_completo)
            cols_data[3].write(email)
            cols_data[4].write(ativo_display)

            # Action buttons in the last column
            actions_col = cols_data[5]
            button_col_edit, button_col_delete = actions_col.columns(2)

            if button_col_edit.button("✏️", key=f"edit_user_{user_id}", help="Editar este usuário"):
                st.session_state.editing_user = user_item
                st.session_state.show_add_user_modal = False
                st.rerun()
            
            if button_col_delete.button("🗑️", key=f"delete_user_{user_id}", help="Deletar este usuário"):
                if delete_user_data(user_id):
                    st.rerun()
