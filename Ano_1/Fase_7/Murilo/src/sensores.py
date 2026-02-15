import streamlit as st
import requests
from datetime import datetime, date, time

# Configuration
API_BASE_URL = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/sensores/"

# --- Helper Functions ---
def format_api_timestamp(dt_object):
    """Formats a datetime object to ISO 8601 string for the API (assuming UTC)."""
    if dt_object:
        return dt_object.isoformat() + "Z"
    return None

def parse_api_timestamp(timestamp_str):
    """Parses ISO 8601 string from API to datetime object."""
    if timestamp_str:
        try:
            # Handle timestamps with or without milliseconds and 'Z'
            if '.' in timestamp_str:
                 timestamp_str = timestamp_str.split('.')[0] # Remove fractional seconds
            if timestamp_str.endswith("Z"):
                timestamp_str = timestamp_str[:-1] # Remove 'Z'
            dt_obj = datetime.fromisoformat(timestamp_str)
            return dt_obj
        except ValueError:
            st.error(f"Erro ao parsear timestamp: {timestamp_str}")
            return None
    return None

def display_timestamp(dt_object):
    """Formats datetime object for display."""
    if dt_object:
        return dt_object.strftime("%d/%m/%Y %H:%M")
    return "N/A"

def map_irrigation_to_bool_display(value):
    return "Ligada" if value == 1 else "Desligada"

def map_irrigation_to_int(value_str):
    return 1 if value_str == "Ligada" else 0

# --- API Interaction Functions ---
def get_all_sensors_data():
    try:
        response = requests.get(API_BASE_URL)
        response.raise_for_status()
        return response.json().get("items", [])
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados dos sensores: {e}")
        return []
    except ValueError: # Includes JSONDecodeError
        st.error("Erro ao decodificar a resposta JSON da API.")
        return []


def add_sensor_data(data):
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(API_BASE_URL, json=data, headers=headers)
        response.raise_for_status()
        st.success("Sensor adicionado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao adicionar sensor: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao adicionar sensor: {e}")
    return False

def update_sensor_data(sensor_id, data):
    headers = {'Content-Type': 'application/json'}
    try:
        payload_for_put = {k.lower(): v for k, v in data.items()}
        # ORDS often requires the ID in the payload for PUT to specific item endpoint
        payload_for_put['sensor_id'] = sensor_id

        url = f"{API_BASE_URL}{sensor_id}"
        response = requests.put(url, json=payload_for_put, headers=headers)

        response.raise_for_status()
        st.success(f"Sensor ID {sensor_id} atualizado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao atualizar sensor {sensor_id}: {e.response.status_code} - {e.response.text}")
        st.error(f"Payload enviado: {payload_for_put}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao atualizar sensor {sensor_id}: {e}")
    return False

def delete_sensor_data(sensor_id):
    try:
        url = f"{API_BASE_URL}{sensor_id}"
        response = requests.delete(url)
        response.raise_for_status()
        st.success(f"Sensor ID {sensor_id} deletado com sucesso!")
        return True
    except requests.exceptions.HTTPError as e:
        st.error(f"Erro HTTP ao deletar sensor {sensor_id}: {e.response.status_code} - {e.response.text}")
    except requests.exceptions.RequestException as e:
        st.error(f"Erro de requisição ao deletar sensor {sensor_id}: {e}")
    return False

# --- Streamlit UI ---
st.header("Sensores")

# Session state for managing modals/dialogs
if "show_add_modal" not in st.session_state:
    st.session_state.show_add_modal = False
if "editing_sensor" not in st.session_state:
    st.session_state.editing_sensor = None # Stores the sensor data for editing

# --- Add Sensor "Dialog" ---
if st.button("Novo Registro", type="primary"):
    st.session_state.show_add_modal = True
    st.session_state.editing_sensor = None # Ensure edit mode is off
    st.rerun() # Rerun to show the form below

