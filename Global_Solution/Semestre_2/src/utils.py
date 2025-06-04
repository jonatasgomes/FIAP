import requests
import datetime
import streamlit as st

API_NIVEL_AGUA = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/nivel_agua/"
API_VOLUME_CHUVA = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/volume_chuva/"
API_SALVAR_LEITURA = "https://g12bbd4aea16cc4-orcl1.adb.ca-toronto-1.oraclecloudapps.com/ords/fiap/leituras/"
API_DISPARAR_SMS = "https://ijld8gsll8.execute-api.us-east-1.amazonaws.com/v1/alertaEnchente"

def buscar_nivel_rio():
    try:
        response = requests.get(API_NIVEL_AGUA, timeout=5)
        response.raise_for_status()
        data = response.json() # {'data_leitura': 'YYYY-MM-DDTHH:MM:SS', 'valor': X.Y}
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados do nível do rio: {e}")
        return None
    except ValueError:
        st.error("Erro ao decodificar resposta JSON (buscar_nivel_rio)")
        return None

def buscar_volume_chuva():
    try:
        response = requests.get(API_VOLUME_CHUVA, timeout=5)
        response.raise_for_status()
        data = response.json()  # {'data_leitura': 'YYYY-MM-DDTHH:MM:SS', 'valor': X.Y}
        return data
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao buscar dados do volume de chuva: {e}")
        return None
    except ValueError:
        st.error("Erro ao decodificar resposta JSON (buscar_volume_chuva)")
        return None

def salvar_leitura(sensor, valor):
    payload = {
        "data_leitura": datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000Z"),
        "sensor": sensor,
        "valor": valor
    }
    try:
        response = requests.post(API_SALVAR_LEITURA, json=payload, timeout=10)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao salvar volume de chuva: {e}")
        return False

def enviar_alerta_sms(message: str):
    payload = {"message": message, "phone_numbers": ["+17782282166", "+5511938006662"]}
    try:
        response = requests.post(API_DISPARAR_SMS, json=payload, timeout=10)
        response.raise_for_status()
        st.success(f"Alerta SMS enviado com sucesso! Status: {response.status_code}")
        return True
    except requests.exceptions.RequestException as e:
        st.error(f"Erro ao enviar SMS: {e}")
        return False

def risco_enchente(nivel_atual, nivel_esperado, predicao_com_chuva, limite_moderado, limite_grave):
    # Quão acima do esperado começa a ser preocupante
    diferenca_moderado_esperado = 0.5
    diferenca_grave_esperado = 1.0

    risco = "Mínimo"
    detalhes = []

    # Avaliação baseada no nível atual e previsto
    if predicao_com_chuva >= limite_grave or nivel_atual >= limite_grave:
        risco = "Grave"
        detalhes.append(f"Nível previsto ({predicao_com_chuva:.2f}m) ou atual ({nivel_atual:.2f}m) excede o limiar grave ({limite_grave:.2f}m).")
    elif predicao_com_chuva >= limite_moderado or nivel_atual >= limite_moderado:
        risco = "Moderado"
        detalhes.append(f"Nível previsto ({predicao_com_chuva:.2f}m) ou atual ({nivel_atual:.2f}m) excede o limiar moderado ({limite_moderado:.2f}m).")

    # Avaliação baseada na diferença em relação ao nível esperado
    diferenca_atual_esperado = nivel_atual - nivel_esperado
    diferenca_predicao_esperado = predicao_com_chuva - nivel_esperado

    if diferenca_predicao_esperado >= diferenca_grave_esperado or diferenca_atual_esperado >= diferenca_grave_esperado :
        if risco != "Grave":
             risco = "Grave"
        detalhes.append(f"Nível previsto ({predicao_com_chuva:.2f}m) ou atual ({nivel_atual:.2f}m) está significativamente acima do esperado ({nivel_esperado:.2f}m).")
    elif (diferenca_predicao_esperado >= diferenca_moderado_esperado or diferenca_atual_esperado >= diferenca_moderado_esperado) and risco == "Mínimo":
        risco = "Moderado"
        detalhes.append(f"Nível previsto ({predicao_com_chuva:.2f}m) ou atual ({nivel_atual:.2f}m) está acima do esperado ({nivel_esperado:.2f}m).")

    # Se o nível atual já é alto e a previsão de chuva vai piorar muito
    if nivel_atual >= (limite_moderado * 0.8) and (predicao_com_chuva - nivel_atual) > 0.5:
         if risco == "Mínimo": risco = "Moderado"
         detalhes.append(f"Previsão de aumento considerável ({predicao_com_chuva - nivel_atual:.2f}m) a partir de um nível já elevado.")

    color_map = {"Mínimo": "green", "Moderado": "orange", "Grave": "red"}
    return risco, color_map.get(risco, "grey"), ", ".join(detalhes)
