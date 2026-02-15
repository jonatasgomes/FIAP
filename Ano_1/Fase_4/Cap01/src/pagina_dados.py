import streamlit as st
import json
from db import OracleDatabase
from datetime import datetime

# Instância do banco de dados (a configuração já está no db.py)
db = OracleDatabase()

# Exibe a grid de dados com um spinner
st.title("Entrada de Dados")
with st.spinner("Carregando dados..."):
    df = db.carregar_leituras()
    df.set_index('Leitura', inplace=True)
if df is not None:
    st.write("Leituras Salvas")
    dados_grid = st.dataframe(df, hide_index=True, use_container_width=True)
else:
    st.write("Erro ao obter dados.")

# Exemplo de JSON esperado
exemplo_json = """{"data_hora": "2024-11-12 13:50:30", "potassio": "100", "fosforo": "0", "umidade": "120", "ph": "7"}"""

# Formulário para inserção de dados com JSON
st.subheader("Inserir nova leitura via JSON")
json_input = st.text_area("Cole o JSON com os dados da leitura", value=exemplo_json)

# Botão de inserção
if st.button("Inserir"):
    try:
        # Tenta fazer o parse do JSON
        dados = json.loads(json_input)
        
        # Validação dos dados do JSON
        if "data_hora" in dados and all(key in dados for key in ["potassio", "fosforo", "umidade", "ph"]):
            # Convertendo a string de data_hora para datetime
            data_hora = datetime.strptime(dados["data_hora"], "%Y-%m-%d %H:%M:%S")
            id_cultura = 1  # ID fixo para a cultura

            # Mapeamento de sensores para seus respectivos IDs
            sensores = {
                "potassio": 2,
                "fosforo": 3,
                "ph": 4,
                "umidade": 5
            }
            
            # Inserir leituras para cada sensor no banco
            for sensor, id_sensor in sensores.items():
                valor = dados[sensor]
                db.inserir_leitura(id_sensor, id_cultura, data_hora, valor)

            # Exibe mensagem de sucesso
            st.success("Dados inseridos com sucesso!")
            
            # Atualiza a grid de dados após a inserção
            df = db.carregar_leituras()  # Recarrega os dados atualizados
            df.set_index('Leitura', inplace=True)
            dados_grid.dataframe(df, hide_index=True, use_container_width=True)  # Atualiza a exibição da grid
        else:
            st.error("JSON inválido: faltam campos necessários.")
    except json.JSONDecodeError:
        st.error("JSON inválido: erro ao fazer o parse. Verifique a estrutura do JSON.")
    except ValueError as e:
        st.error(f"Erro de validação: {e}")