if st.session_state.show_add_modal:
    st.subheader("Dados do Registro")
    with st.form("add_sensor_form", clear_on_submit=True):
        add_timestamp_date = st.date_input("Data", value=date.today(), key="add_date")
        add_timestamp_time = st.time_input("Hora", value=datetime.now().time(), key="add_time")
        add_humidity = st.number_input("Umidade (%)", min_value=0.0, max_value=100.0, step=0.1, format="%.1f", key="add_hum")
        add_temperature = st.number_input("Temperatura (°C)", step=0.1, format="%.1f", key="add_temp")
        add_ph = st.number_input("pH", min_value=0.0, max_value=14.0, step=0.1, format="%.1f", key="add_ph")
        add_phosphorus = st.text_input("Fósforo", key="add_phos")
        add_potassium = st.text_input("Potássio", key="add_pot")
        add_irrigation_on_str = st.selectbox("Irrigação", ["Desligada", "Ligada"], key="add_irr")

        col_save, col_cancel = st.columns(2)
        with col_save:
            submitted = st.form_submit_button("Salvar", type="primary", use_container_width=True)
            if submitted:
                combined_datetime = datetime.combine(add_timestamp_date, add_timestamp_time)
                new_sensor_data = {
                    "timestamp": format_api_timestamp(combined_datetime),
                    "humidity": add_humidity,
                    "temperature": add_temperature,
                    "ph": add_ph,
                    "phosphorus": add_phosphorus,
                    "potassium": add_potassium,
                    "irrigationon": map_irrigation_to_int(add_irrigation_on_str)
                }
                if add_sensor_data(new_sensor_data):
                    st.session_state.show_add_modal = False
                    st.rerun()
                else:
                    st.error("Falha ao adicionar sensor. Verifique os logs.")
        with col_cancel:
            if st.form_submit_button("Cancelar", type="secondary", use_container_width=True):
                st.session_state.show_add_modal = False
                st.rerun()


# --- Edit Sensor "Dialog" ---
if st.session_state.editing_sensor:
    sensor = st.session_state.editing_sensor
    parsed_dt = parse_api_timestamp(sensor.get("timestamp"))
    sensor_id_edit = sensor.get('sensor_id', 'N/A')

    st.subheader(f"Editar Sensor ID: {sensor_id_edit}")
    with st.form(f"edit_sensor_form_{sensor_id_edit}", clear_on_submit=False): # clear_on_submit=False to keep values if update fails
        edit_timestamp_date = st.date_input(
            "Data",
            value=parsed_dt.date() if parsed_dt else date.today(),
            key=f"edit_date_{sensor_id_edit}"
        )
        edit_timestamp_time = st.time_input(
            "Hora",
            value=parsed_dt.time() if parsed_dt else datetime.now().time(),
            key=f"edit_time_{sensor_id_edit}"
        )
        edit_humidity = st.number_input(
            "Umidade (%)",
            min_value=0.0, max_value=100.0, step=0.1, format="%.1f",
            value=float(sensor.get("humidity", 0.0) or 0.0),
            key=f"edit_hum_{sensor_id_edit}"
        )
        edit_temperature = st.number_input(
            "Temperatura (°C)", step=0.1, format="%.1f",
            value=float(sensor.get("temperature", 0.0) or 0.0),
            key=f"edit_temp_{sensor_id_edit}"
        )
        edit_ph = st.number_input(
            "pH", min_value=0.0, max_value=14.0, step=0.1, format="%.1f",
            value=float(sensor.get("ph", 7.0) or 7.0),
            key=f"edit_ph_{sensor_id_edit}"
        )
        edit_phosphorus = st.text_input(
            "Fósforo",
            value=sensor.get("phosphorus", ""),
            key=f"edit_phos_{sensor_id_edit}"
        )
        edit_potassium = st.text_input(
            "Potássio",
            value=sensor.get("potassium", ""),
            key=f"edit_pot_{sensor_id_edit}"
        )
        current_irrigation_status = map_irrigation_to_bool_display(sensor.get("irrigationon", 0))
        edit_irrigation_on_str = st.selectbox(
            "Irrigação", ["Desligada", "Ligada"],
            index=1 if current_irrigation_status == "Ligada" else 0,
            key=f"edit_irr_{sensor_id_edit}"
        )

        col_save, col_cancel_edit = st.columns(2)
        with col_save:
            submitted = st.form_submit_button("Salvar Alterações", type="primary", use_container_width=True)
        with col_cancel_edit:
            # The cancel button inside the form will also submit it.
            # A true cancel needs to be outside or handle differently.
            # For simplicity, let's make it part of the form for now.
            # If "Cancelar Edição" is clicked, we'll check its value.
            cancel_pressed = st.form_submit_button("Cancelar", type="secondary", use_container_width=True)


        if submitted: # "Salvar Alterações" was pressed
            combined_datetime = datetime.combine(edit_timestamp_date, edit_timestamp_time)
            updated_sensor_data = {
                "timestamp": format_api_timestamp(combined_datetime),
                "humidity": edit_humidity,
                "temperature": edit_temperature,
                "ph": edit_ph,
                "phosphorus": edit_phosphorus,
                "potassium": edit_potassium,
                "irrigationon": map_irrigation_to_int(edit_irrigation_on_str)
            }
            if update_sensor_data(sensor_id_edit, updated_sensor_data):
                st.session_state.editing_sensor = None
                st.rerun()
            else:
                st.error("Falha ao atualizar sensor. Verifique os logs.")
                # Do not clear form, allow user to retry or cancel
        elif cancel_pressed: # "Cancelar Edição" was pressed
            st.session_state.editing_sensor = None
            st.rerun()


