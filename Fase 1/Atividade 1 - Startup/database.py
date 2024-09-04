import sqlite3
import pandas as pd

_conn = None

def log_error(error):
    f = open('app_errors.log', 'a')
    f.write(error + '\n')
    f.close()

def get_connection():
    global _conn
    if _conn is None:
        _conn = sqlite3.connect("database.db", check_same_thread=False)
    return _conn

def check_database():
    try:
        c = get_connection().cursor()
        c.executescript('CREATE TABLE IF NOT EXISTS culturas (id INTEGER PRIMARY KEY, cultura TEXT);'
                        'CREATE TABLE IF NOT EXISTS areas ('
                        'id INTEGER PRIMARY KEY, '
                        'id_cultura INTEGER, '
                        'figura TEXT, '
                        'largura INTEGER, '
                        'comprimento INTEGER, '
                        'base INTEGER, '
                        'altura INTEGER, '
                        'raio INTEGER, '
                        'base_menor INTEGER, '
                        'area INTEGER'
                        ');'
                        'CREATE TABLE IF NOT EXISTS insumos ('
                        'id INTEGER PRIMARY KEY, '
                        'id_cultura INTEGER, '
                        'produto TEXT, '
                        'dosagem REAL, '
                        'unidade TEXT, '
                        'ruas INTEGER, '
                        'comprimento INTEGER, '
                        'total REAL'
                        ');'
                        )
        get_connection().commit()
    except Exception as e:
        log_error(str(e))

def query(stmt) -> list:
    try:
        c = get_connection().cursor()
        c.execute(stmt)
        return c.fetchall()
    except Exception as e:
        log_error(str(e))

def run(stmt, params=None):
    try:
        c = get_connection().cursor()
        if params is None:
            c.execute(stmt)
        else:
            c.execute(stmt, params)
        get_connection().commit()
    except Exception as e:
        log_error(str(e))

def close_connection():
    global _conn
    try:
        if _conn is not None and isinstance(_conn, sqlite3.Connection):
            _conn.close()
            _conn = None
    except Exception as e:
        _conn = None
        log_error(str(e))

def culturas() -> list:
    return query('SELECT id, cultura FROM culturas')

def salvar_insumo(_id, id_cultura, produto, dosagem, unidade, ruas, comprimento, total):
    if _id is not None:
        run(
            'UPDATE insumos SET id_cultura = ?, produto = ?, dosagem = ?, unidade = ?, ruas = ?, comprimento = ?, total = ? WHERE id = ?',
            (id_cultura, produto, dosagem, unidade, ruas, comprimento, total, _id)
        )
    else:
        run(
            'INSERT INTO insumos (id_cultura, produto, dosagem, unidade, ruas, comprimento, total) VALUES (?, ?, ?, ?, ?, ?, ?)',
            (id_cultura, produto, dosagem, unidade, ruas, comprimento, total)
        )

def excluir_insumo(id):
    run('DELETE FROM insumos WHERE id = ?', (id,))

def insumos() -> pd.DataFrame:
    r = query(
        'SELECT i.id, c.cultura, i.produto, i.dosagem, i.unidade, i.ruas, i.comprimento, i.total || i.unidade as total'
        '  FROM insumos i LEFT JOIN'
        '       culturas c'
        '    ON c.id = i.id_cultura'
    )
    return pd.DataFrame(r, columns=['ID', 'Cultura', 'Produto', 'Dosagem', 'Unidade', 'Ruas', 'Comprimento', 'Total']).set_index('ID')

def insumo(_id) -> list:
    return query(
        'SELECT i.id_cultura, i.produto, i.dosagem, i.unidade, i.ruas, i.comprimento'
        '  FROM insumos i'
        ' WHERE i.id = ' + str(_id)
    )
