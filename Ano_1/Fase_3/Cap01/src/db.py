import cx_Oracle
import pandas as pd
from datetime import datetime
import env

class OracleDatabase:
    def __init__(self):
        self.user = env.user
        self.password = env.password
        self.dsn = env.dsn
        self.encoding = env.encoding
        self.connection = None

    # Estabelece a conexão com o banco de dados Oracle.
    def connect(self):
        try:
            self.connection = cx_Oracle.connect(
                user=self.user,
                password=self.password,
                dsn=self.dsn,
                encoding=self.encoding,
            )
            print("Conexão com o banco Oracle estabelecida com sucesso.")
        except cx_Oracle.DatabaseError as e:
            print(f"Erro ao conectar ao banco de dados Oracle: {e}")

    # Fecha a conexão com o banco de dados.
    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("Conexão com o banco Oracle encerrada.")

    # Executa uma consulta e retorna os dados em um DataFrame do Pandas.
    def execute_query(self, query, params=None):
        if not self.connection:
            self.connect()

        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or {})
            columns = [col[0] for col in cursor.description]
            data = cursor.fetchall()
            df = pd.DataFrame(data, columns=columns)
            return df
        except cx_Oracle.DatabaseError as e:
            print(f"Erro ao executar a consulta: {e}")
            return None
        finally:
            cursor.close()

    # Executa um comando de inserção com os valores fornecidos.
    def execute_insert(self, query, params):
        if not self.connection:
            self.connect()
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params)
            self.connection.commit()
            print("Inserção realizada com sucesso.")
        except cx_Oracle.DatabaseError as e:
            print(f"Erro ao executar a inserção: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

    # Carrega todos os dados da tabela leitura.
    def carregar_leituras(self):
        query = """
          SELECT l.id_leitura as "Leitura", to_char(l.data_hora, 'DD/MM/YYYY HH24:MI:SS') as "Data",
                 c.nome as "Cultura", s.descricao as "Sensor", l.valor as "Valor"
            FROM cultura c, sensor s, leitura l
           WHERE s.id_sensor = l.id_sensor
             AND c.id_cultura = l.id_cultura
        ORDER BY l.data_hora DESC
        """
        return self.execute_query(query)

    # Insere uma nova leitura na tabela.
    def inserir_leitura(self, id_sensor, id_cultura, data_hora, valor):
        insert_query = """
            INSERT INTO leitura (id_sensor, id_cultura, data_hora, valor)
            VALUES (:1, :2, :3, :4)
        """
        return self.execute_insert(insert_query, [id_sensor, id_cultura, data_hora, valor])