# Only fetch and display data if not in add or edit mode to prevent UI jumps
if not st.session_state.show_add_modal and not st.session_state.editing_sensor:

    sensors_data = get_all_sensors_data()

    if not sensors_data:
        st.info("Nenhum dado de sensor encontrado.")
    else:
        # Headers - matching the wireframe
        cols = st.columns((0.5, 2, 1, 1, 0.8, 1.2, 1.2, 1, 1.5)) # Adjusted for actions
        headers = ["ID", "Timestamp", "Umidade", "Temp.", "Ph", "Fósforo", "Potássio", "Irrigação", "Ações"]
        for col, header_text in zip(cols, headers):
            col.markdown(f"**{header_text}**")

        for sensor in sensors_data:
            sensor_id = sensor.get("sensor_id", "N/A")
            dt_obj = parse_api_timestamp(sensor.get("timestamp"))
            timestamp_display = display_timestamp(dt_obj)
            humidity = f'{sensor.get("humidity", "N/A")}%' if sensor.get("humidity") is not None else "N/A"
            temperature = f'{sensor.get("temperature", "N/A")}°C' if sensor.get("temperature") is not None else "N/A"
            ph = sensor.get("ph", "N/A")
            phosphorus = sensor.get("phosphorus", "N/A")
            potassium = sensor.get("potassium", "N/A")
            irrigation = map_irrigation_to_bool_display(sensor.get("irrigationon", 0))

            data_cols = st.columns((0.5, 2, 1, 1, 0.8, 1.2, 1.2, 1, 1.5))
            data_cols[0].write(str(sensor_id)[:6] + "..." if len(str(sensor_id)) > 6 else sensor_id) # Shorten ID if too long
            data_cols[1].write(timestamp_display)
            data_cols[2].write(humidity)
            data_cols[3].write(temperature)
            data_cols[4].write(ph)
            data_cols[5].write(phosphorus)
            data_cols[6].write(potassium)
            data_cols[7].write(irrigation)

            button_col_edit, button_col_delete = data_cols[8].columns(2)

            if button_col_edit.button("✏️", key=f"edit_{sensor_id}", help="Editar este sensor"):
                st.session_state.editing_sensor = sensor
                st.session_state.show_add_modal = False # Ensure add mode is off
                st.rerun()
            if button_col_delete.button("🗑️", key=f"delete_{sensor_id}", help="Deletar este sensor"):
                if delete_sensor_data(sensor_id):
                    st.rerun()
                else:
                    st.error(f"Falha ao deletar sensor ID {sensor_id}")
