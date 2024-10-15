import streamlit as st
import json
import os
import cx_Oracle
import pandas as pd

conn: cx_Oracle.Connection | None = None
table_exists = False

def conexao_oracle():
    global conn
    if conn is None:
        lib_dir = os.environ.get("LD_LIBRARY_PATH")
        try:
            cx_Oracle.init_oracle_client(lib_dir=lib_dir)
        except:
            pass
        dsn_tns = cx_Oracle.makedsn('oracle.fiap.com.br', '1521', service_name='ORCL')
        conn = cx_Oracle.connect(user='rm559693', password='060180', dsn=dsn_tns)
    return conn

cursor = conexao_oracle().cursor()
if not table_exists:
    create_table_sql = open('datatabase_script.sql', 'r').read()
    try:
        cursor.execute(create_table_sql)
        conn.commit()
        table_exists = True
    except:
        pass

# salvar dados
def salvar_dados(data):
    cursor.execute("INSERT INTO producao_agricola (cultura, area, produtividade, custo, receita) VALUES (:1, :2, :3, :4, :5)",
                   (data['cultura'], data['area'], data['produtividade'], data['custo'], data['receita']))
    conn.commit()

# buscar todos os dados da tabela
def buscar_dados():
    cursor.execute("SELECT id, cultura, area, produtividade, custo, receita FROM producao_agricola")
    rows = cursor.fetchall()
    return rows

# calcular receita
def calcular_receita(_area, _produtividade):
    return _area * _produtividade * 100

def excluir_dados(_id):
    cursor.execute("DELETE FROM producao_agricola WHERE id = " + str(_id))
    conn.commit()
    st.rerun()

def download_json(_id):
    cursor.execute("SELECT * FROM producao_agricola WHERE id = " + str(_id))
    rows = cursor.fetchall()
    data = []
    for row in rows:
        data.append({
            'id': row[0],
            'cultura': row[1],
            'area': row[2],
            'produtividade': row[3],
            'custo': row[4],
            'receita': row[5]
        })
    return json.dumps(data)

# interface Streamlit
st.title('Calcule a Receita de sua Fazenda')

# inserção de dados
with st.form("form_dados"):
    cultura = st.text_input('Cultura')
    area = st.number_input('Área plantada (em hectares)', min_value=0.01)
    produtividade = st.number_input('Produtividade esperada (ton/ha)', min_value=0.01)
    custo = st.number_input('Custo total estimado (R$)', min_value=0.01)
    submit_button = st.form_submit_button(label="Calcular e Salvar")

    if submit_button:
        if cultura.strip() == '':
            st.error('Por favor, informe a cultura.')
            # st.stop()
        else:
            receita_esperada = calcular_receita(area, produtividade)
            st.write(f'A receita esperada para a cultura de {cultura} é de R$ {receita_esperada:.2f}')
            dados = {'cultura': cultura, 'area': area, 'produtividade': produtividade, 'custo': custo, 'receita': receita_esperada}
            salvar_dados(dados)
            st.success('Dados salvos com sucesso!')

# dados em uma grid usando st.dataframe
dados = buscar_dados()

if dados:
    df = pd.DataFrame(dados, columns=["ID", "Cultura", "Área", "Produtividade", "Custo", "Receita"]).set_index('ID')
    st.write("## Dados Salvos")
    grid = st.dataframe(df, hide_index=True, use_container_width=True, selection_mode="single-row", on_select='rerun')
    if len(grid.selection['rows']) > 0:
        col1, col2 = st.columns([2, 14])
        with col1:
            selected_idx = grid.selection['rows'][0]
            selected_id = int(df.index[selected_idx])
            if st.button("Excluir", type="primary"):
                excluir_dados(selected_id)
        with col2:
            selected_idx = grid.selection['rows'][0]
            selected_id = int(df.index[selected_idx])
            json_data = download_json(selected_id)
            st.download_button(label="Download JSON", data=json_data, file_name="dados.json", mime="application/json")
