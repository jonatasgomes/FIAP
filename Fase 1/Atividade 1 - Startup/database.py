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
                        'id_cultura INTEGER, '
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

def culturas() -> pd.DataFrame:
    r = query('SELECT id, cultura FROM culturas')
    return pd.DataFrame(r, columns=['ID', 'Cultura']).set_index('ID')

def cultura(_id) -> list:
    return query('SELECT id, cultura FROM culturas WHERE id = ' + str(_id))

def culturas_info() -> list:
    return query(
        'SELECT c.id, c.cultura, a.largura, a.comprimento, a.base, a.altura, a.raio, a.base_menor, a.figura,'
        '       "🌱&nbsp;&nbsp;" || c.cultura || "\n\r📏&nbsp;&nbsp;" ||'
        '       case'
        '           when a.area is null then "...\n\r📐&nbsp;&nbsp;..."'
        '           else a.area || "ha (" || trim(coalesce("lg " || a.largura || ", ", "") || coalesce("cp " || a.comprimento || ", ", "") ||'
        '                coalesce("bs " || a.base || ", ", "") || coalesce("al " || a.altura || ", ", "") || coalesce("ra " || a.raio || ", ", "") ||'
        '                coalesce("bm " || a.base_menor || ", ", ""), ", ") || ")\n\r📐️&nbsp;&nbsp;" || a.figura'
        '       end btn'
        '  FROM culturas c'
        '  LEFT JOIN areas a ON a.id_cultura = c.id'
    )

def salvar_cultura(_id, _nome):
    if _id:
        run('UPDATE culturas SET cultura = ? WHERE id = ?', (_nome.capitalize(), _id))
    else:
        run('INSERT INTO culturas (cultura) VALUES (?)', (_nome.capitalize(),))

def excluir_cultura(_id):
    run('DELETE FROM insumos WHERE id_cultura = ?', (_id,))
    run('DELETE FROM areas WHERE id_cultura = ?', (_id,))
    run('DELETE FROM culturas WHERE id = ?', (_id,))

def salvar_area(_id_cultura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area, _figura):
    run('DELETE FROM areas WHERE id_cultura = ?', (_id_cultura,))
    run(
        'INSERT INTO areas (id_cultura, largura, comprimento, base, altura, raio, base_menor, area, figura)'
        ' VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)',
        (_id_cultura, _largura, _comprimento, _base, _altura, _raio, _base_menor, _area, _figura)
    )

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

def excluir_insumo(_id):
    run('DELETE FROM insumos WHERE id = ?', (_id,))

def insumos() -> pd.DataFrame:
    r = query(
        'SELECT i.id, c.cultura, printf("%,.2f", a.area) || "ha - " || a.figura as area, i.produto, i.dosagem, i.unidade, i.ruas, i.comprimento, i.total || i.unidade as total'
        '  FROM insumos i'
        '  LEFT JOIN culturas c'
        '    ON c.id = i.id_cultura'
        '  LEFT JOIN areas a'
        '    ON a.id_cultura = i.id_cultura'
    )
    return pd.DataFrame(r, columns=['ID', 'Cultura', 'Área', 'Produto', 'Dosagem', 'Unidade', 'Ruas', 'Comprimento', 'Total']).set_index('ID')

def insumo(_id) -> list:
    return query(
        'SELECT i.id_cultura, i.produto, i.dosagem, i.unidade, i.ruas, i.comprimento'
        '  FROM insumos i'
        ' WHERE i.id = ' + str(_id)
    )
