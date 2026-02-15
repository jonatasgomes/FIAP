import sqlite3
import pandas as pd
import datetime

_conn = None

def log_error(error):
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open('app_errors.log', 'a') as f:
        f.write(f"{timestamp} - {error}\n")

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
                        'nome TEXT, '
                        'figura TEXT, '
                        'largura INTEGER, '
                        'comprimento INTEGER, '
                        'base INTEGER, '
                        'altura INTEGER, '
                        'raio INTEGER, '
                        'base_menor INTEGER, '
                        'area REAL'
                        ');'
                        'CREATE TABLE IF NOT EXISTS insumos ('
                        'id INTEGER PRIMARY KEY, '
                        'id_cultura INTEGER, '
                        'id_area INTEGER, '
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

def culturas_lov() -> list:
    return query('SELECT id, cultura FROM culturas')

def culturas() -> pd.DataFrame:
    r = query('SELECT id, cultura FROM culturas')
    return pd.DataFrame(r, columns=['ID', 'Cultura']).set_index('ID')

def cultura(_id) -> list:
    return query('SELECT id, cultura FROM culturas WHERE id = ' + str(_id))

def salvar_cultura(_id, _nome):
    if _id:
        run('UPDATE culturas SET cultura = ? WHERE id = ?', (_nome.capitalize(), _id))
    else:
        run('INSERT INTO culturas (cultura) VALUES (?)', (_nome.capitalize(),))

def excluir_cultura(_id):
    run('DELETE FROM insumos WHERE id_cultura = ?', (_id,))
    run('DELETE FROM areas WHERE id_cultura = ?', (_id,))
    run('DELETE FROM culturas WHERE id = ?', (_id,))

def area(_id) -> list:
    return query('SELECT nome, figura, largura, comprimento, base, altura, raio, base_menor, area FROM areas WHERE id = ' + str(_id))

def areas() -> pd.DataFrame:
    r = query(
        'SELECT a.id, a.nome, a.figura, a.largura || "m" as largura, a.comprimento || "m" as comprimento,'
        '       a.base || "m" as base, a.altura || "m" as altura, a.raio || "m" as raio,'
        '       a.base_menor || "m" as base_menor, printf("%,.2f", a.area) || "ha" as area'
        '  FROM areas a'
    )
    return pd.DataFrame(r, columns=['ID', 'Nome', 'Figura', 'Largura', 'Comprimento', 'Base', 'Altura', 'Raio', 'Base Menor', 'Área']).set_index('ID')

def areas_lov() -> list:
    return query('SELECT id, nome FROM areas')

def salvar_area(_id, _nome, _figura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area):
    if _id is not None:
        run(
            'UPDATE areas SET nome = ?, figura = ?, largura = ?, comprimento = ?, base = ?, altura = ?, raio = ?, base_menor = ?, area = ? WHERE id = ?',
            (_nome, _figura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area, _id)
        )
    else:
        run(
            'INSERT INTO areas (nome, figura, largura, comprimento, base, altura, raio, base_menor, area) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
            (_nome, _figura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area)
        )

def excluir_area(_id):
    run('DELETE FROM insumos WHERE id_area = ?', (_id,))
    run('DELETE FROM areas WHERE id = ?', (_id,))

def salvar_insumo(_id, _id_cultura, _id_area, _produto, _dosagem, _unidade, _ruas, _comprimento, _total):
    if _id is not None:
        run(
            'UPDATE insumos SET id_cultura = ?, id_area = ?, produto = ?, dosagem = ?, unidade = ?, ruas = ?, comprimento = ?, total = ? WHERE id = ?',
            (_id_cultura, _id_area, _produto, _dosagem, _unidade, _ruas, _comprimento, _total, _id)
        )
    else:
        run(
            'INSERT INTO insumos (id_cultura, id_area, produto, dosagem, unidade, ruas, comprimento, total) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
            (_id_cultura, _id_area, _produto, _dosagem, _unidade, _ruas, _comprimento, _total)
        )

def excluir_insumo(_id):
    run('DELETE FROM insumos WHERE id = ?', (_id,))

def insumos() -> pd.DataFrame:
    r = query(
        'SELECT i.id, c.cultura, printf("%,.2f", a.area) || "ha - " || a.figura as area, i.ruas, i.comprimento || "m" as comprimento,'
        '       i.produto, i.dosagem || i.unidade || "/m" as dosagem, i.total || i.unidade as total'
        '  FROM insumos i'
        '  LEFT JOIN culturas c'
        '    ON c.id = i.id_cultura'
        '  LEFT JOIN areas a'
        '    ON a.id = i.id_area'
    )
    return pd.DataFrame(r, columns=['ID', 'Cultura', 'Área', 'Ruas', 'Comprimento', 'Produto', 'Dosagem', 'Total']).set_index('ID')

def insumo(_id) -> list:
    return query(
        'SELECT i.id_cultura, i.id_area, i.produto, i.dosagem, i.unidade, i.ruas, i.comprimento'
        '  FROM insumos i'
        ' WHERE i.id = ' + str(_id)
    )
